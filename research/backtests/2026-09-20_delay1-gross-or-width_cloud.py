#!/usr/bin/env python3
"""Idea 907 (lane cloud, 2026-09-20): is the DELAY-1 DRAWDOWN MOVE a GROSS fact, a TURNOVER fact,
a WIDTH fact -- or none of them?

Idea 887's reached 4b cell loses **4.51 pp of MaxDD** to one further day of execution delay at
g = 1.00 and only **3.50 pp** at g = 0.75 on the SAME width, and the g = 0.75 rung stays inside
the 4b drawdown cap.  Two readings of that pair are observationally equivalent at one cell:

    (A) the delay cost SCALES WITH EXPOSURE -- it is gross times the same per-unit slippage, so
        it is a leverage fact and de-grossing buys it back;
    (B) the delay cost SCALES WITH TURNOVER -- it is the number of trades that go stale, so it is
        a cadence/width fact and only trading less buys it back;
    (C) neither -- the cost is a level, set by the tape's own gap risk, and the 4.51-vs-3.50 pair
        is noise off one cell.

This walks DELAY x GROSS x WIDTH on three panels, publishes every rung, and reads the cost
function directly by regressing the realised delay cost on each candidate carrier alone and on
both together.

Axes (180 books = 3 panels x 4 d x 3 g x 5 N):
    d   EXTRA execution delay in {0, 1, 2, 3} trading days BEYOND the engine's own t+1.
        d = 0 is the live convention (decide at close t, trade at close t+1).
        DELAY IS NOT A TUNED PARAMETER: it is an execution-realism axis, swept and published in
        full, and no chooser is ever allowed to pick it.
    g   gross in {0.50, 0.75, 1.00}
    N   width (names held) in {5, 10, 20, 40, 80}, capped at the panel's own size
Exactly TWO parameters are ever CHOSEN -- (g, N), and only on 2009-2016 IS rows (PROTOCOL rule 8,
which is therefore stricter here than the idea's own "max 2 params (delay, gross)" allowance).

Book: names inside the live 200d +/-3% band (RULES v2 clause 2), ranked by `baseline.score`'s
composite, top N held equal-weighted at gross g; when fewer than N are eligible the shortfall goes
to CASH and is never re-spread.  Weekly cadence, 10 bps, t+1(+d).

Cost function read (the deliverable):
    DCOST(d) = MaxDD(d) - MaxDD(0) in pp, and the same for Sharpe and CAGR, per (panel, g, N).
    Regress DCOST(1) on  (i) gross alone, (ii) realised turnover alone, (iii) realised MEAN GROSS
    alone, (iv) width N alone, (v) gross+turnover together; report R^2 and the residual SD of each.
    If (A) holds, gross alone carries it; if (B), turnover alone does; if (C), no R^2 is large.

Rule 8: (g, N) chosen on 2009-2016 ONLY by two independent IS-only choosers (argmax IS Sharpe,
argmax IS Calmar) AT d = 0; 2017-2026 then read ONCE and the chosen book scored at EVERY delay on
BOTH KEEP paths against live RULES v2 and SPY.

Panels: U56, B136 and SMALL (the 483-name sub-$2B panel, with the tickers whose
`max_1d_move >= 1.0` in data/small_meta.csv dropped first).  SURVIVORSHIP: all three panels are
CURRENT constituents of their screens, so every absolute level here is optimistic; SMALL is the
worst affected (sub-$2B names that delisted are simply absent).  On SMALL the joined SPY column
is a BENCHMARK only and is never held.
Price-only.  No EDGAR / Form 4 / 8-K / options / spin-offs / live data.

Deterministic, offline, standalone:
    python3 research/backtests/2026-09-20_delay1-gross-or-width_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score  # noqa
from engine import backtest, rebalance_mask  # noqa

T0 = time.time()
COST = 10.0
FREQ = "W"
WARM = 260
IS_END = pd.Timestamp("2016-12-31")
D_GRID = (0, 1, 2, 3)
G_GRID = (0.50, 0.75, 1.00)
N_GRID = (5, 10, 20, 40, 80)
BAND = 0.03
OUT = Path(__file__).with_suffix("")

# ---------------------------------------------------------------------------------- engine
def fast_run(px_v, w_v, mask_v, delay=0, cost_bps=0.0):
    """Gross-of-cost path (cost_bps=0) + turnover.  `delay` adds d days ON TOP of the engine's
    own t -> t+1 application, i.e. weights decided at t are traded at the close of t+1+d."""
    n, k = px_v.shape
    rets = np.zeros_like(px_v); rets[1:] = px_v[1:] / px_v[:-1] - 1.0
    rets = np.nan_to_num(rets, nan=0.0, posinf=0.0, neginf=0.0)
    lag = 1 + delay
    w_t = np.zeros_like(w_v); w_t[lag:] = w_v[:-lag]
    m = np.zeros(n, dtype=bool); m[lag:] = mask_v[:-lag]
    cur = np.zeros(k); turn = np.zeros(n); port = np.zeros(n); heldg = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            turn[i] = np.abs(w_t[i] - cur).sum(); cur = w_t[i].copy()
        heldg[i] = cur.sum()
        port[i] = (cur * rets[i]).sum() - turn[i] * cost_bps / 1e4
        growth = cur * (1.0 + rets[i]); tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0: cur = growth / tot
    return port, turn, heldg

def net(gp, turn, c): return gp - turn * c / 1e4
def sh(r):
    v = r.std(ddof=1) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan
def mdd(r):
    eq = np.cumprod(1.0 + r); return float((eq / np.maximum.accumulate(eq) - 1.0).min())
def cagr(r):
    eq = np.cumprod(1.0 + r); y = len(r) / 252.0
    return float(eq[-1] ** (1.0 / y) - 1.0) if y > 0 else np.nan
def calmar(r):
    d = mdd(r); return float(cagr(r) / abs(d)) if d < 0 else np.nan

def keep_4a(r, b, win):
    rw, bw = r[win], b[win]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(bw[:h]) and sh(rw[h:]) > sh(bw[h:]) and mdd(rw) >= mdd(bw))
def keep_4a_1w(r, b, win): return bool(sh(r[win]) > sh(b[win]) and mdd(r[win]) >= mdd(b[win]))
def keep_4b(r, s, win):
    rw, sw = r[win], s[win]; h = len(rw) // 2
    return bool(sh(rw[:h]) > sh(sw[:h]) and sh(rw[h:]) > sh(sw[h:])
                and mdd(rw) >= 0.60 * mdd(sw) and cagr(rw) >= 0.70 * cagr(sw))
def keep_4b_1w(r, s, win):
    rw, sw = r[win], s[win]
    return bool(sh(rw) > sh(sw) and mdd(rw) >= 0.60 * mdd(sw) and cagr(rw) >= 0.70 * cagr(sw))

def ols(y, X):
    """R^2 and residual SD of y ~ [1, X]; X is (n, p)."""
    y = np.asarray(y, float); X = np.asarray(X, float).reshape(len(y), -1)
    ok = np.isfinite(y) & np.isfinite(X).all(axis=1)
    y, X = y[ok], X[ok]
    A = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ beta
    ss = ((y - y.mean()) ** 2).sum()
    return dict(R2=float(1 - (res ** 2).sum() / ss) if ss > 0 else np.nan,
                resid_SD=float(res.std(ddof=1)), n=int(len(y)),
                slope=float(beta[1]) if len(beta) > 1 else np.nan)

# ------------------------------------------------------------------------------- the books
def build(px, cols, N, g):
    """Top-N by the live composite among names inside the 200d +/-3% band, equal weight at gross
    g; shortfall to CASH (never re-spread)."""
    sub = px[cols]
    s, _, _ = score(sub, vol_scale=True)
    elig = s.where(band_state(sub, BAND) & sub.notna())
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= N) & elig.notna()
    Nc = min(N, len(cols))
    w = sel.astype(float) * (g / Nc)
    return w.reindex(columns=px.columns).fillna(0.0)

def panels():
    px56 = load_universe().dropna(how="all").ffill()
    px136 = load_universe(broad=True).dropna(how="all").ffill()
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    small_cols = [c for c in pxs.columns if c != "SPY" and c not in bad]
    return [("U56", px56, list(px56.columns)),
            ("B136", px136, list(px136.columns)),
            ("SMALL", pxs, small_cols)]

# ------------------------------------------------------------------------------------ main
def main():
    gates, rows, cost_rows, pick_rows = [], [], [], []
    lines = []
    P = lambda s="": (print(s), lines.append(s))

    for pname, px, cols in panels():
        idx = px.index; px_v = px.values.astype(float)
        mask_v = rebalance_mask(idx, FREQ).values
        full = np.zeros(len(idx), dtype=bool); full[WARM:] = True
        IS = full & np.asarray(idx <= IS_END); OOS = full & np.asarray(idx > IS_END)

        sc = px.columns.get_loc("SPY")
        spy_r = np.zeros(len(idx)); spy_r[1:] = px_v[1:, sc] / px_v[:-1, sc] - 1.0
        spy_r = np.nan_to_num(spy_r)

        live_w = rules_v2_weights(px[cols], band=BAND, gross=0.75).reindex(columns=px.columns).fillna(0.0)
        lg, lt, _ = fast_run(px_v, live_w.values.astype(float), mask_v, delay=0)
        live_p = net(lg, lt, COST)

        if pname == "U56":
            eng = backtest(px, rules_v2_weights(px), cost_bps=COST, freq=FREQ)["returns"].values
            d = float(np.abs(eng[full] - live_p[full]).max())
            gates.append(("G1 delay=0 fast_run == engine.backtest (RULES v2, FULL)", f"{d:.3e}", d < 1e-12))
            # G2: delay d must equal shifting the weight frame by d days at delay 0
            wv = live_w.values.astype(float)
            a, ta, _ = fast_run(px_v, wv, mask_v, delay=2)
            wsh = np.zeros_like(wv); wsh[2:] = wv[:-2]
            msh = np.zeros(len(idx), dtype=bool); msh[2:] = mask_v[:-2]
            b, tb, _ = fast_run(px_v, wsh, msh, delay=0)
            d2 = float(np.abs(net(a, ta, COST) - net(b, tb, COST)).max())
            gates.append(("G2 delay=d identical to pre-shifting weights+mask by d (d=2)", f"{d2:.3e}", d2 < 1e-12))
            g3 = float(np.abs(live_p[full] - net(*fast_run(px_v, wv, mask_v, delay=1)[:2], COST)[full]).max())
            gates.append(("G3 delay axis is LIVE (d=1 path differs from d=0)", f"{g3:.4f}", g3 > 0))

        base = {}
        for g in G_GRID:
            for N in N_GRID:
                w = build(px, cols, N, g).values.astype(float)
                for d in D_GRID:
                    gp, to, hg = fast_run(px_v, w, mask_v, delay=d)
                    p = net(gp, to, COST)
                    row = dict(panel=pname, d=d, g=g, N=N,
                               mean_gross=float(hg[full].mean()),
                               turn_yr=float(to[full].sum() / (full.sum() / 252.0)),
                               IS_Sharpe=sh(p[IS]), IS_Calmar=calmar(p[IS]),
                               FULL_CAGR=cagr(p[full]), FULL_Sharpe=sh(p[full]), FULL_MaxDD=mdd(p[full]),
                               H1_Sharpe=sh(p[full][:int(full.sum()//2)]),
                               H2_Sharpe=sh(p[full][int(full.sum()//2):]),
                               OOS_CAGR=cagr(p[OOS]), OOS_Sharpe=sh(p[OOS]), OOS_MaxDD=mdd(p[OOS]),
                               keep4a_FULL=keep_4a(p, live_p, full), keep4a_OOS=keep_4a_1w(p, live_p, OOS),
                               keep4b_FULL=keep_4b(p, spy_r, full), keep4b_OOS=keep_4b_1w(p, spy_r, OOS))
                    rows.append(row)
                    if d == 0: base[(g, N)] = row
                    else:
                        b0 = base[(g, N)]
                        cost_rows.append(dict(panel=pname, g=g, N=N, d=d,
                                              mean_gross=b0["mean_gross"], turn_yr=b0["turn_yr"],
                                              dMaxDD_pp=(row["FULL_MaxDD"] - b0["FULL_MaxDD"]) * 100,
                                              dSharpe=row["FULL_Sharpe"] - b0["FULL_Sharpe"],
                                              dCAGR_pp=(row["FULL_CAGR"] - b0["FULL_CAGR"]) * 100,
                                              dMaxDD_OOS_pp=(row["OOS_MaxDD"] - b0["OOS_MaxDD"]) * 100,
                                              k4b_FULL_0=b0["keep4b_FULL"], k4b_FULL_d=row["keep4b_FULL"],
                                              k4b_OOS_0=b0["keep4b_OOS"], k4b_OOS_d=row["keep4b_OOS"]))

        # ---- rule 8: (g, N) chosen on IS ONLY at d = 0; OOS read ONCE at EVERY delay
        dd = pd.DataFrame([r for r in rows if r["panel"] == pname and r["d"] == 0]).reset_index(drop=True)
        for ch, col in (("IS_Sharpe", "IS_Sharpe"), ("IS_Calmar", "IS_Calmar")):
            pk = dd.loc[int(dd[col].idxmax())]
            w = build(px, cols, int(pk.N), float(pk.g)).values.astype(float)
            for d in D_GRID:
                gp, to, _ = fast_run(px_v, w, mask_v, delay=d); p = net(gp, to, COST)
                pick_rows.append(dict(panel=pname, chooser=ch, pick_g=pk.g, pick_N=int(pk.N), d=d,
                                      OOS_CAGR=cagr(p[OOS]), OOS_Sharpe=sh(p[OOS]), OOS_MaxDD=mdd(p[OOS]),
                                      live_OOS_Sharpe=sh(live_p[OOS]), live_OOS_MaxDD=mdd(live_p[OOS]),
                                      spy_OOS_CAGR=cagr(spy_r[OOS]), spy_OOS_Sharpe=sh(spy_r[OOS]),
                                      spy_OOS_MaxDD=mdd(spy_r[OOS]),
                                      keep4a_OOS=keep_4a_1w(p, live_p, OOS),
                                      keep4b_OOS=keep_4b_1w(p, spy_r, OOS),
                                      keep4b_FULL=keep_4b(p, spy_r, full)))
        P(f"[{pname}] done  t={time.time()-T0:.0f}s")

    G = pd.DataFrame(rows); C = pd.DataFrame(cost_rows); K = pd.DataFrame(pick_rows)
    G.to_csv(f"{OUT}_grid.csv", index=False); C.to_csv(f"{OUT}_delaycost.csv", index=False)
    K.to_csv(f"{OUT}_rule8.csv", index=False)
    pd.set_option("display.width", 250, "display.max_columns", 40, "display.max_rows", 400)

    P("\n" + "=" * 112); P("FULL GRID (10 bps) -- ALL 180 books, every (d, g, N) rung published"); P("=" * 112)
    P(G[["panel","d","g","N","mean_gross","turn_yr","FULL_CAGR","FULL_Sharpe","FULL_MaxDD",
         "H1_Sharpe","H2_Sharpe","OOS_CAGR","OOS_Sharpe","OOS_MaxDD",
         "keep4a_FULL","keep4a_OOS","keep4b_FULL","keep4b_OOS"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P("\n" + "=" * 112); P("DELAY COST -- MaxDD(d) - MaxDD(0) in pp, and the Sharpe/CAGR legs"); P("=" * 112)
    P(C.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))

    c1 = C[C.d == 1]
    P("\n" + "=" * 112); P("IS THE DELAY-1 COST A GROSS FACT, A TURNOVER FACT, OR A WIDTH FACT?"); P("=" * 112)
    P("\nmean dMaxDD(d=1) in pp, by NOMINAL gross (across all panels and widths):")
    P(c1.groupby("g").dMaxDD_pp.agg(["mean", "min", "max", "count"]).to_string(float_format=lambda x: f"{x:+.3f}"))
    P("\nmean dMaxDD(d=1) in pp, by WIDTH N:")
    P(c1.groupby("N").dMaxDD_pp.agg(["mean", "min", "max", "count"]).to_string(float_format=lambda x: f"{x:+.3f}"))
    P("\nmean dMaxDD(d=1) in pp, by PANEL:")
    P(c1.groupby("panel").dMaxDD_pp.agg(["mean", "min", "max", "count"]).to_string(float_format=lambda x: f"{x:+.3f}"))
    P("\nSingle-carrier regressions of dMaxDD(d=1) (pooled, n = %d cells):" % len(c1))
    for lbl, X in (("nominal gross g", c1[["g"]].values),
                   ("realised MEAN GROSS", c1[["mean_gross"]].values),
                   ("realised TURNOVER /yr", c1[["turn_yr"]].values),
                   ("WIDTH N", c1[["N"]].values),
                   ("log WIDTH N", np.log(c1[["N"]].values.astype(float))),
                   ("gross + turnover", c1[["g", "turn_yr"]].values),
                   ("gross + turnover + logN", np.column_stack([c1.g, c1.turn_yr, np.log(c1.N)]))):
        r = ols(c1.dMaxDD_pp.values, X)
        P(f"   {lbl:26s}  R2 = {r['R2']:+.4f}   resid SD = {r['resid_SD']:.3f} pp   slope = {r['slope']:+.4f}")
    P(f"   [total SD of dMaxDD(d=1) = {c1.dMaxDD_pp.std(ddof=1):.3f} pp, mean = {c1.dMaxDD_pp.mean():+.3f} pp]")
    P("\nWITHIN-PANEL regressions (the panel is the largest single effect; remove it):")
    for pn in c1.panel.unique():
        s = c1[c1.panel == pn]
        rg = ols(s.dMaxDD_pp.values, s[["g"]].values)
        rt = ols(s.dMaxDD_pp.values, s[["turn_yr"]].values)
        rn = ols(s.dMaxDD_pp.values, np.log(s[["N"]].values.astype(float)))
        P(f"   {pn:6s} n={len(s):2d}  gross R2 {rg['R2']:+.4f} | turnover R2 {rt['R2']:+.4f} | "
          f"logN R2 {rn['R2']:+.4f} | mean {s.dMaxDD_pp.mean():+.3f} pp, SD {s.dMaxDD_pp.std(ddof=1):.3f} pp")

    P("\n887's OWN PAIR, re-priced on this grid (same width, g=1.00 vs g=0.75, d=1):")
    P(c1[c1.g.isin([0.75, 1.00])].pivot_table(index=["panel", "N"], columns="g", values="dMaxDD_pp")
       .assign(**{"g1.00 - g0.75": lambda t: t[1.00] - t[0.75]}).to_string(float_format=lambda x: f"{x:+.3f}"))
    both = c1[c1.g.isin([0.75, 1.00])].pivot_table(index=["panel", "N"], columns="g", values="dMaxDD_pp")
    worse = int((both[1.00] < both[0.75]).sum())
    P(f"\ng=1.00 loses MORE drawdown to delay than g=0.75 in {worse} of {len(both)} matched-width pairs.")

    P("\nDOES DELAY BREAK 4b?  (cells clearing 4b at d=0 that still clear at d)")
    for d in (1, 2, 3):
        s = C[C.d == d]
        n0 = int(s.k4b_FULL_0.sum()); nd = int((s.k4b_FULL_0 & s.k4b_FULL_d).sum())
        o0 = int(s.k4b_OOS_0.sum());  od = int((s.k4b_OOS_0 & s.k4b_OOS_d).sum())
        P(f"   d={d}: FULL {nd}/{n0} survive ; OOS {od}/{o0} survive "
          f"(new 4b FULL passes appearing at d: {int((~s.k4b_FULL_0 & s.k4b_FULL_d).sum())})")

    P("\n" + "=" * 112); P("RULE 8 -- (g, N) chosen on 2009-2016 ONLY at d=0; 2017-2026 read ONCE at every d"); P("=" * 112)
    P(K.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    k0 = K[K.d == 0]
    P(f"\nAt d=0: picks clearing 4a OOS {int(k0.keep4a_OOS.sum())}/{len(k0)}, 4b OOS {int(k0.keep4b_OOS.sum())}/{len(k0)}")
    for d in (1, 2, 3):
        kd = K[K.d == d]
        P(f"At d={d}: 4a OOS {int(kd.keep4a_OOS.sum())}/{len(kd)}, 4b OOS {int(kd.keep4b_OOS.sum())}/{len(kd)}; "
          f"mean OOS MaxDD move vs d=0 {(kd.OOS_MaxDD.values - k0.OOS_MaxDD.values).mean()*100:+.2f} pp, "
          f"mean OOS Sharpe move {(kd.OOS_Sharpe.values - k0.OOS_Sharpe.values).mean():+.4f}")

    P("\n" + "=" * 112); P("GATES"); P("=" * 112)
    for n, v, ok in gates: P(f"  [{'PASS' if ok else 'FAIL':4s}] {n}: {v}")
    P(f"\nGates {sum(1 for _,_,o in gates if o)}/{len(gates)}.  elapsed {time.time()-T0:.0f}s")
    P("SURVIVORSHIP: U56/B136/SMALL are CURRENT constituents; absolute levels are optimistic, "
      "SMALL worst (delisted sub-$2B names absent).")
    Path(f"{OUT}_out.txt").write_text("\n".join(lines))

if __name__ == "__main__":
    main()
