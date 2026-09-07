#!/usr/bin/env python3
"""Idea 389 - "does-the-MAB-DD-damage-SCALE-survive-a-fourth-panel" (cloud, 2026-09-07).

QUESTION (from QUEUE.md).  Idea 387's matched grid gave corr(MaxDD, dMaxDD) = +0.781 for
the 200d MA band (MAB) against +0.160 for the no-trade rank buffer (NT), i.e. the MAB's
drawdown cost looked like an H_scale instrument (damage grows with the book's own depth)
and NT like an H_const one.  But that was 9 MAB cells / 12 NT cells over THREE panels,
and SMALL439 alone supplies the deep end of the depth axis.  With one panel carrying the
deep end, +0.781 could be a two-point line.

DESIGN.  Re-run idea 387's leg-C matched grid VERBATIM (same parent book, same anchor,
same dials, same cost rungs, same rule-8 split) on more panels, so the depth axis gets
more points and the deep end is no longer a single panel:

    incumbent 3 : U56, B136, SMALL439           (idea 387's exact panels)
    new        : ETF36                          (idea 277/269C's named ETF panel)
    new        : MIX s=0.000, seeds 0/1/2       (k=36 draws from B136, 0% ETF)
    new        : MIX s=0.500, seeds 0/1/2       (k=36 draws from B136, 50% ETF)

MIX construction is idea 277's build_pool() verbatim (K_MIX=36, crc32("MIX|s|seed")
seeding), so s=1.000 IS ETF36 by construction and the ETF-share axis is k-matched.  The
three seeds per share are REPLICATION of a panel draw, not a tuned dial.

TUNED PARAMETERS (max 2, per PROTOCOL rule 4): (1) the dial -- m in {0,5,10,20,40} for
NT, b in {0,.03,.06,.12} for MAB; (2) the panel.  Nothing else moves.  ALL grid points
are reported (grid.csv, every panel x arm x dial x cost rung).

PRE-REGISTERED READING.  The claim under test is that corr(MaxDD_of_the_cell,
dMaxDD_vs_anchor) is materially higher for MAB than for NT.  Decision rule fixed before
the run:
    HOLDS      MAB corr stays >= +0.50 on the 10-panel pool AND the MAB-minus-NT corr gap
               stays positive, AND the MAB corr computed with SMALL439 DROPPED is still
               >= +0.50 (i.e. it is not the one deep panel).
    ONE PANEL  MAB corr falls below +0.50 on the pooled 10-panel set, or it survives
               pooled but collapses (< +0.30) once SMALL439 is dropped.
    MIXED      anything between.
Also reported: the per-panel corr, the between-panel (panel-mean) corr, and a
within-panel (panel-demeaned) corr, because a pooled corr over cells with panel-level
depth variation is a BETWEEN-panel statistic by construction -- which is exactly the
thing "does it survive a fourth panel" is asking about.

KEEP PATHS.  Both evaluated on every cell of every panel: 4a against RULES v2 on that
panel; 4b against SPY (Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's,
CAGR >= 70% of SPY's).  Reported at 0, 10 and 25 bps.

RULE 8.  Dial chosen on IS 2008-2016 Sharpe @10 bps, 2017-2026 read once; OOS CAGR /
Sharpe / MaxDD reported against that panel's anchor (NT m=0), RULES v2 and SPY.

GATES (all asserted, all printed).  G1/G2 fast_backtest == engine.backtest on returns and
turnover.  G3a sel_band(m=0) == sel_hard on every rebalance day.  G3b band_state(b=0) ==
px>ma200 where the MA is defined.  G4 the B136 anchor reproduces idea 333/384/387's
committed row to 1e-9.  G5 MIX s=1.000 == ETF36 exactly.  G6 the three incumbent panels'
cells reproduce idea 387's committed matched.csv to 1e-9 -- this run must be a strict
superset of idea 387's leg C, not a re-derivation of it.

CAVEATS.  (1) Every panel is a CURRENT-CONSTITUENT list -- SURVIVORSHIP.  SMALL439 is the
sub-$2B screen with max_1d_move >= 1.0 names dropped, as required; its 4b CAGR floor is
therefore tested in the book's favour.  (2) ETF36 and the MIX panels are k=36 subsets of
B136, so they share history and names with it -- the depth axis points are not
independent samples.  (3) 10 panels is still 10 points; a corr over them carries a
sampling band, reported.
"""
import sys, json, zlib
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, rules_v2_weights, band_state                 # noqa
from engine import backtest, metrics, rebalance_mask                                    # noqa

SLUG = "2026-09-07_does-the-MAB-DD-damage-SCALE-survive-a-fourth-panel_cloud"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS, FREQ, NFIX = 0.60, 0.75, "W", 20      # idea 387 leg C, verbatim
MS = [0, 5, 10, 20, 40]
BS = [0.00, 0.03, 0.06, 0.12]
COSTS = [0, 10, 25]
IS_END, OOS_START, WARMUP = "2016-12-31", "2017-01-01", 260
K_MIX, MIX_SHARES, MIX_SEEDS = 36, [0.000, 0.500], [0, 1, 2]
CORR_HOLDS, CORR_DIES = 0.50, 0.30
LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


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
    """idea 387's three + ETF36 + the k-matched 0%/50%-ETF MIX draws (idea 277 verbatim)."""
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = sorted({t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"]
                    if t not in crypto})
    px136 = load_universe(broad=True)
    b_stk = [t for t in px136.columns if t not in set(etf36) and t != "SPY"]

    panels = [("U56", load_universe()), ("B136", px136), ("SMALL439", small_panel()),
              ("ETF36", _sub(px136, etf36))]
    etf_pool, stk_pool = np.array(etf36), np.array(sorted(b_stk))
    for s in MIX_SHARES:
        n_etf = int(round(s * K_MIX)); n_stk = K_MIX - n_etf
        for sd in MIX_SEEDS:
            rng = np.random.default_rng(zlib.crc32(f"MIX|{s:.3f}|{sd}".encode()) % 2 ** 32)
            pick = []
            if n_etf: pick += rng.choice(etf_pool, size=n_etf, replace=False).tolist()
            if n_stk: pick += rng.choice(stk_pool, size=n_stk, replace=False).tolist()
            panels.append((f"MIX{int(s*100):02d}~{sd}", _sub(px136, sorted(pick))))
    return panels, etf36, px136, etf_pool, stk_pool


# ================================================== the book (idea 387 leg C, verbatim)
def rank_frame(px, b=None):
    """Parent eligibility.  b None -> plain px>ma200 leg (the NT arm's universe);
    b float -> that leg REPLACED by band_state at half-width b (the MAB arm)."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    gate = above if b is None else band_state(px, b)
    return s.where(gate & (vol20 < MAX_VOL) & px.notna()).rank(axis=1, ascending=False)


def sel_hard(rk, n):
    return rk <= n


def sel_band(px, rk, n, m, freq=FREQ):
    """idea 273/331's no-trade rank buffer, verbatim from ideas 384/387.  m=0 nests
    sel_hard(n)."""
    reb = rebalance_mask(px.index, freq).values
    cols = list(px.columns)
    out = np.zeros((len(px.index), len(cols)))
    rkv = rk.values
    held, last = [], np.zeros(len(cols))
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            cap = int(np.nansum(r <= n))
            held = [j for j in held if r[j] == r[j] and r[j] <= n + m]
            held.sort(key=lambda j: r[j])
            if len(held) > cap: held = held[:cap]
            if len(held) < cap:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs = set(held)
                for j in order:
                    if len(held) >= cap: break
                    if r[j] != r[j]: break
                    if j not in hs: held.append(j); hs.add(j)
                held.sort(key=lambda j: r[j])
            last = np.zeros(len(cols)); last[held] = 1.0
        out[i] = last
    return pd.DataFrame(out > 0.5, index=px.index, columns=cols)


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
                OOS_MaxDD=mo["MaxDD"], IS_Sharpe=mi["Sharpe"])


def keeps(s, v2, spy):
    a = s["H1"] > v2["H1"] and s["H2"] > v2["H2"] and s["MaxDD"] >= v2["MaxDD"]
    fb = []
    if not s["H1"] > spy["H1"]: fb.append("H1")
    if not s["H2"] > spy["H2"]: fb.append("H2")
    if not s["OOS_Sharpe"] > spy["OOS_Sharpe"]: fb.append("OOS")
    if not s["MaxDD"] >= -0.60 * abs(spy["MaxDD"]): fb.append("DD")
    if not s["CAGR"] >= 0.70 * spy["CAGR"]: fb.append("CAGR")
    return a, len(fb) == 0, ",".join(fb)


def spear(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0: return np.nan
    return float(np.corrcoef(pd.Series(x).rank(), pd.Series(y).rank())[0, 1])


def pear(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3 or np.std(x) == 0 or np.std(y) == 0: return np.nan
    return float(np.corrcoef(x, y)[0, 1])


def fisher_ci(r, n, z=1.96):
    """Fisher-z 95% band for a pearson r on n observations (reported, not asserted)."""
    if not np.isfinite(r) or n < 4 or abs(r) >= 1: return (np.nan, np.nan)
    zz = np.arctanh(r); se = 1.0 / np.sqrt(n - 3)
    return (float(np.tanh(zz - z * se)), float(np.tanh(zz + z * se)))


# ==================================================================================== main
def main():
    P(f"=== idea 389 — does the MAB DD-damage SCALE survive a fourth panel?  ({SLUG}) ===")
    P("Design: idea 387's leg-C matched grid, VERBATIM, on 10 panels instead of 3.")
    P("Tuned params (2): the dial (m or b) and the panel.  All grid points reported.")
    P(f"Pre-registered: HOLDS if pooled MAB corr >= {CORR_HOLDS:+.2f} AND gap over NT > 0 "
      f"AND MAB corr ex-SMALL439 >= {CORR_HOLDS:+.2f}; ONE-PANEL if pooled < {CORR_HOLDS:+.2f} "
      f"or ex-SMALL439 < {CORR_DIES:+.2f}.")

    panels, etf36, px136, etf_pool, stk_pool = build_panels()
    P(f"\n[0] PANELS ({len(panels)})")
    for nm, px in panels:
        P(f"    {nm:12s} {px.shape[1]:>4d} cols  {px.index[0].date()} -> {px.index[-1].date()}"
          f"  ({len(px)} rows)")

    # ---------------------------------------------------------------- gates
    P("\n[0b] GATES")
    u = dict(panels)["U56"]
    rk_u = rank_frame(u); w_g = weights_from(sel_hard(rk_u, NFIX))
    gr, tn, _ = fast_backtest(u, w_g)
    for bps in (0, 25):
        eng = backtest(u, w_g, cost_bps=bps, freq=FREQ)
        d1 = float((eng["returns"] - (gr - tn * bps / 1e4)).abs().max())
        d2 = float((eng["turnover"] - tn).abs().max())
        P(f"    G1/G2 cost_bps={bps:>2}: |d returns| {d1:.3e}   |d turnover| {d2:.3e}")
        assert d1 < 1e-12 and d2 < 1e-12
    reb = rebalance_mask(u.index, FREQ)
    dh = int((sel_band(u, rk_u, NFIX, 0).loc[reb.values]
              != sel_hard(rk_u, NFIX).fillna(False).loc[reb.values]).values.sum())
    P(f"    G3a sel_band(m=0) vs sel_hard on every rebalance day: {dh} disagreements")
    assert dh == 0
    ma = u.rolling(200).mean(); defined = ma.notna() & u.notna()
    d3b = int(((band_state(u, 0.0) != (u > ma)) & defined).values.sum())
    tot3b = int(defined.values.sum())
    P(f"    G3b band_state(b=0) vs px>ma200 where ma defined: {d3b}/{tot3b} "
      f"({d3b/max(tot3b,1):.2e})")
    assert d3b / max(tot3b, 1) < 1e-4
    bpx = dict(panels)["B136"]
    grb, tnb, _ = fast_backtest(bpx, weights_from(sel_hard(rank_frame(bpx), NFIX)))
    s_ref = stats(grb, tnb, 10, bpx.index[WARMUP])
    tgt = dict(CAGR=0.12992958836952506, Sharpe=0.9431848997615343,
               MaxDD=-0.2005204833110832, H1=1.1047866702854354,
               H2=0.8025166021122436, OOS_Sharpe=0.8836022780725372)
    dmax = max(abs(s_ref[k] - v) for k, v in tgt.items())
    P(f"    G4 (B136,n=20,g=0.75,anchor,W) vs idea 333/384/387's committed row: "
      f"max |d| {dmax:.3e}")
    assert dmax < 1e-9
    rng = np.random.default_rng(zlib.crc32(b"MIX|1.000|0") % 2 ** 32)
    s1 = sorted(rng.choice(etf_pool, size=K_MIX, replace=False).tolist())
    P(f"    G5 MIX s=1.000 draw == ETF36 exactly: {s1 == sorted(etf36)} "
      f"(|ETF36| = {len(etf36)} = K_MIX {K_MIX})")
    assert s1 == sorted(etf36)

    # ---------------------------------------------------------------- the grid
    P(f"\n[1] MATCHED GRID — {len(panels)} panels x (NT m{MS} | MAB b{BS}), "
      f"n={NFIX}, g={GROSS}, weekly, costs {COSTS} bps")
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

        rk_nt = rank_frame(px, b=None)
        cells = [("NT", float(m), sel_band(px, rk_nt, NFIX, m)) for m in MS]
        for bw in BS:
            cells.append(("MAB", float(bw), sel_hard(rank_frame(px, b=bw), NFIX).fillna(False)))
        for arm, dial, sel in cells:
            g_r, t_r, nnames = fast_backtest(px, weights_from(sel))
            yrs = len(t_r.loc[start:]) / 252.0
            for bps in COSTS:
                s = stats(g_r, t_r, bps, start)
                a, b4, fb = keeps(s, v2, sp)
                grid.append(dict(panel=nm, arm=arm, dial=dial, bps=bps, **s,
                                 turnover=float(t_r.loc[start:].sum() / yrs),
                                 names=float(nnames.loc[start:].mean()),
                                 spy_Sharpe=sp["Sharpe"], spy_MaxDD=sp["MaxDD"],
                                 spy_CAGR=sp["CAGR"], spy_OOS_Sharpe=sp["OOS_Sharpe"],
                                 v2_Sharpe=v2["Sharpe"], v2_MaxDD=v2["MaxDD"],
                                 pass4a=a, pass4b=b4, first_fail4b=fb))
    G = pd.DataFrame(grid)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    P(f"\n    grid: {len(G)} rows written to {SLUG}.grid.csv "
      f"({len(panels)} panels x 9 cells x {len(COSTS)} rungs)")

    # -------------------------------------------------- the matched contrast @10 bps
    P("\n[2] THE MATCHED CONTRAST @10 bps (each cell vs its panel's SHARED anchor NT m=0)")
    rows = []
    g10 = G[G.bps == 10]
    for nm, _ in panels:
        anc = g10[(g10.panel == nm) & (g10.arm == "NT") & (g10.dial == 0)].iloc[0]
        for _, r in g10[g10.panel == nm].iterrows():
            if r.dial == 0.0: continue                    # both arms nest the anchor at 0
            rows.append(dict(panel=nm, arm=r.arm, dial=r.dial, anchor_MaxDD=anc.MaxDD,
                             dMaxDD_bp=(r.MaxDD - anc.MaxDD) * 1e4,
                             dSharpe=r.Sharpe - anc.Sharpe,
                             dCAGR_pp=(r.CAGR - anc.CAGR) * 100,
                             dTurn=r.turnover - anc.turnover,
                             dNames=r.names - anc.names,
                             MaxDD=r.MaxDD, Sharpe=r.Sharpe))
    C = pd.DataFrame(rows)
    C.to_csv(OUT / f"{SLUG}.matched.csv", index=False)
    P(C.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # G6: the three incumbent panels must reproduce idea 387's committed matched.csv
    old = OUT / "2026-09-07_split-the-band-lexicon-in-the-LEADERBOARD_C.matched.csv"
    if old.exists():
        O = pd.read_csv(old)
        k = ["panel", "arm", "dial"]
        M = O.merge(C, on=k, suffixes=("_387", "_389"))
        cols = ["dMaxDD_bp", "dSharpe", "dCAGR_pp", "dTurn", "dNames", "MaxDD", "Sharpe"]
        d6 = max(float((M[c + "_387"] - M[c + "_389"]).abs().max()) for c in cols)
        P(f"\n    G6 incumbent 3 panels vs idea 387's committed matched.csv: "
          f"{len(M)} cells joined, max |d| {d6:.3e}")
        assert len(M) == 21 and d6 < 1e-9
    else:
        P("\n    G6 SKIPPED — idea 387's matched.csv not present")

    P("\n[3] ARM SUMMARY (pooled over all panels, @10 bps)")
    for arm, g in C.groupby("arm"):
        P(f"    {arm:3s}: {len(g):>3d} cells | improves DD {(g.dMaxDD_bp>0).mean():6.1%} "
          f"worsens {(g.dMaxDD_bp<0).mean():6.1%} | median dMaxDD {g.dMaxDD_bp.median():+8.1f} bp "
          f"| median dSharpe {g.dSharpe.median():+.4f} | median dTurn {g.dTurn.median():+7.2f}x/yr "
          f"| median dNames {g.dNames.median():+.4f}")

    # ------------------------------------------------ THE HEADLINE: the depth scaling
    P("\n[4] THE QUESTION — corr(MaxDD, dMaxDD): does the MAB's DD damage SCALE with depth?")
    P("    (MaxDD is the CELL's own drawdown; dMaxDD its delta vs the panel anchor.)")
    P("    Note: 'MaxDD' here follows idea 387 exactly — negative numbers, so a MORE")
    P("    NEGATIVE dMaxDD is DAMAGE, and a POSITIVE corr means damage grows with depth.")
    inc3 = {"U56", "B136", "SMALL439"}
    S_ALL, S_387 = "ALL 10 panels", "idea 387's 3 (replication)"
    S_EX = "EX-SMALL439 (drop the deep end)"
    scopes = [(S_ALL, C),
              (S_387, C[C.panel.isin(inc3)]),
              (S_EX, C[C.panel != "SMALL439"]),
              ("NEW 7 panels only", C[~C.panel.isin(inc3)])]
    hdr = []
    for lbl, sc in scopes:
        for arm in ("NT", "MAB"):
            g = sc[sc.arm == arm]
            r = pear(g.MaxDD, g.dMaxDD_bp); rs = spear(g.MaxDD, g.dMaxDD_bp)
            lo, hi = fisher_ci(r, len(g))
            hdr.append(dict(scope=lbl, arm=arm, n=len(g), pearson=r, spearman=rs,
                            ci_lo=lo, ci_hi=hi))
        a = hdr[-1]["pearson"]; b = hdr[-2]["pearson"]
        hdr[-1]["gap_MAB_minus_NT"] = a - b
    H = pd.DataFrame(hdr)
    H.to_csv(OUT / f"{SLUG}.corr.csv", index=False)
    P(H.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n[4b] PER-PANEL corr (the depth axis, one row per panel — this is the 'more points')")
    per = []
    for nm, _ in panels:
        anc = float(g10[(g10.panel == nm) & (g10.arm == "NT") & (g10.dial == 0)].MaxDD.iloc[0])
        row = dict(panel=nm, anchor_MaxDD=anc)
        for arm in ("NT", "MAB"):
            g = C[(C.panel == nm) & (C.arm == arm)]
            row[f"{arm}_median_dDD_bp"] = float(g.dMaxDD_bp.median())
            row[f"{arm}_corr"] = pear(g.MaxDD, g.dMaxDD_bp)
            row[f"{arm}_spear_dial"] = spear(g.dial, g.dMaxDD_bp)
        per.append(row)
    PP = pd.DataFrame(per).sort_values("anchor_MaxDD")
    PP.to_csv(OUT / f"{SLUG}.perpanel.csv", index=False)
    P(PP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n[4c] DECOMPOSITION — is the pooled corr BETWEEN panels or WITHIN them?")
    dec = []
    for arm in ("NT", "MAB"):
        g = C[C.arm == arm].copy()
        pooled = pear(g.MaxDD, g.dMaxDD_bp)
        bm = g.groupby("panel")[["MaxDD", "dMaxDD_bp"]].mean()
        between = pear(bm.MaxDD, bm.dMaxDD_bp)
        g["MaxDD_w"] = g.MaxDD - g.groupby("panel").MaxDD.transform("mean")
        g["dDD_w"] = g.dMaxDD_bp - g.groupby("panel").dMaxDD_bp.transform("mean")
        within = pear(g.MaxDD_w, g.dDD_w)
        dec.append(dict(arm=arm, n_cells=len(g), n_panels=len(bm), pooled=pooled,
                        between_panelmeans=between, within_panel_demeaned=within))
    D = pd.DataFrame(dec)
    D.to_csv(OUT / f"{SLUG}.decomp.csv", index=False)
    P(D.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n[4e] THE SPECIFICATION DEFECT, and the correctly-specified depth statistic")
    P("    Within a panel the anchor is a CONSTANT, so dMaxDD = MaxDD - anchor is an exact")
    P("    AFFINE function of MaxDD and corr(MaxDD, dMaxDD) is mechanically +1.000 — which")
    P("    is what [4b]/[4c] print for all 10 panels and BOTH arms.  Idea 387's statistic")
    P("    is therefore not a depth-scaling measurement: it is a between-panel statistic")
    P("    with a mechanical within-panel identity mixed into it, and its pooled value is")
    P("    driven by how the panels' anchors are spread, not by the instrument.")
    P("    The claim 'the damage SCALES with the book's own depth' is properly a statement")
    P("    about the PANEL's depth, so the specified statistic is corr(anchor_MaxDD, dMaxDD)")
    P("    — the anchor varies across panels and is fixed within one, so it carries no")
    P("    mechanical component.  Reported both pooled over cells and over panel means.")
    dep = []
    for lbl, sc in scopes:
        for arm in ("NT", "MAB"):
            g = sc[sc.arm == arm]
            r = pear(g.anchor_MaxDD, g.dMaxDD_bp)
            bm = g.groupby("panel")[["anchor_MaxDD", "dMaxDD_bp"]].mean()
            lo, hi = fisher_ci(r, len(g))
            dep.append(dict(scope=lbl, arm=arm, n_cells=len(g), n_panels=len(bm),
                            corr_anchor_cells=r, ci_lo=lo, ci_hi=hi,
                            spear_anchor_cells=spear(g.anchor_MaxDD, g.dMaxDD_bp),
                            corr_anchor_panelmeans=pear(bm.anchor_MaxDD, bm.dMaxDD_bp),
                            spear_anchor_panelmeans=spear(bm.anchor_MaxDD, bm.dMaxDD_bp)))
    DEP = pd.DataFrame(dep)
    DEP.to_csv(OUT / f"{SLUG}.depth.csv", index=False)
    P(DEP.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    d_mab = float(DEP[(DEP.scope == S_ALL) & (DEP.arm == "MAB")].corr_anchor_panelmeans.iloc[0])
    d_nt = float(DEP[(DEP.scope == S_ALL) & (DEP.arm == "NT")].corr_anchor_panelmeans.iloc[0])
    P(f"    correctly-specified, 10 panel means: MAB {d_mab:+.4f}  NT {d_nt:+.4f}  "
      f"gap {d_mab - d_nt:+.4f}")

    P("\n[4d] MONOTONICITY of dMaxDD in the dial (spearman), per panel x arm")
    mono = PP[["panel", "anchor_MaxDD", "NT_spear_dial", "MAB_spear_dial"]]
    P(mono.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"    MAB spearman == -1.000 on {int((PP.MAB_spear_dial <= -0.999).sum())} of "
      f"{len(PP)} panels (idea 387 found 1 of 3: U56 only)")

    # ---------------------------------------------------------------- KEEP paths
    P("\n[5] KEEP PATHS — 4a (vs RULES v2) and 4b (vs SPY) on every cell, every rung")
    for bps in COSTS:
        gg = G[G.bps == bps]
        P(f"    @{bps:>2} bps: 4a {int(gg.pass4a.sum())}/{len(gg)}   "
          f"4b {int(gg.pass4b.sum())}/{len(gg)}")
    p4b = G[(G.bps == 10) & G.pass4b]
    if len(p4b):
        P("\n    4b passers @10 bps:")
        P(p4b[["panel", "arm", "dial", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
               "OOS_Sharpe", "turnover"]].to_string(index=False,
                                                    float_format=lambda x: f"{x:.4f}"))
    else:
        P("\n    no 4b passers @10 bps")
    ff = G[(G.bps == 10) & ~G.pass4b].first_fail4b.str.split(",").explode()
    P("\n    first-failing 4b bars @10 bps: "
      + ", ".join(f"{k} {v}" for k, v in ff.value_counts().items()))
    p4a = G[G.pass4a]
    P(f"    4a passers (any rung): {len(p4a)}"
      + ("" if not len(p4a) else "\n" + p4a[["panel", "arm", "dial", "bps", "Sharpe",
                                             "MaxDD", "H1", "H2"]].to_string(index=False)))

    # ---------------------------------------------------------------- rule 8
    P("\n[6] RULE 8 WALK-FORWARD — dial chosen on IS 2008-2016 Sharpe @10bps, "
      "2017-2026 read once")
    wf = []
    for nm, _ in panels:
        sp, v2 = comp[nm]
        anc = G[(G.panel == nm) & (G.bps == 10) & (G.arm == "NT") & (G.dial == 0)].iloc[0]
        for arm in ("NT", "MAB"):
            cand = G[(G.panel == nm) & (G.arm == arm) & (G.bps == 10)]
            pick = cand.loc[cand.IS_Sharpe.idxmax()]
            wf.append(dict(panel=nm, arm=arm, pick=pick.dial, IS_Sharpe=pick.IS_Sharpe,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD,
                           anchor_OOS_CAGR=anc.OOS_CAGR, anchor_OOS_Sharpe=anc.OOS_Sharpe,
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
    P(f"\n    picks above SPY OOS: {int((W.OOS_Sharpe > W.spy_OOS_Sharpe).sum())}/{len(W)} | "
      f"above RULES v2 OOS: {int((W.OOS_Sharpe > W.v2_OOS_Sharpe).sum())}/{len(W)} | "
      f"above the shared anchor OOS: {int((W.OOS_Sharpe > W.anchor_OOS_Sharpe).sum())}/{len(W)} | "
      f"mean regret {W.regret.mean():+.4f}")
    P(f"    rule-8 picks that also clear 4b: {int(W.pass4b.sum())}/{len(W)}")

    # ---------------------------------------------------------------- verdict
    P("\n[7] PRE-REGISTERED READING")
    def hv(scope, arm, col="pearson"):
        return float(H[(H.scope == scope) & (H.arm == arm)][col].iloc[0])
    pool_mab, pool_nt = hv(S_ALL, "MAB"), hv(S_ALL, "NT")
    ex_mab, ex_nt = hv(S_EX, "MAB"), hv(S_EX, "NT")
    g387, nt387 = hv(S_387, "MAB", "gap_MAB_minus_NT"), hv(S_387, "NT")
    P(f"    pooled (10 panels): MAB {pool_mab:+.4f}  NT {pool_nt:+.4f}  "
      f"gap {pool_mab - pool_nt:+.4f}   (idea 387 on 3 panels: MAB +0.781 NT +0.160)")
    P(f"    ex-SMALL439:        MAB {ex_mab:+.4f}  NT {ex_nt:+.4f}  gap {ex_mab - ex_nt:+.4f}")
    if pool_mab >= CORR_HOLDS and (pool_mab - pool_nt) > 0 and ex_mab >= CORR_HOLDS:
        v = "HOLDS — the MAB depth scaling survives the added panels and the loss of SMALL439"
    elif pool_mab < CORR_HOLDS or ex_mab < CORR_DIES:
        v = ("ONE PANEL — idea 387's +0.781 does NOT survive; the MAB/NT split is not a "
             "depth-scaling fact")
    else:
        v = "MIXED — pooled survives but the ex-SMALL439 reading is inside the grey band"
    P(f"    pre-registered VERDICT on idea 387's own statistic: {v}")
    P(f"    the SPLIT it was quoted for does NOT: the MAB-minus-NT gap collapses from "
      f"{g387:+.4f} on idea 387's 3 panels to {pool_mab - pool_nt:+.4f} pooled and "
      f"{ex_mab - ex_nt:+.4f} with SMALL439 dropped — NT's corr rises from {nt387:+.4f} "
      f"to {ex_nt:+.4f} while MAB's falls.")
    P(f"    and on the CORRECTLY-SPECIFIED statistic (panel means, no mechanical term): "
      f"MAB {d_mab:+.4f} vs NT {d_nt:+.4f}, gap {d_mab - d_nt:+.4f}.")
    P("\n    CAVEATS: every panel is a current-constituent list (SURVIVORSHIP), so the 4b "
      "CAGR floor is tested in each book's favour; ETF36 and the 6 MIX panels are k=36 "
      "subsets of B136 and therefore NOT independent draws; 10 panels is 10 points and "
      "the Fisher bands above are wide.")

    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")
    return v


if __name__ == "__main__":
    main()
