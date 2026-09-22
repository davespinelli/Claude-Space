#!/usr/bin/env python3
"""Idea 1425 (2026-09-22, lane cloud, run 11) -- DOES THE FROZEN INCUMBENT'S WEIGHT VECTOR
CARRY ANY DRAWDOWN INFORMATION AT ALL?

WHY THIS RUN EXISTS
    Before any SIZING rule can be a finding, the axis it moves has to have variance, and the
    record's anchor has to sit somewhere non-trivial on it.  The live RULES v2 book holds every
    name inside the 200d +/-3% band at EQUAL weight, gross 0.75.  This run draws RANDOM weight
    vectors over the incumbent's OWN held set at each rebalance -- same names, same gross, same
    cadence, same t+1 execution, same costs -- and places the EQUAL-WEIGHT ANCHOR's PROTOCOL 4b
    DRAWDOWN MARGIN inside that distribution.
        * If the anchor sits mid-band, intra-book sizing is a DEAD AXIS and every sizing result
          in the record is a draw from this null.
        * If the anchor sits in a tail, equal weight is doing real work and sizing is live.

THE NULL (matched on everything except the weight vector)
    At each weekly rebalance date the held set H_t is exactly the set of names the live book
    holds that day (200d +/-3% band, `baseline.band_state`).  Equal weight is the Dirichlet MEAN
    for every alpha, so the anchor is the null's own centre of mass in WEIGHT space -- the whole
    question is whether it is also central in DRAWDOWN space, which is a non-linear functional of
    the weights and need not be.  alpha -> infinity collapses the null onto the anchor;
    alpha = 0.5 is near-degenerate (few names carry almost all the gross).

    TWO NULL SHAPES are run, because a re-sizing null is NOT automatically turnover-matched and
    the record has been burned by exactly that confound (ideas 931 / 943: a turnover rebate is a
    gain every book collects):
      IID   x_t ~ Dirichlet(alpha * 1_{|H_t|}) drawn INDEPENDENTLY at EVERY rebalance date.
            This re-sizes AND re-trades: its turnover is far above the anchor's, so at any
            positive cost rung it is a JOINT test of sizing and trading and CANNOT on its own
            support a sizing claim.  Published, and read only at 0 bps.
      PERS  one multiplier vector m ~ Gamma(alpha) drawn ONCE per draw and held for the whole
            sample; at each rebalance w_t = g_t * m_H / sum(m_H) over the CURRENT held set, where
            g_t is the anchor's own gross that date.
            Turnover then comes only from held-set changes and renormalisation, i.e. from the
            SAME events that make the anchor trade, so PERS is the turnover-matched null and is
            the one that answers the filed question.  Its realised turnover is published beside
            the anchor's at every cell.

THE TWO TUNED PARAMETERS (PROTOCOL rule 4 budget, and no more)
    alpha       in {0.5, 1, 2, 5, 20, 100}          Dirichlet / Gamma concentration
    draw count  in {50, 200}   (the 50 is the first 50 of the 200 -- a nested prefix, so the
                                draw-count axis is a RESOLUTION axis and costs no extra tape)
    Panel {u56, broad}, null shape {IID, PERS} and cost rung {0, 5, 10, 25, 50} bps are REPORTED
    axes, never selected on.
    Every one of the 2 x 2 x 6 x 2 x 5 = 240 published cells is reported, pass or fail.

GATES (printed before any hypothesis is read)
    G1  the fast simulator reproduces `engine.backtest` on the live RULES v2 book to < 1e-12 on
        both returns and turnover, at every panel.
    G2  every draw, under BOTH null shapes, holds EXACTLY the anchor's held set at EXACTLY the
        anchor's OWN gross on that date (set mismatch 0, max|dgross| < 1e-12), and the anchor
        itself passed through the identical draw pipeline reproduces `rules_v2_weights` to 0.
        This matters: the live book weights gross/N_PRICED and sends gated-out weight to CASH,
        so its realised gross is gross * N_held/N_priced and NOT 0.75.  A null normalised to a
        flat 0.75 would carry MORE exposure than the anchor and every contrast below would be an
        exposure contrast, not a sizing one.
    G3  the draws are seeded deterministically (md5 of panel/alpha/index) and a re-draw
        reproduces draw 0's Sharpe bit-for-bit.
    G4  the Dirichlet mean check: the mean weight vector over the 200 draws converges on the
        anchor (max|mean - anchor| reported per alpha).
    G5  all 240 cells published.
    G6  PERS is turnover-matched: its median realised turnover is reported against the anchor's
        at every cell, and IID's is reported beside it to show the size of the confound.

RULE 8 (PROTOCOL rule 8 -- walk-forward, 2017-2026 read ONCE)
    If the weight vector carries DD information, a chooser that may look ONLY at 2009-2016 should
    be able to find it.  Two legal IS-only choosers are run per (panel, alpha, cost):
        C_SHARPE  argmax IN-SAMPLE Sharpe over the draws
        C_DD      argmax IN-SAMPLE 4b DD margin over the draws
    Each pick's 2017-2026 leg is then read ONCE against the anchor's OOS, the live RULES v2
    book's OOS and SPY's OOS -- and, decisively, against the pick's OWN OOS PERCENTILE inside the
    draw distribution.  A chooser landing at the ~50th OOS percentile has found nothing.

CAVEATS carried
    Survivorship (PROTOCOL rule 9 / idea 54): u56 and broad are CURRENT constituents, so every
    CAGR level is optimistic and both 4b bars are easier than on a point-in-time panel.  The
    anchor-vs-null CONTRAST is same-tape / same-names / same-gross and is first-order immune.
    Costs flat per unit turnover, no spread, impact or borrow.  One cadence (W), one execution
    delay (t+1), one gross (0.75), one gate (200d +/-3%).  Dirichlet is one null shape among
    many; a null with cross-sectional structure (e.g. vol- or beta-tilted) is a different test
    and is NOT run here.
    Deterministic, standalone.  Writes .log.txt / .grid.csv / .draws.csv / .walkforward.csv
    next to itself.  Modifies nothing.
"""
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-22_incumbent-weight-vector-dd-information_cloud"
OUT = ROOT / "research" / "backtests"

ALPHAS = [0.5, 1.0, 2.0, 5.0, 20.0, 100.0]
NDRAWS = [50, 200]
NMAX = max(NDRAWS)
COSTS = [0.0, 5.0, 10.0, 25.0, 50.0]
SHAPES = ["PERS", "IID"]
PANELS = ["u56", "broad"]
FREQ, GROSS, BAND = "W", 0.75, 0.03
IS_END, OOS_START = "2016-12-31", "2017-01-01"
PHI0, DELTA0 = 0.70, 0.60

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)
_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def seed_of(*parts):
    return int(hashlib.md5("|".join(str(p) for p in parts).encode()).hexdigest()[:8], 16)


# ------------------------------------------------------------------- fast simulator ----
def sim(rv, wv, mv):
    """`engine.backtest` with costs factored out: returns (gross daily return, turnover)."""
    T, n = rv.shape
    cur = np.zeros(n)
    out = np.empty(T); to = np.zeros(T)
    for i in range(T):
        if mv[i] or i == 0:
            new = wv[i]
            to[i] = np.abs(new - cur).sum()
            cur = new.copy()
        out[i] = cur @ rv[i]
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return out, to


def fast_metrics(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    cagr = eq[-1] ** (1 / yrs) - 1
    dd = (eq / np.maximum.accumulate(eq) - 1).min()
    vol = r.std(ddof=1) * np.sqrt(252)
    return cagr, (r.mean() * 252 / vol if vol else np.nan), dd


def full_stats(r, i_h, i_is, i_oos):
    c, s, d = fast_metrics(r)
    _, s1, _ = fast_metrics(r[:i_h]); _, s2, _ = fast_metrics(r[i_h:])
    _, sis, dis = fast_metrics(r[:i_is])
    co, so, do = fast_metrics(r[i_oos:])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=s1, H2=s2, IS_Sharpe=sis, IS_MaxDD=dis,
                OOS_CAGR=co, OOS_Sharpe=so, OOS_MaxDD=do)


def main():
    grid, draws_out, wf = [], [], []
    for panel in PANELS:
        px = load_universe(broad=(panel == "broad"))
        anchor_w = rules_v2_weights(px, band=BAND, gross=GROSS)
        start = px.index[260]
        rets = px.pct_change().fillna(0.0)
        mask = rebalance_mask(px.index, FREQ).shift(1, fill_value=False)
        wA = anchor_w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0)
        rv, mv = rets.values, mask.values
        i0 = px.index.get_loc(start)
        n = px.shape[1]

        # ---- G1 / anchor
        ga, ta = sim(rv, wA.values, mv)
        eng = backtest(px, anchor_w, cost_bps=10.0, freq=FREQ)
        g1r = float(np.abs((pd.Series(ga, index=px.index) - ta * 10.0 / 1e4) - eng["returns"]).max())
        g1t = float(np.abs(pd.Series(ta, index=px.index) - eng["turnover"]).max())
        say(f"[G1] {panel}: max|dret| = {g1r:.3e}   max|dturnover| = {g1t:.3e}")
        assert g1r < 1e-12 and g1t < 1e-12

        held = (wA.values > 0)                       # the incumbent's OWN held set, per date
        cnt = held.sum(axis=1)
        reb = np.flatnonzero(mv); reb = np.concatenate(([0], reb)) if mv[0] == False else reb
        reb = np.unique(reb)
        tgross = wA.values[reb].sum(axis=1)          # the anchor's OWN gross, per rebalance date
        spy = px["SPY"].pct_change().fillna(0.0).values
        base_r = eng["returns"].values                # live RULES v2 @10 bps (cost re-applied below)
        sub = slice(i0, len(px.index))
        L = len(px.index) - i0
        i_h, i_is = L // 2, int(np.searchsorted(px.index[i0:], pd.Timestamp(IS_END))) + 1
        i_oos = int(np.searchsorted(px.index[i0:], pd.Timestamp(OOS_START)))
        sp = full_stats(spy[sub], i_h, i_is, i_oos)
        say(f"[info] {panel}: sample {px.index[i0].date()}..{px.index[-1].date()}  {L} days, "
            f"IS ends idx {i_is}, OOS starts idx {i_oos}, held-set size mean {cnt[reb].mean():.1f}")

        for shape, alpha in [(s, a) for s in SHAPES for a in ALPHAS]:
            W = np.zeros((NMAX, L)); TO = np.zeros((NMAX, L))
            wsum = np.zeros(n); gmax = 0.0; setmis = 0
            for k in range(NMAX):
                rng = np.random.default_rng(seed_of(panel, shape, alpha, k))
                wv = np.zeros((len(px.index), n))
                if shape == "IID":
                    g = rng.gamma(alpha, size=(len(reb), n))
                else:                                  # PERS: ONE multiplier vector, held
                    g = np.repeat(rng.gamma(alpha, size=(1, n)), len(reb), axis=0)
                g = g * held[reb]
                s = g.sum(axis=1)
                ok = s > 0
                # GROSS-MATCH to the anchor DATE BY DATE.  The live book weights gross/N_PRICED
                # and sends the gated-out weight to CASH, so its realised gross is
                # gross * N_held/N_priced, NOT `gross`.  Normalising the draw to `gross` would
                # hand the null a larger exposure than the anchor and every contrast would be an
                # exposure contrast.  The draw gets the anchor's OWN gross on that date.
                g[ok] = tgross[ok, None] * g[ok] / s[ok, None]
                wv[reb] = g
                # forward-fill between rebalance dates (engine only reads the rebalance rows)
                idx = np.maximum.accumulate(np.where(np.isin(np.arange(len(px.index)), reb),
                                                     np.arange(len(px.index)), -1))
                wv = wv[np.where(idx < 0, 0, idx)]
                gr, to = sim(rv, wv, mv)
                W[k] = gr[sub]; TO[k] = to[sub]
                wsum += g.sum(axis=0) / len(reb)
                gmax = max(gmax, float(np.abs(g[ok].sum(axis=1) - tgross[ok]).max()))
                setmis += int(((g > 0) & ~held[reb]).sum())
            anchor_mean = (wA.values[reb] * 1.0).sum(axis=0) / len(reb)
            g4 = float(np.abs(wsum / NMAX - anchor_mean).max())
            if alpha == ALPHAS[0]:
                ga_ = np.ones((len(reb), n)) * held[reb]      # the anchor THROUGH the draw pipeline
                sa_ = ga_.sum(axis=1); oka = sa_ > 0
                ga_[oka] = tgross[oka, None] * ga_[oka] / sa_[oka, None]
                say(f"[G2] {panel}/{shape}: max|draw gross - anchor gross| = {gmax:.3e}   "
                    f"held-set mismatches = {setmis}   "
                    f"max|anchor via draw pipeline - anchor w| = "
                    f"{float(np.abs(ga_ - wA.values[reb]).max()):.3e}")
            say(f"[G4] {panel}/{shape} alpha={alpha}: max|mean(draw w) - anchor w| = {g4:.4f} "
                f"(anchor mean weight {anchor_mean[anchor_mean>0].mean():.4f})")

            for cost in COSTS:
                ar = ga[sub] - ta[sub] * cost / 1e4
                anc = full_stats(ar, i_h, i_is, i_oos)
                br = eng["returns"].values[sub] + eng["turnover"].values[sub] * 10.0 / 1e4 \
                    - eng["turnover"].values[sub] * cost / 1e4
                bs = full_stats(br, i_h, i_is, i_oos)
                D = []
                for k in range(NMAX):
                    r = W[k] - TO[k] * cost / 1e4
                    st = full_stats(r, i_h, i_is, i_oos)
                    st["draw"] = k; st["TO"] = TO[k].sum() / (L / 252)
                    st["m_DD"] = (st["MaxDD"] - DELTA0 * sp["MaxDD"]) * 100
                    st["m_CAGR"] = (st["CAGR"] - PHI0 * sp["CAGR"]) * 100
                    st["IS_mDD"] = (st["IS_MaxDD"] - DELTA0 * sp["MaxDD"]) * 100
                    st["p4b"] = bool(st["H1"] > sp["H1"] and st["H2"] > sp["H2"]
                                     and st["OOS_Sharpe"] > sp["OOS_Sharpe"]
                                     and st["m_DD"] >= 0 and st["m_CAGR"] >= 0)
                    st["p4a"] = bool(st["H1"] > bs["H1"] and st["H2"] > bs["H2"]
                                     and st["MaxDD"] >= bs["MaxDD"])
                    D.append(st)
                DF = pd.DataFrame(D)
                a_mDD = (anc["MaxDD"] - DELTA0 * sp["MaxDD"]) * 100
                a_mC = (anc["CAGR"] - PHI0 * sp["CAGR"]) * 100
                a_isDD = (anc["IS_MaxDD"] - DELTA0 * sp["MaxDD"]) * 100
                for nd in NDRAWS:
                    d = DF.iloc[:nd]
                    pct = lambda col, v: float((d[col] < v).mean() * 100)
                    grid.append(dict(
                        panel=panel, null_shape=shape, alpha=alpha, ndraws=nd, cost_bps=cost,
                        anchor_CAGR=anc["CAGR"], anchor_Sharpe=anc["Sharpe"], anchor_MaxDD=anc["MaxDD"],
                        anchor_H1=anc["H1"], anchor_H2=anc["H2"], anchor_OOS_S=anc["OOS_Sharpe"],
                        anchor_OOS_CAGR=anc["OOS_CAGR"], anchor_OOS_DD=anc["OOS_MaxDD"],
                        anchor_TO=ta[sub].sum() / (L / 252),
                        anchor_mDD=a_mDD, anchor_mCAGR=a_mC,
                        pct_mDD=pct("m_DD", a_mDD), pct_Sharpe=pct("Sharpe", anc["Sharpe"]),
                        pct_CAGR=pct("CAGR", anc["CAGR"]), pct_OOS_S=pct("OOS_Sharpe", anc["OOS_Sharpe"]),
                        pct_MaxDD=pct("MaxDD", anc["MaxDD"]),
                        draw_mDD_p05=d.m_DD.quantile(0.05), draw_mDD_med=d.m_DD.median(),
                        draw_mDD_p95=d.m_DD.quantile(0.95), draw_mDD_sd=d.m_DD.std(),
                        draw_S_p05=d.Sharpe.quantile(0.05), draw_S_med=d.Sharpe.median(),
                        draw_S_p95=d.Sharpe.quantile(0.95), draw_S_sd=d.Sharpe.std(),
                        draw_TO_med=d.TO.median(), draw_TO_p05=d.TO.quantile(0.05),
                        draw_TO_p95=d.TO.quantile(0.95),
                        draws_4b=int(d.p4b.sum()), draws_4a=int(d.p4a.sum()),
                        anchor_4b=bool(anc["H1"] > sp["H1"] and anc["H2"] > sp["H2"]
                                       and anc["OOS_Sharpe"] > sp["OOS_Sharpe"]
                                       and a_mDD >= 0 and a_mC >= 0),
                        anchor_4a=bool(anc["H1"] > bs["H1"] and anc["H2"] > bs["H2"]
                                       and anc["MaxDD"] >= bs["MaxDD"]),
                        SPY_S=sp["Sharpe"], SPY_CAGR=sp["CAGR"], SPY_DD=sp["MaxDD"],
                        SPY_H1=sp["H1"], SPY_H2=sp["H2"], SPY_OOS_S=sp["OOS_Sharpe"],
                        SPY_OOS_CAGR=sp["OOS_CAGR"],
                        BASE_S=bs["Sharpe"], BASE_CAGR=bs["CAGR"], BASE_DD=bs["MaxDD"],
                        BASE_OOS_S=bs["OOS_Sharpe"], BASE_OOS_CAGR=bs["OOS_CAGR"]))
                    # ---- RULE 8: two legal IS-only choosers, OOS read once
                    for cname, col in (("C_SHARPE", "IS_Sharpe"), ("C_DD", "IS_mDD")):
                        pick = d.loc[d[col].idxmax()]
                        wf.append(dict(panel=panel, null_shape=shape, alpha=alpha, ndraws=nd, cost_bps=cost,
                                       chooser=cname, draw=int(pick["draw"]),
                                       IS_stat=pick[col],
                                       OOS_CAGR=pick["OOS_CAGR"], OOS_Sharpe=pick["OOS_Sharpe"],
                                       OOS_MaxDD=pick["OOS_MaxDD"],
                                       OOS_S_pctile=float((d.OOS_Sharpe < pick["OOS_Sharpe"]).mean() * 100),
                                       OOS_DD_pctile=float((d.OOS_MaxDD < pick["OOS_MaxDD"]).mean() * 100),
                                       beats_anchor_OOS_S=bool(pick["OOS_Sharpe"] > anc["OOS_Sharpe"]),
                                       anchor_OOS_S=anc["OOS_Sharpe"], anchor_OOS_CAGR=anc["OOS_CAGR"],
                                       anchor_OOS_DD=anc["OOS_MaxDD"],
                                       BASE_OOS_S=bs["OOS_Sharpe"], SPY_OOS_S=sp["OOS_Sharpe"],
                                       BASE_OOS_CAGR=bs["OOS_CAGR"], SPY_OOS_CAGR=sp["OOS_CAGR"],
                                       p4a=bool(pick["p4a"]), p4b=bool(pick["p4b"])))
                if cost == 10.0:
                    dd = DF.copy(); dd.insert(0, "alpha", alpha); dd.insert(0, "null_shape", shape)
                    dd.insert(0, "panel", panel)
                    draws_out.append(dd)

        # ---- G3 determinism
        rng = np.random.default_rng(seed_of(panel, SHAPES[0], ALPHAS[0], 0))
        chk = rng.gamma(ALPHAS[0], size=(3, n))[0, 0]
        rng2 = np.random.default_rng(seed_of(panel, SHAPES[0], ALPHAS[0], 0))
        say(f"[G3] {panel}: md5-seeded re-draw reproduces bit-for-bit: "
            f"{chk == rng2.gamma(ALPHAS[0], size=(3, n))[0, 0]}")

    G = pd.DataFrame(grid); WF = pd.DataFrame(wf); DR = pd.concat(draws_out, ignore_index=True)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    DR.to_csv(OUT / f"{STEM}.draws.csv", index=False)
    say(f"[G5] {len(G)} of {len(PANELS)*len(SHAPES)*len(ALPHAS)*len(NDRAWS)*len(COSTS)} cells published.\n")
    say("[G6] turnover match, 200 draws (x/yr):")
    say(G[G.ndraws == NMAX].groupby(["panel", "null_shape"])
        .agg(anchor_TO=("anchor_TO", "first"), draw_TO_med=("draw_TO_med", "median"),
             draw_TO_p05=("draw_TO_p05", "min"), draw_TO_p95=("draw_TO_p95", "max"))
        .to_string(float_format=lambda x: f"{x:.3f}"))
    say("")

    say("=" * 128)
    say("ALL 240 CELLS -- the anchor's percentile inside its own re-sizing null "
        "(pct_X = % of draws BELOW the anchor; 50 = dead axis)")
    say("=" * 128)
    say(G[["panel", "null_shape", "alpha", "ndraws", "cost_bps", "anchor_Sharpe", "anchor_MaxDD", "anchor_mDD",
           "pct_mDD", "pct_MaxDD", "pct_Sharpe", "pct_CAGR", "pct_OOS_S",
           "draw_mDD_p05", "draw_mDD_med", "draw_mDD_p95", "draw_mDD_sd",
           "draw_S_med", "draw_S_sd", "draw_TO_med", "draws_4b", "draws_4a",
           "anchor_4b", "anchor_4a"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("")
    say("BENCHMARKS (same sample, per panel per cost rung)")
    say(G[["panel", "cost_bps", "anchor_CAGR", "anchor_Sharpe", "anchor_MaxDD", "anchor_H1",
           "anchor_H2", "anchor_OOS_CAGR", "anchor_OOS_S", "anchor_TO",
           "BASE_CAGR", "BASE_S", "BASE_OOS_S", "SPY_CAGR", "SPY_S", "SPY_DD",
           "SPY_H1", "SPY_H2", "SPY_OOS_CAGR", "SPY_OOS_S"]].drop_duplicates()
        .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    say("")
    say("=" * 128)
    say("RULE 8 WALK-FORWARD (chooser sees 2009-2016 ONLY; 2017-2026 read once)")
    say("=" * 128)
    say(WF[(WF.ndraws == NMAX) & (WF.null_shape == "PERS")][["panel", "alpha", "cost_bps", "chooser", "draw", "OOS_CAGR",
                               "OOS_Sharpe", "OOS_MaxDD", "OOS_S_pctile", "OOS_DD_pctile",
                               "anchor_OOS_S", "anchor_OOS_CAGR", "BASE_OOS_S", "SPY_OOS_S",
                               "beats_anchor_OOS_S", "p4a", "p4b"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say("")

    say("=" * 128)
    say("HYPOTHESES")
    say("=" * 128)
    for panel in PANELS:
        g = G[(G.panel == panel) & (G.ndraws == NMAX) & (G.cost_bps == 10.0) & (G.null_shape == "PERS")]
        say(f"H1  {panel} @10 bps, 200 draws: the anchor's 4b DD margin sits at percentile "
            + " / ".join(f"a={a:g}:{v:.1f}" for a, v in zip(g.alpha, g.pct_mDD)) + " of the null.")
        say(f"H2  {panel} @10 bps: the null's own DD-margin spread (p05..p95 pp) is "
            + " / ".join(f"a={a:g}:[{lo:.2f},{hi:.2f}]" for a, lo, hi
                         in zip(g.alpha, g.draw_mDD_p05, g.draw_mDD_p95)) + f"; anchor {g.anchor_mDD.iloc[0]:.2f} pp.")
        say(f"H3  {panel} @10 bps: the anchor's SHARPE percentile is "
            + " / ".join(f"a={a:g}:{v:.1f}" for a, v in zip(g.alpha, g.pct_Sharpe)) + ".")
    say("")
    gg = G[(G.ndraws == NMAX) & (G.null_shape == "PERS")]
    say(f"H4  over all {len(gg)} (panel x alpha x cost) cells at 200 draws: median anchor DD-margin "
        f"percentile {gg.pct_mDD.median():.1f}, range [{gg.pct_mDD.min():.1f}, {gg.pct_mDD.max():.1f}]; "
        f"median anchor Sharpe percentile {gg.pct_Sharpe.median():.1f} "
        f"[{gg.pct_Sharpe.min():.1f}, {gg.pct_Sharpe.max():.1f}].")
    say(f"H5  4b passage: the anchor clears 4b in {int(gg.anchor_4b.sum())} of {len(gg)} cells; the "
        f"draws clear it in {int(gg.draws_4b.sum())} of {int(gg.ndraws.sum())} draw-cells "
        f"({gg.draws_4b.sum()/gg.ndraws.sum():.1%}).  4a: anchor {int(gg.anchor_4a.sum())} of {len(gg)}, "
        f"draws {gg.draws_4a.sum()/gg.ndraws.sum():.1%}.")
    w = WF[(WF.ndraws == NMAX) & (WF.null_shape == "PERS")]
    for c in ("C_SHARPE", "C_DD"):
        s = w[w.chooser == c]
        say(f"H6  rule 8 / {c}: the IS-only pick lands at OOS Sharpe percentile median "
            f"{s.OOS_S_pctile.median():.1f} (mean {s.OOS_S_pctile.mean():.1f}) and beats the ANCHOR's "
            f"OOS Sharpe in {int(s.beats_anchor_OOS_S.sum())} of {len(s)} cells; "
            f"{int(s.p4b.sum())} of {len(s)} picks clear 4b, {int(s.p4a.sum())} clear 4a.")
    key = ["panel", "null_shape", "alpha", "cost_bps"]
    say(f"H7  resolution: moving 50 -> 200 draws moves the anchor's DD percentile by a median of "
        f"{(G[G.ndraws==200].set_index(key).pct_mDD - G[G.ndraws==50].set_index(key).pct_mDD).abs().median():.1f} points.")
    ii = G[(G.ndraws == NMAX) & (G.null_shape == 'IID')]
    say(f"H8  THE CONFOUND, quantified: the IID (not turnover-matched) null trades a median "
        f"{ii.draw_TO_med.median():.2f}x/yr against the anchor's {ii.anchor_TO.iloc[0]:.2f}x, and its "
        f"anchor DD percentile reads median {ii.pct_mDD.median():.1f} / Sharpe {ii.pct_Sharpe.median():.1f}. "
        f"At the 0 bps rung, where the confound cannot bite, IID reads DD "
        f"{ii[ii.cost_bps==0].pct_mDD.median():.1f} / Sharpe {ii[ii.cost_bps==0].pct_Sharpe.median():.1f}.")

    (OUT / f"{STEM}.log.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
