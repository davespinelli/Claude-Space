#!/usr/bin/env python3
"""QUEUE idea 279 — does-the-buffer-beat-the-cadence-dial-at-matched-realised-turnover
   (cloud, 2026-09-06).

QUESTION (verbatim from QUEUE.md idea 279)
    "idea 273 cut the broad ranked book from 13.78x to 3.46x/yr and RAISED Sharpe
     0.958 -> 1.061, but a monthly or quarterly cadence reaches similar turnover by a
     different route.  Put the buffer ladder and the cadence ladder on one axis of
     REALISED turnover and test whether the buffer is a distinct instrument or a
     re-parameterised cadence; run idea 273's anchor slide (0-7 bars) on every cadence
     rung so the comparison is not an anchor artefact.  Max 2 params."

WHAT IS AT STAKE
    Idea 273's headline (`buffer m=999 lifts broad Sharpe +0.103 while cutting turnover
    13.78x -> 3.46x`) is quoted in the record as a property of the BUFFER.  But cadence
    is the record's oldest and cheapest turnover dial (idea 3, idea 107) and it reaches
    the same turnover levels.  If the two ladders trace ONE curve in (realised turnover,
    Sharpe) space, then idea 273 discovered nothing beyond "trade less on this panel" and
    the buffer is a re-parameterised cadence.  If the buffer sits systematically ABOVE the
    cadence curve at matched turnover — by more than the anchor band — it is a distinct
    instrument and deserves its own line in RULES.

    The decisive test is NOT the matched-turnover gap alone (two ladders can cross one
    curve at different places for mechanical reasons).  It is the INTERACTION: run the
    full cross m x cadence.  A re-parameterised cadence has NOTHING LEFT TO ADD once the
    cadence is already slow — d(Sharpe)/dm must collapse as cadence slows.  A distinct
    instrument keeps paying on top of M and Q.  Both readings are reported.

THE TWO LADDERS (exactly 2 tuned parameters, as the idea requires)
    param 1  m       no-trade band width on the composite rank, idea 273's buffer, verbatim:
                     entry bar rank <= NPOS, exit bar rank > NPOS + m.  m in
                     {0, 2, 5, 10, 15, 20, 30, 50, 999};  999 = hold until INELIGIBLE.
                     j (idea 273's second dial) is FIXED at 999 (uncapped) — not tuned here,
                     because this run spends its second parameter on cadence.
    param 2  cadence rebalance frequency in {D, W, M, Q}.
    ALL 9 x 4 = 36 cells are reported on both panels and both cost rungs.  Nothing is picked.

THE ANCHOR SLIDE (a reporting axis, NOT a tuned parameter)
    A cadence rung is not one schedule: a monthly rule has ~21 distinct phases and a weekly
    rule 5 (idea 223).  Every cell is therefore run at PHASE p in 0..7 — the decision bar
    and the fill bar slide together by p bars, the decision-to-fill gap stays 1 (PROTOCOL
    rule 2).  For D the phase is degenerate (every bar is a decision bar) so only p=0 is run
    and its band is 0 by construction.  For W the 8 phases wrap onto 5 distinct schedules;
    that is reported, not hidden.  THE ANCHOR BAND (max-min Sharpe over the phases of a cell)
    is the run's noise floor: a buffer-vs-cadence gap narrower than the band is NOT a finding.

DESIGN (PROTOCOL rules 1-9)
    Universe  research/universe_broad.json via load_universe(broad=True), 136 tickers, the
              panel idea 273 ran on.  SURVIVORSHIP: current constituents only, so absolute
              CAGR/Sharpe are optimistic; every comparison here is between arms on the SAME
              panel and the SAME days.  u56 (load_universe()) is a TRANSFER panel — an arm,
              never a place anything is chosen.
    Book      idea 66's `top20-200d` at gross 0.75, verbatim (composite = mean pct-rank of
              12-1 / 6m / 3m, NO vol scaler; eligibility vol20 < 0.60 AND price > 200d MA;
              equal weight 0.75/20, cash otherwise).  Nothing about the parent is tuned.
    Costs     10 bps is the PROTOCOL rung and the verdict rung.  25 bps is a reporting axis:
              a turnover instrument must pay MORE as costs rise or it is not one.  Both rungs
              are derived EXACTLY from a single 0 bps run per cell via the engine's own
              turnover series (costs enter linearly), asserted against engine.backtest.
    Rule 8    (m, cadence) chosen on 2009-2016 ONLY by IS Sharpe; 2017-2026 untouched.  Two
              choosers are run: PHASE-0 (the record's habit) and ANCHOR-AGNOSTIC (mean Sharpe
              over the cell's phases), because idea 223 showed the phase can flip a pick.
              STATED WEAKNESS, as idea 273 stated it: 2017-2026 is essentially H2, so the OOS
              window and the 4b H2 bar overlap ~100% and this walk-forward is weak by
              construction (idea 111's window problem).
    Verdict   both KEEP paths on EVERY grid point; 4a against the LIVE book (RULES v2), with
              RULES v1 carried alongside for continuity.

REPRODUCTION GATES (asserted BEFORE any new number is read)
    G1  the parent (m=0, W, phase 0) reproduces idea 66/273's published broad numbers
        13.1% / 0.958 / -20.1%, halves 1.125 / 0.814, SPY H2 0.837.
    G2  the phased state machine at (m=0, phase 0, W) is IDENTICAL to the stateless top-20
        book: max|weight diff| on decision rows == 0.
    G3  fast_backtest == engine.backtest on the parent (returns and turnover).
    G4  idea 273's published buffer row reproduces: m=999 W @10bps = 13.48% / 1.0610 /
        -17.57%, 3.46x/yr, halves 1.401 / 0.775.

Outputs: .console.txt, .grid.csv (every cell x phase x rung), .matched.csv (the
buffer-vs-cadence matched-turnover comparison), .walkforward.csv.
Deterministic, standalone, no network, no randomness.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask                    # noqa: E402

NPOS, GROSS, MAX_VOL = 20, 0.75, 0.60
JFIX = 999                                    # idea 273's cap dial, FIXED (not tuned here)
END = "2026-09-03"                            # idea 66/70/273's last eval day
IS_END, OOS_START = "2016-12-31", "2017-01-01"
MGRID = [0, 2, 5, 10, 15, 20, 30, 50, 999]    # tuned param 1
CGRID = ["D", "W", "M", "Q"]                  # tuned param 2
PHASES = list(range(8))                       # reporting axis (idea 279's "0-7 bars")
RUNGS = [10, 25]
STEM = Path(__file__).stem
OUT = Path(__file__).parent

_LINES = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LINES.append(s)


# --------------------------------------------------------------- construction
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6 = px / px.shift(126) - 1
    r3 = px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def eligible(px):
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    return (vol20 < MAX_VOL) & (px > px.rolling(200).mean())


def parent_weights(px):
    """Idea 66's stateless `top20-200d` at gross 0.75."""
    rank = composite(px).where(eligible(px)).rank(axis=1, ascending=False)
    return (rank <= NPOS).astype(float) * (GROSS / NPOS)


def decision_rows(idx, freq, phase):
    """Integer positions of the DECISION bars for cadence `freq` slid `phase` bars later.
    The fill bar is decision+1 in every case, so the decision-to-fill gap never moves."""
    m = rebalance_mask(idx, freq)
    if phase:
        m = m.shift(phase, fill_value=False)
    return np.flatnonzero(m.values)


def band_weights(px, m, dec, rank_all):
    """Idea 273's no-trade band, verbatim, but on an arbitrary set of decision bars `dec`.

    At each decision bar:
      1. drop every holding that is INELIGIBLE (risk rule: never banded, never capped);
      2. among still-eligible holdings, sell those with rank > NPOS + m (j = 999 here, so
         the cap never binds and every breach goes);
      3. refill with the best-ranked non-held eligible names of rank <= NPOS until the
         PARENT'S OWN set size |{rank <= NPOS}| on that date is reached (ties at the cut are
         all taken, exactly as the parent's `rank <= NPOS` mask does, which is what lets
         m = 0 nest the parent EXACTLY rather than approximately).
    Weight is GROSS/NPOS per held name; the remainder is cash.
    """
    cols = list(px.columns)
    pos = {c: i for i, c in enumerate(cols)}
    rk = rank_all.values
    W = np.zeros((len(px.index), len(cols)))
    held = []
    row = np.zeros(len(cols))
    prev = 0
    for i in dec:
        W[prev:i] = row
        r = rk[i]
        held = [t for t in held if not np.isnan(r[pos[t]])]
        if m < 10**6:
            held = [t for t in held if r[pos[t]] <= NPOS + m]
        npos_t = int(np.nansum(r <= NPOS))
        need = npos_t - len(held)
        if need > 0:
            hs = set(held)
            cand = sorted((r[pos[c]], c) for c in cols
                          if c not in hs and not np.isnan(r[pos[c]]) and r[pos[c]] <= NPOS)
            held += [c for _, c in cand[:need]]
        row = np.zeros(len(cols))
        for t in held:
            row[pos[t]] = GROSS / NPOS
        W[i] = row
        prev = i + 1
    W[prev:] = row
    return pd.DataFrame(W, index=px.index, columns=px.columns)


def fast_backtest(px, weights, dec, cost_bps=0.0):
    """Vectorised engine.backtest for an explicit decision-bar set (fill = decision+1).
    Asserted identical to engine.backtest in gate G3."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    T, N = rets.shape
    fill = dec + 1
    fill = fill[fill < T]                     # a decision on the last bar never fills
    mask = np.zeros(T, bool); mask[fill] = True; mask[0] = True
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx),
            "gross": pd.Series(held.sum(axis=1), index=idx)}


def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


# ------------------------------------------------------------------ KEEP paths
def path4a(r, base):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(base.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(base.iloc[h:])["Sharpe"]: bad.append("H2")
    if metrics(r)["MaxDD"] < metrics(base)["MaxDD"]: bad.append("DD")
    return bad


def path4b(r, spy, oos_s, spy_oos_s):
    h = len(r) // 2
    bad = []
    if metrics(r.iloc[:h])["Sharpe"] <= metrics(spy.iloc[:h])["Sharpe"]: bad.append("H1")
    if metrics(r.iloc[h:])["Sharpe"] <= metrics(spy.iloc[h:])["Sharpe"]: bad.append("H2")
    if oos_s <= spy_oos_s: bad.append("OOS")
    if abs(metrics(r)["MaxDD"]) > 0.60 * abs(metrics(spy)["MaxDD"]): bad.append("DD")
    if metrics(r)["CAGR"] < 0.70 * metrics(spy)["CAGR"]: bad.append("CAGR")
    return bad


def vstr(bad, tag):
    return f"KEEP {tag}" if not bad else "KILL " + tag + "(" + ",".join(bad) + ")"


# ============================================================ the grid for one panel
def run_panel(pname, px):
    start = px.index[260]
    i0 = px.index.get_loc(start)
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    n = len(spy); h = n // 2; yrs = n / 252.0
    oos_idx = spy.loc[OOS_START:].index
    is_idx = spy.loc[:IS_END].index
    spy_oos_s = metrics(spy.loc[oos_idx])["Sharpe"]
    rank_all = composite(px).where(eligible(px)).rank(axis=1, ascending=False)

    base_v2 = {b: backtest(px, rules_v2_weights(px), cost_bps=b, freq="W")["returns"].loc[start:]
               for b in RUNGS}
    base_v1 = {b: backtest(px, rules_v1_weights(px), cost_bps=b, freq="W")["returns"].loc[start:]
               for b in RUNGS}

    rows = []
    for cad in CGRID:
        phs = [0] if cad == "D" else PHASES
        for ph in phs:
            dec = decision_rows(px.index, cad, ph)
            for m in MGRID:
                w = band_weights(px, m, dec, rank_all)
                res = fast_backtest(px, w, dec, 0.0)
                r0 = res["returns"].loc[start:]
                t0 = res["turnover"].loc[start:]
                tpy = t0.sum() / yrs
                gr = res["gross"].loc[start:].mean()
                for b in RUNGS:
                    r = r0 - t0 * b / 1e4
                    c, s, dd = m3(r)
                    oc, os_, odd = m3(r.loc[oos_idx])
                    d = dict(panel=pname, cadence=cad, phase=ph, m=m, cost_bps=b,
                             turn_yr=tpy, gross=gr, CAGR=c, Sharpe=s, MaxDD=dd,
                             H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                             IS_Sharpe=metrics(r.loc[is_idx])["Sharpe"],
                             OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=odd)
                    b4a = path4a(r, base_v2[b]); b4b = path4b(r, spy, os_, spy_oos_s)
                    d["v4a"] = vstr(b4a, "4a"); d["v4b"] = vstr(b4b, "4b")
                    d["pass4a"] = not b4a; d["pass4b"] = not b4b
                    rows.append(d)
    g = pd.DataFrame(rows)
    ctx = dict(spy=spy, h=h, yrs=yrs, oos_idx=oos_idx, is_idx=is_idx, spy_oos_s=spy_oos_s,
               base_v2=base_v2, base_v1=base_v1, start=start, i0=i0, rank_all=rank_all)
    return g, ctx


# ==================================================================== main
def main():
    pd.set_option("display.width", 240)
    P(f"=== idea 279  does-the-buffer-beat-the-cadence-dial-at-matched-realised-turnover  ({STEM}) ===")
    P("book: idea 66 top20-200d, gross 0.75, t+1 | buffer m (idea 273, j fixed 999) x cadence D/W/M/Q")
    P(f"phases 0..7 on W/M/Q (D degenerate) | cost rungs {RUNGS} bps | eval end {END}")
    P("SURVIVORSHIP: broad/u56 are CURRENT constituents; absolute levels optimistic, all")
    P("comparisons are within-panel between arms on identical days.")

    px = load_universe(broad=True).loc[:END]
    P(f"\nuniverse_broad.json: {px.shape[1]} tickers, {px.index[0].date()} -> {px.index[-1].date()}")
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    n = len(spy); h = n // 2; yrs = n / 252.0
    rank_all = composite(px).where(eligible(px)).rank(axis=1, ascending=False)

    # ---------------------------------------------------------------- gates
    P("\n" + "=" * 104)
    P("REPRODUCTION GATES (asserted before any new number is read)")
    P("=" * 104)
    pw = parent_weights(px)
    pres = backtest(px, pw, cost_bps=10, freq="W")
    pr = pres["returns"].loc[start:]
    got = dict(CAGR=metrics(pr)["CAGR"], Sharpe=metrics(pr)["Sharpe"], MaxDD=metrics(pr)["MaxDD"],
               H1=metrics(pr.iloc[:h])["Sharpe"], H2=metrics(pr.iloc[h:])["Sharpe"],
               SPY_H2=metrics(spy.iloc[h:])["Sharpe"])
    want = dict(CAGR=0.131, Sharpe=0.958, MaxDD=-0.201, H1=1.125, H2=0.814, SPY_H2=0.837)
    ok1 = all(abs(got[k] - want[k]) <= 5e-4 for k in want)
    for k in want:
        P(f"  G1 {k:8s} published {want[k]:8.3f}   reproduced {got[k]:8.4f}   "
          f"{'EXACT' if abs(got[k]-want[k])<=5e-4 else 'MISMATCH'}")
    P(f"  G1: {'6/6 EXACT' if ok1 else 'FAILED'}")
    assert ok1, "G1 failed"

    dec0 = decision_rows(px.index, "W", 0)
    w0 = band_weights(px, 0, dec0, rank_all)
    dw = (w0 - pw).abs().to_numpy()[dec0].max()
    P(f"  G2 max|weight diff| (m=0,W,phase0) vs stateless parent on decision rows: {dw:.3e}"
      f"   {'EXACT' if dw == 0.0 else 'FAILED'}")
    assert dw == 0.0, "G2 failed"

    fb = fast_backtest(px, pw, dec0, 10.0)
    dr = (fb["returns"] - pres["returns"]).abs().max()
    dt = (fb["turnover"] - pres["turnover"]).abs().max()
    P(f"  G3 fast_backtest vs engine.backtest: max|dreturn| {dr:.2e}  max|dturnover| {dt:.2e}"
      f"   {'EXACT' if dr < 1e-12 and dt < 1e-12 else 'FAILED'}")
    assert dr < 1e-12 and dt < 1e-12, "G3 failed"

    w999 = band_weights(px, 999, dec0, rank_all)
    r999f = fast_backtest(px, w999, dec0, 0.0)
    r999 = (r999f["returns"] - r999f["turnover"] * 10 / 1e4).loc[start:]
    t999 = r999f["turnover"].loc[start:].sum() / yrs
    g4 = dict(CAGR=metrics(r999)["CAGR"], Sharpe=metrics(r999)["Sharpe"], MaxDD=metrics(r999)["MaxDD"],
              H1=metrics(r999.iloc[:h])["Sharpe"], H2=metrics(r999.iloc[h:])["Sharpe"], turn=t999)
    w4 = dict(CAGR=0.1348, Sharpe=1.0610, MaxDD=-0.1757, H1=1.401, H2=0.775, turn=3.46)
    tol = dict(CAGR=1e-3, Sharpe=1e-3, MaxDD=1e-3, H1=1e-3, H2=1e-3, turn=0.02)
    ok4 = all(abs(g4[k] - w4[k]) <= tol[k] for k in w4)
    for k in w4:
        P(f"  G4 m=999 {k:6s} published {w4[k]:8.4f}   reproduced {g4[k]:8.4f}   "
          f"{'MATCH' if abs(g4[k]-w4[k])<=tol[k] else 'MISMATCH'}")
    P(f"  G4: {'6/6 MATCH (idea 273 reproduced)' if ok4 else 'FAILED'}")
    assert ok4, "G4 failed"

    # ---------------------------------------------------------------- grids
    P("\n" + "=" * 104)
    P("THE GRID  (9 buffer widths x 4 cadences x 8 phases x 2 cost rungs, both panels)")
    P("=" * 104)
    gb, cb = run_panel("BROAD136", px)
    pu = load_universe().loc[:END]
    P(f"transfer panel u56: {pu.shape[1]} tickers, {pu.index[0].date()} -> {pu.index[-1].date()}")
    gu, cu = run_panel("U56", pu)
    grid = pd.concat([gb, gu], ignore_index=True)
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"grid rows: {len(grid)}  ->  {STEM}.grid.csv")

    PANELS = {"BROAD136": (gb, cb, px), "U56": (gu, cu, pu)}

    # ------------------------------------------------- D0: reference + anchor band
    for pn, (g, c, ppx) in PANELS.items():
        P("\n" + "-" * 104)
        P(f"D0  {pn}: every cell at phase 0, plus the ANCHOR BAND over its phases")
        P("-" * 104)
        for b in RUNGS:
            P(f"  --- @{b} bps ---")
            P(f"  {'cad':>4s} {'m':>4s} {'turn/yr':>8s} {'CAGR':>7s} {'Sharpe':>7s} {'MaxDD':>8s} "
              f"{'H1':>6s} {'H2':>6s} {'OOSShrp':>8s} {'band(S)':>8s} {'band(turn)':>10s} "
              f"{'4b':>22s} {'4a':>18s}")
            for cad in CGRID:
                for m in MGRID:
                    sub = g[(g.cost_bps == b) & (g.cadence == cad) & (g.m == m)]
                    r0 = sub[sub.phase == 0].iloc[0]
                    bS = sub.Sharpe.max() - sub.Sharpe.min()
                    bT = sub.turn_yr.max() - sub.turn_yr.min()
                    P(f"  {cad:>4s} {m:4d} {r0.turn_yr:8.2f} {r0.CAGR:7.2%} {r0.Sharpe:7.3f} "
                      f"{r0.MaxDD:8.2%} {r0.H1:6.3f} {r0.H2:6.3f} {r0.OOS_Sharpe:8.3f} "
                      f"{bS:8.3f} {bT:10.2f} {r0.v4b:>22s} {r0.v4a:>18s}")
            ref = {"RULES v2 (live)": c["base_v2"][b], "RULES v1": c["base_v1"][b], "SPY": c["spy"]}
            for nm, rr in ref.items():
                cc, ss, dd = m3(rr)
                P(f"  {nm:>28s}  CAGR {cc:7.2%}  Sharpe {ss:6.3f}  MaxDD {dd:8.2%}  "
                  f"H1 {metrics(rr.iloc[:c['h']])['Sharpe']:6.3f}  H2 {metrics(rr.iloc[c['h']:])['Sharpe']:6.3f}  "
                  f"OOS {metrics(rr.loc[c['oos_idx']])['Sharpe']:6.3f}")

    # -------------------------------------- D1: THE QUEUED TEST, matched realised turnover
    P("\n" + "=" * 104)
    P("D1  THE QUEUED TEST — buffer ladder vs cadence ladder on ONE axis of REALISED turnover")
    P("=" * 104)
    P("  The cadence ladder is the m=0 book at D/W/M/Q (all phases).  For each BUFFER point")
    P("  (cadence=W, m>0, phase p) the cadence curve is linearly interpolated in log(turnover)")
    P("  at the buffer's OWN realised turnover, using the m=0 phase-mean curve; dS = buffer")
    P("  Sharpe - interpolated cadence Sharpe.  A buffer point whose turnover lies OUTSIDE the")
    P("  cadence ladder's turnover span is reported as OUT-OF-SPAN and never extrapolated.")
    mrows = []
    for pn, (g, c, ppx) in PANELS.items():
        for b in RUNGS:
            cad_curve = (g[(g.cost_bps == b) & (g.m == 0)]
                         .groupby("cadence")[["turn_yr", "Sharpe", "CAGR", "MaxDD"]].mean()
                         .sort_values("turn_yr"))
            xs = np.log(cad_curve.turn_yr.values); ys = cad_curve.Sharpe.values
            lo, hi = xs.min(), xs.max()
            P(f"\n  --- {pn} @{b} bps: cadence ladder (m=0, phase-mean) ---")
            for cad, rr in cad_curve.iterrows():
                P(f"      {cad}  turn {rr.turn_yr:7.2f}x/yr  Sharpe {rr.Sharpe:6.3f}  "
                  f"CAGR {rr.CAGR:7.2%}  MaxDD {rr.MaxDD:8.2%}")
            band = {cad: (g[(g.cost_bps == b) & (g.m == 0) & (g.cadence == cad)].Sharpe.max()
                          - g[(g.cost_bps == b) & (g.m == 0) & (g.cadence == cad)].Sharpe.min())
                    for cad in CGRID}
            noise = max(band.values())
            P(f"      anchor band of the cadence ladder (max over rungs): {noise:.3f} Sharpe "
              f"[D {band['D']:.3f} W {band['W']:.3f} M {band['M']:.3f} Q {band['Q']:.3f}]")
            P(f"      {'m':>4s} {'phase':>5s} {'turn/yr':>8s} {'Sharpe':>7s} {'cad@turn':>8s} "
              f"{'dS':>7s} {'> band?':>8s}")
            bp = g[(g.cost_bps == b) & (g.cadence == "W") & (g.m > 0)]
            for _, rr in bp.iterrows():
                x = np.log(rr.turn_yr)
                if x < lo or x > hi:
                    P(f"      {rr.m:4d} {rr.phase:5d} {rr.turn_yr:8.2f} {rr.Sharpe:7.3f} "
                      f"{'OUT-OF-SPAN':>8s}")
                    mrows.append(dict(panel=pn, cost_bps=b, m=rr.m, phase=rr.phase,
                                      turn_yr=rr.turn_yr, Sharpe=rr.Sharpe, cad_Sharpe=np.nan,
                                      dS=np.nan, in_span=False, band=noise))
                    continue
                cs = float(np.interp(x, xs, ys))
                dS = rr.Sharpe - cs
                mrows.append(dict(panel=pn, cost_bps=b, m=rr.m, phase=rr.phase,
                                  turn_yr=rr.turn_yr, Sharpe=rr.Sharpe, cad_Sharpe=cs,
                                  dS=dS, in_span=True, band=noise))
                P(f"      {rr.m:4d} {rr.phase:5d} {rr.turn_yr:8.2f} {rr.Sharpe:7.3f} {cs:8.3f} "
                  f"{dS:+7.3f} {'YES' if abs(dS) > noise else 'no':>8s}")
            ins = [d for d in mrows if d["panel"] == pn and d["cost_bps"] == b and d["in_span"]]
            if ins:
                ds = np.array([d["dS"] for d in ins])
                P(f"      SUMMARY {pn}@{b}bps: {len(ins)} in-span buffer points, mean dS {ds.mean():+.4f}, "
                  f"median {np.median(ds):+.4f}, min {ds.min():+.4f}, max {ds.max():+.4f}; "
                  f"{int((ds > 0).sum())}/{len(ds)} above the cadence curve, "
                  f"{int((np.abs(ds) > noise).sum())}/{len(ds)} by more than the anchor band {noise:.3f}")
    matched = pd.DataFrame(mrows)
    matched.to_csv(OUT / f"{STEM}.matched.csv", index=False)

    # ---------------------------------------- D2: THE INTERACTION (the decisive reading)
    P("\n" + "=" * 104)
    P("D2  THE DECISIVE READING — does the buffer still pay ON TOP OF a slow cadence?")
    P("=" * 104)
    P("  If the buffer is a re-parameterised cadence, d(Sharpe)/dm must COLLAPSE as the cadence")
    P("  slows (nothing left to slow down).  If it is a distinct instrument the increment")
    P("  survives at M and Q.  Increment = phase-mean Sharpe(m) - phase-mean Sharpe(m=0) at the")
    P("  SAME cadence, so cadence is differenced out entirely.")
    for pn, (g, c, ppx) in PANELS.items():
        for b in RUNGS:
            P(f"\n  --- {pn} @{b} bps: Sharpe increment over m=0, at each cadence (phase means) ---")
            P(f"      {'m':>4s} " + " ".join(f"{cad:>16s}" for cad in CGRID))
            base = {cad: g[(g.cost_bps == b) & (g.cadence == cad) & (g.m == 0)].Sharpe.mean()
                    for cad in CGRID}
            P(f"      {'m=0':>4s} " + " ".join(f"{base[cad]:16.3f}" for cad in CGRID)
              + "   <- absolute Sharpe")
            for m in MGRID[1:]:
                cells = []
                for cad in CGRID:
                    s = g[(g.cost_bps == b) & (g.cadence == cad) & (g.m == m)].Sharpe.mean()
                    t = g[(g.cost_bps == b) & (g.cadence == cad) & (g.m == m)].turn_yr.mean()
                    cells.append(f"{s-base[cad]:+8.3f}@{t:6.2f}x")
                P(f"      {m:4d} " + " ".join(f"{c_:>16s}" for c_ in cells))
            bestm = {cad: max(MGRID, key=lambda m: g[(g.cost_bps == b) & (g.cadence == cad) & (g.m == m)].Sharpe.mean())
                     for cad in CGRID}
            P("      best m per cadence: " + "  ".join(f"{cad}->{bestm[cad]}" for cad in CGRID))
            inc = {cad: max(g[(g.cost_bps == b) & (g.cadence == cad)].groupby("m").Sharpe.mean()) - base[cad]
                   for cad in CGRID}
            P("      max increment  : " + "  ".join(f"{cad} {inc[cad]:+.3f}" for cad in CGRID))

    # ------------------------------------------------------- D3: rule-8 walk-forward
    P("\n" + "=" * 104)
    P("D3  PROTOCOL rule 8 WALK-FORWARD — (m, cadence) chosen on 2009-2016, 2017-2026 untouched")
    P("=" * 104)
    P("  WEAKNESS, stated up front: the OOS window is essentially H2, so OOS and the 4b H2 bar")
    P("  overlap ~100% (idea 111's window problem).  Two choosers: PHASE-0 (the record's habit)")
    P("  and ANCHOR-AGNOSTIC (IS phase-mean).  Controls: the parent (m=0,W), idea 273's m=999,W,")
    P("  RULES v2, and SPY.")
    wf = []
    for pn, (g, c, ppx) in PANELS.items():
        for b in RUNGS:
            sub = g[g.cost_bps == b]
            p0 = sub[sub.phase == 0]
            pick0 = p0.loc[p0.IS_Sharpe.idxmax()]
            am = sub.groupby(["cadence", "m"])[["IS_Sharpe", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD",
                                                "turn_yr"]].mean()
            ka = am.IS_Sharpe.idxmax()
            par = p0[(p0.cadence == "W") & (p0.m == 0)].iloc[0]
            b273 = p0[(p0.cadence == "W") & (p0.m == 999)].iloc[0]
            spy_o = metrics(c["spy"].loc[c["oos_idx"]])
            v2_o = metrics(c["base_v2"][b].loc[c["oos_idx"]])
            P(f"\n  --- {pn} @{b} bps ---")
            P(f"      {'arm':38s} {'IS S':>7s} {'OOS CAGR':>9s} {'OOS S':>7s} {'OOS DD':>8s} {'turn/yr':>8s}")
            def wrow(nm, isS, oc, os_, odd, t):
                P(f"      {nm:38s} {isS:7.3f} {oc:9.2%} {os_:7.3f} {odd:8.2%} {t:8.2f}")
                wf.append(dict(panel=pn, cost_bps=b, arm=nm, IS_Sharpe=isS, OOS_CAGR=oc,
                               OOS_Sharpe=os_, OOS_MaxDD=odd, turn_yr=t))
            wrow(f"IS-PICK phase0  (cad={pick0.cadence}, m={int(pick0.m)})", pick0.IS_Sharpe,
                 pick0.OOS_CAGR, pick0.OOS_Sharpe, pick0.OOS_MaxDD, pick0.turn_yr)
            ra = am.loc[ka]
            wrow(f"IS-PICK anchor-agnostic (cad={ka[0]}, m={int(ka[1])})", ra.IS_Sharpe,
                 ra.OOS_CAGR, ra.OOS_Sharpe, ra.OOS_MaxDD, ra.turn_yr)
            wrow("CONTROL parent (cad=W, m=0)", par.IS_Sharpe, par.OOS_CAGR, par.OOS_Sharpe,
                 par.OOS_MaxDD, par.turn_yr)
            wrow("CONTROL idea 273 (cad=W, m=999)", b273.IS_Sharpe, b273.OOS_CAGR, b273.OOS_Sharpe,
                 b273.OOS_MaxDD, b273.turn_yr)
            wrow("CONTROL RULES v2 (live)", metrics(c["base_v2"][b].loc[c["is_idx"]])["Sharpe"],
                 v2_o["CAGR"], v2_o["Sharpe"], v2_o["MaxDD"], np.nan)
            wrow("CONTROL SPY", metrics(c["spy"].loc[c["is_idx"]])["Sharpe"], spy_o["CAGR"],
                 spy_o["Sharpe"], spy_o["MaxDD"], np.nan)
            wrow("CONTROL grid mean (do-nothing draw)", sub.IS_Sharpe.mean(), sub.OOS_CAGR.mean(),
                 sub.OOS_Sharpe.mean(), sub.OOS_MaxDD.mean(), sub.turn_yr.mean())
            rho = sub.groupby(["cadence", "m"])[["IS_Sharpe", "OOS_Sharpe"]].mean().corr(method="spearman").iloc[0, 1]
            P(f"      Spearman(IS Sharpe, OOS Sharpe) over the 36 (cadence,m) cells: {rho:+.3f}")
    pd.DataFrame(wf).to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ------------------------------------------------------------- D4: 4b census
    P("\n" + "=" * 104)
    P("D4  KEEP-path census over every grid point")
    P("=" * 104)
    for pn, (g, c, ppx) in PANELS.items():
        for b in RUNGS:
            sub = g[g.cost_bps == b]
            P(f"  {pn}@{b}bps: 4b PASS {int(sub.pass4b.sum())}/{len(sub)}   "
              f"4a PASS {int(sub.pass4a.sum())}/{len(sub)}")
            if sub.pass4b.any():
                pc = sub[sub.pass4b].groupby(["cadence", "m"]).size()
                P(f"     4b cells (cadence,m -> phases passing): "
                  + ", ".join(f"{k}:{v}/{1 if k[0]=='D' else len(PHASES)}" for k, v in pc.items()))
    P("\nDone.")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_LINES) + "\n")


if __name__ == "__main__":
    main()
