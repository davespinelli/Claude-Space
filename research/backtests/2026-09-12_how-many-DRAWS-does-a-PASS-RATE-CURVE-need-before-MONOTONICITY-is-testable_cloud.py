#!/usr/bin/env python3
"""Idea 528 (cloud, 2026-09-12) - how-many-DRAWS-does-a-PASS-RATE-CURVE-need-before-MONOTONICITY-is-testable.

QUESTION (QUEUE idea 528, verbatim)
    Idea 285's non-monotonicity is a resolution statement: at 20 draws per rung the pass-rate
    standard error is ~0.11 at 50%, which is the size of the wrong-way steps it reports.  Bootstrap
    the 1,680 committed arm-rows to find the draws-per-rung at which the up-step count of a truly
    monotone curve falls below 1 in 20, and publish it as the minimum for any future admissibility
    claim.  Max 2 params (draws, rungs).

WHY THIS RUN HAS A PRICE LEG (three previous cloud runs skipped this idea for not having one)
    The queue says "bootstrap the committed arm-rows".  Those rows are markdown, so the idea kept
    being skipped as unable to carry rule 8 or either KEEP path.  This run rebuilds the object
    instead of re-reading it: 160 REAL random books per panel, each one priced through the engine
    at every gross rung, 10 bps, t+1, weekly.  The pass-rate curve is then a curve over books, the
    bootstrap is over books, and rule 8 and both KEEP paths apply to the books themselves.

WHAT IS MEASURED, AND WHERE THE MONOTONE CURVE COMES FROM
    A "truly monotone" null cannot be assumed here - PROTOCOL 4b's pass rate against gross is a
    HUMP (idea 670/677's gross window), not a monotone curve.  So the monotone reference is taken
    where it is monotone BY CONSTRUCTION and CHECKED at full resolution (gate G4):
      leg_cagr  CAGR >= 70% of SPY's        - a book's CAGR rises with gross, so this leg's pass
                                              rate is monotone INCREASING in gross
      leg_dd    MaxDD <= 60% of SPY's       - monotone DECREASING in gross
      4b        the conjunction              - reported beside them, NOT used as the monotone null
    A WRONG-WAY STEP is a strictly backwards move along the rung ladder (ties never count).  For a
    rung ladder whose N=160 reference curve is monotone, every wrong-way step a D-draw subsample
    shows is pure sampling noise.  D* is the smallest ladder rung of D at which
    P(at least one wrong-way step) < 0.05 - "1 in 20", the queue's own bar - over 2,000 resamples.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two)
    1. DRAWS per rung D in {5, 10, 20, 40, 80, 160}  (idea 285 used 20)
    2. RUNG SET: FINE = 7 gross rungs {0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00}
                 COARSE = 4 rungs {0.25, 0.50, 0.75, 1.00}
    6 x 2 x 3 panels x 3 legs x 2 resampling modes x 2 windows = 432 D-cells, all reported.
    PINNED: book width k = 20 names, equal weight, names drawn ONCE per book (not re-drawn at
    rebalance), weekly rebalance, 10 bps, t+1, N = 160 base draws, B = 2,000 resamples, seed 528.

REPORTED, NEVER SELECTED
    RESAMPLING MODE - PAIRED (the same D books priced at every rung, which is how a real sweep is
    run) and INDEPENDENT (a fresh D books at each rung, which is what a binomial standard error
    assumes).  Both always published; neither is chosen.
    PANEL - U56, B136, SMALL664.  SURVIVORSHIP: B136 and SMALL664 are CURRENT constituents
    (PROTOCOL rule 9); SMALL664 drops every ticker with max_1d_move >= 1.0 in data/small_meta.csv.

PRE-REGISTERED HYPOTHESES (written before any number below was read)
    H_20     : idea 285's 20 draws per rung is NOT enough - P(>=1 wrong-way step) >= 0.05 at D = 20
               on the FINE ladder, on all three panels, for at least one monotone leg.
    H_D      : D* exists on the ladder (<= 160) for every (panel, leg) on the FINE ladder.
    H_PAIR   : PAIRING IS FREE RESOLUTION - at every D, the paired mode's wrong-way rate is lower
               than the independent mode's, so a sweep that re-draws per rung is throwing away
               power a sweep that re-uses books keeps.
    H_COARSE : fewer rungs is cheaper - D*(COARSE) <= D*(FINE) everywhere.
    H_OOS    : rule 8 on the ANSWER - D* calibrated on IS (<= 2016-12-31) also clears the 1-in-20
               bar when the pass labels are recomputed on OOS (2017+), at every (panel, leg, mode).

GATES (printed BEFORE any new number is read)
    G1 engine     : vectorised runner vs engine.backtest on one drawn book per panel    bar 1e-12
    G2 no leverage: max daily target gross over every drawn book                          bar 1.0
    G3 determinism: a drawn book repriced twice, bit-identical returns (the draw itself is a
                    seeded permutation, seed 528, reproducible by re-running the file)          bar 0
    G4 monotone   : the N=160 reference curve for leg_cagr (increasing) and leg_dd
                    (decreasing) has ZERO wrong-way steps on the FINE ladder, or the leg is
                    reported as NOT a usable monotone null                                   bar 0

RULE 8 WALK-FORWARD (required, PROTOCOL rule 8)
    Pass labels are computed twice: IS = <= 2016-12-31 only, OOS = >= 2017-01-01 only, each with
    its own SPY bars and its own halves.  D* is CALIBRATED on IS and READ on OOS.  Every drawn book
    also carries its OOS CAGR/Sharpe/MaxDD against RULES v2 (live) and SPY, and both KEEP paths.

OUTPUTS
    ..._cloud.books.csv  ..._cloud.curves.csv  ..._cloud.dstar.csv  ..._cloud.console.txt
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest as engine_backtest, rebalance_mask, metrics  # noqa

STEM = Path(__file__).with_suffix("")
OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

COST_BPS = 10.0
K = 20                      # book width, pinned
NDRAW = 160                 # base draws per panel, pinned
NBOOT = 2000                # resamples, pinned
SEED = 528
DS = [5, 10, 20, 40, 80, 160]
RUNGS = {"FINE": [0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.00],
         "COARSE": [0.25, 0.50, 0.75, 1.00]}
MODES = ["PAIRED", "INDEPENDENT"]
IS_END = pd.Timestamp("2016-12-31")
OOS_START = pd.Timestamp("2017-01-01")

def run_np(rets, w_t, mask, cost_bps=COST_BPS):
    n = rets.shape[0]; cur = np.zeros(rets.shape[1]); port = np.empty(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = w_t[i]; to = np.abs(new - cur).sum(); cur = new.copy()
        else:
            to = 0.0
        port[i] = cur @ rets[i] - to * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return port

def book_returns(px_sub, g):
    """Equal-weight book over the k drawn names at gross g: weight g/k per priced name, the rest
    to CASH (de-gross, never re-spread).  Same engine convention as everything else here."""
    priced = px_sub.notna().to_numpy().astype(float)
    W = priced * (g / px_sub.shape[1])
    rets = px_sub.pct_change().fillna(0.0).to_numpy()
    w_t = np.vstack([np.full(px_sub.shape[1], np.nan), W[:-1]])
    w_t = np.nan_to_num(w_t)
    mask = rebalance_mask(px_sub.index, "W").shift(1, fill_value=False).to_numpy()
    return pd.Series(run_np(rets, w_t, mask), index=px_sub.index), float(W.sum(axis=1).max())

def legs(r, spy):
    """PROTOCOL 4b's three legs on whatever window r and spy are already cut to."""
    h = len(r) // 2
    s1, s2 = metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]
    p1, p2 = metrics(spy.iloc[:h])["Sharpe"], metrics(spy.iloc[h:])["Sharpe"]
    m, ms = metrics(r), metrics(spy)
    return dict(leg_sharpe=bool(s1 > p1 and s2 > p2),
                leg_dd=bool(m["MaxDD"] >= 0.60 * ms["MaxDD"]),
                leg_cagr=bool(m["CAGR"] >= 0.70 * ms["CAGR"]),
                CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=s1, H2=s2)

def wrong_way(p, direction):
    d = np.diff(p)
    return int((d < 0).sum()) if direction > 0 else int((d > 0).sum())

def boot_rate(passes, rung_idx, D, mode, direction, rng):
    """P(>=1 wrong-way step) over NBOOT resamples of D draws.  passes: (NDRAW, nrung) bool."""
    sub = passes[:, rung_idx]; N = sub.shape[0]; hits = 0
    for _ in range(NBOOT):
        if mode == "PAIRED":
            idx = rng.integers(0, N, D); p = sub[idx].mean(axis=0)
        else:
            p = np.array([sub[rng.integers(0, N, D), j].mean() for j in range(sub.shape[1])])
        if wrong_way(p, direction) > 0: hits += 1
    return hits / NBOOT

def panels():
    P = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    P["SMALL664"] = sm[[c for c in sm.columns if c not in bad]]
    return P

def main():
    say("=" * 100)
    say("IDEA 528  how-many-DRAWS-does-a-PASS-RATE-CURVE-need-before-MONOTONICITY-is-testable  (cloud, 2026-09-12)")
    say(f"k={K} equal-weight names per book | {NDRAW} books per panel | {len(RUNGS['FINE'])} gross rungs |"
        f" 10 bps | t+1 | weekly | seed {SEED} | {NBOOT} resamples")
    say("=" * 100)

    P = panels()
    books, curves, dstar = [], [], []
    g1 = g2 = 0.0; g3_ok = True

    for panel, px_raw in P.items():
        px = px_raw.drop(columns=["SPY"]) if panel == "SMALL664" else px_raw
        start = px.index[260]
        spy = px_raw["SPY"].pct_change().fillna(0.0).loc[start:]
        base = None
        # live baseline on this panel, for the 4a leg and the OOS comparison
        bw = rules_v2_weights(px)
        brets = px.pct_change().fillna(0.0).to_numpy()
        bmask = rebalance_mask(px.index, "W").shift(1, fill_value=False).to_numpy()
        bwt = np.nan_to_num(np.vstack([np.full(px.shape[1], np.nan), bw.to_numpy()[:-1]]))
        base = pd.Series(run_np(brets, bwt, bmask), index=px.index).loc[start:]

        cov = px.notna().mean()
        pool = sorted(cov[cov >= 0.90].index)            # names priced on >= 90% of the panel's days
        say(f"panel {panel:9s} cols={px.shape[1]:4d} eligible pool (>=90% coverage) = {len(pool)}"
            f"  rows={len(px)}  {px.index[0].date()} .. {px.index[-1].date()}")

        rng = np.random.default_rng(SEED)
        sel = [rng.choice(len(pool), size=K, replace=False) for _ in range(NDRAW)]
        rows = {}
        for d, s in enumerate(sel):
            sub = px[[pool[i] for i in s]]
            for g in RUNGS["FINE"]:
                r, mg = book_returns(sub, g)
                g2 = max(g2, mg)
                r = r.loc[start:]
                L_full = legs(r, spy)
                L_is = legs(r.loc[:IS_END], spy.loc[:IS_END])
                L_oos = legs(r.loc[OOS_START:], spy.loc[OOS_START:])
                bh = len(base) // 2
                p4a = bool(L_full["H1"] > metrics(base.iloc[:bh])["Sharpe"]
                           and L_full["H2"] > metrics(base.iloc[bh:])["Sharpe"]
                           and L_full["MaxDD"] >= metrics(base)["MaxDD"])
                p4b = bool(L_full["leg_sharpe"] and L_full["leg_dd"] and L_full["leg_cagr"]
                           and L_oos["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"])
                rows[(d, g)] = dict(panel=panel, draw=d, gross=g,
                                    CAGR=L_full["CAGR"], Sharpe=L_full["Sharpe"], MaxDD=L_full["MaxDD"],
                                    H1=L_full["H1"], H2=L_full["H2"],
                                    OOS_CAGR=L_oos["CAGR"], OOS_Sharpe=L_oos["Sharpe"], OOS_MaxDD=L_oos["MaxDD"],
                                    full_cagr=L_full["leg_cagr"], full_dd=L_full["leg_dd"],
                                    full_4b=p4b, pass4a=p4a,
                                    is_cagr=L_is["leg_cagr"], is_dd=L_is["leg_dd"],
                                    is_4b=bool(L_is["leg_sharpe"] and L_is["leg_dd"] and L_is["leg_cagr"]),
                                    oos_cagr=L_oos["leg_cagr"], oos_dd=L_oos["leg_dd"],
                                    oos_4b=bool(L_oos["leg_sharpe"] and L_oos["leg_dd"] and L_oos["leg_cagr"]))
        books.extend(rows.values())

        # G1 / G3 on one drawn book
        sub = px[[pool[i] for i in sel[0]]]
        Wdf = pd.DataFrame((sub.notna().to_numpy().astype(float)) * (0.75 / K), index=sub.index, columns=sub.columns)
        eng = engine_backtest(sub, Wdf, cost_bps=COST_BPS, freq="W")["returns"]
        mine = book_returns(sub, 0.75)[0]
        g1 = max(g1, float(np.abs(eng - mine).max()))
        if not np.allclose(book_returns(sub, 0.75)[0].to_numpy(), mine.to_numpy(), rtol=0, atol=0, equal_nan=True):
            g3_ok = False

        # ------------------------------------------------ curves and D* ---
        for rs, gl in RUNGS.items():
            for window, keys in (("FULL", ("full_cagr", "full_dd", "full_4b")),
                                 ("IS", ("is_cagr", "is_dd", "is_4b")),
                                 ("OOS", ("oos_cagr", "oos_dd", "oos_4b"))):
                for leg, direction in zip(keys, (+1, -1, 0)):
                    M = np.array([[rows[(d, g)][leg] for g in gl] for d in range(NDRAW)], dtype=bool)
                    ref = M.mean(axis=0)
                    ww = wrong_way(ref, direction if direction else +1)
                    dd = np.diff(M.astype(int), axis=1)
                    if direction >= 0:  mono_book = float((dd >= 0).all(axis=1).mean())
                    else:               mono_book = float((dd <= 0).all(axis=1).mean())
                    curves.append(dict(panel=panel, rungset=rs, window=window, leg=leg,
                                       legkey=leg.split("_")[-1],
                                       direction=direction, ref="|".join(f"{x:.4f}" for x in ref),
                                       ref_wrongway=ww, book_monotone_share=mono_book))
                    if direction == 0:            # 4b: reported, never used as a monotone null
                        continue
                    for mode in MODES:
                        rng2 = np.random.default_rng(SEED + 1)
                        rates = {}
                        for D in DS:
                            rates[D] = boot_rate(M, list(range(len(gl))), D, mode, direction, rng2)
                        ds = next((D for D in DS if rates[D] < 0.05), np.nan)
                        dstar.append(dict(panel=panel, rungset=rs, window=window, leg=leg,
                                          legkey=leg.split("_")[-1], resample=mode,
                                          ref_wrongway=ww, Dstar=ds,
                                          **{f"P{D}": rates[D] for D in DS}))

    bk = pd.DataFrame(books); cv = pd.DataFrame(curves); dsr = pd.DataFrame(dstar)

    say("")
    say("GATES")
    say(f"  G1 engine vs runner            max|dret| = {g1:.3e}  bar 1e-12  {'PASS' if g1 < 1e-12 else 'FAIL'}")
    say(f"  G2 no leverage                 max gross = {g2:.6f}   bar <= 1.0 {'PASS' if g2 <= 1.0 + 1e-12 else 'FAIL'}")
    say(f"  G3 determinism                 rebuilt identical      {'PASS' if g3_ok else 'FAIL'}")
    mono = cv[(cv.rungset == "FINE") & (cv.window == "FULL") & (cv.direction != 0)]
    say(f"  G4 monotone reference (FINE, FULL)  wrong-way steps in the N={NDRAW} reference curve: " +
        "  ".join(f"{r.panel}/{r.leg}={r.ref_wrongway}" for _, r in mono.iterrows()) +
        f"   bar 0  {'PASS' if mono.ref_wrongway.sum() == 0 else 'FAIL - that leg is NOT a usable monotone null'}")

    say("")
    say(f"SECTION 1  THE REFERENCE CURVES (all {NDRAW} draws; pass rate per gross rung)")
    for _, r in cv[(cv.rungset == "FINE")].iterrows():
        say(f"  {r.panel:9s} {r.window:4s} {r.leg:9s} dir={r.direction:+d}  {r.ref}   wrong-way steps {r.ref_wrongway}")

    say("")
    say("SECTION 1b  WHY PAIRING IS FREE: the share of BOOKS whose own pass vector is already")
    say("            monotone along the rung ladder (a paired subsample of monotone books cannot")
    say("            produce a wrong-way step at any D)")
    for _, r in cv[(cv.rungset == "FINE")].iterrows():
        say(f"  {r.panel:9s} {r.window:4s} {r.leg:9s} dir={r.direction:+d}  book-monotone share "
            f"{r.book_monotone_share:.4f}")

    say("")
    say("SECTION 2  P(>=1 WRONG-WAY STEP) BY DRAWS PER RUNG, AND D* (first rung below 1 in 20)")
    for _, r in dsr.iterrows():
        say(f"  {r.panel:9s} {r.rungset:6s} {r.window:4s} {r.leg:9s} {r['resample']:11s} " +
            " ".join(f"D{D}={r[f'P{D}']:.3f}" for D in DS) +
            f"   D* = {int(r.Dstar) if pd.notna(r.Dstar) else '>160'}"
            + ("" if r.ref_wrongway == 0 else f"   [reference itself has {r.ref_wrongway} wrong-way steps - D* not meaningful]"))

    say("")
    say("HYPOTHESES")
    f = dsr[(dsr.rungset == "FINE") & (dsr.window == "FULL") & (dsr.ref_wrongway == 0)]
    h20 = {p: float(f[f.panel == p].P20.max()) for p in P if len(f[f.panel == p])}
    say(f"  H_20     {'PASSES' if h20 and min(h20.values()) >= 0.05 else 'FAILS'}  worst-leg "
        f"P(>=1 wrong-way step) at idea 285's D=20: " + "  ".join(f"{k} {v:.3f}" for k, v in h20.items()))
    reach = f.Dstar.notna()
    say(f"  H_D      {'PASSES' if reach.all() else 'FAILS'}  D* reached on the ladder in "
        f"{int(reach.sum())} of {len(f)} (panel, leg, mode) FULL cells; D* values " +
        ", ".join(f"{r.panel}/{r.leg}/{r['resample']}={int(r.Dstar) if pd.notna(r.Dstar) else '>160'}" for _, r in f.iterrows()))
    pair_win = []
    for (pn, rs, w, lg), grp in dsr[dsr.ref_wrongway == 0].groupby(["panel", "rungset", "window", "leg"]):
        if set(grp["resample"]) == set(MODES):
            a = grp[grp["resample"] == "PAIRED"].iloc[0]; b = grp[grp["resample"] == "INDEPENDENT"].iloc[0]
            for D in DS: pair_win.append(a[f"P{D}"] <= b[f"P{D}"])
    say(f"  H_PAIR   {'PASSES' if all(pair_win) else 'FAILS'}  paired <= independent in "
        f"{sum(pair_win)} of {len(pair_win)} (cell, D) comparisons")
    cw = []
    for (pn, w, lg, md), grp in dsr[dsr.ref_wrongway == 0].groupby(["panel", "window", "leg", "resample"]):
        if set(grp.rungset) == {"FINE", "COARSE"}:
            a = grp[grp.rungset == "COARSE"].iloc[0].Dstar; b = grp[grp.rungset == "FINE"].iloc[0].Dstar
            a = 320 if a != a or a is None else a; b = 320 if b != b or b is None else b
            cw.append(a <= b)
    say(f"  H_COARSE {'PASSES' if all(cw) else 'FAILS'}  D*(COARSE) <= D*(FINE) in {sum(cw)} of {len(cw)} cells")
    # rule 8: D* calibrated on IS, read on OOS
    ok, tot, detail = 0, 0, []
    for (pn, rs, lg, md), grp in dsr.groupby(["panel", "rungset", "legkey", "resample"]):
        gi = grp[grp.window == "IS"]; go = grp[grp.window == "OOS"]
        if not len(gi) or not len(go): continue
        di = gi.iloc[0].Dstar
        if di != di or di is None: continue
        tot += 1; po = float(go.iloc[0][f"P{int(di)}"])
        ok += int(po < 0.05); detail.append(f"{pn}/{rs}/{lg}/{md}: D*_IS={int(di)} -> P_OOS={po:.3f}")
    say(f"  H_OOS    {'PASSES' if tot and ok == tot else 'FAILS'}  the IS-calibrated D* clears the "
        f"1-in-20 bar out of sample in {ok} of {tot} cells")
    for d in detail: say("           " + d)

    say("")
    say("SECTION 3  THE BOOKS THEMSELVES (rule 8 price leg; 10 bps, t+1, weekly)")
    for panel, px_raw in P.items():
        px = px_raw.drop(columns=["SPY"]) if panel == "SMALL664" else px_raw
        start = px.index[260]
        spy = px_raw["SPY"].pct_change().fillna(0.0).loc[start:]
        so = spy.loc[OOS_START:]
        sb = bk[bk.panel == panel]
        say(f"  --- {panel} ---  SPY full CAGR {metrics(spy)['CAGR']:+.2%} Sharpe {metrics(spy)['Sharpe']:+.3f} "
            f"MaxDD {metrics(spy)['MaxDD']:+.2%} | OOS CAGR {metrics(so)['CAGR']:+.2%} Sharpe {metrics(so)['Sharpe']:+.3f}")
        for g in RUNGS["FINE"]:
            s = sb[sb.gross == g]
            say(f"    gross {g:<6g} books={len(s)}  median CAGR {s.CAGR.median():+.2%} Sharpe {s.Sharpe.median():+.3f} "
                f"MaxDD {s.MaxDD.median():+.2%} | OOS median CAGR {s.OOS_CAGR.median():+.2%} "
                f"Sharpe {s.OOS_Sharpe.median():+.3f} MaxDD {s.OOS_MaxDD.median():+.2%} | "
                f"4b {int(s.full_4b.sum())}/{len(s)}  4a {int(s.pass4a.sum())}/{len(s)}")

    bk.to_csv(f"{STEM}.books.csv", index=False)
    cv.to_csv(f"{STEM}.curves.csv", index=False)
    dsr.to_csv(f"{STEM}.dstar.csv", index=False)
    say("")
    say("WROTE  .books.csv  .curves.csv  .dstar.csv")
    Path(f"{STEM}.console.txt").write_text("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
