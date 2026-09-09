#!/usr/bin/env python3
"""QUEUE idea 283 — does-the-no-signal-shape-appear-on-any-panel-that-passes (cloud, 2026-09-09).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 60's saturation test is two numbers off any band ladder (the 0.00->0.03 increment vs the
0.03->widest increment) and it separates 'the gate loses on noise crossings' from 'the gate loses
on every crossing'.  Back-fill it over idea 61's 408 cells and idea 57's 40, and report whether
the arms that clear 4b are exactly the ones whose recovery curve SATURATES.  If the diagnostic
separates them it is a screening column; if not it is a KILL.  Max 2 params."

The diagnostic (idea 60's own wording, made arithmetic)
------------------------------------------------------
For a band ladder b = 0.00 (the bare 200d gate) .. widest, on one cell:

    inc1 = CAGR(b=0.03) - CAGR(b=0.00)          # what the first 3% of band buys back
    inc2 = CAGR(b=widest) - CAGR(b=0.03)        # what everything past 3% buys back
    R    = inc2 / inc1

  R small  -> SATURATES.  Nearly all the damage the gate does is bought back by the first 3%:
              the gate was losing on NOISE CROSSINGS near the MA and a band fixes it.
  R large  -> NO-SIGNAL SHAPE.  The curve is still rising at the widest band; widening is just
              turning the gate off, so the gate loses on EVERY crossing, not just noisy ones.
              Idea 60 measured R = 4.0-4.6 on SMALL439 and called that the no-signal shape.

PRE-REGISTERED BARS (written before any number was read).  Primary: SATURATES iff R <= 1.0
(everything past 3% buys back no more than the first 3% did).  The bar is a tuned parameter, so
the whole ladder R* in {0.25, 0.5, 1.0, 2.0, 4.0} is reported and nothing is selected.  Cells
with inc1 <= 0 (the first 3% of band buys back NOTHING) are a separate class, `NO-RECOVERY`,
because a ratio through a non-positive denominator is not a diagnostic; they are counted, never
silently dropped.

Two tuned parameters (PROTOCOL rule 4): the BAND b (a ladder, every point reported) and the
saturation bar R* (a ladder, every point reported).  Panel, book, convention and cost rung are
reported dimensions, not tuned: every cell is printed.

Part A — LITERAL BACK-FILL of idea 61's published grid
    `2026-09-06_gate-instrument-speed-curve_cloud.keep.csv` carries all 408 published cells with
    pass4a / pass4b, and its BAND family is a 7-point ladder (0.00 .. 0.20) over 24 cells
    (3 panels x 2 books x 2 conventions x 2 rungs).  R is computed from those published CAGRs -
    no re-run, no new numbers - and tested against the published 4b flags.  Idea 57's 40 cells
    carry only b in {0.00, 0.03} (no widest band), so inc2 does not exist there; Part B extends
    that ladder rather than pretending idea 57 answers it.

Part B — INDEPENDENT REPLICATION on a superset
    Fresh band ladders on the record's clause harness (idea 94's price list, as re-used by idea
    505): 3 panels x 3 base books (V1u, TOP20, EWall - idea 57's two books plus the live v1 book)
    x 2 conventions (dg de-gross / rw reweight) x 3 rungs (0/10/25 bps) x 8 band points = 432 arm
    rows against 27 ungated controls, so the recovery SHARE (fraction of the gate's own damage
    that the band buys back) is available too, which Part A cannot give.

Rule 8: (i) the band b is chosen per cell on IS 2009-2016 Sharpe and read once on 2017-2026
against the ungated control, the live RULES v2 book and SPY; (ii) the diagnostic itself is walked
forward - R is recomputed from IS-ONLY CAGRs and tested as a screening column for an OOS 4b-style
pass, which is the only test that decides the idea's own question honestly.

SURVIVORSHIP: universe.json / universe_broad.json are current-constituent lists and SMALL439 is a
current screen (data/SMALL_PANEL_README.md); tickers with max_1d_move >= 1.0 in data/small_meta.csv
are dropped first (44 of 483).  Absolute levels are optimistic; R is a ratio of two same-cell,
same-days CAGR increments and is far less exposed.

Deterministic, standalone, no network.  Does not modify RULES.md, scan.py, bot.py or baseline.py.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = Path(__file__).stem
HERE = ROOT / "research" / "backtests"
IDEA61 = HERE / "2026-09-06_gate-instrument-speed-curve_cloud.keep.csv"
FREQ, GROSS, NTOP, NV1, WV1 = "W", 0.75, 20, 5, 0.15
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20]
RBARS = [0.25, 0.5, 1.0, 2.0, 4.0]
RSTAR = 1.0                                   # pre-registered primary bar
RUNGS = [0.0, 10.0, 25.0]
BOOKS = ["V1u", "TOP20", "EWall"]
CONVS = ["dg", "rw"]

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)


# ---------------------------------------------------------------- harness (idea 94 / 505)
def composite(px):
    mom = px.shift(21) / px.shift(252) - 1
    r6, r3 = px / px.shift(126) - 1, px / px.shift(63) - 1
    return (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True) + r3.rank(axis=1, pct=True)) / 3


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def band_gate(px, b):
    """200d MA gate with a +/-b hysteresis band.  b = 0.00 is the bare 200d gate."""
    ma = px.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + b), 1.0).mask(px < ma * (1 - b), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def base_book(px, book):
    if book == "EWall":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    s = composite(px)
    if book == "V1u":
        s = s / vol20(px).clip(lower=0.08) ** 0.5
        n, w = NV1, WV1
    else:
        n, w = NTOP, GROSS / NTOP
    return (s.rank(axis=1, ascending=False) <= n).astype(float) * w


def targets(px, book, b=None, conv="dg"):
    if b is None:
        return base_book(px, book)
    g = band_gate(px, b)
    if conv == "rw":
        if book == "EWall":
            e = g.astype(float)
            return GROSS * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        s = composite(px)
        if book == "V1u":
            s = s / vol20(px).clip(lower=0.08) ** 0.5
            n, w = NV1, WV1
        else:
            n, w = NTOP, GROSS / NTOP
        return (s.where(g).rank(axis=1, ascending=False) <= n).astype(float) * w
    return base_book(px, book).where(g, 0.0)


def run(px, W, bps=10.0, freq=FREQ):
    """engine.backtest with costs charged inside the loop (identical to engine.backtest; the
    equality is asserted in GATE 1)."""
    rets = px.pct_change().fillna(0.0).values
    tgt = W.reindex(px.index).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nrow, ncol = rets.shape
    cur = np.zeros(ncol)
    held = np.zeros((nrow, ncol))
    turn = np.zeros(nrow)
    for i in range(nrow):
        if mask[i] or i == 0:
            new = np.nan_to_num(tgt[i - 1] if i > 0 else tgt[i] * 0.0)
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    r = (pd.Series((held * rets).sum(axis=1), index=px.index)
         - pd.Series(turn, index=px.index) * bps / 1e4)
    return dict(r=r, to=pd.Series(turn, index=px.index))


def stats(r, to=None):
    m = metrics(r)
    h = len(r) // 2
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
             H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])
    if to is not None:
        d["Turn"] = to.sum() / (len(to) / 252)
    return d


def small_panel():
    mt = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(mt.loc[mt.max_1d_move >= 1.0, "ticker"])
    px = load_universe(small=True)
    return px[[c for c in px.columns if c == "SPY" or c not in bad]]


def sat_class(inc1, inc2, rstar=RSTAR):
    if not np.isfinite(inc1) or inc1 <= 0:
        return "NO-RECOVERY"
    return "SATURATES" if (inc2 / inc1) <= rstar else "NO-SIGNAL"


def two_by_two(flag, passed, lbl_f, lbl_p):
    """contingency + separation stats for a boolean screening column."""
    flag, passed = np.asarray(flag, bool), np.asarray(passed, bool)
    a = int((flag & passed).sum()); b = int((flag & ~passed).sum())
    c = int((~flag & passed).sum()); d = int((~flag & ~passed).sum())
    n = a + b + c + d
    num = a * d - b * c
    den = np.sqrt(float((a + b) * (c + d) * (a + c) * (b + d)))
    phi = num / den if den > 0 else np.nan
    print(f"    {lbl_f:14s} x {lbl_p:14s}   n={n}")
    print(f"      flag&pass {a:4d}   flag&fail {b:4d}")
    print(f"      not&pass  {c:4d}   not&fail  {d:4d}")
    print(f"      precision {a / max(a + b, 1):.3f}  recall {a / max(a + c, 1):.3f}  "
          f"accuracy {(a + d) / max(n, 1):.3f}  phi {phi:+.3f}  base rate {(a + c) / max(n, 1):.3f}")
    return dict(a=a, b=b, c=c, d=d, phi=phi)


def auc(scores, passed):
    """Mann-Whitney AUC of a continuous screening column; 0.5 = no separation."""
    s = np.asarray(scores, float); y = np.asarray(passed, bool)
    ok = np.isfinite(s)
    s, y = s[ok], y[ok]
    if y.sum() == 0 or (~y).sum() == 0:
        return np.nan
    rk = pd.Series(s).rank().values
    n1, n0 = y.sum(), (~y).sum()
    return (rk[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


# ================================================================= PART A
def part_a():
    print("\n" + "=" * 110)
    print("PART A — LITERAL BACK-FILL of idea 61's 408 published cells (no re-run; published CAGRs)")
    K = pd.read_csv(IDEA61)
    B = K[K.family == "BAND"].copy()
    print(f"  idea 61 grid rows {len(K)}, BAND family rows {len(B)}, "
          f"cells {B.groupby(['panel', 'cost', 'book', 'conv']).ngroups}, "
          f"dials {sorted(B.dial.unique())}")
    widest = B.dial.max()
    out = []
    for key, g in B.groupby(["panel", "cost", "book", "conv"]):
        g = g.set_index("dial")
        c0, c3, cw = g.loc[0.0, "CAGR"], g.loc[0.03, "CAGR"], g.loc[widest, "CAGR"]
        inc1, inc2 = c3 - c0, cw - c3
        out.append(dict(panel=key[0], cost=key[1], book=key[2], conv=key[3],
                        CAGR0=c0, CAGR3=c3, CAGRw=cw, inc1=inc1, inc2=inc2,
                        R=(inc2 / inc1) if inc1 > 0 else np.nan,
                        klass=sat_class(inc1, inc2),
                        n4b=int(g.pass4b.sum()), n4a=int(g.pass4a.sum()), narms=len(g),
                        pass4b_at_003=bool(g.loc[0.03, "pass4b"]),
                        pass4b_at_0=bool(g.loc[0.0, "pass4b"])))
    A = pd.DataFrame(out).sort_values(["panel", "book", "conv", "cost"])
    A.to_csv(HERE / f"{STEM}.partA.csv", index=False)
    print("\n  the 24 published BAND cells, every one printed "
          f"(inc1 = CAGR(0.03)-CAGR(0.00), inc2 = CAGR({widest})-CAGR(0.03))")
    print("    panel     cost book    conv   CAGR0   CAGR3   CAGRw    inc1     inc2      R      class        4b/arms")
    for _, r in A.iterrows():
        rs = f"{r.R:7.2f}" if np.isfinite(r.R) else "    n/a"
        print(f"    {r.panel:9s} {int(r.cost):4d} {r.book:7s} {r.conv:4s} {r.CAGR0:7.2%} {r.CAGR3:7.2%} "
              f"{r.CAGRw:7.2%} {r.inc1:+7.2%} {r.inc2:+8.2%} {rs}  {r.klass:12s} {r.n4b:2d}/{r.narms}")

    print("\n  DOES THE DIAGNOSTIC SEPARATE THE 4b PASSERS?  (cell level: does the cell contain any"
          " 4b-passing band arm?)")
    for bar in RBARS:
        A[f"sat{bar}"] = [sat_class(i1, i2, bar) == "SATURATES" for i1, i2 in zip(A.inc1, A.inc2)]
        print(f"\n  R* = {bar}")
        two_by_two(A[f"sat{bar}"], A.n4b > 0, "SATURATES", "any 4b arm")
    print(f"\n  continuous AUC of R as a screening column for 'cell has a 4b arm': "
          f"{auc(-A.R, A.n4b > 0):.3f}  (0.5 = no separation; sign set so LOW R = 'should pass')")
    print(f"  NO-RECOVERY cells (inc1 <= 0, the ratio is undefined): "
          f"{int((A.klass == 'NO-RECOVERY').sum())} of {len(A)}; "
          f"{int(((A.klass == 'NO-RECOVERY') & (A.n4b > 0)).sum())} of them contain a 4b passer")

    print("\n  ARM LEVEL — every one of idea 61's 168 published BAND arms, screened by ITS CELL's R")
    Bm = B.merge(A[["panel", "cost", "book", "conv", "R", "klass"] + [f"sat{b}" for b in RBARS]],
                 on=["panel", "cost", "book", "conv"], how="left")
    for bar in RBARS:
        print(f"\n  R* = {bar}")
        two_by_two(Bm[f"sat{bar}"].fillna(False), Bm.pass4b, "cell SATURATES", "arm passes 4b")
    print(f"\n  continuous AUC of cell R for arm-level 4b: {auc(-Bm.R, Bm.pass4b):.3f}")
    print(f"  published 4b pass rate among BAND arms: {Bm.pass4b.mean():.3f} "
          f"({int(Bm.pass4b.sum())}/{len(Bm)}); 4a {int(Bm.pass4a.sum())}/{len(Bm)}")
    return A, Bm


# ================================================================= PART B
def part_b():
    print("\n" + "=" * 110)
    print("PART B — INDEPENDENT REPLICATION: fresh band ladders, 3 panels x 3 books x 2 convs x 3 rungs")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}
    print({k: v.shape for k, v in panels.items()})

    print("\nGATE 1 — run() vs engine.backtest, max abs return difference")
    for pn, px in panels.items():
        for bk in BOOKS:
            W = targets(px, bk)
            print(f"  {pn:9s} {bk:6s}: "
                  f"{np.abs(run(px, W, 10.0)['r'] - backtest(px, W, cost_bps=10.0, freq=FREQ)['returns']).max():.3e}")

    rows = []
    keep_bars = {}
    for pn, px in panels.items():
        s0 = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[s0:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=10.0, freq=FREQ)["returns"].loc[s0:]
        sp, bs = stats(spy), stats(v2)
        spy_oos = metrics(spy.loc[OOS_START:])
        keep_bars[pn] = dict(spy=sp, base=bs, spy_oos=spy_oos,
                             base_oos=metrics(v2.loc[OOS_START:]))
        for bk in BOOKS:
            ctl = {}
            for cb in RUNGS:
                res = run(px, targets(px, bk), cb)
                ctl[cb] = stats(res["r"].loc[s0:], res["to"].loc[s0:])
            for conv in CONVS:
                for b in BANDS:
                    W = targets(px, bk, b=b, conv=conv)
                    for cb in RUNGS:
                        res = run(px, W, cb)
                        r = res["r"].loc[s0:]
                        st = stats(r, res["to"].loc[s0:])
                        oos = metrics(r.loc[OOS_START:])
                        is_m = metrics(r.loc[:IS_END])
                        p4a = (st["H1"] > bs["H1"] and st["H2"] > bs["H2"]
                               and st["MaxDD"] >= bs["MaxDD"])
                        p4b = (st["H1"] > sp["H1"] and st["H2"] > sp["H2"]
                               and oos["Sharpe"] > spy_oos["Sharpe"]
                               and st["MaxDD"] >= 0.6 * sp["MaxDD"]
                               and st["CAGR"] >= 0.7 * sp["CAGR"])
                        rows.append(dict(panel=pn, book=bk, conv=conv, cost=cb, band=b, **st,
                                         ctlCAGR=ctl[cb]["CAGR"], ctlSharpe=ctl[cb]["Sharpe"],
                                         ctlMaxDD=ctl[cb]["MaxDD"],
                                         IS_CAGR=is_m["CAGR"], IS_Sharpe=is_m["Sharpe"],
                                         OOS_CAGR=oos["CAGR"], OOS_Sharpe=oos["Sharpe"],
                                         OOS_MaxDD=oos["MaxDD"], pass4a=p4a, pass4b=p4b))
    G = pd.DataFrame(rows)
    G.to_csv(HERE / f"{STEM}.grid.csv", index=False)
    return G, keep_bars, panels


def curves(G, col="CAGR", suffix=""):
    """one row per cell: the two increments, R, the class, the recovery share, and the 4b count."""
    out = []
    for key, g in G.groupby(["panel", "book", "conv", "cost"]):
        g = g.set_index("band")
        c0, c3, cw = g.loc[0.00, col], g.loc[0.03, col], g.loc[max(BANDS), col]
        ctl = g.loc[0.00, "ctlCAGR"]
        inc1, inc2 = c3 - c0, cw - c3
        gap = ctl - c0
        out.append(dict(panel=key[0], book=key[1], conv=key[2], cost=key[3],
                        ctl=ctl, c0=c0, c3=c3, cw=cw, gap=gap, inc1=inc1, inc2=inc2,
                        R=(inc2 / inc1) if inc1 > 0 else np.nan,
                        rec3=(inc1 / gap) if gap > 0 else np.nan,
                        recw=((cw - c0) / gap) if gap > 0 else np.nan,
                        klass=sat_class(inc1, inc2),
                        n4b=int(g.pass4b.sum()), n4a=int(g.pass4a.sum()), narms=len(g)))
    return pd.DataFrame(out).sort_values(["panel", "book", "conv", "cost"])


def main():
    print(__doc__)
    A, Bm = part_a()
    G, bars, panels = part_b()

    C = curves(G)
    C.to_csv(HERE / f"{STEM}.curves.csv", index=False)
    print("\n" + "=" * 110)
    print("PART B — all 54 cells, every one printed.  gap = ungated CAGR - CAGR(b=0.00) (the gate's")
    print("own damage); rec3 / recw = share of that gap bought back by b=0.03 / b=0.20.")
    print("  panel     book   conv cost  ungated  CAGR0   CAGR3   CAGR20    gap     inc1     inc2  "
          "     R    rec3   recw   class        4b/8")
    for _, r in C.iterrows():
        rs = f"{r.R:7.2f}" if np.isfinite(r.R) else "    n/a"
        r3 = f"{r.rec3:6.1%}" if np.isfinite(r.rec3) else "   n/a"
        rw = f"{r.recw:6.1%}" if np.isfinite(r.recw) else "   n/a"
        print(f"  {r.panel:9s} {r.book:6s} {r.conv:4s} {int(r.cost):4d} {r.ctl:7.2%} {r.c0:7.2%} "
              f"{r.c3:7.2%} {r.cw:7.2%} {r.gap:+7.2%} {r.inc1:+7.2%} {r.inc2:+8.2%} {rs} {r3} {rw}"
              f"  {r.klass:12s} {r.n4b:2d}/{r.narms}")

    print("\n" + "=" * 110)
    print("THE IDEA'S QUESTION — are the 4b passers EXACTLY the saturating cells?")
    for bar in RBARS:
        C[f"sat{bar}"] = [sat_class(i1, i2, bar) == "SATURATES" for i1, i2 in zip(C.inc1, C.inc2)]
        print(f"\n  CELL LEVEL, R* = {bar}")
        two_by_two(C[f"sat{bar}"], C.n4b > 0, "SATURATES", "any 4b arm")
    print(f"\n  continuous AUC of R for 'cell has a 4b arm': {auc(-C.R, C.n4b > 0):.3f}")
    Gm = G.merge(C[["panel", "book", "conv", "cost", "R", "klass"] + [f"sat{b}" for b in RBARS]],
                 on=["panel", "book", "conv", "cost"], how="left")
    for bar in RBARS:
        print(f"\n  ARM LEVEL (432 arms), R* = {bar}")
        two_by_two(Gm[f"sat{bar}"].fillna(False), Gm.pass4b, "cell SATURATES", "arm passes 4b")
    print(f"\n  continuous AUC of cell R for arm-level 4b: {auc(-Gm.R, Gm.pass4b):.3f}")
    print(f"  4b pass rate {Gm.pass4b.mean():.3f} ({int(Gm.pass4b.sum())}/{len(Gm)}); "
          f"4a {int(Gm.pass4a.sum())}/{len(Gm)}")
    print("\n  class x panel (cells):")
    print(pd.crosstab(C.panel, C.klass).to_string())
    print("\n  class x 4b (cells):")
    print(pd.crosstab(C.klass, C.n4b > 0).to_string())

    # ------------------------------------------------------------ rule 8 (i): pick the band
    print("\n" + "=" * 110)
    print("RULE 8 (i) — band b chosen per cell on IS 2009-2016 Sharpe, 2017-2026 read once, 10 bps")
    wf = []
    sub = G[G.cost == 10.0]
    for key, g in sub.groupby(["panel", "book", "conv"]):
        pn = key[0]
        best = g.loc[g.IS_Sharpe.idxmax()]
        ctl = g[g.band == 0.00].iloc[0]
        wf.append(dict(panel=pn, book=key[1], conv=key[2], b_star=best.band,
                       IS_Sharpe=best.IS_Sharpe, OOS_CAGR=best.OOS_CAGR,
                       OOS_Sharpe=best.OOS_Sharpe, OOS_MaxDD=best.OOS_MaxDD,
                       base_OOS=bars[pn]["base_oos"]["Sharpe"], spy_OOS=bars[pn]["spy_oos"]["Sharpe"],
                       spy_OOS_CAGR=bars[pn]["spy_oos"]["CAGR"], R=np.nan))
        print(f"\n  {pn} / {key[1]} / {key[2]}: IS argmax b = {best.band:.2f}  IS Sharpe {best.IS_Sharpe:.4f}")
        print(f"    OOS arm b={best.band:.2f}            CAGR {best.OOS_CAGR:6.2%}  Sharpe {best.OOS_Sharpe:7.4f}  MaxDD {best.OOS_MaxDD:7.2%}")
        print(f"    OOS bare 200d gate (b=0.00)  CAGR {ctl.OOS_CAGR:6.2%}  Sharpe {ctl.OOS_Sharpe:7.4f}  MaxDD {ctl.OOS_MaxDD:7.2%}")
        print(f"    OOS RULES v2 baseline (live) CAGR {bars[pn]['base_oos']['CAGR']:6.2%}  "
              f"Sharpe {bars[pn]['base_oos']['Sharpe']:7.4f}  MaxDD {bars[pn]['base_oos']['MaxDD']:7.2%}")
        print(f"    OOS SPY                      CAGR {bars[pn]['spy_oos']['CAGR']:6.2%}  "
              f"Sharpe {bars[pn]['spy_oos']['Sharpe']:7.4f}  MaxDD {bars[pn]['spy_oos']['MaxDD']:7.2%}")
    WF = pd.DataFrame(wf)
    WF.to_csv(HERE / f"{STEM}.walkforward.csv", index=False)
    print(f"\n  IS-chosen band beats SPY OOS Sharpe in {int((WF.OOS_Sharpe > WF.spy_OOS).sum())}/{len(WF)} cells; "
          f"beats the live RULES v2 book in {int((WF.OOS_Sharpe > WF.base_OOS).sum())}/{len(WF)}; "
          f"b* = 0.00 in {int((WF.b_star == 0).sum())}, 0.20 in {int((WF.b_star == 0.20).sum())}")

    # ------------------------------------------------------------ rule 8 (ii): walk the diagnostic
    print("\n" + "=" * 110)
    print("RULE 8 (ii) — THE DIAGNOSTIC ITSELF WALKED FORWARD.  R recomputed from IS-ONLY (2009-2016)")
    print("CAGRs; the target is an OOS-only 4b-style pass (OOS Sharpe > SPY OOS, OOS MaxDD <= 60% of")
    print("SPY's, OOS CAGR >= 70% of SPY's) on 2017-2026, which the IS numbers cannot see.")
    Cis = curves(G, col="IS_CAGR")
    oos_rows = []
    for _, r in G.iterrows():
        so = bars[r.panel]["spy_oos"]
        oos_rows.append(r.OOS_Sharpe > so["Sharpe"] and r.OOS_MaxDD >= 0.6 * so["MaxDD"]
                        and r.OOS_CAGR >= 0.7 * so["CAGR"])
    G["pass4b_oos"] = oos_rows
    Cis = Cis.rename(columns={"R": "R_IS", "klass": "klass_IS"})
    Go = G.merge(Cis[["panel", "book", "conv", "cost", "R_IS", "klass_IS"]],
                 on=["panel", "book", "conv", "cost"], how="left")
    Co = Go.groupby(["panel", "book", "conv", "cost"]).agg(
        R_IS=("R_IS", "first"), n_oos=("pass4b_oos", "sum")).reset_index()
    both = Cis[["panel", "book", "conv", "cost", "R_IS"]].merge(
        C[["panel", "book", "conv", "cost", "R"]], on=["panel", "book", "conv", "cost"])
    both = both.dropna(subset=["R_IS", "R"])
    print(f"\n  IS-only R vs full-sample R over the {len(both)} cells where both are defined: "
          f"Spearman {both.R_IS.rank().corr(both.R.rank()):.3f}")
    for bar in RBARS:
        flag = Go.R_IS.notna() & (Go.R_IS <= bar)
        print(f"\n  ARM LEVEL, IS-only R* = {bar}  ->  OOS 4b-style pass")
        two_by_two(flag, Go.pass4b_oos, "IS SATURATES", "OOS 4b pass")
    print(f"\n  continuous AUC of IS-only R for the OOS pass: {auc(-Go.R_IS, Go.pass4b_oos):.3f}")
    print(f"  OOS pass base rate {Go.pass4b_oos.mean():.3f} ({int(Go.pass4b_oos.sum())}/{len(Go)})")
    Go.to_csv(HERE / f"{STEM}.walkdiag.csv", index=False)

    # ------------------------------------------------------------ KEEP paths
    print("\n" + "=" * 110)
    print("KEEP PATHS — 4a / 4b counts per panel at 10 bps (144 arms per rung), bars printed")
    for pn in panels:
        bb = bars[pn]
        print(f"\n  {pn}: live v2 CAGR {bb['base']['CAGR']:6.2%} Sharpe {bb['base']['Sharpe']:.4f} "
              f"MaxDD {bb['base']['MaxDD']:7.2%} (OOS Sharpe {bb['base_oos']['Sharpe']:.4f});  "
              f"SPY CAGR {bb['spy']['CAGR']:6.2%} Sharpe {bb['spy']['Sharpe']:.4f} MaxDD {bb['spy']['MaxDD']:7.2%}")
        print(f"    4b bars: H1 {bb['spy']['H1']:.4f} / H2 {bb['spy']['H2']:.4f} / OOS "
              f"{bb['spy_oos']['Sharpe']:.4f}; MaxDD floor {0.6 * bb['spy']['MaxDD']:.2%}; "
              f"CAGR floor {0.7 * bb['spy']['CAGR']:.2%}")
        s = G[(G.panel == pn) & (G.cost == 10.0)]
        print(f"    @10bps  4a {int(s.pass4a.sum())}/{len(s)}   4b {int(s.pass4b.sum())}/{len(s)}")
        for _, r in s[s.pass4b].iterrows():
            print(f"      4b: {r.book:6s} {r.conv:3s} b={r.band:.2f}  CAGR {r.CAGR:6.2%}  "
                  f"Sharpe {r.Sharpe:.4f}  MaxDD {r.MaxDD:7.2%}  H1/H2 {r.H1:.3f}/{r.H2:.3f}  "
                  f"OOS {r.OOS_Sharpe:.4f}  cellR {C[(C.panel == pn) & (C.book == r.book) & (C.conv == r.conv) & (C.cost == 10.0)].R.iloc[0]:.2f}")
    print("\nfiles written:", f"{STEM}.partA.csv", f"{STEM}.grid.csv", f"{STEM}.curves.csv",
          f"{STEM}.walkforward.csv", f"{STEM}.walkdiag.csv")


if __name__ == "__main__":
    main()
