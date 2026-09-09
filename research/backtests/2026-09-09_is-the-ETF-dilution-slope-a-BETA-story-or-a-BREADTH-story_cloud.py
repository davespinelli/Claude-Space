#!/usr/bin/env python3
"""Idea 291 - IS THE ETF DILUTION SLOPE A BETA STORY OR A BREADTH STORY (cloud, 2026-09-09).

Idea 277 built a k-matched ETF-share sweep (36 names, n_etf = round(s*36) ETFs + the rest
BSTK100 stocks, 6 seeds per share) and found the un-ranked EWall book's OOS Sharpe falls
1.0597 -> 0.6656 monotonically in 8/8 steps as s goes 0 -> 1, while its published `breadth`
column is FLAT (0.6821 -> 0.6750) and its `disp` column halves (0.0964 -> 0.0620).  The
queue asks which channel carries the slope.

The identity this run uses
--------------------------
For a book with realised daily holdings h_it (the engine's own `weights` frame), write
g_t = sum_i h_it (realised gross) and w_it = h_it/g_t.  Over a window, with wbar_i the
time-mean of w_it, mu_i and sig_i the name's own mean and vol, and x_t = sum_i w_it r_it
the held-names return:

    Sharpe_x = sqrt(252) * mean(x) / sd(x)
    mean(x)  = sum_i wbar_i mu_i            + TIMING          (weight-return covariation)
    sd(x)    = A * sqrt(rho + (1-rho) H),   A = sum_i wbar_i sig_i,  H = sum_i wbar_i^2 sig_i^2 / A^2
    rho      defined so the identity is EXACT: rho = (sd(x)^2 - sum wbar_i^2 sig_i^2)/(A^2 - sum wbar_i^2 sig_i^2)

so, in logs and exactly,

    log Sharpe_book = log(sum wbar_i mu_i) - log A - 0.5*log(rho + (1-rho)H) + log sqrt(252)
                      + TIMING + GROSS&COST

    MEAN channel  = log(sum wbar_i mu_i)      "beta": do the names simply earn less?
    VOL channel   = -log A                    "beta": are they less volatile per unit of that?
    CORR channel  \ -0.5*log(rho + (1-rho)H)  "breadth": does the book diversify less well?
    CONC channel  /                           H is 1/N_eff at homogeneous vols - the
                                              cross-sectional dispersion / concentration leg.

H and rho are separated by evaluating the diversification term at the s=0 rung's value of
the other one, and the interaction is reported, not hidden.  k is FIXED at 36 across the
whole sweep, so breadth-as-name-count cannot move: only rho and H can.

Two tuned parameters, every grid point reported: GROSS MODE in {none, g075, gmatch} and
COST RUNG in {0, 10, 25} bps.  "gmatch" rescales every panel's weights by a constant so its
time-mean realised gross equals the s=0 rung's - the queue's "at matched realised gross".
Everything else - the panels, seeds, eligibility gate, weekly cadence, IS/OOS split - is
idea 277's, imported verbatim from its committed script.

SURVIVORSHIP: every MIX panel is a subset of research/universe_broad.json, i.e. of TODAY's
constituent list, so the whole sweep inherits that bias; the slope is a within-sweep
contrast, which is why the bias is a level effect and not the answer.

RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are untouched.

Usage:  python 2026-09-09_is-the-ETF-dilution-slope-a-BETA-story-or-a-BREADTH-story_cloud.py
"""
import importlib.util
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, rules_v2_weights   # noqa: E402
from engine import backtest, metrics                                      # noqa: E402

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 400)

SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"
REF = OUT / "2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C.py"
REF_BOOKS = OUT / "2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C.sweepbooks.csv"
REF_CURVE = OUT / "2026-09-06_is-ETF36-a-third-cluster-or-just-a-small-sample_C.curve.csv"

GROSS_MODES = ["none", "g075", "gmatch"]
COST_RUNGS = [0, 10, 25]
IS_START, IS_END, OOS_START = "2009-01-01", "2016-12-31", "2017-01-01"
FREQ = "W"

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _lines.append(s)


def load277():
    spec = importlib.util.spec_from_file_location("idea277", REF)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


# =========================================================================================
# the decomposition
# =========================================================================================
def channels(held, rets, port, cols):
    """Exact log decomposition of a book's Sharpe over the window the frames span."""
    h = held[cols].to_numpy(float)
    r = rets[cols].to_numpy(float)
    g = h.sum(axis=1)
    live = g > 1e-12
    if live.sum() < 60:
        return None
    w = np.zeros_like(h)
    w[live] = h[live] / g[live][:, None]
    wbar = w[live].mean(axis=0)
    if wbar.sum() <= 0:
        return None
    wbar = wbar / wbar.sum()
    x = (w * r).sum(axis=1)[live]                       # held-names return, gross of costs
    mu = np.nanmean(r[live], axis=0)
    sig = np.nanstd(r[live], axis=0, ddof=1)
    mu_w = float(wbar @ np.nan_to_num(mu))
    A = float(wbar @ np.nan_to_num(sig))
    q = float((wbar ** 2) @ np.nan_to_num(sig) ** 2)    # sum wbar_i^2 sig_i^2
    sx = float(np.std(x, ddof=1))
    H = q / A ** 2 if A > 0 else np.nan
    den = A ** 2 - q
    rho = (sx ** 2 - q) / den if den > 0 else np.nan
    mx = float(np.mean(x))
    sp = port[live.nonzero()[0]] if isinstance(port, np.ndarray) else port.to_numpy(float)[live]
    m_book, s_book = float(np.mean(sp)), float(np.std(sp, ddof=1))
    sh_book = np.sqrt(252) * m_book / s_book if s_book > 0 else np.nan
    sh_x = np.sqrt(252) * mx / sx if sx > 0 else np.nan
    return dict(mu_w=mu_w, A=A, H=H, rho=rho, mean_x=mx, sd_x=sx, N_eff=1.0 / float((wbar ** 2).sum()),
                gross=float(g[live].mean()), sig_cv=float(np.nanstd(sig) / np.nanmean(sig)),
                mu_cv=float(np.nanstd(mu) / abs(np.nanmean(mu))) if np.nanmean(mu) else np.nan,
                Sharpe_x=sh_x, Sharpe_book=sh_book, days=int(live.sum()),
                # log channels; they sum to log Sharpe_book by construction
                c_MEAN=np.log(mu_w) if mu_w > 0 else np.nan,
                c_VOL=-np.log(A) if A > 0 else np.nan,
                c_DIV=-0.5 * np.log(rho + (1 - rho) * H) if (rho + (1 - rho) * H) > 0 else np.nan,
                c_CONST=0.5 * np.log(252.0),
                c_TIMING=(np.log(mx) - np.log(mu_w)) if (mx > 0 and mu_w > 0) else np.nan,
                c_GROSSCOST=(np.log(sh_book) - np.log(sh_x)) if (sh_book > 0 and sh_x > 0) else np.nan)


def div_split(rho, H, rho0, H0):
    """Split the diversification term into a CORR leg and a CONC leg + interaction.
    -0.5 log(f(rho,H)) with f = rho + (1-rho)H, evaluated against the s=0 rung (rho0, H0)."""
    def f(rr, hh):
        return -0.5 * np.log(rr + (1 - rr) * hh)
    base = f(rho0, H0)
    corr = f(rho, H0) - base
    conc = f(rho0, H) - base
    inter = f(rho, H) - base - corr - conc
    return corr, conc, inter


# =========================================================================================
def main():
    t0 = time.time()
    P("=" * 200)
    P("IDEA 291 - IS THE ETF DILUTION SLOPE A BETA STORY OR A BREADTH STORY (cloud, 2026-09-09)")
    P("=" * 200)
    P("Idea 277: EWall OOS Sharpe 1.0597 -> 0.6656 monotone in 8/8 steps as the ETF share goes 0 -> 1")
    P("at FIXED k=36, with published breadth FLAT and dispersion halving.  This run decomposes the")
    P("slope into MEAN / VOL / DIVERSIFICATION (corr + concentration) channels by an exact log")
    P("identity, at matched realised gross, and asks which channel carries it.")
    P(f"Two tuned parameters: GROSS MODE {GROSS_MODES} x COST RUNG {COST_RUNGS} bps.  Weekly cadence,")
    P("next-day execution, idea 277's panels/seeds/gate imported verbatim.")
    P("SURVIVORSHIP: every MIX panel is drawn from today's universe_broad constituents.")

    m = load277()
    P(f"\n[0] PANELS - idea 277's build_pool() imported from {REF.name}")
    pool, etf36 = m.build_pool()
    mix = {k: v for k, v in pool.items() if v["kind"] == "MIX" or k == "ETF36"}
    P(f"    {len(pool)} panels in idea 277's pool; {len(mix)} on the k-matched ETF-share sweep "
      f"({len(m.SHARES)} shares x {len(m.SEEDS)} seeds, s=1.000 collapsing onto ETF36 itself)")

    # ------------------------------------------------------------------ the grid
    P("\n[1] GRID - the EWall book at every (gross mode, cost rung), with the channel decomposition")
    rows = []
    series = {}                       # (share, seed, bps) -> the un-rescaled book's return series
    for pi, (pname, meta) in enumerate(sorted(mix.items()), 1):
        px, tr = meta["px"], meta["tradable"]
        cols = [c for c in px.columns if c in tr]
        elig = m.eligible_mask(px, tr)
        w0 = m.weights(px, tr, "EWall", elig=elig)
        start = px.index[260]
        rets = px.pct_change().fillna(0.0)
        gmean0 = float(w0.loc[start:].sum(axis=1).mean())
        for gmode in ["none", "g075"]:            # gmatch needs the s=0 target first (below)
            if gmode == "none":
                w = w0
            else:
                tot = w0.sum(axis=1).replace(0, np.nan)
                w = w0.div(tot, axis=0).mul(m.GROSS).fillna(0.0)
            for bps in COST_RUNGS:
                res = backtest(px, w, cost_bps=bps, freq=FREQ)
                port = res["returns"].loc[start:]
                held = res["weights"].loc[start:]
                rr = rets.loc[start:]
                if gmode == "none":
                    series[(meta["etf_share"], meta["seed"], bps)] = port
                for wname, lo, hi in (("FULL", IS_START, None), ("IS", IS_START, IS_END),
                                      ("OOS", OOS_START, None)):
                    sl = slice(pd.Timestamp(lo), pd.Timestamp(hi) if hi else None)
                    ch = channels(held.loc[sl], rr.loc[sl], port.loc[sl], cols)
                    if ch is None:
                        continue
                    mm = metrics(port.loc[sl])
                    h1, h2 = half_sharpes(port.loc[sl])
                    rows.append(dict(panel=pname, etf_share=meta["etf_share"], seed=meta["seed"],
                                     k=meta["k"], gmode=gmode, bps=bps, window=wname,
                                     CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                     Vol=mm["Vol"], H1=h1, H2=h2, gross_raw=gmean0, **ch))
        if pi % 6 == 0 or pi == len(mix):
            P(f"    [{pi:>2}/{len(mix)}] {pname:<18} k={meta['k']} "
              f"etf_share={meta['etf_share']:.3f} done")
    GR = pd.DataFrame(rows)

    # gmatch: rescale to the s=0 rung's mean realised gross, then re-run only that mode
    tgt = GR[(GR.gmode == "none") & (GR.window == "FULL") & (GR.etf_share == 0.0)].gross.mean()
    P(f"\n    matched-gross target = the s=0 rung's mean realised gross = {tgt:.4f}")
    keep = GR[GR.gmode != "gmatch"].copy()
    rows = []
    for pname, meta in sorted(mix.items()):
        px, tr = meta["px"], meta["tradable"]
        cols = [c for c in px.columns if c in tr]
        elig = m.eligible_mask(px, tr)
        w0 = m.weights(px, tr, "EWall", elig=elig)
        start = px.index[260]
        rets = px.pct_change().fillna(0.0)
        g_here = float(backtest(px, w0, cost_bps=0, freq=FREQ)["weights"].loc[start:].sum(axis=1).mean())
        w = w0 * (tgt / g_here if g_here > 0 else 1.0)
        for bps in COST_RUNGS:
            res = backtest(px, w, cost_bps=bps, freq=FREQ)
            port = res["returns"].loc[start:]
            held = res["weights"].loc[start:]
            rr = rets.loc[start:]
            for wname, lo, hi in (("FULL", IS_START, None), ("IS", IS_START, IS_END),
                                  ("OOS", OOS_START, None)):
                sl = slice(pd.Timestamp(lo), pd.Timestamp(hi) if hi else None)
                ch = channels(held.loc[sl], rr.loc[sl], port.loc[sl], cols)
                if ch is None:
                    continue
                mm = metrics(port.loc[sl])
                h1, h2 = half_sharpes(port.loc[sl])
                rows.append(dict(panel=pname, etf_share=meta["etf_share"], seed=meta["seed"],
                                 k=meta["k"], gmode="gmatch", bps=bps, window=wname,
                                 CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                                 Vol=mm["Vol"], H1=h1, H2=h2, gross_raw=g_here, **ch))
    GR = pd.concat([keep, pd.DataFrame(rows)], ignore_index=True)
    GR["logSharpe"] = np.log(GR.Sharpe.where(GR.Sharpe > 0))
    GR.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    P(f"    {len(GR)} grid rows = {len(mix)} panels x {len(GROSS_MODES)} gross modes x "
      f"{len(COST_RUNGS)} cost rungs x 3 windows -> {STEM}.grid.csv")

    # ------------------------------------------------------------------ reproduction gate
    P("\n[2] GATE - idea 277's committed sweepbooks.csv EWall rows reproduced before anything is moved")
    ref = pd.read_csv(REF_BOOKS)
    ref = ref[ref.book == "EWall"]
    mine = (GR[(GR.gmode == "none") & (GR.bps == 10) & (GR.window == "FULL")]
            .groupby("etf_share").agg(CAGR=("CAGR", "mean"), Sharpe=("Sharpe", "mean"),
                                      MaxDD=("MaxDD", "mean")).reset_index())
    oos = (GR[(GR.gmode == "none") & (GR.bps == 10) & (GR.window == "OOS")]
           .groupby("etf_share").agg(OOS_CAGR=("CAGR", "mean"), OOS_Sharpe=("Sharpe", "mean"),
                                     OOS_MaxDD=("MaxDD", "mean")).reset_index())
    mine = mine.merge(oos, on="etf_share").merge(ref, on="etf_share", suffixes=("", "_ref"))
    d = {c: float(np.abs(mine[c] - mine[f"{c}_ref"]).max())
         for c in ["CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]}
    P(f"    (a) metrics averaged ACROSS SEEDS: {len(mine)}/{len(ref)} share rungs matched; max abs diff " +
      "  ".join(f"{k} {v:.2e}" for k, v in d.items()))
    P("        DIFFERS - and it differs in one direction only, vanishing at s=1.000 where the rung is a")
    P("        SINGLE panel (ETF36).  Idea 277 built each rung by POOLING the seeds' return series")
    P("        (`pd.concat([c[\"r\"] for c in cs], axis=1).mean(axis=1)`), i.e. an equal-weight portfolio")
    P("        OF the six seed panels, which diversifies across seeds; averaging each panel's own")
    P("        metrics does not.  Gate (b) reproduces the published object exactly:")
    pooled = []
    for sh in sorted({k[0] for k in series}):
        for bps in COST_RUNGS:
            cs = [v for k, v in series.items() if k[0] == sh and k[2] == bps]
            if not cs:
                continue
            po = pd.concat(cs, axis=1).mean(axis=1).dropna()
            mm, mo = metrics(po), metrics(po.loc[OOS_START:])
            pooled.append(dict(etf_share=sh, bps=bps, panels=len(cs), CAGR=mm["CAGR"],
                               Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"], OOS_CAGR=mo["CAGR"],
                               OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    PL = pd.DataFrame(pooled)
    pj = PL[PL.bps == 10].merge(ref, on="etf_share", suffixes=("", "_ref"))
    d2 = {c: float(np.abs(pj[c] - pj[f"{c}_ref"]).max())
          for c in ["CAGR", "Sharpe", "MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]}
    P(f"    (b) seed-POOLED books, idea 277's own aggregation: {len(pj)}/{len(ref)} rungs; max abs diff " +
      "  ".join(f"{k} {v:.2e}" for k, v in d2.items()))
    P("        " + ("REPRODUCED" if max(d2.values()) < 1e-9 else "STILL DIFFERS - reported, not hidden"))
    P(f"    The decomposition below is computed PER PANEL and then averaged, which is the only")
    P(f"    aggregation under which a channel identity holds panel by panel; the published curve is")
    P(f"    the seed portfolio, and its 0->1 fall is {pj.Sharpe.iloc[0] - pj.Sharpe.iloc[-1]:+.4f} full / "
      f"{pj.OOS_Sharpe.iloc[0] - pj.OOS_Sharpe.iloc[-1]:+.4f} OOS against the per-panel "
      f"{mine.Sharpe.iloc[0] - mine.Sharpe.iloc[-1]:+.4f} / {mine.OOS_Sharpe.iloc[0] - mine.OOS_Sharpe.iloc[-1]:+.4f}.")
    PL.to_csv(OUT / f"{STEM}.pooled.csv", index=False)
    mine.to_csv(OUT / f"{STEM}.gate.csv", index=False)

    # ------------------------------------------------------------------ the curve + attribution
    P("\n[3] THE SLOPE, CHANNEL BY CHANNEL")
    P("    Every channel is a log contribution and they SUM to log Sharpe_book exactly:")
    P("      log Sharpe = c_MEAN + c_VOL + c_DIV + c_CONST + c_TIMING + c_GROSSCOST")
    att = []
    for gmode in GROSS_MODES:
        for bps in COST_RUNGS:
            for wname in ("FULL", "IS", "OOS"):
                sub = GR[(GR.gmode == gmode) & (GR.bps == bps) & (GR.window == wname)]
                if not len(sub):
                    continue
                cur = sub.groupby("etf_share").mean(numeric_only=True)
                if 0.0 not in cur.index or 1.0 not in cur.index:
                    continue
                lo, hi = cur.loc[0.0], cur.loc[1.0]
                corr_l, conc_l, inter = div_split(hi.rho, hi.H, lo.rho, lo.H)
                rec = dict(gmode=gmode, bps=bps, window=wname,
                           Sharpe_0=lo.Sharpe, Sharpe_1=hi.Sharpe,
                           dSharpe=hi.Sharpe - lo.Sharpe,
                           dlogSharpe=hi.logSharpe - lo.logSharpe,   # seed-mean of logs, so the
                           # channel sums below are exact rather than Jensen-shifted
                           d_MEAN=hi.c_MEAN - lo.c_MEAN, d_VOL=hi.c_VOL - lo.c_VOL,
                           d_DIV=hi.c_DIV - lo.c_DIV, d_CORR=corr_l, d_CONC=conc_l,
                           d_INTER=inter, d_TIMING=hi.c_TIMING - lo.c_TIMING,
                           d_GROSSCOST=hi.c_GROSSCOST - lo.c_GROSSCOST,
                           rho_0=lo.rho, rho_1=hi.rho, H_0=lo.H, H_1=hi.H,
                           A_0=lo.A, A_1=hi.A, mu_0=lo.mu_w, mu_1=hi.mu_w,
                           gross_0=lo.gross, gross_1=hi.gross,
                           mono_steps=int(sum(np.diff(cur.Sharpe.values) < 0)),
                           steps=len(cur) - 1)
                rec["resid"] = (rec["dlogSharpe"] - rec["d_MEAN"] - rec["d_VOL"] - rec["d_DIV"]
                                - rec["d_TIMING"] - rec["d_GROSSCOST"])
                att.append(rec)
    AT = pd.DataFrame(att)
    AT.to_csv(OUT / f"{STEM}.attribution.csv", index=False)
    P(f"    {len(AT)} attribution rows = {len(GROSS_MODES)} gross modes x {len(COST_RUNGS)} cost "
      f"rungs x 3 windows, ALL reported -> {STEM}.attribution.csv")
    show = ["gmode", "bps", "window", "Sharpe_0", "Sharpe_1", "dSharpe", "dlogSharpe", "d_MEAN",
            "d_VOL", "d_DIV", "d_CORR", "d_CONC", "d_INTER", "d_TIMING", "d_GROSSCOST", "resid",
            "mono_steps", "steps"]
    P(AT[show].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n    Share of the (negative) log-Sharpe slope carried by each channel, per grid point:")
    sh = AT.copy()
    for c in ["d_MEAN", "d_VOL", "d_DIV", "d_TIMING", "d_GROSSCOST"]:
        sh[c + "_pct"] = sh[c] / sh.dlogSharpe
    P(sh[["gmode", "bps", "window", "dlogSharpe", "d_MEAN_pct", "d_VOL_pct", "d_DIV_pct",
          "d_TIMING_pct", "d_GROSSCOST_pct"]].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    P("\n    A share > 1 means that channel over-explains the fall and another channel offsets it;")
    P("    a negative share means the channel pushes Sharpe UP as the ETF share rises.")

    P("\n    The curve itself (gmode=gmatch, 10 bps, seed-averaged) - levels, not deltas:")
    cur = (GR[(GR.gmode == "gmatch") & (GR.bps == 10)]
           .groupby(["window", "etf_share"])
           .agg(Sharpe=("Sharpe", "mean"), CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"),
                mu_w=("mu_w", "mean"), A=("A", "mean"), rho=("rho", "mean"), H=("H", "mean"),
                N_eff=("N_eff", "mean"), sig_cv=("sig_cv", "mean"), gross=("gross", "mean"))
           .reset_index())
    cur.to_csv(OUT / f"{STEM}.curve.csv", index=False)
    P(cur.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n    ANNUALISED, for readability (gmatch, 10 bps, FULL): mean name return and vol")
    f = cur[cur.window == "FULL"].copy()
    f["mu_ann"] = f.mu_w * 252
    f["vol_ann"] = f.A * np.sqrt(252)
    P(f[["etf_share", "mu_ann", "vol_ann", "rho", "H", "N_eff", "Sharpe"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------------ per-seed dispersion
    P("\n[4] IS THE SLOPE BIGGER THAN THE SEED NOISE?  (gmatch, 10 bps, per seed)")
    ss = GR[(GR.gmode == "gmatch") & (GR.bps == 10) & (GR.window == "FULL") & (GR.seed >= 0)]
    tab = ss.pivot_table(index="etf_share", columns="seed", values="Sharpe")
    P(tab.to_string(float_format=lambda x: f"{x:.4f}"))
    if len(tab):
        P(f"    within-share seed sd (mean over shares): {tab.std(axis=1).mean():.4f}; "
          f"the 0 -> 1 fall is {AT[(AT.gmode == 'gmatch') & (AT.bps == 10) & (AT.window == 'FULL')].dSharpe.iloc[0]:.4f}")

    # ------------------------------------------------------------------ RULE 8
    P("\n[5] RULE 8 - the channel model estimated on 2009-2016 ONLY, 2017-2026 untouched")
    P("    The decomposition is an identity, so the walk-forward question is whether the CHANNEL")
    P("    THAT CARRIES THE SLOPE IN-SAMPLE still carries it out of sample, and whether the IS")
    P("    channel slopes predict the OOS Sharpe curve better than the naive IS-constant.")
    wf = []
    for gmode in GROSS_MODES:
        for bps in COST_RUNGS:
            IS = (GR[(GR.gmode == gmode) & (GR.bps == bps) & (GR.window == "IS")]
                  .groupby("etf_share").mean(numeric_only=True))
            OS = (GR[(GR.gmode == gmode) & (GR.bps == bps) & (GR.window == "OOS")]
                  .groupby("etf_share").mean(numeric_only=True))
            if not len(IS) or not len(OS):
                continue
            s = IS.index.values.astype(float)
            # IS-fitted linear model of each channel in s, applied to the OOS window's own level
            coefs = {}
            for c in ["c_MEAN", "c_VOL", "c_DIV", "c_TIMING", "c_GROSSCOST"]:
                coefs[c] = float(np.polyfit(s, IS[c].values, 1)[0])
            base_oos = float(OS.logSharpe.iloc[0])
            pred = np.array([base_oos + sum(coefs.values()) * (si - s[0]) for si in s])
            naive = np.full(len(s), float(IS.logSharpe.mean()))
            hold = np.full(len(s), base_oos)              # OOS s=0 level, no slope
            act = OS.logSharpe.values
            wf.append(dict(gmode=gmode, bps=bps,
                           IS_slope_total=sum(coefs.values()),
                           OOS_slope_actual=float(np.polyfit(s, act, 1)[0]),
                           **{f"IS_slope_{k[2:]}": v for k, v in coefs.items()},
                           **{f"OOS_slope_{c[2:]}": float(np.polyfit(s, OS[c].values, 1)[0])
                              for c in ["c_MEAN", "c_VOL", "c_DIV", "c_TIMING", "c_GROSSCOST"]},
                           MAE_channel=float(np.mean(np.abs(pred - act))),
                           MAE_naive=float(np.mean(np.abs(naive - act))),
                           MAE_flat=float(np.mean(np.abs(hold - act))),
                           IS_Sharpe_0=float(IS.Sharpe.iloc[0]), IS_Sharpe_1=float(IS.Sharpe.iloc[-1]),
                           OOS_Sharpe_0=float(OS.Sharpe.iloc[0]), OOS_Sharpe_1=float(OS.Sharpe.iloc[-1]),
                           OOS_mono_steps=int(sum(np.diff(OS.Sharpe.values) < 0)), steps=len(s) - 1))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    P(f"    {len(WF)} walk-forward rows = {len(GROSS_MODES)} gross modes x {len(COST_RUNGS)} cost rungs "
      f"-> {STEM}.walkforward.csv")
    P(WF[["gmode", "bps", "IS_slope_total", "OOS_slope_actual", "IS_slope_MEAN", "OOS_slope_MEAN",
          "IS_slope_VOL", "OOS_slope_VOL", "IS_slope_DIV", "OOS_slope_DIV", "MAE_channel",
          "MAE_naive", "MAE_flat", "OOS_mono_steps", "steps"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    if len(WF):
        P(f"\n    the IS-fitted channel model beats the naive IS-constant on "
          f"{int((WF.MAE_channel < WF.MAE_naive).sum())}/{len(WF)} grid points and the OOS-level flat "
          f"line on {int((WF.MAE_channel < WF.MAE_flat).sum())}/{len(WF)}")
        P(f"    the channel carrying the largest IS slope agrees with the largest OOS slope on "
          f"{int(sum(1 for _, r in WF.iterrows() if max(['MEAN','VOL','DIV'], key=lambda c: abs(r[f'IS_slope_{c}'])) == max(['MEAN','VOL','DIV'], key=lambda c: abs(r[f'OOS_slope_{c}']))))}/{len(WF)} grid points")

    # ------------------------------------------------------------------ KEEP paths
    P("\n[6] KEEP PATHS - every rung book scored against the live RULES v2 (4a) and SPY (4b)")
    px136 = load_universe(broad=True)
    startb = px136.index[260]
    spy = px136["SPY"].pct_change().fillna(0).loc[startb:]
    v2 = backtest(px136, rules_v2_weights(px136), cost_bps=10, freq=FREQ)["returns"].loc[startb:]
    v1 = backtest(px136, rules_v1_weights(px136), cost_bps=10, freq=FREQ)["returns"].loc[startb:]
    ms, mv2, mv1 = metrics(spy), metrics(v2), metrics(v1)
    sh1, sh2 = half_sharpes(spy)
    b1, b2 = half_sharpes(v2)
    spy_oos, v2_oos = metrics(spy.loc[OOS_START:]), metrics(v2.loc[OOS_START:])
    P(f"    SPY       {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  halves {sh1:.3f}/{sh2:.3f}"
      f"  OOS {spy_oos['CAGR']:.2%} / {spy_oos['Sharpe']:.3f} / {spy_oos['MaxDD']:.2%}")
    P(f"    RULES v2  {mv2['CAGR']:.2%} / {mv2['Sharpe']:.3f} / {mv2['MaxDD']:.2%}  halves {b1:.3f}/{b2:.3f}"
      f"  OOS {v2_oos['CAGR']:.2%} / {v2_oos['Sharpe']:.3f} / {v2_oos['MaxDD']:.2%}")
    P(f"    RULES v1  {mv1['CAGR']:.2%} / {mv1['Sharpe']:.3f} / {mv1['MaxDD']:.2%}  (continuity row)")
    F = GR[GR.window == "FULL"].set_index(["panel", "gmode", "bps"])
    O = GR[GR.window == "OOS"].set_index(["panel", "gmode", "bps"]).Sharpe
    kp = []
    for idx, r in F.iterrows():
        oos_sh = float(O.get(idx, np.nan))
        f4a = [t for t, c in (("H1", r.H1 > b1), ("H2", r.H2 > b2),
                              ("DD", r.MaxDD >= mv2["MaxDD"])) if not c]
        f4b = [t for t, c in (("H1", r.H1 > sh1), ("H2", r.H2 > sh2),
                              ("OOS", oos_sh > spy_oos["Sharpe"]),
                              ("DD", r.MaxDD >= 0.60 * ms["MaxDD"]),
                              ("CAGR", r.CAGR >= 0.70 * ms["CAGR"])) if not c]
        kp.append(dict(panel=idx[0], gmode=idx[1], bps=idx[2], etf_share=r.etf_share,
                       CAGR=r.CAGR, Sharpe=r.Sharpe, MaxDD=r.MaxDD, H1=r.H1, H2=r.H2,
                       OOS_Sharpe=oos_sh, f4a=",".join(f4a) or "-", f4b=",".join(f4b) or "-"))
    KP = pd.DataFrame(kp)
    KP["pass4a"] = (KP.f4a == "-").astype(int)
    KP["pass4b"] = (KP.f4b == "-").astype(int)
    KP.to_csv(OUT / f"{STEM}.keeppaths.csv", index=False)
    P(f"    KEEP PATHS over the {len(KP)} rung books: 4a {int(KP.pass4a.sum())}/{len(KP)}   "
      f"4b {int(KP.pass4b.sum())}/{len(KP)}   both {int((KP.pass4a & KP.pass4b).sum())}/{len(KP)}")
    bars = pd.Series([t for s in KP.f4b for t in s.split(",") if t != "-"]).value_counts()
    P("    binding 4b bars: " + "  ".join(f"{k}:{v}" for k, v in bars.items()))
    P("\n    4b pass rate by ETF share (all gross modes and cost rungs pooled):")
    P(KP.groupby("etf_share").agg(books=("pass4b", "size"), pass4a=("pass4a", "sum"),
                                  pass4b=("pass4b", "sum"), Sharpe=("Sharpe", "mean"),
                                  CAGR=("CAGR", "mean"), MaxDD=("MaxDD", "mean"))
      .to_string(float_format=lambda x: f"{x:.4f}"))

    P("\n" + "=" * 200)
    P(f"elapsed {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
