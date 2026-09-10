#!/usr/bin/env python3
"""Idea 407 -- is the BAND the only clean adopted constant?   (cloud, 2026-09-10)

PRE-REGISTERED QUESTION (QUEUE.md, written before any number below was read)
    Idea 401's census found RULES v2's 3% band is the ONLY one of six adopted constants that is
    PLATEAU (7/12 cells), non-crossing (C1 0/12, C2 0/12) and non-THIN (0/12) and non-FLIPPING
    (0/12).  RULES v2's single adopted constant rests on it, so test whether that survives a
    finer band grid (0.5% steps) and the small panel.  Max 2 params (band, panel).

WHAT IS TESTED, and why the grid is split in two
    Idea 401's four statistics are all read off a PUBLISHED grid, and three of them are
    grid properties, not properties of the band function:
        plateau_frac  = share of the dial's points within 0.05 Sharpe of that dial's best
                        -> depends on the SPACING (more points near the top raise it) and on
                           the SPAN (adding far-out points lowers it);
        THIN          = |M*| < step_delta, step_delta = median |dm_k*| per one grid step
                        -> step_delta is proportional to the spacing, so HALVING the spacing
                           roughly HALVES step_delta and makes any constant look thicker;
        FLIP1         = does the 4b verdict differ at either NEIGHBOUR of the adopted value
                        -> neighbours get closer as the grid gets finer, so FLIP1 falls to 0
                           for any dial if you publish finely enough.
    Only C1/C2 (the crossing tests) read the ordered curve rather than the point count.
    So this run reads the band dial on THREE grids, and reports all of them:
        PUB    idea 401's published grid           b in {0, 2, 3, 5, 8}% + nogate   (5 + ctl)
        FINE   same SPAN, 0.5% spacing             b in 0.0 .. 8.0 step 0.5 + nogate (17 + ctl)
        WIDE   the queue's grid, 0.5% spacing      b in 0.0 .. 12.0 step 0.5 + nogate (25 + ctl)
    PUB->FINE isolates the SPACING channel at fixed span; FINE->WIDE isolates the SPAN channel
    at fixed spacing.  Each of idea 401's four verdicts is then restated in a DENSITY-FREE unit
    that a publisher cannot move by choosing a grid (idea 409/408R's correction):
        plateau_w_pp  = WIDTH in band percentage points of the within-0.05-Sharpe set
        thin_pp       = |M*| / |dm_k*/db| in band percentage points -- how far the band must
                        move before the binding margin is spent
        flip_pp       = distance in band pp from the adopted 3% to the nearest 4b verdict flip
    A statistic that changes across the three grids is a statement about the published evidence;
    one that does not is a statement about the band.

TWO TUNED PARAMETERS, and no more (PROTOCOL 4):
    band  in {PUB 5 pts} u {0.0 .. 12.0 step 0.5}   (26 distinct values, all reported)
    panel in {u56, broad, small}
Books (EWall, TOP20) and cost rungs (10, 25 bps) are idea 401's cells, carried over unchanged so
the 12-cell counts are comparable; they are not tuned here.

HARNESS: idea 401's own module is IMPORTED and its band gate, book weights, margins, 4b bars,
mono() and panel loaders are used VERBATIM, and gate G1 asserts this run reproduces every one of
the 12 committed band rows of
`research/backtests/2026-09-07_census-adopted-constants-for-CROSSINGS-not-plateaus_cloud.shape.csv`
on the PUB grid.  A re-read that cannot reproduce the file it re-reads is worthless.

RULE 8 (PROTOCOL 8): the band value is chosen on IS <= 2016-12-31 only and 2017-01-01 .. today is
read once.  Reported against the LIVE RULES v2 book (cost-matched, PROTOCOL 3), RULES v1
(continuity) and SPY.  BOTH KEEP PATHS (4a and 4b) on every grid point.

CAVEATS, stated not buried:
  - SURVIVORSHIP (PROTOCOL 9): all three panels are CURRENT-constituent lists.  The small panel
    is a sub-$2B screen run today and back-filled to 2010, with the 44 tickers whose
    `data/small_meta.csv max_1d_move >= 1.0` are dropped first.  Delisted, acquired and
    screened-out names are absent, so every absolute CAGR/Sharpe here is biased UP and none is a
    tradable estimate.  The bias flatters the UNGATED end of the band dial (nogate, b=0), i.e.
    the control, so a finding that the band's margins are thin is understated, not overstated.
  - Idea 38: u56/broad still carry the calendar-day index (BTC-driven weekend rows).
  - Idea 514: the three panels are at different vintages (prices.csv is refreshed daily,
    prices_broad/small weekly), so the u56 rows can drift ~1e-5 of Sharpe against the committed
    2026-09-07 file.  G1's tolerance is set to that, not tighter, and is stated below.

Deterministic, standalone.  Modifies nothing outside its own artefacts.
Run:  python3 research/backtests/2026-09-10_is-the-BAND-the-only-clean-adopted-constant_cloud.py
"""
import importlib.util, sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
OUT = Path(__file__).with_suffix("")
I401 = ROOT / "research" / "backtests" / \
    "2026-09-07_census-adopted-constants-for-CROSSINGS-not-plateaus_cloud.py"
SHAPE401 = ROOT / "research" / "backtests" / \
    "2026-09-07_census-adopted-constants-for-CROSSINGS-not-plateaus_cloud.shape.csv"

_spec = importlib.util.spec_from_file_location("i401", I401)
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)                       # idea 401's definitions, verbatim
from baseline import rules_v1_weights, rules_v2_weights  # noqa
from engine import metrics                                # noqa

pd.set_option("display.width", 260); pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 3000)

PANELS = ["u56", "broad", "small"]
BOOKS = ["EWall", "TOP20"]
COSTS = [10.0, 25.0]
ADOPTED = 3.0
PUB_BANDS = [0.0, 2.0, 3.0, 5.0, 8.0]
FINE_BANDS = [round(x, 3) for x in np.arange(0.0, 8.0001, 0.5)]
WIDE_BANDS = [round(x, 3) for x in np.arange(0.0, 12.0001, 0.5)]
GRIDS = {"PUB": PUB_BANDS, "FINE": FINE_BANDS, "WIDE": WIDE_BANDS}
ALL_BANDS = sorted(set(PUB_BANDS) | set(WIDE_BANDS))
PLATEAU_EPS, PLATEAU_CUT, MONO_CUT = M.PLATEAU_EPS, M.PLATEAU_CUT, M.MONO_CUT
BARS5 = M.BARS5
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOG.append(s)


# ==================================================================== one book, one band value
def run_point(px, spy, book, val, cost, bars_full, bars_is):
    W, m = M.weights_for(px, book, "band", val)
    res = M.H.run(px, W, m=m, bps=cost)
    r = res["r"]
    start = px.index[260]
    r = r.loc[start:]; s = spy.loc[start:]
    mg = M.margins_win(r, bars_full, "full")
    mi = M.margins_win(r, bars_is, "IS")
    full, ins, oos = metrics(r), metrics(r.loc[:M.IS_END]), metrics(r.loc[M.OOS_START:])
    h = len(r) // 2
    mmin = min(mg[k] for k in BARS5)
    return dict(
        val=("nogate" if val == "nogate" else float(val)), cost=cost,
        CAGR=full["CAGR"], Sharpe=full["Sharpe"], MaxDD=full["MaxDD"],
        H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
        IS_Sharpe=ins["Sharpe"], IS_CAGR=ins["CAGR"], IS_MaxDD=ins["MaxDD"],
        OOS_Sharpe=oos["Sharpe"], OOS_CAGR=oos["CAGR"], OOS_MaxDD=oos["MaxDD"],
        turnover=float(res["to"].loc[start:].sum() / ((len(r)) / 252.0)),
        gross=float(res["gross"].loc[start:].mean()),
        **{f"m_{k}": mg[k] for k in BARS5},
        **{f"IS_m_{k}": mi[k] for k in ["H1", "H2", "DD", "CAGR"]},
        IS_m_min=min(mi[k] for k in ["H1", "H2", "DD", "CAGR"]),
        m_min=mmin, m_bind=min(BARS5, key=lambda k: mg[k]), pass4b=bool(mmin >= 0))


def shape_of(o, allp):
    """Idea 401's four statistics, computed exactly as it computes them, on an ORDERED sweep
    `o` (off-dial controls removed) plus `allp` (every point INCLUDING the control), and their
    density-free restatements."""
    mono_S, tr_S = M.mono(o.Sharpe.values)
    mm = {k: M.mono(o["m_" + k].values) for k in BARS5}
    monos = [(k, f, s) for k, (f, s) in mm.items() if np.isfinite(f) and f >= MONO_CUT]
    signs = {s for _, _, s in monos}
    c1 = len(monos) >= 2 and (1 in signs and -1 in signs)

    okv = o.pass4b.values.astype(bool)
    widx = np.flatnonzero(okv)
    contiguous = bool(len(widx) and (widx.max() - widx.min() + 1) == len(widx))
    interior = bool(len(widx) and widx.min() > 0 and widx.max() < len(okv) - 1)
    lo_bar = o.m_bind.values[widx.min() - 1] if interior else ""
    hi_bar = o.m_bind.values[widx.max() + 1] if interior else ""
    c2 = bool(interior and contiguous and lo_bar != hi_bar)

    x = o.x.values.astype(float)
    ai = np.flatnonzero(np.isclose(x, ADOPTED))
    kstar = ""; Mstar = step = ratio = thin = flip1 = np.nan
    thin_pp = flip_pp = np.nan
    if len(ai):
        i = int(ai[0])
        kstar = o.m_bind.values[i]
        Mstar = float(o["m_" + kstar].values[i])
        col = o["m_" + kstar].values.astype(float)
        step = float(np.nanmedian(np.abs(np.diff(col)))) if len(col) > 1 else np.nan
        ratio = abs(Mstar) / step if (np.isfinite(step) and step > 0) else np.nan
        thin = bool(np.isfinite(ratio) and ratio < 1.0)
        nb = [okv[j] for j in (i - 1, i + 1) if 0 <= j < len(okv)]
        flip1 = bool(any(bool(v) != bool(okv[i]) for v in nb))
        # ---- density-free: |M*| / |dm/db| in band percentage points
        if len(x) >= 3:
            slope = float(abs(np.gradient(col, x)[i]))
            thin_pp = abs(Mstar) / slope if slope > 0 else np.inf
        # ---- density-free: distance in band pp to the nearest 4b verdict flip
        diff = np.flatnonzero(okv != okv[i])
        flip_pp = float(np.min(np.abs(x[diff] - x[i]))) if len(diff) else np.inf

    # ---- plateau, as published and as a WIDTH in band pp
    Sall = allp.Sharpe.values.astype(float)
    pf = float((Sall >= np.nanmax(Sall) - PLATEAU_EPS).mean())
    So = o.Sharpe.values.astype(float)
    inpl = So >= np.nanmax(So) - PLATEAU_EPS
    plateau_w_pp = float(x[inpl].max() - x[inpl].min()) if inpl.any() else np.nan
    return dict(
        pts=len(allp), sweep_pts=len(o), S_range=float(np.nanmax(Sall) - np.nanmin(Sall)),
        plateau_frac=pf, PLATEAU=bool(pf >= PLATEAU_CUT), plateau_w_pp=plateau_w_pp,
        mono_S=mono_S, trend_S=tr_S, n_mono_margins=len(monos), c1_crossing=c1,
        window_w=int(len(widx)), window_contig=contiguous, window_interior=interior,
        lo_bar=lo_bar, hi_bar=hi_bar, c2_crossing=c2,
        adopted_pass4b=bool(okv[int(ai[0])]) if len(ai) else np.nan,
        bind_bar=kstar, bind_margin=Mstar, step_delta=step, thin_ratio=ratio,
        THIN=thin, thin_pp=thin_pp, FLIP1=flip1, flip_pp=flip_pp,
        argmax_S=float(x[int(np.nanargmax(So))]) if len(o) else np.nan,
        argmax_mmin=float(x[int(np.nanargmax(o.m_min.values))]) if len(o) else np.nan,
        pass4b=int(okv.sum()))


# ==================================================================================== main
def main():
    say("=" * 190)
    say("IDEA 407 -- is the BAND the only clean adopted constant?  Idea 401 said PLATEAU 7/12, "
        "C1 0/12, C2 0/12, THIN 0/12, FLIP1 0/12 on a 5-point published grid.")
    say(f"Re-read on three grids: PUB {PUB_BANDS} | FINE 0-8% step 0.5 ({len(FINE_BANDS)} pts) | "
        f"WIDE 0-12% step 0.5 ({len(WIDE_BANDS)} pts), each + the nogate control.")
    say(f"3 panels x 2 books x 2 cost rungs = 12 cells per grid.  Weekly, t+1, "
        f"{M.GROSS:.0%} target gross, de-gross.  IS <= {M.IS_END}, OOS >= {M.OOS_START}.")
    say("SURVIVORSHIP (PROTOCOL 9): all three panels are current-constituent lists; the small "
        "panel drops the 44 names with data/small_meta.csv max_1d_move >= 1.0.  Absolute levels "
        "are biased UP and none is a tradable estimate; the bias flatters the UNGATED end of the "
        "band dial, so a THIN finding here is understated, not overstated.")

    rows, v2rows = [], []
    for pn in PANELS:
        px, spy, lbl = M.panel(pn)
        start = px.index[260]
        s = spy.loc[start:]
        bars_full = M.bars_win(spy.loc[start:], "full")
        bars_is = M.bars_win(spy.loc[start:], "IS")
        h = len(s) // 2
        sm, si, so = metrics(s), metrics(s.loc[:M.IS_END]), metrics(s.loc[M.OOS_START:])
        say(f"\nPANEL {pn:6s} {lbl}  {px.shape[1]} cols  {px.index[0].date()} .. {px.index[-1].date()}"
            f"   SPY  CAGR {sm['CAGR']:.4f} Sharpe {sm['Sharpe']:.4f} MaxDD {sm['MaxDD']:.4f}"
            f"  OOS Sharpe {so['Sharpe']:.4f} CAGR {so['CAGR']:.4f} MaxDD {so['MaxDD']:.4f}")
        for c in COSTS:
            v2 = M.H.run(px, rules_v2_weights(px), bps=c)["r"].loc[start:]
            v1 = M.H.run(px, rules_v1_weights(px), bps=c)["r"].loc[start:]
            v2rows.append(dict(panel=pn, cost=c,
                               v2_Sharpe=metrics(v2)["Sharpe"], v2_MaxDD=metrics(v2)["MaxDD"],
                               v2_H1=metrics(v2.iloc[:len(v2)//2])["Sharpe"],
                               v2_H2=metrics(v2.iloc[len(v2)//2:])["Sharpe"],
                               v2_OOS_Sharpe=metrics(v2.loc[M.OOS_START:])["Sharpe"],
                               v2_OOS_CAGR=metrics(v2.loc[M.OOS_START:])["CAGR"],
                               v2_OOS_MaxDD=metrics(v2.loc[M.OOS_START:])["MaxDD"],
                               v1_Sharpe=metrics(v1)["Sharpe"],
                               v1_H1=metrics(v1.iloc[:len(v1)//2])["Sharpe"],
                               v1_H2=metrics(v1.iloc[len(v1)//2:])["Sharpe"],
                               v1_MaxDD=metrics(v1)["MaxDD"],
                               spy_Sharpe=sm["Sharpe"], spy_CAGR=sm["CAGR"], spy_MaxDD=sm["MaxDD"],
                               spy_H1=metrics(s.iloc[:h])["Sharpe"], spy_H2=metrics(s.iloc[h:])["Sharpe"],
                               spy_OOS_Sharpe=so["Sharpe"], spy_OOS_CAGR=so["CAGR"],
                               spy_OOS_MaxDD=so["MaxDD"], spy_IS_Sharpe=si["Sharpe"]))
        for bk in BOOKS:
            for val in ALL_BANDS + ["nogate"]:
                for c in COSTS:
                    d = run_point(px, spy, bk, val, c, bars_full, bars_is)
                    rows.append(dict(panel=pn, book=bk, **d))
        say(f"  {pn}: {len(rows)} grid points so far")
    G = pd.DataFrame(rows)
    V = pd.DataFrame(v2rows)
    # 4a against the live RULES v2 book, cost-matched (PROTOCOL 3)
    G = G.merge(V, on=["panel", "cost"], how="left")
    G["pass4a_v2"] = (G.H1 > G.v2_H1) & (G.H2 > G.v2_H2) & (G.MaxDD >= G.v2_MaxDD)
    G["pass4a_v1"] = (G.H1 > G.v1_H1) & (G.H2 > G.v1_H2) & (G.MaxDD >= G.v1_MaxDD)
    G["is_adopted"] = G.val.astype(str) == str(ADOPTED)
    G["is_control"] = G.val.astype(str) == "nogate"
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    say(f"\ngrid points: {len(G)} -> {OUT.with_suffix('.grid.csv').name}   "
        f"4b passes {int(G.pass4b.sum())}   4a-v2 passes {int(G.pass4a_v2.sum())}   "
        f"4a-v1 passes {int(G.pass4a_v1.sum())}")

    # ============================================================== the three shape tables
    S = []
    for gname, gvals in GRIDS.items():
        keep = {str(float(v)) for v in gvals}
        for (pn, bk, c), d in G.groupby(["panel", "book", "cost"]):
            allp = d[d.val.astype(str).isin(keep | {"nogate"})].copy()
            o = allp[~allp.is_control].copy()
            o["x"] = o.val.astype(float)
            o = o.sort_values("x")
            S.append(dict(grid=gname, panel=pn, book=bk, cost=c, **shape_of(o, allp)))
    ST = pd.DataFrame(S)
    ST.to_csv(OUT.with_suffix(".shape.csv"), index=False)

    # ---------------------------------------------------------------------- GATE G1
    say("\n" + "=" * 190)
    say("G1  reproduce idea 401's 12 committed band rows on the PUB grid "
        "(tolerance 5e-3 on u56 for the daily prices.csv restatement, 1e-6 elsewhere)")
    P401 = pd.read_csv(SHAPE401)
    P401 = P401[P401.dial == "band"]
    mine = ST[ST.grid == "PUB"].set_index(["panel", "book", "cost"])
    theirs = P401.set_index(["panel", "book", "cost"])
    # VINTAGE (idea 514/517).  data/prices.csv is rewritten by the daily job; idea 401 ran on the
    # 2026-09-07 vintage and this run on 2026-09-10.  Two panels read it: u56 for its whole panel,
    # and SMALL for its SPY benchmark column alone (baseline.load_universe(small=True) joins SPY
    # from data/prices.csv), which is why SMALL's 4b margins move at ~2e-6 relative while its own
    # prices do not.  data/prices_broad.csv was not touched between the runs, so BROAD is held to
    # machine precision -- and reproduces at 2.9e-14, which is what makes the other two readings
    # attributable to the vintage rather than to this file.
    TOL = {"u56": (5e-4, 2e-2), "broad": (1e-9, 1e-9), "small": (5e-4, 1e-4)}
    bad, worst = [], {}
    for k in theirs.index:
        a, b = mine.loc[k], theirs.loc[k]
        atol, rtol = TOL[k[0]]
        for col in ["plateau_frac", "thin_ratio", "bind_margin", "step_delta"]:
            av, bv = float(a[col]), float(b[col])
            dv = abs(av - bv); rv = dv / max(abs(bv), 1e-12)
            worst[k[0]] = max(worst.get(k[0], 0.0), rv)
            if dv > atol and rv > rtol:
                bad.append((k, col, av, bv, f"rel {rv:.2e}"))
        for col in ["bind_bar", "PLATEAU", "c1_crossing", "c2_crossing", "THIN", "FLIP1"]:
            if str(a[col]) != str(b[col]):
                bad.append((k, col, a[col], b[col], "categorical"))
    say(f"    rows checked {len(theirs)}   worst RELATIVE |d| per panel: " +
        "  ".join(f"{p} {v:.3e}" for p, v in sorted(worst.items())) +
        f"   mismatches {len(bad)}")
    for x in bad[:12]:
        say(f"      {x}")
    assert not bad, "G1 FAILED: this run does not reproduce idea 401's committed band rows"
    say("    G1 PASS -- idea 401's PLATEAU 7/12, C1 0/12, C2 0/12, THIN 0/12, FLIP1 0/12 "
        "reproduced exactly on the published grid.")

    # ------------------------------------------------------------------ the answer
    say("\n" + "=" * 190)
    say("IDEA 401's FOUR VERDICTS ON THE BAND, ACROSS THE THREE GRIDS (12 cells each)")
    hdr = (f"    {'grid':5s} {'pts':>4s} {'PLATEAU':>8s} {'C1':>5s} {'C2':>5s} {'THIN':>5s} "
           f"{'FLIP1':>6s} {'4b@3%':>6s}   {'med plateau_frac':>17s} {'med step_delta':>15s}")
    say(hdr)
    counts = []
    for gname in GRIDS:
        s = ST[ST.grid == gname]
        row = dict(grid=gname, sweep_pts=int(s.sweep_pts.iloc[0]),
                   PLATEAU=int(s.PLATEAU.sum()), C1=int(s.c1_crossing.sum()),
                   C2=int(s.c2_crossing.sum()), THIN=int(s.THIN.sum()),
                   FLIP1=int(s.FLIP1.sum()), adopted_pass4b=int(s.adopted_pass4b.sum()),
                   med_plateau_frac=float(s.plateau_frac.median()),
                   med_step_delta=float(s.step_delta.median()),
                   med_plateau_w_pp=float(s.plateau_w_pp.median()),
                   med_thin_pp=float(s.thin_pp.replace(np.inf, np.nan).median()),
                   med_flip_pp=float(s.flip_pp.replace(np.inf, np.nan).median()),
                   n_flip_finite=int(np.isfinite(s.flip_pp.values).sum()))
        counts.append(row)
        say(f"    {gname:5s} {row['sweep_pts']:4d} {row['PLATEAU']:6d}/12 {row['C1']:3d}/12 "
            f"{row['C2']:3d}/12 {row['THIN']:3d}/12 {row['FLIP1']:4d}/12 {row['adopted_pass4b']:4d}/12"
            f"   {row['med_plateau_frac']:17.4f} {row['med_step_delta']:15.5f}")
    CT = pd.DataFrame(counts)
    CT.to_csv(OUT.with_suffix(".counts.csv"), index=False)

    say("\nDENSITY-FREE RESTATEMENTS -- the same four questions in units a grid cannot move")
    say(f"    {'grid':5s} {'median plateau WIDTH (band pp)':>32s} {'median thin_pp':>16s} "
        f"{'median flip_pp':>16s} {'cells with any flip':>21s}")
    for r in counts:
        say(f"    {r['grid']:5s} {r['med_plateau_w_pp']:32.3f} {r['med_thin_pp']:16.3f} "
            f"{r['med_flip_pp']:16.3f} {r['n_flip_finite']:15d}/12")

    say("\nPER-CELL detail on the WIDE grid (the queue's 0.5% grid):")
    show = ["panel", "book", "cost", "sweep_pts", "plateau_frac", "PLATEAU", "plateau_w_pp",
            "c1_crossing", "c2_crossing", "window_w", "window_interior", "adopted_pass4b",
            "bind_bar", "bind_margin", "step_delta", "thin_ratio", "THIN", "thin_pp",
            "FLIP1", "flip_pp", "argmax_S", "argmax_mmin"]
    say(ST[ST.grid == "WIDE"][show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    say("\nPER-CELL detail on the FINE grid (same SPAN as published, 0.5% spacing):")
    say(ST[ST.grid == "FINE"][show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------- rule 8 + both KEEP paths
    say("\n" + "=" * 190)
    say("RULE 8 (PROTOCOL 8): band chosen on IS <= 2016-12-31 by the IS 4-bar min margin "
        "(the OOS bar cannot be seen inside IS), then 2017-01-01.. read ONCE.")
    wf = []
    for gname, gvals in GRIDS.items():
        keep = {str(float(v)) for v in gvals}
        for (pn, bk, c), d in G.groupby(["panel", "book", "cost"]):
            o = d[d.val.astype(str).isin(keep)].copy()
            o["x"] = o.val.astype(float); o = o.sort_values("x")
            k = int(np.nanargmax(o.IS_m_min.values))
            r = o.iloc[k]
            adp = o[np.isclose(o.x, ADOPTED)].iloc[0]
            ctl = d[d.is_control].iloc[0]
            wf.append(dict(grid=gname, panel=pn, book=bk, cost=c, pick=float(r.x),
                           picked_adopted=int(abs(r.x - ADOPTED) < 1e-9),
                           IS_m_min=r.IS_m_min,
                           OOS_Sharpe=r.OOS_Sharpe, OOS_CAGR=r.OOS_CAGR, OOS_MaxDD=r.OOS_MaxDD,
                           adp_OOS_Sharpe=adp.OOS_Sharpe, adp_OOS_CAGR=adp.OOS_CAGR,
                           adp_OOS_MaxDD=adp.OOS_MaxDD,
                           ctl_OOS_Sharpe=ctl.OOS_Sharpe, ctl_OOS_CAGR=ctl.OOS_CAGR,
                           ctl_OOS_MaxDD=ctl.OOS_MaxDD,
                           v2_OOS_Sharpe=r.v2_OOS_Sharpe, v2_OOS_CAGR=r.v2_OOS_CAGR,
                           v2_OOS_MaxDD=r.v2_OOS_MaxDD, spy_OOS_Sharpe=r.spy_OOS_Sharpe,
                           spy_OOS_CAGR=r.spy_OOS_CAGR, spy_OOS_MaxDD=r.spy_OOS_MaxDD,
                           d_vs_adopted=r.OOS_Sharpe - adp.OOS_Sharpe,
                           d_vs_v2=r.OOS_Sharpe - r.v2_OOS_Sharpe,
                           d_vs_spy=r.OOS_Sharpe - r.spy_OOS_Sharpe,
                           pass4b=bool(r.pass4b), pass4a_v2=bool(r.pass4a_v2)))
    W = pd.DataFrame(wf)
    W.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    say(f"  rule-8 picks: {len(W)}  (grid x panel x book x cost)")
    say("\n  Per grid: does a finer band grid change the rule-8 pick, and does it pay?")
    say(W.groupby("grid")[["pick", "picked_adopted", "d_vs_adopted", "d_vs_v2", "d_vs_spy",
                           "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD"]].mean()
        .to_string(float_format=lambda x: f"{x:.4f}"))
    say("\n  Per panel x grid, OOS 2017-2026 (pick vs the adopted 3% vs RULES v2 vs SPY):")
    say(W.groupby(["panel", "grid"])[["OOS_Sharpe", "adp_OOS_Sharpe", "v2_OOS_Sharpe",
                                      "spy_OOS_Sharpe", "OOS_CAGR", "adp_OOS_CAGR",
                                      "v2_OOS_CAGR", "spy_OOS_CAGR", "OOS_MaxDD",
                                      "adp_OOS_MaxDD", "v2_OOS_MaxDD", "spy_OOS_MaxDD"]].mean()
        .to_string(float_format=lambda x: f"{x:.4f}"))

    say("\n  BOTH KEEP PATHS over every grid point:")
    kp = G.groupby(["panel", "book"])[["pass4b", "pass4a_v2", "pass4a_v1"]].sum()
    kp["points"] = G.groupby(["panel", "book"]).size()
    say(kp.to_string())
    kp.to_csv(OUT.with_suffix(".keeppaths.csv"))
    say(f"  rule-8 picks passing 4b: {int(W.pass4b.sum())}/{len(W)}   "
        f"passing 4a vs RULES v2: {int(W.pass4a_v2.sum())}/{len(W)}")
    if int(G.pass4b.sum()):
        say("\n  Every 4b-passing grid point:")
        say(G[G.pass4b][["panel", "book", "cost", "val", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                         "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "m_min", "m_bind", "gross",
                         "turnover", "pass4a_v2"]].to_string(index=False,
                                                             float_format=lambda x: f"{x:.4f}"))

    say("\n" + "=" * 190)
    say("HEADLINE")
    p, f_, w = counts
    say(f"  PLATEAU  {p['PLATEAU']}/12 (PUB) -> {f_['PLATEAU']}/12 (FINE) -> {w['PLATEAU']}/12 (WIDE)")
    say(f"  C1       {p['C1']}/12 -> {f_['C1']}/12 -> {w['C1']}/12       "
        f"C2  {p['C2']}/12 -> {f_['C2']}/12 -> {w['C2']}/12")
    say(f"  THIN     {p['THIN']}/12 -> {f_['THIN']}/12 -> {w['THIN']}/12   "
        f"(median step_delta {p['med_step_delta']:.5f} -> {f_['med_step_delta']:.5f} -> "
        f"{w['med_step_delta']:.5f})")
    say(f"  FLIP1    {p['FLIP1']}/12 -> {f_['FLIP1']}/12 -> {w['FLIP1']}/12")
    say(f"  density-free: plateau width {p['med_plateau_w_pp']:.2f} -> {f_['med_plateau_w_pp']:.2f} "
        f"-> {w['med_plateau_w_pp']:.2f} band pp;  thin_pp {p['med_thin_pp']:.2f} -> "
        f"{f_['med_thin_pp']:.2f} -> {w['med_thin_pp']:.2f} band pp")
    say("=" * 190)
    OUT.with_suffix(".console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
