#!/usr/bin/env python3
"""Idea 585 — does the BREADTH gate's 4b pass live ONLY at gross 1.00?

idea 581 PARKed `U56 BREADTH-DG q=0.20 g=1.00` as a 4b passer (full 16.01% / 1.258 / -16.48%,
OOS 16.39% / 1.456 / -14.16%) while the 2026-09-09 KILL run failed the SAME family at g=0.75.
Both runs are right; they differ by one dial.  This run prices that dial properly.

WHAT IS SWEPT (the only two tuned parameters, per PROTOCOL rule 4):
    g  — gross, 17-point ladder 0.20 .. 1.00 step 0.05.  No leverage (PROTOCOL rule 2).
    q  — the breadth gate's trailing-quantile dial, in {0.10, 0.20, 0.35, 0.50} (idea 581's grid).
Panels: U56 (research/universe.json) and B136 (research/universe_broad.json), as the idea says.
ALL 2 x 17 x 4 = 136 clause books and 2 x 17 = 34 EWall controls are reported; nothing is hidden.

THE BOOK (idea 581's BREADTH-DG, reproduced verbatim from its committed source):
    hold every priced name at g/N; breadth = share of priced names above their own 200d MA;
    the gate FIRES (whole book -> CASH at 0%) when breadth is below its own trailing 5-year
    q-quantile (1260 trading days, min 504).  De-gross, never re-spread.  Weekly, t+1, 10 bps.

RULE 8 (required, PROTOCOL rule 8): (q, g) chosen on 2009-01-01..2016-12-31 ONLY under two
pre-stated conventions, then 2017-01-01..2026 read ONCE.
    S1  max IS Sharpe over the whole 68-cell grid.
    S2  max IS Sharpe among cells that pass a 4b-shaped screen computed on IS DATA ONLY
        (IS Sharpe > IS SPY Sharpe, IS MaxDD >= 0.60 x IS SPY MaxDD, IS CAGR >= 0.70 x IS SPY CAGR);
        falls back to S1 if the screen is empty.
Both KEEP paths are evaluated on every grid point (4a vs RULES v2, 4b vs SPY incl. the OOS leg).

Deterministic; no network (load_universe reads the committed caches).  Never calls yfinance.
SURVIVORSHIP: B136 is a CURRENT-constituent list, so every LEVEL on it is biased up; the
g-ladder SHAPE (which is what this idea asks about) is a within-panel comparison and is not.
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STAMP = "2026-09-10_does-the-BREADTH-gate-4b-pass-live-only-at-gross-1.00_cloud"
OUT = Path(__file__).resolve().parent
COST, FREQ = 10.0, "W"
MA_WIN = 200
QWIN, QMIN = 1260, 504
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
GS = tuple(round(0.20 + 0.05 * i, 2) for i in range(17))      # 17-point ladder, 0.20 .. 1.00
QS = (0.10, 0.20, 0.35, 0.50)                                  # idea 581's dial grid

_LOG: list[str] = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); _LOG.append(s)


# ---------------------------------------------------------------- engine clone (idea 317/581)
def fast_bt(px, W, cost_bps=COST, freq=FREQ):
    """Closed-form equivalent of engine.backtest: same t+1 application, same weekly schedule,
    same intra-period drift with cash flat, same turnover-based cost."""
    idx = px.index
    rets = px.pct_change().fillna(0.0).to_numpy(float)
    wt = W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).to_numpy(float)
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).to_numpy(bool).copy()
    mask[0] = True
    T, N = rets.shape
    Cs = np.empty((T, N)); Cs[0] = 1.0
    np.cumprod(1.0 + rets[:-1], axis=0, out=Cs[1:])
    starts = np.flatnonzero(mask)
    seg = np.searchsorted(starts, np.arange(T), side="right") - 1
    s_of_t = starts[seg]
    new = wt[s_of_t]
    num = new * (Cs / Cs[s_of_t])
    D = num.sum(axis=1) + (1.0 - new.sum(axis=1))
    held = num / D[:, None]
    turn = np.zeros(T); turn[0] = np.abs(wt[0]).sum()
    later = starts[1:]
    if len(later):
        sp = starts[seg[later] - 1]
        prev_new = wt[sp]
        np_ = prev_new * (Cs[later] / Cs[sp])
        Dp = np_.sum(axis=1) + (1.0 - prev_new.sum(axis=1))
        turn[later] = np.abs(wt[later] - np_ / Dp[:, None]).sum(axis=1)
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx), pd.Series(held.sum(axis=1), index=idx)


def mrow(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def spearman(a, b):
    """Rank-then-Pearson; scipy is not installed in this sandbox."""
    a = pd.Series(np.asarray(a, float)).rank()
    b = pd.Series(np.asarray(b, float)).rank()
    return float(a.corr(b))


def mean_target_gross(W, start=None):
    rb = rebalance_mask(W.index, FREQ)
    g = W.loc[rb].sum(axis=1)
    if start is not None: g = g.loc[start:]
    return float(g.mean())


# ---------------------------------------------------------------- the book (idea 581 verbatim)
def build_panel(px, tradable):
    elig = px.notna() & pd.DataFrame(np.tile(tradable, (len(px), 1)),
                                     index=px.index, columns=px.columns)
    ma200 = (px > px.rolling(MA_WIN).mean()) & elig
    n = elig.sum(axis=1).replace(0, np.nan)
    breadth = (ma200.sum(axis=1) / n).ffill()
    return elig, breadth


def ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.astype(float).div(n, axis=0).fillna(0.0)


def gate_off(breadth, q):
    """Risk-off when breadth is below its own trailing 5y q-quantile."""
    thr = breadth.rolling(QWIN, min_periods=QMIN).quantile(q)
    return (breadth < thr).fillna(False)


def breadth_dg(elig, breadth, q, g):
    return ew(elig, g).where(~gate_off(breadth, q), 0.0)


# ---------------------------------------------------------------- KEEP paths (PROTOCOL rule 4)
def keep_4a(m, b):
    return bool(m["H1"] > b["H1"] and m["H2"] > b["H2"] and m["MaxDD"] >= b["MaxDD"])


def keep_4b(m, mo, s, so):
    """4b legs, named so the binding one can be reported."""
    legs = dict(H1=m["H1"] > s["H1"], H2=m["H2"] > s["H2"], OOS=mo["Sharpe"] > so["Sharpe"],
                DD=m["MaxDD"] >= 0.60 * s["MaxDD"], CAGR=m["CAGR"] >= 0.70 * s["CAGR"])
    return bool(all(legs.values())), legs


# ---------------------------------------------------------------- pre-registered gate
def gate_g1(px, W, label):
    """The vectorised runner must reproduce engine.backtest exactly.

    engine.backtest emits NaN on the first rows where some panel columns are not yet priced
    (7 of U56's 56 columns are NaN on 2008-01-02); fast_bt emits 0.0 there.  Those rows are
    ALL before the scored window (which starts at px.index[260]), so the gate is read on the
    finite rows and the NaN count is printed rather than hidden."""
    ref = backtest(px, W, cost_bps=COST, freq=FREQ)["returns"]
    r, _ = fast_bt(px, W)
    nan_idx = ref.index[ref.isna()]
    start = px.index[max(260, MA_WIN + 20)]
    late = [t for t in nan_idx if t >= start]
    d = float(np.nanmax(np.abs(ref.to_numpy() - r.to_numpy())))
    ok = d < 1e-12 and not late
    P(f"  G1 {label:24s} max|fast_bt - engine.backtest| = {d:.3e} over "
      f"{len(ref)-len(nan_idx)} finite rows ({len(nan_idx)} engine-NaN warm-up rows, "
      f"{len(late)} of them inside the scored window)   {'PASS' if ok else 'FAIL'}")
    return 0.0 if ok else 1.0


def run_panel(pname, px, tradable, cells):
    t0 = time.time()
    elig, breadth = build_panel(px, tradable)
    start = px.index[max(260, MA_WIN + 20)]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    b2, _ = fast_bt(px, rules_v2_weights(px)); b2 = b2.loc[start:]

    S, B = mrow(spy), mrow(b2)
    So, Bo = mrow(spy.loc[OOS_START:]), mrow(b2.loc[OOS_START:])
    Si = mrow(spy.loc[IS_START:IS_END])
    P(f"\nPANEL {pname}: {len(px.columns)} cols, {int(tradable.sum())} tradable, "
      f"{px.index[0].date()}..{px.index[-1].date()}, scored from {start.date()}")
    P(f"  SPY      full CAGR {S['CAGR']:7.2%} Sharpe {S['Sharpe']:6.3f} MaxDD {S['MaxDD']:7.2%} "
      f"H1/H2 {S['H1']:.3f}/{S['H2']:.3f} | OOS {So['CAGR']:7.2%}/{So['Sharpe']:6.3f}/{So['MaxDD']:7.2%}")
    P(f"  RULESv2  full CAGR {B['CAGR']:7.2%} Sharpe {B['Sharpe']:6.3f} MaxDD {B['MaxDD']:7.2%} "
      f"H1/H2 {B['H1']:.3f}/{B['H2']:.3f} | OOS {Bo['CAGR']:7.2%}/{Bo['Sharpe']:6.3f}/{Bo['MaxDD']:7.2%}")
    P(f"  4b bars on this panel: Sharpe > SPY halves ({S['H1']:.3f}/{S['H2']:.3f}) and OOS "
      f"({So['Sharpe']:.3f}); MaxDD >= {0.60*S['MaxDD']:.2%}; CAGR >= {0.70*S['CAGR']:.2%}")

    # controls: EWall (gate never fires) at every rung of the ladder
    for g in GS:
        r, _ = fast_bt(px, ew(elig, g)); r = r.loc[start:]
        m, mo, mi = mrow(r), mrow(r.loc[OOS_START:]), mrow(r.loc[IS_START:IS_END])
        p4b, legs = keep_4b(m, mo, S, So)
        cells.append(dict(panel=pname, arm="EWALL-control", q=np.nan, gross=g,
                          CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                          H1=m["H1"], H2=m["H2"],
                          IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                          OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                          pass4a=keep_4a(m, B), pass4b=p4b,
                          fail_legs=";".join(k for k, v in legs.items() if not v),
                          spy_CAGR=S["CAGR"], spy_Sharpe=S["Sharpe"], spy_MaxDD=S["MaxDD"],
                          spy_H1=S["H1"], spy_H2=S["H2"], spy_OOS_Sharpe=So["Sharpe"],
                          spy_OOS_CAGR=So["CAGR"], spy_OOS_MaxDD=So["MaxDD"],
                          spy_IS_Sharpe=Si["Sharpe"], spy_IS_CAGR=Si["CAGR"], spy_IS_MaxDD=Si["MaxDD"],
                          b2_Sharpe=B["Sharpe"], b2_MaxDD=B["MaxDD"], b2_H1=B["H1"], b2_H2=B["H2"],
                          b2_OOS_Sharpe=Bo["Sharpe"], b2_OOS_CAGR=Bo["CAGR"], b2_OOS_MaxDD=Bo["MaxDD"],
                          mean_target_gross=mean_target_gross(ew(elig, g), start)))

    for q in QS:
        off = gate_off(breadth, q)
        fire = float(off.loc[start:].mean())
        for g in GS:
            W = breadth_dg(elig, breadth, q, g)
            r, _ = fast_bt(px, W); r = r.loc[start:]
            m, mo, mi = mrow(r), mrow(r.loc[OOS_START:]), mrow(r.loc[IS_START:IS_END])
            p4b, legs = keep_4b(m, mo, S, So)
            cells.append(dict(panel=pname, arm="BREADTH-DG", q=q, gross=g,
                              CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                              H1=m["H1"], H2=m["H2"],
                              IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                              OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                              pass4a=keep_4a(m, B), pass4b=p4b,
                              fail_legs=";".join(k for k, v in legs.items() if not v),
                              fire_rate=fire,
                              spy_CAGR=S["CAGR"], spy_Sharpe=S["Sharpe"], spy_MaxDD=S["MaxDD"],
                              spy_H1=S["H1"], spy_H2=S["H2"], spy_OOS_Sharpe=So["Sharpe"],
                              spy_OOS_CAGR=So["CAGR"], spy_OOS_MaxDD=So["MaxDD"],
                              spy_IS_Sharpe=Si["Sharpe"], spy_IS_CAGR=Si["CAGR"], spy_IS_MaxDD=Si["MaxDD"],
                              b2_Sharpe=B["Sharpe"], b2_MaxDD=B["MaxDD"], b2_H1=B["H1"], b2_H2=B["H2"],
                              b2_OOS_Sharpe=Bo["Sharpe"], b2_OOS_CAGR=Bo["CAGR"], b2_OOS_MaxDD=Bo["MaxDD"],
                              mean_target_gross=mean_target_gross(W, start)))
    P(f"  {len(QS)*len(GS)} clause books + {len(GS)} controls  [{time.time()-t0:.1f}s]")


def main():
    P(f"=== {STAMP} ===")
    P(__doc__.strip())

    pxU = load_universe()
    pxB = load_universe(broad=True)
    panels = [("U56", pxU, np.ones(len(pxU.columns), bool)),
              ("B136", pxB, np.ones(len(pxB.columns), bool))]

    P("\nGATES (pre-registered, printed before any hypothesis number)")
    ok = True
    for nm, px, tr in panels:
        el, br = build_panel(px, tr)
        ok &= gate_g1(px, ew(el, 0.75), f"{nm}/EWall g=0.75") < 1e-12
        ok &= gate_g1(px, breadth_dg(el, br, 0.20, 1.00), f"{nm}/BREADTH-DG q.20 g1.0") < 1e-12
    # G2: gross is a pure exposure dial -> the gate's FIRING PATH must not depend on g.
    elu, bru = build_panel(pxU, panels[0][2])
    a = breadth_dg(elu, bru, 0.20, 0.50).sum(axis=1) / 0.50
    b = breadth_dg(elu, bru, 0.20, 1.00).sum(axis=1) / 1.00
    d2 = float(np.abs(a - b).max())
    P(f"  G2 gate path is g-invariant           max|W(g=.5)/.5 - W(g=1)/1| = {d2:.3e}   "
      f"{'PASS' if d2 < 1e-12 else 'FAIL'}")
    ok &= d2 < 1e-12
    P(f"  GATES: {'ALL PASS' if ok else 'SOME FAILED — read the numbers with that caveat'}")

    cells = []
    for nm, px, tr in panels:
        run_panel(nm, px, tr, cells)
    df = pd.DataFrame(cells)
    df.to_csv(OUT / f"{STAMP}.grid.csv", index=False)

    # ---------------------------------------------------------------- THE ANSWER: the g-ladder
    P("\n" + "=" * 100)
    P("PART A — THE ADMISSIBLE 4b BAND IN GROSS (all 136 clause books, nothing dropped)")
    cl = df[df.arm == "BREADTH-DG"]
    for pname in ("U56", "B136"):
        sub = cl[cl.panel == pname]
        P(f"\n  {pname}: 4b passes at {int(sub.pass4b.sum())}/{len(sub)} (q,g) cells; "
          f"4a at {int(sub.pass4a.sum())}/{len(sub)}")
        for q in QS:
            s = sub[sub.q == q].sort_values("gross")
            band = s.loc[s.pass4b, "gross"].tolist()
            contiguous = (len(band) == 0 or
                          (round(max(band) - min(band), 2) == round(0.05 * (len(band) - 1), 2)))
            P(f"    q={q:.2f} fire {s.fire_rate.iloc[0]:5.1%}  4b band = "
              f"{('none' if not band else f'[{min(band):.2f}, {max(band):.2f}] ({len(band)}/17 rungs' + (', contiguous)' if contiguous else ', GAPPY)'))}")
            P("      " + "  ".join(f"{g:.2f}:{'P' if p else '.'}"
                                   for g, p in zip(s.gross, s.pass4b)))
            P("      binding leg by rung: " + "  ".join(
                f"{g:.2f}:{(fl.split(';')[0] if fl else '-')}" for g, fl in zip(s.gross, s.fail_legs)))
        # the same for the gate-less control, so the gate's contribution is visible
        c = df[(df.panel == pname) & (df.arm == "EWALL-control")].sort_values("gross")
        cband = c.loc[c.pass4b, "gross"].tolist()
        P(f"    CONTROL EWall (no gate)  4b band = "
          f"{('none' if not cband else f'[{min(cband):.2f}, {max(cband):.2f}] ({len(cband)}/17)')}")
        P("      " + "  ".join(f"{g:.2f}:{'P' if p else '.'}" for g, p in zip(c.gross, c.pass4b)))

    P("\nPART A2 — the full ladder for idea 581's own cell (q=0.20), every rung reported")
    for pname in ("U56", "B136"):
        s = cl[(cl.panel == pname) & (cl.q == 0.20)].sort_values("gross")
        s0 = df[(df.panel == pname) & (df.arm == "EWALL-control")].set_index("gross")
        P(f"\n  {pname}   g    CAGR   Sharpe   MaxDD    H1     H2  | OOS CAGR  Shrp   MaxDD | 4a 4b  fail")
        for _, r in s.iterrows():
            P(f"       {r.gross:5.2f} {r.CAGR:7.2%} {r.Sharpe:7.3f} {r.MaxDD:7.2%} "
              f"{r.H1:6.3f} {r.H2:6.3f} | {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:6.3f} {r.OOS_MaxDD:7.2%} "
              f"| {'Y' if r.pass4a else 'n'}  {'Y' if r.pass4b else 'n'}   {r.fail_legs}")
        P(f"    (control EWall at g=1.00: CAGR {s0.loc[1.00,'CAGR']:.2%} Sharpe "
          f"{s0.loc[1.00,'Sharpe']:.3f} MaxDD {s0.loc[1.00,'MaxDD']:.2%}, 4b "
          f"{'PASS' if s0.loc[1.00,'pass4b'] else 'FAIL ' + str(s0.loc[1.00,'fail_legs'])})")

    # ---------------------------------------------------------------- PART B — rule 8
    P("\n" + "=" * 100)
    P("PART B — RULE 8 WALK-FORWARD.  (q, g) chosen on 2009-2016 ONLY; 2017-2026 read ONCE.")
    wf = []
    for pname in ("U56", "B136"):
        sub = cl[cl.panel == pname].copy()
        r0 = sub.iloc[0]
        screen = ((sub.IS_Sharpe > r0.spy_IS_Sharpe) &
                  (sub.IS_MaxDD >= 0.60 * r0.spy_IS_MaxDD) &
                  (sub.IS_CAGR >= 0.70 * r0.spy_IS_CAGR))
        for conv, pool in (("S1_maxISsharpe", sub),
                           ("S2_IS4bscreen", sub[screen] if screen.any() else sub)):
            pick = pool.loc[pool.IS_Sharpe.idxmax()]
            wf.append(dict(panel=pname, convention=conv, n_pool=len(pool),
                           pick_q=pick.q, pick_g=pick.gross, IS_Sharpe=pick.IS_Sharpe,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           spy_OOS_CAGR=pick.spy_OOS_CAGR, spy_OOS_Sharpe=pick.spy_OOS_Sharpe,
                           spy_OOS_MaxDD=pick.spy_OOS_MaxDD,
                           b2_OOS_CAGR=pick.b2_OOS_CAGR, b2_OOS_Sharpe=pick.b2_OOS_Sharpe,
                           b2_OOS_MaxDD=pick.b2_OOS_MaxDD,
                           full_pass4a=pick.pass4a, full_pass4b=pick.pass4b,
                           full_fail_legs=pick.fail_legs))
            P(f"  {pname:5s} {conv:15s} pool {len(pool):3d}  ->  q={pick.q:.2f} g={pick.gross:.2f} "
              f"(IS Sharpe {pick.IS_Sharpe:.3f})")
            P(f"        OOS  CAGR {pick.OOS_CAGR:7.2%}  Sharpe {pick.OOS_Sharpe:6.3f}  "
              f"MaxDD {pick.OOS_MaxDD:7.2%}")
            P(f"        SPY  CAGR {pick.spy_OOS_CAGR:7.2%}  Sharpe {pick.spy_OOS_Sharpe:6.3f}  "
              f"MaxDD {pick.spy_OOS_MaxDD:7.2%}")
            P(f"        v2   CAGR {pick.b2_OOS_CAGR:7.2%}  Sharpe {pick.b2_OOS_Sharpe:6.3f}  "
              f"MaxDD {pick.b2_OOS_MaxDD:7.2%}")
            P(f"        full-sample verdict of the PICKED cell: 4a "
              f"{'PASS' if pick.pass4a else 'FAIL'}, 4b "
              f"{'PASS' if pick.pass4b else 'FAIL (' + str(pick.fail_legs) + ')'}")
    wfd = pd.DataFrame(wf); wfd.to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- PART C — is g the dial?
    P("\n" + "=" * 100)
    P("PART C — IS THE 4b VERDICT A GROSS ARTEFACT?  (Spearman of each 4b leg's margin on g)")
    for pname in ("U56", "B136"):
        s = cl[(cl.panel == pname) & (cl.q == 0.20)].sort_values("gross")
        marg = dict(
            CAGR=(s.CAGR - 0.70 * s.spy_CAGR),
            DD=(s.MaxDD - 0.60 * s.spy_MaxDD),
            H1=(s.H1 - s.spy_H1), H2=(s.H2 - s.spy_H2),
            OOS=(s.OOS_Sharpe - s.spy_OOS_Sharpe))
        P(f"  {pname} q=0.20:")
        for k, v in marg.items():
            rho = spearman(s.gross.to_numpy(), v.to_numpy())
            P(f"    {k:5s} margin  rho(g) {rho:+.4f}   at g=0.20 {v.iloc[0]:+.4f}  "
              f"at g=1.00 {v.iloc[-1]:+.4f}   (positive = leg clears)")
        P(f"    Sharpe itself: g=0.20 {s.Sharpe.iloc[0]:.3f} -> g=1.00 {s.Sharpe.iloc[-1]:.3f}, "
          f"rho(g, Sharpe) {spearman(s.gross.to_numpy(), s.Sharpe.to_numpy()):+.4f}  "
          f"(a pure exposure dial with 0% cash leaves Sharpe ~flat and scales CAGR and MaxDD)")

    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")
    P(f"\nwrote {STAMP}.grid.csv ({len(df)} rows), .walkforward.csv ({len(wfd)}), .console.txt")


if __name__ == "__main__":
    main()
