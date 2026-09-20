#!/usr/bin/env python3
"""Idea 1715 (lane cloud, 2026-09-20): does a VOL-TARGET gross dial give rule 8 something it
can RESOLVE?

1713 measured the record's exposure dial and found it UNRESOLVABLE in sample: IS Sharpe moves
only 0.0015-0.0106 across the WHOLE constant-gross ladder (G 0.30 -> 1.00) against a
leave-one-IS-year-out (LOYO) deletion SD of 0.090-0.248 -- a signal-to-noise ratio of
0.010-0.075 -- while the same ladder moves OOS MaxDD by 10.9-29.2 pp.  The IS argmax landed at
G=1.00 on 3 of 3 panels and the OOS oracle at G=0.30 on 3 of 3: perfect disagreement.  So rule 8
is blind to the one dial that moves the drawdown.

This replaces the CONSTANT-gross dial with a realised-VOL-TARGET path,

    g_t = clip(target_vol / sigma20_t, 0, 1),

where sigma20_t is the annualised 20-day realised vol of the UNLEVERED equal-weight panel
portfolio through yesterday's close -- a quantity that IS observable in sample -- and asks
whether the IS window can now resolve the exposure dial.  Both ladders are run side by side on
the same panels, the same band settings and the same windows, so the comparison is paired.

Dials -- exactly TWO tuned parameters, as the idea specifies:
    c   band width in {NOGATE, 0.00, 0.03, 0.10}   (NOGATE = hold every priced name)
    t   vol target in {0.08 ... 0.30}   (VOLTGT ladder)
        G   constant gross in {0.30 ... 1.00}      (CONSTG control ladder, 1713's own dial)
ALL grid points are reported.

Resolution statistics, per (panel, band, ladder):
    SPREAD    max-min IS Sharpe across the ladder
    LOYO_SD   median over rungs of the SD of IS Sharpe across the 8 leave-one-IS-year-out refits
    RATIO     SPREAD / LOYO_SD            (1713's statistic; >> 1 means the dial is resolvable)
    MARGIN    IS Sharpe of the argmax minus the runner-up
    AGREE     IS argmax rung vs OOS oracle rung, and Spearman(IS Sharpe, OOS Sharpe) over rungs
    DD_SPAN   max-min OOS MaxDD across the ladder (what is at stake if the dial is mis-set)

Rule 8: c and the ladder rung are chosen on 2009-2016 IS rows ONLY (argmax IS Sharpe over the
full 2-parameter grid); 2017-2026 is read ONCE and the chosen book scored on BOTH KEEP paths
against live RULES v2 and SPY.

Panels: U56, B136 and SMALL (the 483-name sub-$2B panel, with the 54 tickers whose
`max_1d_move >= 1.0` in data/small_meta.csv dropped first).  SURVIVORSHIP: all three panels are
CURRENT constituents of their screens, so every absolute level here is optimistic; SMALL is the
worst affected (sub-$2B names that delisted are simply absent).  On SMALL the joined SPY column
is a BENCHMARK only and is never held.
Price-only.  No EDGAR / Form 4 / 8-K / options / spin-offs / live data.

Deterministic, offline, standalone:
    python3 research/backtests/2026-09-20_voltgt-dial-rule8-resolvable_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state  # noqa
from engine import backtest, rebalance_mask  # noqa

T0 = time.time()
COST = 10.0                 # PROTOCOL rule 2
FREQ = "W"                  # live cadence
WARM = 260
IS_END = pd.Timestamp("2016-12-31")
BANDS = [("NOGATE", None), ("c=0.00", 0.00), ("c=0.03", 0.03), ("c=0.10", 0.10)]
T_GRID = (0.08, 0.10, 0.12, 0.14, 0.16, 0.20, 0.25, 0.30)
G_GRID = (0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00)
OUT = Path(__file__).with_suffix("")

# ------------------------------------------------------------------ engine (1730's, gated G1)
def fast_run(px_v, w_v, mask_v, cost_bps=COST):
    n, k = px_v.shape
    rets = np.zeros_like(px_v); rets[1:] = px_v[1:] / px_v[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    w_t = np.zeros_like(w_v); w_t[1:] = w_v[:-1]
    m = np.zeros(n, dtype=bool); m[1:] = mask_v[:-1]
    cur = np.zeros(k); turn = np.zeros(n); port = np.zeros(n); heldg = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            turn[i] = np.abs(w_t[i] - cur).sum(); cur = w_t[i].copy()
        heldg[i] = cur.sum()
        port[i] = (cur * rets[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return port, turn, heldg

def sh(r):
    v = r.std(ddof=1) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan
def mdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1.0).min())
def cagr(r):
    eq = np.cumprod(1.0 + r); y = len(r) / 252.0
    return float(eq[-1] ** (1.0 / y) - 1.0) if y > 0 else np.nan

def keep_4a(r, b, win):
    rw, bw = r[win], b[win]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(bw[:h]) and sh(rw[h:]) > sh(bw[h:]) and mdd(rw) >= mdd(bw))
def keep_4a_1w(r, b, win):
    return bool(sh(r[win]) > sh(b[win]) and mdd(r[win]) >= mdd(b[win]))
def keep_4b(r, s, win):
    rw, sw = r[win], s[win]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(sw[:h]) and sh(rw[h:]) > sh(sw[h:])
                and mdd(rw) >= 0.60 * mdd(sw) and cagr(rw) >= 0.70 * cagr(sw))
def keep_4b_1w(r, s, win):
    rw, sw = r[win], s[win]
    return bool(sh(rw) > sh(sw) and mdd(rw) >= 0.60 * mdd(sw) and cagr(rw) >= 0.70 * cagr(sw))

# ------------------------------------------------------------------------------ the books
def panel_sigma20(px, cols, extra_lag=0):
    """Annualised 20d realised vol of the UNLEVERED equal-weight panel portfolio.

    extra_lag=0 is the RECORD's convention (and the standing KEEP-4b memo's): the value at
    date t uses returns through t's close, and the engine applies the weight decided at t on
    t+1, so nothing is look-ahead.  extra_lag=1 is a STRICTER, staler variant (through t-1)
    that costs one more day of information; it is reported as a convention robustness read,
    not as a correction."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    pr = (ew.shift(1) * sub.pct_change()).sum(axis=1)
    s = pr.rolling(20).std() * np.sqrt(252)
    return s.shift(extra_lag) if extra_lag else s

def build(px, cols, band_c, gross_path):
    """Equal weight over the priced constituents that pass the band, scaled to gross_path.
    De-gross-to-CASH: gated-out weight is never re-spread (the record's convention)."""
    sub = px[cols]
    e = pd.DataFrame(1.0, index=sub.index, columns=sub.columns).where(sub.notna(), 0.0)
    ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    if band_c is not None:
        ew = ew.where(band_state(sub, band_c), 0.0)
    w = ew.mul(gross_path, axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)

def loyo_sd(r, dates, is_mask):
    """SD of IS Sharpe across the 8 leave-one-IS-year-out refits (1713's deletion statistic)."""
    yrs = sorted(set(dates[is_mask].year))
    out = []
    for y in yrs:
        m = is_mask & np.asarray(dates.year != y)
        if m.sum() > 250: out.append(sh(r[m]))
    return float(np.std(out, ddof=1)) if len(out) > 2 else np.nan

def spearman(a, b):
    ra = pd.Series(a).rank(); rb = pd.Series(b).rank()
    return float(ra.corr(rb))

# ----------------------------------------------------------------------------------- main
def panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    small_cols = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return [("U56", px56, list(px56.columns)),                     # live convention: SPY is held
            ("B136", px136, list(px136.columns)),
            ("SMALL", pxs, small_cols)]                            # SPY is benchmark only

def main():
    gates, grid_rows, res_rows, pick_rows = [], [], [], []
    lines = []
    P = lambda s="": (print(s), lines.append(s))

    for pname, px, cols in panels():
        idx = px.index; px_v = px.values.astype(float)
        mask_v = rebalance_mask(idx, FREQ).values
        full = np.zeros(len(idx), dtype=bool); full[WARM:] = True
        IS = full & np.asarray(idx <= IS_END)
        OOS = full & np.asarray(idx > IS_END)

        sc = px.columns.get_loc("SPY")
        spy_r = np.zeros(len(idx)); spy_r[1:] = px_v[1:, sc] / px_v[:-1, sc] - 1.0
        spy_r = np.nan_to_num(spy_r)

        live_w = rules_v2_weights(px[cols], band=0.03, gross=0.75).reindex(columns=px.columns).fillna(0.0)
        live_p, live_t, live_g = fast_run(px_v, live_w.values.astype(float), mask_v)

        if pname == "U56":
            eng = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
            d = float(np.abs(eng[full] - live_p[full]).max())
            gates.append(("G1 U56 fast_run == engine.backtest (RULES v2, FULL)", f"{d:.3e}", d < 1e-12))
            gates.append(("G2 U56 RULES v2 OOS cell",
                          f"{cagr(live_p[OOS]):.2%} / {sh(live_p[OOS]):.4f} / {mdd(live_p[OOS]):.2%}", True))

        sig0 = panel_sigma20(px, cols, 0)
        sig1 = panel_sigma20(px, cols, 1)
        g_vt = {(0, t): (t / sig0.replace(0, np.nan)).clip(upper=1.0).fillna(0.0) for t in T_GRID}
        g_vt.update({(1, t): (t / sig1.replace(0, np.nan)).clip(upper=1.0).fillna(0.0) for t in T_GRID})
        g_cg = {(0, G): pd.Series(G, index=idx) for G in G_GRID}

        # ---- G3: sigma20 at t is a TRAILING 20-day window closing at t (no future returns)
        if pname == "U56":
            e = pd.DataFrame(1.0, index=px[cols].index, columns=cols).where(px[cols].notna(), 0.0)
            ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
            pr = (ew.shift(1) * px[cols].pct_change()).sum(axis=1).values
            k = 800
            manual = float(np.std(pr[k-19:k+1], ddof=1) * np.sqrt(252))
            d = abs(manual - float(sig0.iloc[k]))
            gates.append(("G3 U56 sigma20(t) == trailing std(returns[t-19..t]) (max |diff| at t=800)",
                          f"{d:.3e}", d < 1e-12))
            gates.append(("G4 U56 sigma20 lag-1 variant differs from lag-0 (convention axis is live)",
                          f"{float((sig0 - sig1).abs().max()):.4f}", float((sig0 - sig1).abs().max()) > 0))

        for bname, bc in BANDS:
            for kind, gmap in (("VOLTGT", g_vt), ("CONSTG", g_cg)):
                cur = []
                for (lag, rung), gp in gmap.items():
                    w = build(px, cols, bc, gp)
                    p, to, hg = fast_run(px_v, w.values.astype(float), mask_v)
                    row = dict(panel=pname, band=bname, ladder=kind, rung=rung, sig_lag=lag,
                               mean_gross=float(hg[full].mean()),
                               turn_yr=float(to[full].sum() / (full.sum() / 252)),
                               IS_Sharpe=sh(p[IS]), IS_LOYO_SD=loyo_sd(p, idx, IS),
                               FULL_CAGR=cagr(p[full]), FULL_Sharpe=sh(p[full]), FULL_MaxDD=mdd(p[full]),
                               OOS_CAGR=cagr(p[OOS]), OOS_Sharpe=sh(p[OOS]), OOS_MaxDD=mdd(p[OOS]),
                               keep4a_FULL=keep_4a(p, live_p, full), keep4a_OOS=keep_4a_1w(p, live_p, OOS),
                               keep4b_FULL=keep_4b(p, spy_r, full), keep4b_OOS=keep_4b_1w(p, spy_r, OOS))
                    cur.append((rung, row, p))
                    grid_rows.append(row)

                dall = pd.DataFrame([r for _, r, _ in cur])
                for lag in sorted(dall.sig_lag.unique()):
                  d = dall[dall.sig_lag == lag].reset_index(drop=True)
                  order = list(d.IS_Sharpe.sort_values(ascending=False).index)
                  spread = float(d.IS_Sharpe.max() - d.IS_Sharpe.min())
                  sd = float(np.nanmedian(d.IS_LOYO_SD))
                  margin = float(d.IS_Sharpe.iloc[order[0]] - d.IS_Sharpe.iloc[order[1]])
                  res_rows.append(dict(panel=pname, band=bname, ladder=kind, sig_lag=lag,
                                       IS_argmax=d.rung.iloc[order[0]],
                                       OOS_oracle=d.rung.iloc[int(d.OOS_Sharpe.idxmax())],
                                       SPREAD=spread, LOYO_SD=sd, RATIO=spread / sd if sd else np.nan,
                                       MARGIN=margin, MARGIN_over_SD=margin / sd if sd else np.nan,
                                       RHO_IS_OOS=spearman(d.IS_Sharpe, d.OOS_Sharpe),
                                       DD_SPAN_pp=float((d.OOS_MaxDD.max() - d.OOS_MaxDD.min()) * 100),
                                       n4b_OOS=int(d.keep4b_OOS.sum()), n_rungs=len(d)))


        # ------------------------------------------------- rule 8: joint IS-only pick of (c, rung)
        gp_df = pd.DataFrame(grid_rows)
        gp_df = gp_df[gp_df.panel == pname]
        for kind, lag in (("VOLTGT", 0), ("VOLTGT", 1), ("CONSTG", 0)):
            d = gp_df[(gp_df.ladder == kind) & (gp_df.sig_lag == lag)]
            best = d.loc[d.IS_Sharpe.idxmax()]
            bc = dict(BANDS)[best.band]
            gpath = (g_vt if kind == "VOLTGT" else g_cg)[(lag, best.rung)]
            w = build(px, cols, bc, gpath)
            p, to, hg = fast_run(px_v, w.values.astype(float), mask_v)
            oracle = d.loc[d.OOS_Sharpe.idxmax()]
            pick_rows.append(dict(panel=pname, ladder=kind, sig_lag=lag,
                                  pick_band=best.band, pick_rung=best.rung,
                                  IS_Sharpe=best.IS_Sharpe,
                                  OOS_CAGR=cagr(p[OOS]), OOS_Sharpe=sh(p[OOS]), OOS_MaxDD=mdd(p[OOS]),
                                  FULL_CAGR=cagr(p[full]), FULL_Sharpe=sh(p[full]), FULL_MaxDD=mdd(p[full]),
                                  mean_gross=float(hg[full].mean()),
                                  turn_yr=float(to[full].sum() / (full.sum() / 252)),
                                  keep4a_FULL=keep_4a(p, live_p, full), keep4a_OOS=keep_4a_1w(p, live_p, OOS),
                                  keep4b_FULL=keep_4b(p, spy_r, full), keep4b_OOS=keep_4b_1w(p, spy_r, OOS),
                                  oracle_band=oracle.band, oracle_rung=oracle.rung,
                                  oracle_OOS_Sharpe=oracle.OOS_Sharpe,
                                  regret=float(oracle.OOS_Sharpe - sh(p[OOS])),
                                  base_OOS_CAGR=cagr(live_p[OOS]), base_OOS_Sharpe=sh(live_p[OOS]),
                                  base_OOS_MaxDD=mdd(live_p[OOS]),
                                  base_FULL_CAGR=cagr(live_p[full]), base_FULL_Sharpe=sh(live_p[full]),
                                  base_FULL_MaxDD=mdd(live_p[full]),
                                  spy_OOS_CAGR=cagr(spy_r[OOS]), spy_OOS_Sharpe=sh(spy_r[OOS]),
                                  spy_OOS_MaxDD=mdd(spy_r[OOS]),
                                  spy_FULL_CAGR=cagr(spy_r[full]), spy_FULL_Sharpe=sh(spy_r[full]),
                                  spy_FULL_MaxDD=mdd(spy_r[full])))
        print(f"[{pname}] done {time.time()-T0:.0f}s")

    G = pd.DataFrame(grid_rows); R = pd.DataFrame(res_rows); K = pd.DataFrame(pick_rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    R.to_csv(f"{OUT}.resolution.csv", index=False)
    K.to_csv(f"{OUT}.picks.csv", index=False)

    # -------------------------------------------------------------------------- report
    P("# Idea 1715 — does a VOL-TARGET gross dial give rule 8 something it can RESOLVE?")
    P()
    P(f"{len(G)} books: 3 panels x {len(BANDS)} bands x (VOLTGT at 2 sigma conventions + CONSTG) "
      f"x {len(T_GRID)} rungs. "
      f"{COST:.0f} bps, weekly, t+1. Survivorship: current constituents (SMALL worst affected).")
    P()
    P("## The answer, in one table: is the exposure dial resolvable in sample?")
    P()
    P("| panel | band | ladder | sigma lag | IS argmax | OOS oracle | SPREAD | LOYO_SD | RATIO | "
      "MARGIN | MARGIN/SD | rho(IS,OOS) | OOS MaxDD span (pp) | 4b OOS passes |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for _, r in R.sort_values(["panel", "ladder", "sig_lag", "band"]).iterrows():
        rg = f"{r.IS_argmax:.2f}" if isinstance(r.IS_argmax, float) else str(r.IS_argmax)
        og = f"{r.OOS_oracle:.2f}" if isinstance(r.OOS_oracle, float) else str(r.OOS_oracle)
        P(f"| {r.panel} | {r.band} | {r.ladder} | {r.sig_lag} | {rg} | {og} | {r.SPREAD:.4f} | {r.LOYO_SD:.4f} | "
          f"{r.RATIO:.3f} | {r.MARGIN:.4f} | {r.MARGIN_over_SD:.4f} | {r.RHO_IS_OOS:+.3f} | "
          f"{r.DD_SPAN_pp:.1f} | {r.n4b_OOS}/{r.n_rungs} |")
    P()
    P("| ladder (sigma lag) | cells | mean SPREAD | mean LOYO_SD | mean RATIO | mean MARGIN/SD | "
      "mean rho(IS,OOS) | mean OOS DD span (pp) | 4b OOS passes |")
    P("|---|---|---|---|---|---|---|---|---|")
    for kind, lag in (("VOLTGT", 0), ("VOLTGT", 1), ("CONSTG", 0)):
        d = R[(R.ladder == kind) & (R.sig_lag == lag)]
        P(f"| {kind} (lag {lag}) | {len(d)} | {d.SPREAD.mean():.4f} | {d.LOYO_SD.mean():.4f} | "
          f"{d.RATIO.mean():.3f} | {d.MARGIN_over_SD.mean():.4f} | {d.RHO_IS_OOS.mean():+.3f} | "
          f"{d.DD_SPAN_pp.mean():.1f} | {int(d.n4b_OOS.sum())}/{int(d.n_rungs.sum())} |")
    P()

    P("## Every grid point (ALL reported)")
    P()
    for pname in G.panel.unique():
        P(f"### {pname}")
        P()
        P("| band | ladder | sig lag | rung | mean gross | turn/yr | IS Sharpe | LOYO SD | "
          "FULL CAGR/Sh/MaxDD | OOS CAGR/Sh/MaxDD | 4a FULL | 4a OOS | 4b FULL | 4b OOS |")
        P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for _, r in G[G.panel == pname].iterrows():
            P(f"| {r.band} | {r.ladder} | {r.sig_lag} | {r.rung:.2f} | {r.mean_gross:.3f} | {r.turn_yr:.2f} | "
              f"{r.IS_Sharpe:.4f} | {r.IS_LOYO_SD:.4f} | "
              f"{r.FULL_CAGR:.2%} / {r.FULL_Sharpe:.4f} / {r.FULL_MaxDD:.2%} | "
              f"{r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%} | "
              f"{'P' if r.keep4a_FULL else '-'} | {'P' if r.keep4a_OOS else '-'} | "
              f"{'P' if r.keep4b_FULL else '-'} | {'P' if r.keep4b_OOS else '-'} |")
        P()

    P("## Rule 8 — (band, rung) chosen on 2009-2016 IS Sharpe ONLY; 2017-2026 read ONCE")
    P()
    P("| panel | ladder | sig lag | IS pick | mean gross | FULL CAGR/Sh/MaxDD | OOS CAGR/Sh/MaxDD | "
      "4a FULL | 4a OOS | 4b FULL | 4b OOS | OOS oracle | regret (Sharpe) |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for _, r in K.iterrows():
        P(f"| {r.panel} | {r.ladder} | {r.sig_lag} | {r.pick_band} / {r.pick_rung:.2f} | {r.mean_gross:.3f} | "
          f"{r.FULL_CAGR:.2%} / {r.FULL_Sharpe:.4f} / {r.FULL_MaxDD:.2%} | "
          f"{r.OOS_CAGR:.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:.2%} | "
          f"{'PASS' if r.keep4a_FULL else 'fail'} | {'PASS' if r.keep4a_OOS else 'fail'} | "
          f"{'PASS' if r.keep4b_FULL else 'fail'} | {'PASS' if r.keep4b_OOS else 'fail'} | "
          f"{r.oracle_band} / {r.oracle_rung:.2f} ({r.oracle_OOS_Sharpe:.4f}) | {r.regret:+.4f} |")
    P()
    for _, r in K.drop_duplicates("panel").iterrows():
        P(f"Reference {r.panel}: RULES v2 FULL {r.base_FULL_CAGR:.2%} / {r.base_FULL_Sharpe:.4f} / "
          f"{r.base_FULL_MaxDD:.2%}, OOS {r.base_OOS_CAGR:.2%} / {r.base_OOS_Sharpe:.4f} / "
          f"{r.base_OOS_MaxDD:.2%};  SPY FULL {r.spy_FULL_CAGR:.2%} / {r.spy_FULL_Sharpe:.4f} / "
          f"{r.spy_FULL_MaxDD:.2%}, OOS {r.spy_OOS_CAGR:.2%} / {r.spy_OOS_Sharpe:.4f} / "
          f"{r.spy_OOS_MaxDD:.2%}")
    P()

    P("## Gates")
    P()
    P("| gate | value | ok |")
    P("|---|---|---|")
    for g, v, ok in gates:
        P(f"| {g} | {v} | {'OK' if ok else 'FAIL'} |")
    P()
    P(f"Runtime {time.time()-T0:.0f}s. Artifacts: {Path(OUT).name}.grid.csv / .resolution.csv / .picks.csv")

    Path(f"{OUT}.result.md").write_text("\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
