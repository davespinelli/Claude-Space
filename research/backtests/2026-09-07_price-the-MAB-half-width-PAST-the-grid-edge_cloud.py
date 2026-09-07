#!/usr/bin/env python3
"""Idea 390 - "price-the-MAB-half-width-PAST-the-grid-edge" (cloud, 2026-09-07).

QUESTION (from QUEUE.md).  Idea 387's rule-8 chooser picked b = 0.12 for the 200d MA
band (MAB) on U56 -- the WIDEST half-width its grid tested -- at OOS Sharpe 1.2384,
clearing 4b at 0/10/25 bps.  Idea 240/256's grid-edge flag therefore applies: an argmax
that lands on the last rung tested is not an argmax, it is a statement that the grid
stopped too early.  Sweep b PAST the edge and ask whether the MAB Sharpe curve has an
INTERIOR maximum or whether the instrument is simply "turn the gate off".

DESIGN.  Idea 387's leg-C / idea 389 book, VERBATIM, with exactly one thing changed --
the b ladder is extended past 0.12 and a gate-OFF rung is appended:

    incumbent rungs : b in {0.00, 0.03, 0.06, 0.12}     (idea 387/389, replicated)
    NEW rungs       : b in {0.20, 0.30, 0.50}           (past the grid edge)
    NEW rung        : OFF -- the 200d gate removed entirely (eligibility is the
                      vol20 < 0.60 cap and "priced today", nothing else)

Book: score(vol_scale=False) ranked inside the gate, top n=20, equal weight at 0.75
gross, weekly, next-day execution, on four panels.

TUNED PARAMETERS (max 2, per PROTOCOL rule 4): (1) b, the MAB half-width (8 rungs
including OFF); (2) the panel.  Nothing else moves.  ALL 8 x 4 x 3 = 96 grid points are
reported (grid.csv).

WHAT b ACTUALLY IS (stated before the numbers, because it decides how to read them).
`baseline.band_state(px, b)` is a HYSTERESIS collar, not a loose threshold: a name turns
IN above ma*(1+b), OUT below ma*(1-b), and HOLDS ITS PREVIOUS STATE in between, starting
OUT before 200 closes exist.  So b does not interpolate towards "no gate" as it widens --
it interpolates towards "never change state", whose fixed point from an OUT start is
PERMANENT EXCLUSION.  The b -> infinity limit of this instrument is an ALL-CASH book, not
a gate-off book.  Gate-off is therefore a SEPARATE rung that the b ladder cannot reach,
which is why it is tested as its own arm rather than as the ladder's endpoint.  If that
reading is right the Sharpe curve must eventually turn down, and the question "interior
max or just turn the gate off" has a third answer available to it.

PRE-REGISTERED READING.  Fixed before the run, on full-sample Sharpe @10 bps:
    INTERIOR   the b-ladder argmax is strictly inside {0.03..0.30} (not 0.00, not the
               widest rung tested) on a majority of panels, AND the ladder's Sharpe at
               b=0.50 is below its argmax -- i.e. the curve is single-peaked, not a step.
    EDGE       the argmax is still at the widest rung tested (0.50) on a majority of
               panels -- the grid edge has merely moved again.
    GATE-OFF   the OFF rung beats every b rung on a majority of panels -- the collar is
               a cost, not an instrument.
Reported alongside: the same argmax under the rule-8 IS chooser, and the OOS Sharpe the
chooser earns, because the grid-edge flag is about what a CHOOSER would have picked.

MECHANISM COLUMNS (reported for every cell, because a Sharpe number alone cannot
distinguish "better names" from "less exposure"): in_share (fraction of priced
name-days the collar holds IN), elig (mean eligible names/day), names (mean names
HELD/day), cash_days (share of days the book holds nothing), turnover.

KEEP PATHS.  Both evaluated on every cell: 4a against RULES v2 on that panel; 4b against
SPY (Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's).
Reported at 0, 10 and 25 bps.

RULE 8.  b chosen on IS 2008-2016 Sharpe @10 bps, 2017-2026 read once; OOS CAGR / Sharpe
/ MaxDD reported against the panel's b=0 anchor, RULES v2 and SPY, with the regret
against that panel's best-OOS rung.

GATES (all asserted, all printed).  G1/G2 fast_backtest == engine.backtest on returns
and turnover.  G3 band_state(b=0) == px>ma200 where the MA is defined.  G4 the four
incumbent rungs on the three incumbent panels reproduce idea 389's committed grid.csv to
1e-9 -- this run must be a strict superset of the published grid, not a re-derivation.
G5 the OFF arm's gate is all-True wherever a price exists.

CAVEATS.  (1) Every panel is a CURRENT-CONSTITUENT list -- SURVIVORSHIP.  SMALL439 is
the sub-$2B screen with the max_1d_move >= 1.0 names dropped, as required; its 4b CAGR
floor is therefore tested in the book's favour.  (2) ETF36 is a 36-name subset of B136,
so those two panels share history and names -- four panels is not four independent
samples.  (3) Widening b changes the eligible set, not the gross: `weights_from` always
re-spreads 0.75 gross over whatever is held, so a thinner collar CONCENTRATES rather
than de-grosses until the eligible set empties, at which point the book goes to cash.
Both effects are in the reported columns.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights, band_state                 # noqa
from engine import backtest, metrics, rebalance_mask                                    # noqa

SLUG = "2026-09-07_price-the-MAB-half-width-PAST-the-grid-edge_cloud"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS, FREQ, NFIX = 0.60, 0.75, "W", 20      # idea 387 leg C / idea 389, verbatim
BS_OLD = [0.00, 0.03, 0.06, 0.12]                     # idea 387/389's grid
BS_NEW = [0.20, 0.30, 0.50]                           # past the edge
COSTS = [0, 10, 25]
IS_END, OOS_START, WARMUP = "2016-12-31", "2017-01-01", 260
OFF = -1.0                                            # dial code for the gate-off arm
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


def lab(d):
    return "OFF" if d == OFF else f"{d:.2f}"


# ================================================================= panels
def small_panel():
    """SMALL439: the sub-$2B panel with the max_1d_move >= 1.0 names dropped (required)."""
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    return px[[c for c in px.columns if c not in bad]]


def _sub(px, cols):
    cols = [c for c in cols if c in px.columns]
    keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
    return px[keep].dropna(how="all").ffill()


def build_panels():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = sorted({t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"]
                    if t not in crypto})
    px136 = load_universe(broad=True)
    return [("U56", load_universe()), ("B136", px136), ("SMALL439", small_panel()),
            ("ETF36", _sub(px136, etf36))]


# ================================================== the book (idea 387 leg C, verbatim)
def gate_frame(px, b):
    """The eligibility gate.  b == OFF -> the 200d leg is REMOVED (all-True where priced);
    otherwise band_state at half-width b.  b == 0.00 nests px > ma200."""
    if b == OFF:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    return band_state(px, b)


def rank_frame(px, b):
    s = score(px, vol_scale=False)[0]
    _, _, vol20 = score(px)
    return s.where(gate_frame(px, b) & (vol20 < MAX_VOL) & px.notna()).rank(
        axis=1, ascending=False)


def sel_hard(rk, n):
    return (rk <= n).fillna(False)


def weights_from(sel, gross=GROSS):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return gross * s.div(k, axis=0).fillna(0.0)


def fast_backtest(px, w, freq=FREQ):
    """Clone of engine.backtest returning GROSS returns + turnover (gated in G1/G2)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT); cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]; turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i]); tot = growth.sum() + (1 - cur.sum())
        if tot > 0: cur = growth / tot
    idx = px.index
    return (pd.Series(np.nansum(held * rets, axis=1), index=idx),
            pd.Series(turn, index=idx), pd.Series((held > 0).sum(axis=1), index=idx))


def stats(gross_r, turn, bps, start):
    r = (gross_r - turn * bps / 1e4).loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    mo, mi = metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m1["Sharpe"],
                H2=m2["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                OOS_MaxDD=mo["MaxDD"], IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"])


def keeps(s, v2, spy):
    a = s["H1"] > v2["H1"] and s["H2"] > v2["H2"] and s["MaxDD"] >= v2["MaxDD"]
    fb = []
    if not s["H1"] > spy["H1"]: fb.append("H1")
    if not s["H2"] > spy["H2"]: fb.append("H2")
    if not s["OOS_Sharpe"] > spy["OOS_Sharpe"]: fb.append("OOS")
    if not s["MaxDD"] >= -0.60 * abs(spy["MaxDD"]): fb.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: fb.append("CAGR")
    return a, len(fb) == 0, ",".join(fb)


# ==================================================================================== main
def main():
    BS = BS_OLD + BS_NEW + [OFF]
    P(f"=== idea 390 — price the MAB half-width PAST the grid edge  ({SLUG}) ===")
    P("Design: idea 387 leg-C / idea 389 book VERBATIM; the ONLY change is the b ladder,")
    P(f"        extended from {BS_OLD} to {BS_OLD + BS_NEW} plus a gate-OFF rung.")
    P("Tuned params (2): b and the panel.  All grid points reported.")
    P("Structural note (pre-stated): band_state is a HYSTERESIS collar, so b -> inf is")
    P("        'never change state' == permanently OUT == ALL CASH, NOT 'gate off'.")
    P("        Gate-off is a separate arm the b ladder cannot reach.")
    P("Pre-registered: INTERIOR if the argmax is strictly inside {0.03..0.30} on a")
    P("        majority of panels and Sharpe(0.50) < Sharpe(argmax); EDGE if the argmax")
    P("        is at 0.50; GATE-OFF if OFF beats every b rung on a majority of panels.")

    panels = build_panels()
    P(f"\n[0] PANELS ({len(panels)})")
    for nm, px in panels:
        P(f"    {nm:9s} {px.shape[1]:>4d} cols  {px.index[0].date()} -> {px.index[-1].date()}"
          f"  ({len(px)} rows)")

    # ---------------------------------------------------------------- gates
    P("\n[0b] GATES")
    u = dict(panels)["U56"]
    w_g = weights_from(sel_hard(rank_frame(u, 0.0), NFIX))
    gr, tn, _ = fast_backtest(u, w_g)
    for bps in (0, 25):
        eng = backtest(u, w_g, cost_bps=bps, freq=FREQ)
        d1 = float((eng["returns"] - (gr - tn * bps / 1e4)).abs().max())
        d2 = float((eng["turnover"] - tn).abs().max())
        P(f"    G1/G2 cost_bps={bps:>2}: |d returns| {d1:.3e}   |d turnover| {d2:.3e}")
        assert d1 < 1e-12 and d2 < 1e-12
    ma = u.rolling(200).mean(); defined = ma.notna() & u.notna()
    d3 = int(((band_state(u, 0.0) != (u > ma)) & defined).values.sum())
    tot3 = int(defined.values.sum())
    P(f"    G3 band_state(b=0) vs px>ma200 where ma defined: {d3}/{tot3} "
      f"({d3/max(tot3,1):.2e})")
    assert d3 / max(tot3, 1) < 1e-4
    goff = gate_frame(u, OFF)
    P(f"    G5 OFF gate is all-True where priced: "
      f"{bool((goff | ~u.notna()).values.all())}")
    assert bool((goff | ~u.notna()).values.all())

    # ---------------------------------------------------------------- the grid
    P(f"\n[1] THE b LADDER — {len(panels)} panels x {len(BS)} rungs "
      f"({[lab(b) for b in BS]}), n={NFIX}, g={GROSS}, weekly, costs {COSTS} bps")
    comp, grid = {}, []
    for nm, px in panels:
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        h = len(spy) // 2
        sp = dict(CAGR=metrics(spy)["CAGR"], Sharpe=metrics(spy)["Sharpe"],
                  MaxDD=metrics(spy)["MaxDD"], H1=metrics(spy.iloc[:h])["Sharpe"],
                  H2=metrics(spy.iloc[h:])["Sharpe"],
                  OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                  OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                  OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"])
        v2r = backtest(px, rules_v2_weights(px), cost_bps=10, freq="W")["returns"]
        v2 = stats(v2r, pd.Series(0.0, index=px.index), 0, start)
        comp[nm] = (sp, v2)
        P(f"\n    {nm} comparands @10bps")
        P(f"      SPY      CAGR {sp['CAGR']:7.2%} Sharpe {sp['Sharpe']:.3f} "
          f"MaxDD {sp['MaxDD']:7.2%} H1/H2 {sp['H1']:.3f}/{sp['H2']:.3f} "
          f"OOS {sp['OOS_Sharpe']:.3f} OOS_CAGR {sp['OOS_CAGR']:7.2%}")
        P(f"      RULES v2 CAGR {v2['CAGR']:7.2%} Sharpe {v2['Sharpe']:.3f} "
          f"MaxDD {v2['MaxDD']:7.2%} H1/H2 {v2['H1']:.3f}/{v2['H2']:.3f} "
          f"OOS {v2['OOS_Sharpe']:.3f} OOS_CAGR {v2['OOS_CAGR']:7.2%}")

        priced = px.notna()
        n_priced = float(priced.values.sum())
        for b in BS:
            g = gate_frame(px, b)
            in_share = float((g & priced).values.sum()) / n_priced
            rk = rank_frame(px, b)
            elig = rk.notna().sum(axis=1)
            sel = sel_hard(rk, NFIX)
            g_r, t_r, nnames = fast_backtest(px, weights_from(sel))
            yrs = len(t_r.loc[start:]) / 252.0
            for bps in COSTS:
                s = stats(g_r, t_r, bps, start)
                a, b4, fb = keeps(s, v2, sp)
                grid.append(dict(panel=nm, dial=b, rung=lab(b), bps=bps, **s,
                                 in_share=in_share,
                                 elig=float(elig.loc[start:].mean()),
                                 names=float(nnames.loc[start:].mean()),
                                 cash_days=float((nnames.loc[start:] == 0).mean()),
                                 turnover=float(t_r.loc[start:].sum() / yrs),
                                 spy_Sharpe=sp["Sharpe"], spy_MaxDD=sp["MaxDD"],
                                 spy_CAGR=sp["CAGR"], spy_OOS_Sharpe=sp["OOS_Sharpe"],
                                 v2_Sharpe=v2["Sharpe"], v2_MaxDD=v2["MaxDD"],
                                 pass4a=a, pass4b=b4, first_fail4b=fb))
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    P(f"\n    grid: {len(G)} rows -> {SLUG}.grid.csv "
      f"({len(panels)} panels x {len(BS)} rungs x {len(COSTS)} rungs)")

    # G4: the incumbent rungs must reproduce idea 389's committed grid
    old = OUT / "2026-09-07_does-the-MAB-DD-damage-SCALE-survive-a-fourth-panel_cloud.grid.csv"
    if old.exists():
        O = pd.read_csv(old)
        O = O[(O.arm == "MAB") & O.panel.isin(["U56", "B136", "SMALL439", "ETF36"])]
        M = O.merge(G, on=["panel", "dial", "bps"], suffixes=("_389", "_390"))
        cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "OOS_CAGR",
                "OOS_MaxDD", "IS_Sharpe", "turnover", "names"]
        d4 = max(float((M[c + "_389"] - M[c + "_390"]).abs().max()) for c in cols)
        P(f"    G4 incumbent rungs vs idea 389's committed grid.csv: {len(M)} cells "
          f"joined, max |d| {d4:.3e}")
        assert len(M) == 4 * len(BS_OLD) * len(COSTS) and d4 < 1e-9
    else:
        P("    G4 SKIPPED — idea 389's grid.csv not present")

    # ---------------------------------------------------------------- the ladder
    P("\n[2] THE LADDER @10 bps — full-sample and mechanism, per panel")
    g10 = G[G.bps == 10]
    for nm, _ in panels:
        gg = g10[g10.panel == nm]
        P(f"\n    {nm}")
        P(gg[["rung", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "OOS_Sharpe",
              "in_share", "elig", "names", "cash_days", "turnover", "pass4a",
              "pass4b"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------- THE HEADLINE: the argmax
    P("\n[3] THE QUESTION — where is the argmax, and is the curve single-peaked?")
    P("    'b-ladder' = the 7 collar rungs only (OFF excluded); 'all' includes OFF.")
    arg = []
    for bps in COSTS:
        for nm, _ in panels:
            gg = G[(G.bps == bps) & (G.panel == nm)]
            lad = gg[gg.dial != OFF]
            off = gg[gg.dial == OFF].iloc[0]
            bfull = lad.loc[lad.Sharpe.idxmax()]
            bis = lad.loc[lad.IS_Sharpe.idxmax()]
            boos = lad.loc[lad.OOS_Sharpe.idxmax()]
            arg.append(dict(
                bps=bps, panel=nm,
                argmax_full=bfull.rung, S_full=bfull.Sharpe,
                argmax_IS=bis.rung, argmax_OOS=boos.rung,
                S_at_0=float(lad[lad.dial == 0.0].Sharpe.iloc[0]),
                S_at_012=float(lad[lad.dial == 0.12].Sharpe.iloc[0]),
                S_at_050=float(lad[lad.dial == 0.50].Sharpe.iloc[0]),
                S_OFF=float(off.Sharpe),
                OFF_beats_ladder=bool(off.Sharpe > lad.Sharpe.max()),
                interior=bool(bfull.dial not in (0.0, 0.50)),
                peaked=bool(float(lad[lad.dial == 0.50].Sharpe.iloc[0]) < bfull.Sharpe)))
    A = pd.DataFrame(arg)
    A.to_csv(OUT / f"{SLUG}.argmax.csv", index=False)
    P(A.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    a10 = A[A.bps == 10]
    P(f"\n    @10 bps: interior argmax on {int(a10.interior.sum())}/{len(a10)} panels | "
      f"curve turns down by b=0.50 on {int(a10.peaked.sum())}/{len(a10)} | "
      f"OFF beats the whole ladder on {int(a10.OFF_beats_ladder.sum())}/{len(a10)}")
    P(f"    all rungs, all cost rungs: interior {int(A.interior.sum())}/{len(A)} | "
      f"peaked {int(A.peaked.sum())}/{len(A)} | OFF wins {int(A.OFF_beats_ladder.sum())}/{len(A)}")

    P("\n[3b] IS THE b=0.12 EDGE REAL? — Sharpe at each rung MINUS Sharpe at b=0.12")
    piv = g10.pivot_table(index="panel", columns="rung", values="Sharpe")
    piv = piv[[lab(b) for b in BS]]
    P((piv.sub(piv["0.12"], axis=0)).to_string(float_format=lambda x: f"{x:+.4f}"))
    P("    (a positive entry means that rung BEATS idea 387's chosen b=0.12)")

    # ---------------------------------------------------------------- KEEP paths
    P("\n[4] KEEP PATHS — 4a (vs RULES v2) and 4b (vs SPY), every cell, every rung")
    for bps in COSTS:
        gg = G[G.bps == bps]
        P(f"    @{bps:>2} bps: 4a {int(gg.pass4a.sum())}/{len(gg)}   "
          f"4b {int(gg.pass4b.sum())}/{len(gg)}")
    p4b = G[G.pass4b]
    if len(p4b):
        P("\n    4b passers (all cost rungs):")
        P(p4b[["panel", "rung", "bps", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
               "OOS_Sharpe", "turnover"]].to_string(index=False,
                                                    float_format=lambda x: f"{x:.4f}"))
    else:
        P("\n    no 4b passers at any rung")
    ff = G[(G.bps == 10) & ~G.pass4b].first_fail4b.str.split(",").explode()
    P("\n    failing 4b bars @10 bps: "
      + ", ".join(f"{k} {v}" for k, v in ff.value_counts().items()))
    p4a = G[G.pass4a]
    P(f"    4a passers (any rung): {len(p4a)}"
      + ("" if not len(p4a) else "\n" + p4a[["panel", "rung", "bps", "Sharpe", "MaxDD",
                                             "H1", "H2"]].to_string(index=False)))

    # ---------------------------------------------------------------- rule 8
    P("\n[5] RULE 8 WALK-FORWARD — b chosen on IS 2008-2016 Sharpe @10 bps, "
      "2017-2026 read once")
    wf = []
    for nm, _ in panels:
        sp, v2 = comp[nm]
        anc = G[(G.panel == nm) & (G.bps == 10) & (G.dial == 0.0)].iloc[0]
        for scope, cand in (("b-ladder", g10[(g10.panel == nm) & (g10.dial != OFF)]),
                            ("ladder+OFF", g10[g10.panel == nm]),
                            ("old grid <=0.12",
                             g10[(g10.panel == nm) & (g10.dial >= 0) & (g10.dial <= 0.12)])):
            pick = cand.loc[cand.IS_Sharpe.idxmax()]
            wf.append(dict(panel=nm, scope=scope, pick=pick.rung,
                           IS_Sharpe=pick.IS_Sharpe, OOS_CAGR=pick.OOS_CAGR,
                           OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                           anchor_OOS_CAGR=anc.OOS_CAGR,
                           anchor_OOS_Sharpe=anc.OOS_Sharpe,
                           anchor_OOS_MaxDD=anc.OOS_MaxDD,
                           v2_OOS_Sharpe=v2["OOS_Sharpe"], v2_OOS_CAGR=v2["OOS_CAGR"],
                           spy_OOS_Sharpe=sp["OOS_Sharpe"], spy_OOS_CAGR=sp["OOS_CAGR"],
                           spy_OOS_MaxDD=sp["OOS_MaxDD"],
                           best_OOS=float(cand.OOS_Sharpe.max()),
                           regret=float(cand.OOS_Sharpe.max()) - pick.OOS_Sharpe,
                           pass4b=bool(pick.pass4b)))
    W = pd.DataFrame(wf)
    W.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    P(W.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    for scope, w in W.groupby("scope"):
        P(f"    {scope:16s}: above SPY OOS {int((w.OOS_Sharpe > w.spy_OOS_Sharpe).sum())}/{len(w)} | "
          f"above RULES v2 OOS {int((w.OOS_Sharpe > w.v2_OOS_Sharpe).sum())}/{len(w)} | "
          f"above the b=0 anchor OOS {int((w.OOS_Sharpe > w.anchor_OOS_Sharpe).sum())}/{len(w)} | "
          f"mean regret {w.regret.mean():+.4f} | 4b {int(w.pass4b.sum())}/{len(w)}")
    wide = W[W.scope == "b-ladder"].merge(
        W[W.scope == "old grid <=0.12"], on="panel", suffixes=("_new", "_old"))
    P("\n    DID WIDENING THE GRID CHANGE THE CHOOSER'S PICK, AND DID IT PAY?")
    P(wide[["panel", "pick_old", "pick_new", "OOS_Sharpe_old", "OOS_Sharpe_new",
            "OOS_CAGR_old", "OOS_CAGR_new", "OOS_MaxDD_old",
            "OOS_MaxDD_new"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    ch = int((wide.pick_old != wide.pick_new).sum())
    dS = float((wide.OOS_Sharpe_new - wide.OOS_Sharpe_old).mean())
    P(f"    pick changed on {ch}/{len(wide)} panels | mean OOS Sharpe delta "
      f"{dS:+.4f} (new grid minus old)")

    # ---------------------------------------------------------------- verdict
    P("\n[6] VERDICT")
    maj = len(a10) / 2.0
    if int(a10.OFF_beats_ladder.sum()) > maj:
        read = "GATE-OFF"
    elif int(a10.interior.sum()) > maj and int(a10.peaked.sum()) > maj:
        read = "INTERIOR"
    elif int(a10[a10.argmax_full == "0.50"].shape[0]) > maj:
        read = "EDGE"
    else:
        read = "MIXED"
    P(f"    pre-registered reading: {read}")
    P(f"    interior {int(a10.interior.sum())}/{len(a10)}, peaked "
      f"{int(a10.peaked.sum())}/{len(a10)}, OFF wins "
      f"{int(a10.OFF_beats_ladder.sum())}/{len(a10)} @10 bps")
    P(f"    4b passers overall: {int(G.pass4b.sum())}/{len(G)}; "
      f"4a passers: {int(G.pass4a.sum())}/{len(G)}")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")
    P(f"\n    console -> {SLUG}.console.txt")


if __name__ == "__main__":
    main()
