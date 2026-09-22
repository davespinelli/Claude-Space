#!/usr/bin/env python3
"""Idea 2290 (lane cloud, 2026-09-22): is the CARRY SLEEVE'S GAIN a 2022-2026 RATE-REGIME
DRAW?

WHAT THIS STRESSES.  Idea 2294 (lane B, 2026-09-22, same day) returned the record's
freshest KEEP-candidate: sweep the live RULES v2 band book's idle NAV (46.7% of capital
earning exactly 0% in `engine.backtest`) into a short-duration Treasury sleeve.  4a passes
30 of 104 cells; 4b dies 0 of 104.  But the ENTIRE T-bill carry on this tape is earned after
2021 — SHY's own carry is 0.81%/yr over 2009-2016 and 1.73%/yr over 2017-2026 — so the
gain may be a rate-regime draw and, worse, rule 8's chooser is asked to pick the instrument
on 2009-2016, a window in which every candidate sleeve is worth approximately nothing.
This run prices both halves of that worry.

TWO TUNED DIALS AND NO MORE
  DIAL 1  instrument in {NONE (control), SHY, IEF, TLT}; phi FROZEN at 1.00, the value
          idea 2294's proposed clause 7 ships.
  DIAL 2  excision / counterfactual window in
          {FULL, EX22 (sample ends 2021-12-31), EX21 (ends 2020-12-31), EX20 (ends
           2019-12-31), ZIRPFLAT, ZIRPSWAP}.
          ZIRPFLAT: from 2022-01-01 the sleeve instrument grows at its OWN 2009-2021 mean
          daily log return with zero vol — a literal "the zero-rate regime returned" tape.
          ZIRPSWAP: from 2022-01-01 the sleeve's daily returns are the instrument's own
          2009-2021 daily returns replayed in order — same counterfactual, real vol and
          real correlation with the equity book, deterministic.
  Panel {U56, B136} and cost rung {0, 10, 25, 50} bps are REPORTED at every cell, never
  selected.  2 panels x 4 instruments x 6 windows x 4 rungs = 192 published cells, plus the
  MMF-sweep variant (the sleeve's OWN turnover rebated) at each.

CONSTRUCTION.  The equity book is the LIVE RULES v2 band book (band 0.03, gross 0.75,
weekly, t+1) and is IDENTICAL in every cell: the sleeve is a SYNTHETIC column `CARRY`
appended to the panel and invisible to `rules_v2_weights`, so a counterfactual sleeve tape
cannot move a single equity decision.  Idea 2294 instead added sleeve weight onto the
instrument's OWN panel column (SHY/IEF/TLT are constituents of both universes), so gate G1
reproduces 2294's headline BOTH ways and publishes the difference.

Costs: `engine.backtest`'s held weights and turnover do not depend on `cost_bps` (costs are
subtracted from the return stream after the drift loop), so every cost rung is computed
exactly from one cost-0 run.  Gate G2 verifies this against `engine.backtest` directly.

PROTOCOL: rule 1 (committed caches, >= 10y); rule 2 (10 bps, t+1, long-only, no leverage —
phi=1 leaves sum(w) == 1, never above); rule 3 (live RULES v2 AND SPY); rule 4 (both KEEP
paths at every cell, exactly 2 tuned dials); rule 5 (one idea, one deterministic script);
rule 7 (honest report); rule 8 (walk-forward, 2017-2026 read once); rule 9 (survivorship).

SURVIVORSHIP CAVEAT.  U56 and B136 are CURRENT constituents held from 2008, so every
absolute CAGR here is upward-biased and the 4a/4b pass COUNTS inherit that bias.  The
sleeve contrast (sleeve book minus its own phi=0 control on the same tape, same names, same
days) is first-order immune to it; the regime finding rests on the contrast, not the level.

Run: python3 research/backtests/2026-09-22_carry-sleeve-rate-regime-draw_cloud.py
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights                      # noqa
from engine import backtest, rebalance_mask                               # noqa

SLUG      = "2026-09-22_carry-sleeve-rate-regime-draw_cloud"
OUT       = ROOT / "research" / "backtests"
BAND, GROSS, FREQ = 0.03, 0.75, "W"        # the LIVE book, untouched
PHI       = 1.00                            # FROZEN at clause 7's shipped value
INSTR     = ["NONE", "SHY", "IEF", "TLT"]
COSTS     = [0, 10, 25, 50]
LIVE_COST = 10
WARMUP    = 260
OOS_START = pd.Timestamp("2017-01-01")
ZIRP_END  = pd.Timestamp("2021-12-31")     # the record's own rate-regime boundary
WINDOWS   = ["FULL", "EX22", "EX21", "EX20", "ZIRPFLAT", "ZIRPSWAP"]
WIN_END   = {"FULL": None, "EX22": pd.Timestamp("2021-12-31"),
             "EX21": pd.Timestamp("2020-12-31"), "EX20": pd.Timestamp("2019-12-31"),
             "ZIRPFLAT": None, "ZIRPSWAP": None}
LB, NBOOT, SEED = 65, 400, 20260922

LOG = []
def log(s):
    print(s, flush=True); LOG.append(str(s))

# ------------------------------------------------------------------ metrics
def sharpe(r): s = r.std(); return r.mean() * 252 / (s * np.sqrt(252)) if s > 0 else np.nan
def maxdd(r):  e = (1 + r).cumprod(); return (e / e.cummax() - 1).min()
def cagr(r):   e = (1 + r).cumprod(); return e.iloc[-1] ** (252 / len(r)) - 1

def full_metrics(r):
    h = len(r) // 2; o = r.loc[OOS_START:]
    d = dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
             H1=sharpe(r.iloc[:h]), H2=sharpe(r.iloc[h:]))
    if len(o) > 60:
        d.update(OOS_CAGR=cagr(o), OOS_Sharpe=sharpe(o), OOS_MaxDD=maxdd(o))
    else:
        d.update(OOS_CAGR=np.nan, OOS_Sharpe=np.nan, OOS_MaxDD=np.nan)
    return d

def keep_paths(m, base_m, spy_m):
    """4a: Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse.
       4b: Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
           CAGR >= 70% of SPY's.  Legs returned individually so the binder is published."""
    legs4a = dict(H1=m["H1"] > base_m["H1"], H2=m["H2"] > base_m["H2"],
                  DD=m["MaxDD"] >= base_m["MaxDD"])
    legs4b = dict(H1=m["H1"] > spy_m["H1"], H2=m["H2"] > spy_m["H2"],
                  OOS=bool(m["OOS_Sharpe"] > spy_m["OOS_Sharpe"]),
                  DD=m["MaxDD"] >= 0.60 * spy_m["MaxDD"],
                  CAGR=m["CAGR"] >= 0.70 * spy_m["CAGR"])
    return all(legs4a.values()), all(legs4b.values()), legs4a, legs4b

# ------------------------------------------------------------------ engine with per-column turnover
def bt_percol(prices, weights, freq=FREQ):
    """Exact replica of engine.backtest at cost 0, additionally returning per-column
    turnover.  Held weights and turnover are cost-independent in engine.backtest (costs are
    subtracted after the drift loop), so returns at any rung are gross_ret - turnover*c/1e4."""
    rets = prices.pct_change().fillna(0.0)
    w_t  = weights.reindex(prices.index).fillna(0.0).shift(1)
    mask = rebalance_mask(prices.index, freq).shift(1, fill_value=False)
    cols = prices.columns
    held = np.zeros((len(prices), len(cols)))
    tov  = np.zeros((len(prices), len(cols)))
    cur  = np.zeros(len(cols)); R = rets.values; W = w_t.values; M = mask.values
    for i in range(len(prices)):
        if M[i] or i == 0:
            new = np.nan_to_num(W[i]); tov[i] = np.abs(new - cur); cur = new
        held[i] = cur
        growth = cur * (1 + R[i]); tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    gross_ret = pd.Series((held * R).sum(axis=1), index=prices.index)
    tov_df    = pd.DataFrame(tov, index=prices.index, columns=cols)
    heldw     = pd.DataFrame(held, index=prices.index, columns=cols)
    return gross_ret, tov_df, heldw

# ------------------------------------------------------------------ sleeve tapes
def carry_tape(inst_px, window):
    """The synthetic CARRY column's price series under a counterfactual window."""
    if window not in ("ZIRPFLAT", "ZIRPSWAP"):
        return inst_px.copy()
    r  = inst_px.pct_change().fillna(0.0)
    is_zirp = r.index <= ZIRP_END
    post    = ~is_zirp
    r2 = r.copy()
    if window == "ZIRPFLAT":
        mu = np.log1p(r[is_zirp]).mean()
        r2[post] = np.expm1(mu)
    else:                                    # ZIRPSWAP: replay the ZIRP tape in order
        src = r[is_zirp].values
        n   = int(post.sum())
        reps = int(np.ceil(n / len(src)))
        r2[post] = np.tile(src, reps)[:n]
    return inst_px.iloc[0] * (1 + r2).cumprod()

def sleeve_weights(px_eq, carry_col_name, phi=PHI):
    """Live RULES v2 band book on the EQUITY panel only, plus phi of its idle NAV in the
    synthetic carry column.  Zero hindsight: the sleeve weight at t is a deterministic
    function of the book's own weights at t.  phi=1 => sum(w) == 1, never above."""
    w = rules_v2_weights(px_eq, band=BAND, gross=GROSS)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w = w.copy(); w[carry_col_name] = phi * idle
    return w

# ------------------------------------------------------------------ main
def main():
    t0 = time.time(); gates = []; rows = []; yearly_rows = []; series = {}
    rng = np.random.default_rng(SEED)

    for panel, kw in (("U56", {}), ("B136", dict(broad=True))):
        px = load_universe(**kw)
        start = px.index[WARMUP]
        spy_r = px["SPY"].pct_change().fillna(0.0).loc[start:]

        # ---- gate G1: reproduce 2294's own construction (sleeve ON the panel column)
        w_lb = rules_v2_weights(px, band=BAND, gross=GROSS)
        idle = (1.0 - w_lb.sum(axis=1)).clip(lower=0.0)
        w_lb = w_lb.copy()
        w_lb["SHY"] = w_lb["SHY"] + PHI * idle * px["SHY"].notna().astype(float)
        r_lb = backtest(px, w_lb, cost_bps=LIVE_COST, freq=FREQ)["returns"].loc[start:]
        m_lb = full_metrics(r_lb)

        for window in WINDOWS:
            for inst in INSTR:
                if inst == "NONE":
                    px_ext = px
                    w = rules_v2_weights(px, band=BAND, gross=GROSS)
                    carry_col = None
                else:
                    carry_col = "CARRY"
                    px_ext = px.copy()
                    px_ext[carry_col] = carry_tape(px[inst], window)
                    w = sleeve_weights(px, carry_col).reindex(columns=px_ext.columns).fillna(0.0)
                gr, tov, held = bt_percol(px_ext, w)
                tot_tov = tov.sum(axis=1)
                sl_tov  = tov[carry_col] if carry_col else tot_tov * 0.0
                end     = WIN_END[window]
                sl      = slice(start, end)
                for c in COSTS:
                    r_ch = (gr - tot_tov * c / 1e4).loc[sl]                    # charged
                    r_mm = (gr - (tot_tov - sl_tov) * c / 1e4).loc[sl]         # MMF rebate
                    key = (panel, window, inst, c)
                    series[key] = (r_ch, r_mm)
                # baselines on the SAME window
                if inst == "NONE":
                    for c in COSTS:
                        series[(panel, window, "SPY", c)] = (spy_r.loc[sl], spy_r.loc[sl])
                log(f"[{panel}] {window:9s} {inst:5s} done ({time.time()-t0:.0f}s)")

            # ---- scoring for this window
            for inst in INSTR:
                for c in COSTS:
                    r_ch, r_mm = series[(panel, window, inst, c)]
                    base_ch, base_mm = series[(panel, window, "NONE", c)]
                    spy_w = series[(panel, window, "SPY", c)][0]
                    bm, sm = full_metrics(base_ch), full_metrics(spy_w)
                    for variant, r in (("charged", r_ch), ("mmf", r_mm)):
                        m = full_metrics(r)
                        a, b, la, lb_ = keep_paths(m, bm, sm)
                        rows.append(dict(
                            panel=panel, window=window, instrument=inst, cost_bps=c,
                            variant=variant, keep4a=a, keep4b=b,
                            bind4a="+".join(k for k, v in la.items() if not v) or "-",
                            bind4b="+".join(k for k, v in lb_.items() if not v) or "-",
                            d_CAGR=m["CAGR"] - bm["CAGR"], d_Sharpe=m["Sharpe"] - bm["Sharpe"],
                            d_MaxDD=m["MaxDD"] - bm["MaxDD"],
                            live_CAGR=bm["CAGR"], live_Sharpe=bm["Sharpe"], live_MaxDD=bm["MaxDD"],
                            live_H1=bm["H1"], live_H2=bm["H2"],
                            spy_CAGR=sm["CAGR"], spy_Sharpe=sm["Sharpe"], spy_MaxDD=sm["MaxDD"],
                            spy_H1=sm["H1"], spy_H2=sm["H2"], spy_OOS_Sharpe=sm["OOS_Sharpe"],
                            **m))
        gates.append((f"G1 {panel} construction",
                      f"2294's own sleeve-on-panel-column SHY phi=1 @10bps: CAGR {m_lb['CAGR']:.4%} "
                      f"Sharpe {m_lb['Sharpe']:.4f} MaxDD {m_lb['MaxDD']:.4%}"))

        # ---- gate G2: cost decomposition matches engine.backtest exactly
        w_chk = sleeve_weights(px, "CARRY")
        px_chk = px.copy(); px_chk["CARRY"] = px["SHY"]
        w_chk = w_chk.reindex(columns=px_chk.columns).fillna(0.0)
        gr, tov, _ = bt_percol(px_chk, w_chk)
        mine = (gr - tov.sum(axis=1) * LIVE_COST / 1e4)
        theirs = backtest(px_chk, w_chk, cost_bps=LIVE_COST, freq=FREQ)["returns"]
        gates.append((f"G2 {panel} engine match",
                      f"max |bt_percol - engine.backtest| = {(mine - theirs).abs().max():.3e}"))

        # ---- per-calendar-year decomposition (FULL tape, 10 bps, charged)
        base_r = series[(panel, "FULL", "NONE", LIVE_COST)][0]
        for inst in INSTR[1:]:
            r = series[(panel, "FULL", inst, LIVE_COST)][0]
            inst_r = px[inst].pct_change().fillna(0.0).loc[base_r.index]
            for y, idx in r.groupby(r.index.year).groups.items():
                rb, rr = base_r.loc[idx], r.loc[idx]
                yearly_rows.append(dict(panel=panel, instrument=inst, year=int(y),
                                        book=float((1 + rr).prod() - 1),
                                        control=float((1 + rb).prod() - 1),
                                        sleeve_gain=float((1 + rr).prod() - (1 + rb).prod()),
                                        instrument_ret=float((1 + inst_r.loc[idx]).prod() - 1)))

    df  = pd.DataFrame(rows)
    yr  = pd.DataFrame(yearly_rows)

    # ------------------------------------------------------------ A. is the gain a regime draw?
    log("\n=== A. THE SLEEVE'S GAIN BY CALENDAR YEAR (FULL tape, 10 bps charged) ===")
    log(f"{'panel':6s} {'instr':5s} {'era':10s} {'mean sleeve gain/yr':>20s} {'mean instr ret/yr':>19s}")
    era_rows = []
    for (p, i), g in yr.groupby(["panel", "instrument"]):
        for era, sel in (("2009-2021", g.year <= 2021), ("2022-2026", g.year >= 2022)):
            gg = g[sel]
            era_rows.append(dict(panel=p, instrument=i, era=era,
                                 sleeve_gain=gg.sleeve_gain.mean(), instr_ret=gg.instrument_ret.mean()))
            log(f"{p:6s} {i:5s} {era:10s} {gg.sleeve_gain.mean():+20.4%} {gg.instrument_ret.mean():+19.4%}")
    era = pd.DataFrame(era_rows)
    log("\n  per-year detail (U56):")
    for r in yr[yr.panel == "U56"].sort_values(["instrument", "year"]).itertuples():
        log(f"    {r.instrument:5s} {r.year}  book {r.book:+8.2%}  control {r.control:+8.2%}  "
            f"gain {r.sleeve_gain:+7.2%}  instr {r.instrument_ret:+7.2%}")

    # ------------------------------------------------------------ B. KEEP paths, all windows
    log("\n=== B. BOTH KEEP PATHS AT EVERY PUBLISHED CELL (192 charged + 192 MMF) ===")
    log(f"{'panel':6s} {'window':9s} {'instr':5s} {'var':8s} {'cost':>4s} "
        f"{'CAGR':>8s} {'Sharpe':>8s} {'MaxDD':>8s} {'dCAGR':>8s} {'4a':>3s} {'4b':>3s} {'bind4b':12s}")
    for r in df[df.instrument != "NONE"].itertuples():
        log(f"{r.panel:6s} {r.window:9s} {r.instrument:5s} {r.variant:8s} {r.cost_bps:4d} "
            f"{r.CAGR:8.2%} {r.Sharpe:8.4f} {r.MaxDD:8.2%} {r.d_CAGR:+8.3%} "
            f"{str(r.keep4a):>3s} {str(r.keep4b):>3s} {r.bind4b:12s}")
    dsl = df[df.instrument != "NONE"]
    log(f"\nTOTALS: 4a {int(dsl.keep4a.sum())} of {len(dsl)}   4b {int(dsl.keep4b.sum())} of {len(dsl)}")
    for w, g in dsl.groupby("window"):
        log(f"  window {w:9s}: 4a {int(g.keep4a.sum()):3d}/{len(g)}   4b {int(g.keep4b.sum()):3d}/{len(g)}")
    for (w, v), g in dsl[dsl.instrument == "SHY"].groupby(["window", "variant"]):
        log(f"  SHY {w:9s} {v:8s}: 4a {int(g.keep4a.sum())}/{len(g)}  4b {int(g.keep4b.sum())}/{len(g)}")
    log("  4b binding legs over all sleeve cells: " +
        ", ".join(f"{k}={v}" for k, v in dsl.bind4b.value_counts().items()))

    # the headline comparison: FULL vs the ZIRP counterfactuals at the shipped cell
    log("\n  SHIPPED CELL (SHY, phi=1.00, 10 bps) ACROSS WINDOWS:")
    for p in ("U56", "B136"):
        for v in ("charged", "mmf"):
            for w in WINDOWS:
                r = df[(df.panel == p) & (df.window == w) & (df.instrument == "SHY") &
                       (df.cost_bps == LIVE_COST) & (df.variant == v)].iloc[0]
                log(f"    {p:5s} {v:8s} {w:9s}  CAGR {r.CAGR:7.2%} (live {r.live_CAGR:7.2%}, "
                    f"d {r.d_CAGR:+.3%})  Sharpe {r.Sharpe:.4f} (live {r.live_Sharpe:.4f})  "
                    f"MaxDD {r.MaxDD:7.2%} (live {r.live_MaxDD:7.2%})  4a {str(r.keep4a):5s} "
                    f"4b {str(r.keep4b):5s}")

    # ------------------------------------------------------------ C. rule 8
    log("\n=== C. PROTOCOL RULE 8: THE INSTRUMENT DIAL CHOSEN ON 2009-2016 ONLY ===")
    log("    (the IS window is entirely ZIRP; 2017-2026 read exactly once)")
    wf = []
    for p in ("U56", "B136"):
        for v in ("charged", "mmf"):
            cands = {}
            for inst in INSTR:
                r = series[(p, "FULL", inst, LIVE_COST)][0 if v == "charged" else 1]
                cands[inst] = r
            isr = {k: r.loc[:OOS_START - pd.Timedelta(days=1)] for k, r in cands.items()}
            oos = {k: r.loc[OOS_START:] for k, r in cands.items()}
            issh = {k: sharpe(r) for k, r in isr.items()}
            pick = max(issh, key=issh.get)
            spread = max(issh.values()) - min(issh.values())
            # block-bootstrap SE of the IS Sharpe spread between the best and worst sleeve
            best, worst = max(issh, key=issh.get), min(issh, key=issh.get)
            A, B = isr[best].values, isr[worst].values
            T = len(A); nb = int(np.ceil(T / LB)); dd = np.empty(NBOOT)
            for b in range(NBOOT):
                st = rng.integers(0, T, size=nb)
                idx = (st[:, None] + np.arange(LB)[None, :]).ravel()[:T] % T
                a, w_ = A[idx], B[idx]
                sa = a.std(); sw = w_.std()
                dd[b] = (a.mean() * 252 / (sa * np.sqrt(252)) if sa > 0 else np.nan) - \
                        (w_.mean() * 252 / (sw * np.sqrt(252)) if sw > 0 else np.nan)
            se = np.nanstd(dd)
            log(f"  [{p}] {v:8s} IS Sharpe: " + "  ".join(f"{k} {issh[k]:.4f}" for k in INSTR))
            log(f"        IS spread best({best}) - worst({worst}) = {spread:+.4f}  "
                f"block-bootstrap SE {se:.4f}  t = {spread/se if se>0 else float('nan'):+.2f}"
                f"   -> {'IDENTIFIABLE' if abs(spread/se) > 2 else 'NOT IDENTIFIABLE IS'}")
            for nm, k in (("C_ISSHARPE pick", pick), ("zero-parameter SHY", "SHY"),
                          ("control NONE", "NONE")):
                o = oos[k]
                wf.append(dict(panel=p, variant=v, chooser=nm, pick=k, IS_Sharpe=issh[k],
                               OOS_CAGR=cagr(o), OOS_Sharpe=sharpe(o), OOS_MaxDD=maxdd(o)))
                log(f"        {nm:20s} = {k:5s}  OOS CAGR {cagr(o):7.2%}  Sharpe {sharpe(o):.4f}  "
                    f"MaxDD {maxdd(o):7.2%}")
            o_spy = series[(p, "FULL", "SPY", LIVE_COST)][0].loc[OOS_START:]
            wf.append(dict(panel=p, variant=v, chooser="SPY", pick="SPY", IS_Sharpe=sharpe(
                series[(p, "FULL", "SPY", LIVE_COST)][0].loc[:OOS_START - pd.Timedelta(days=1)]),
                OOS_CAGR=cagr(o_spy), OOS_Sharpe=sharpe(o_spy), OOS_MaxDD=maxdd(o_spy)))
            log(f"        {'SPY':20s} = SPY    OOS CAGR {cagr(o_spy):7.2%}  Sharpe {sharpe(o_spy):.4f}  "
                f"MaxDD {maxdd(o_spy):7.2%}")
    wfd = pd.DataFrame(wf)

    # ------------------------------------------------------------ D. what survives ZIRP
    log("\n=== D. WHAT THE CLAUSE IS WORTH IF THE ZERO-RATE REGIME RETURNS ===")
    for p in ("U56", "B136"):
        for v in ("charged", "mmf"):
            f_ = df[(df.panel == p) & (df.window == "FULL") & (df.instrument == "SHY") &
                    (df.cost_bps == LIVE_COST) & (df.variant == v)].iloc[0]
            for w in ("ZIRPFLAT", "ZIRPSWAP", "EX22"):
                z = df[(df.panel == p) & (df.window == w) & (df.instrument == "SHY") &
                       (df.cost_bps == LIVE_COST) & (df.variant == v)].iloc[0]
                log(f"  {p:5s} {v:8s} {w:9s}: sleeve gain {z.d_CAGR:+.3%}/yr vs FULL "
                    f"{f_.d_CAGR:+.3%}/yr  ({z.d_CAGR/f_.d_CAGR*100 if f_.d_CAGR else float('nan'):5.1f}% "
                    f"of it retained)  4a {str(z.keep4a):5s}")

    log("\n=== GATES ===")
    for k, v in gates: log(f"  {k}: {v}")

    df.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    yr.to_csv(OUT / f"{SLUG}.yearly.csv", index=False)
    era.to_csv(OUT / f"{SLUG}.era.csv", index=False)
    wfd.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    pd.DataFrame(gates, columns=["gate", "value"]).to_csv(OUT / f"{SLUG}.gates.csv", index=False)
    log(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")

if __name__ == "__main__":
    main()
