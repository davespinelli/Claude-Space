#!/usr/bin/env python3
"""idea 2419 (lane C, run 45, 2026-09-23) — IS THE CAPPED CANDIDATE'S DRAWDOWN CARRIED BY ITS
MOST-EXTENDED NAMES?  THE TRIM.

THE GAP.  Idea 2387 priced the BREADTH CAP, which KEEPS the `N_max` names furthest above the
200d MA and discards the rest, and killed it.  Its MIRROR has never been priced anywhere in this
record: DROP the top `f` fraction of the band's IN set by distance above the MA and hold the
REST.  The two devices move the held set in OPPOSITE directions, so together they say whether
extendedness is a risk premium or a crash hazard on this book.  `L_DD` is the binding leg on
essentially every sub-50bps 4b FAIL the candidate family has published, and every device tried
against it so far (inverse-vol 2362, sector cap 2339, breadth cap 2387, relative cap 2381) was
measured by 2381 to be a pure EXPOSURE dial.

    dist_i,t = px_i,t / ma200_i,t - 1                    (only defined for IN names)
    k_t      = floor(f * N_in,t)                         names dropped, the most extended first
    keep     = IN minus the k_t highest dist             (ties by stable column order)
    w_i      = min(g / D_t, cap)   on keep,   D_t = N_keep,t  (conv R)  or  N_in,t  (conv D)
    SHY      = 1 - sum_i w_i                             (phi = 1.00, the whole residual)

DIAL 1 -- f (trim fraction) {0.00, 0.05, 0.10, 0.20, 0.30}.  **f = 0.00 IS CAP2 EXACTLY**
          (k_t == 0 on every row), asserted bit-identically by G3 under BOTH conventions.
DIAL 2 -- g (gross) {0.75 live, 1.00}.

TWO CONVENTIONS, BOTH PUBLISHED, NEITHER SELECTED ON.  The trim confounds two channels and the
whole point of the run is to separate them:
  R = RE-SPREAD (headline).  Divide by N_keep: the trimmed budget goes back to the survivors,
      gross is preserved (subject to the cap) and the book RE-CONCENTRATES.
  D = DE-GROSS.  Divide by N_in: the trimmed weight goes to SHY and the trim is a pure exposure
      dial — which is all every cross-sectional device in this record has turned out to be.
PLACEBO (a published CONTROL, not a dial).  RANDOM-TRIM: the same k_t names dropped, chosen by a
per-name random score FIXED over the whole sample (5 seeds), so the count, the de-grossing and
the turnover profile match and ONLY the selection criterion differs.  If the extendedness trim
does not beat its own random placebo, the answer is "exposure", not "extendedness".

REPORTED, NEVER SELECTED ON: panels {U56, B136}, cost rungs {0, 10, 25, 50} bps, weight cap
{0.02 = CAP2, INF = CAND}, band 0.03, MA 200d, weekly cadence, t+1 execution, SHY sweep phi=1.00.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_extended-name-trim-on-the-capped-candidate_C.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "extended-name-trim-on-the-capped-candidate", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
FVALS = [0.00, 0.05, 0.10, 0.20, 0.30]      # DIAL 1 ; 0.00 IS CAP2
GROSSES = [0.75, 1.00]                      # DIAL 2 ; 0.75 is live
RUNGS = [0.0, 10.0, 25.0, 50.0]
CAPS = {"CAP2": 0.020, "CAND": np.inf}      # reported, never selected on
CONVENTIONS = ["R", "D"]                    # R = re-spread (headline), D = de-gross
HEADLINE_RUNG, HEADLINE_CONV, HEADLINE_CAP, SWEEP = 10.0, "R", "CAP2", "SHY"
SEEDS = [0, 1, 2, 3, 4]                     # random-trim placebo
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


# ------------------------------------------------------------------ the books
def in_set(px, invest):
    """The live clause-2 band gate, restricted to priced names.  Returns (IN mask, distance)."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    dist = (q / q.rolling(MA_LEN).mean() - 1).where(inb)
    return inb, dist


def trim_weights(px, invest, f, gross, cap, conv, score=None):
    """CAP2 with the top `f` fraction of the IN set removed by `score` (default: distance above
    the 200d MA).  conv R divides by N_keep (re-spread), conv D by N_in (de-gross).  The SHY
    residual is added by the caller so the risk sleeve can be measured on its own."""
    inb, dist = in_set(px, invest)
    n_in = inb.sum(axis=1)
    if f <= 0.0:
        keep = inb
    else:
        k = np.floor(f * n_in.values).astype(int)
        s = dist if score is None else inb.astype(float).mul(score, axis=1).where(inb)
        rk = s.rank(axis=1, ascending=False, method="first")     # 1 = most extended
        keep = inb & ~(rk.le(pd.Series(k, index=px.index), axis=0).fillna(False))
    n_keep = keep.sum(axis=1)
    denom = (n_keep if conv == "R" else n_in).replace(0, np.nan)
    per = (gross / denom).clip(upper=cap).fillna(0.0)
    w = keep.astype(float).mul(per, axis=0).reindex(columns=px.columns).fillna(0.0)
    return w, n_in, n_keep


def with_sweep(px, w):
    w = w.copy()
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ------------------------------------------------------------------ numpy replica of engine.backtest
def run(prices, weights, freq=CADENCE):
    """Bit-exact numpy replica of engine.backtest (asserted by G1/G1b), returning the ZERO-COST
    return series and the turnover so every cost rung can be priced from one pass."""
    rv = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).values
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values
    n, m = rv.shape
    held = np.zeros((n, m)); cur = np.zeros(m); to = np.zeros(n); r0 = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            to[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    shy_i = list(prices.columns).index(SWEEP)
    return dict(r0=pd.Series(r0, index=idx), turnover=pd.Series(to, index=idx),
                gross=pd.Series(held.sum(axis=1), index=idx),
                risk_gross=pd.Series(held.sum(axis=1) - held[:, shy_i], index=idx),
                maxw=pd.Series(np.delete(held, shy_i, axis=1).max(axis=1), index=idx),
                nheld=pd.Series((np.delete(held, shy_i, axis=1) > 1e-12).sum(axis=1), index=idx))


def priced(res, bps):
    return res["r0"] - res["turnover"] * bps / 1e4


# ------------------------------------------------------------------ metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    return float((1 + r).cumprod().iloc[-1] ** (252 / len(r)) - 1)


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def calmar(r):
    dd = maxdd(r)
    return float(cagr(r) / abs(dd)) if dd < 0 else np.nan


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def legs(r, base, spy, r_oos, spy_oos):
    h1, h2 = halves(r); b1, b2 = halves(base); s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR),
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy))


def main():
    t0 = time.time()
    say("=== idea 2419 — IS THE CAPPED CANDIDATE'S DRAWDOWN CARRIED BY ITS MOST-EXTENDED NAMES? ===")
    say(f"    {DATE}  lane {LANE} run 45   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  caps {list(CAPS)}  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 trim fraction f {FVALS}   DIAL 2 gross g {GROSSES}")
    say("    k_t = floor(f x N_in,t) names dropped, MOST EXTENDED FIRST (px/ma - 1, descending).")
    say("    f = 0.00 IS CAP2 EXACTLY.  conv R = re-spread over survivors (HEADLINE); conv D = de-gross to SHY.")
    say("    PLACEBO (control, not a dial): RANDOM-TRIM, same k_t, per-name score fixed over the sample, 5 seeds.")
    say("    SMALL NOT PRICED: the candidate family has 0 of 128 / 0 of 40-120 4b cells on that panel")
    say("    (ideas 2318 / 2322 / 2326 / 2343 / 2383) — there is no pass there to keep or break.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008, so L_CAGR is the")
    say("    contaminated leg.  The trimmed-vs-untrimmed contrast is same-tape and first-order immune.")
    gate("G7 exactly two tuned parameters", "f, g", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = (px, list(px.columns))
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u, inv_u = panels["U56"]

    # G2 the gate is the live one, unmodified
    inb_u, dist_u = in_set(px_u, inv_u)
    d2 = int((inb_u != (band_state(px_u[inv_u], BAND) & px_u[inv_u].notna())).sum().sum())
    gate("G2 the gate IS baseline.band_state (live clause 2), unmodified",
         f"{d2} differing cells; mean names IN {inb_u.sum(axis=1).mean():.2f}", "0", d2 == 0)

    # G1 numpy replica == engine.backtest on the LIVE book
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    d1 = float((backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                - priced(run(px_u, w_live), HEADLINE_RUNG)).abs().max())
    gate("G1 numpy replica == engine.backtest (live RULES v2)", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G1b the same on a TRIMMED book (the replica must be exact on the object actually scored)
    w_t, _, _ = trim_weights(px_u, inv_u, 0.20, 0.75, CAPS["CAP2"], "R")
    w_t = with_sweep(px_u, w_t)
    d1b = float((backtest(px_u, w_t, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                 - priced(run(px_u, w_t), HEADLINE_RUNG)).abs().max())
    gate("G1b numpy replica == engine.backtest (trimmed book, f=0.20 conv R)",
         f"max|d| {d1b:.3e}", "< 1e-12", d1b < 1e-12)

    # G3 f = 0.00 IS CAP2, under BOTH conventions, through the engine itself
    # an INDEPENDENT CAP2 construction that shares no code path with trim_weights()
    q = px_u[inv_u]
    inb0 = band_state(q, BAND) & q.notna()
    per0 = (0.75 / inb0.sum(axis=1).replace(0, np.nan)).clip(upper=CAPS["CAP2"]).fillna(0.0)
    w_ind = with_sweep(px_u, inb0.astype(float).mul(per0, axis=0).reindex(columns=px_u.columns).fillna(0.0))
    r_ind = backtest(px_u, w_ind, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d3 = max(float((r_ind - priced(run(px_u, with_sweep(px_u, trim_weights(px_u, inv_u, 0.0, 0.75, CAPS["CAP2"], c)[0])),
                                   HEADLINE_RUNG)).abs().max()) for c in CONVENTIONS)
    gate("G3 f = 0.00 == an independent CAP2 construction through engine.backtest, BOTH conventions",
         f"max|d| {d3:.3e}", "< 1e-12", d3 < 1e-12)

    # G8 causality: truncating the panel must not move the return series
    cut = px_u.index[int(len(px_u) * 0.70)]
    wtr, _, _ = trim_weights(px_u.loc[:cut], inv_u, 0.20, 0.75, CAPS["CAP2"], "R")
    tr = run(px_u.loc[:cut], with_sweep(px_u.loc[:cut], wtr))
    fu = run(px_u, w_t)
    d8 = float((tr["r0"] - fu["r0"].loc[:cut]).abs().max())
    gate(f"G8 no lookahead (panel truncated at {cut.date()}, f=0.20 conv R)",
         f"max|dr| {d8:.3e}", "< 1e-12", d8 < 1e-12)

    # G11 the trim arithmetic: keep + dropped == N_in, and dropped == floor(f*N_in) on every row
    bad = 0
    for f in FVALS:
        _, n_in, n_keep = trim_weights(px_u, inv_u, f, 0.75, CAPS["CAP2"], "R")
        want = np.floor(f * n_in.values).astype(int)
        bad += int(((n_in.values - n_keep.values) != want).sum())
    gate("G11 dropped count == floor(f x N_in) on every row, every f",
         f"{bad} violating rows of {len(px_u) * len(FVALS)}", "0", bad == 0)

    # ---------------------------------------------------------------- the grid
    rows, expo = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        yrs = len(win) / 252
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run(px, rules_v2_weights(px, band=BAND, gross=0.75)), HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname} ({len(invest)} investable)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}"
            f"  halves {halves(base_r)[0]:.4f}/{halves(base_r)[1]:.4f}")
        say(f"    4b bars here: DD cap {DD_CAP * maxdd(spy):.2%}   CAGR floor {CAGR_FLOOR * cagr(spy):.2%}"
            f"   SPY halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f}   SPY OOS Sharpe {sharpe(spy_oos):.4f}")
        scores = {s: pd.Series(np.random.default_rng(1000 + s).random(len(invest)), index=invest)
                  for s in SEEDS}
        arms = [("EXT", None, np.nan)] + [("RAND", scores[s], s) for s in SEEDS]
        for cname, cap in CAPS.items():
            for gross in GROSSES:
                for conv in CONVENTIONS:
                    for f in FVALS:
                        for arm, sc, seed in arms:
                            if arm == "RAND" and (f == 0.0 or gross != 0.75 or cname != "CAP2"):
                                continue        # placebo priced only at the live cell
                            w, n_in, n_keep = trim_weights(px, invest, f, gross, cap, conv, score=sc)
                            res = run(px, with_sweep(px, w))
                            expo.append(dict(panel=pname, arm=arm, seed=seed, cap=cname, conv=conv, f=f,
                                             gross=gross,
                                             n_in=float(n_in.loc[win].mean()),
                                             n_keep=float(n_keep.loc[win].mean()),
                                             nheld=float(res["nheld"].loc[win].mean()),
                                             mean_risk_gross=float(res["risk_gross"].loc[win].mean()),
                                             mean_shy=float((res["gross"] - res["risk_gross"]).loc[win].mean()),
                                             max_name_w=float(res["maxw"].loc[win].max()),
                                             mean_max_name_w=float(res["maxw"].loc[win].mean()),
                                             turnover_yr=float(res["turnover"].loc[win].sum() / yrs),
                                             max_row_sum=float(res["gross"].max()),
                                             real_vol=float(priced(res, HEADLINE_RUNG).loc[win].std() * np.sqrt(252))))
                            for rung in RUNGS:
                                r = priced(res, rung).loc[win]
                                r_oos = r.loc[OOS_START:]
                                h1, h2 = halves(r)
                                rows.append(dict(panel=pname, arm=arm, seed=seed, cap=cname, conv=conv,
                                                 f=f, gross=gross, cost_bps=rung,
                                                 CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                                 H1=h1, H2=h2,
                                                 IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                                 OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                                 spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                                                 spy_OOS_MaxDD=maxdd(spy_oos),
                                                 base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                                                 **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); ef = pd.DataFrame(expo)
    df.to_csv(f"{OUT}.grid.csv", index=False); ef.to_csv(f"{OUT}.exposure.csv", index=False)

    gate("G4 no leverage (all books, realised row sums)", f"max row sum {ef.max_row_sum.max():.9f}",
         "<= 1+1e-12", bool((ef.max_row_sum <= 1 + 1e-12).all()))
    shy_ok = all(bool(p[SWEEP].loc[p.index[WARMUP:]].notna().all()) for p, _ in panels.values())
    gate("G6 sweep instrument priced on every scored row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    e_ext = ef[ef.arm == "EXT"]
    mono = []
    for (pn, cn, cv, g), grp in e_ext.groupby(["panel", "cap", "conv", "gross"]):
        v = grp.set_index("f").reindex(FVALS).n_keep.values
        mono.append(bool(np.all(np.diff(v) < -1e-9)))
    gate("G5 the f dial BITES: mean names KEPT is strictly decreasing in f",
         f"{sum(mono)} of {len(mono)} (panel, cap, conv, gross) cells", f"{len(mono)} of {len(mono)}",
         all(mono))

    monod = []
    for (pn, cn, g), grp in e_ext[e_ext.conv == "D"].groupby(["panel", "cap", "gross"]):
        v = grp.set_index("f").reindex(FVALS).mean_risk_gross.values
        monod.append(bool(np.all(np.diff(v) < -1e-9)))
    gate("G9 convention D IS a pure de-grosser: mean RISK gross strictly decreasing in f",
         f"{sum(monod)} of {len(monod)} cells", f"{len(monod)} of {len(monod)}", all(monod))

    h = df[(df.panel == "U56") & (df.arm == "EXT") & (df.cap == "CAP2") & (df.conv == "R")
           & (df.f == 0.00) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    e0 = ef[(ef.panel == "U56") & (ef.arm == "EXT") & (ef.cap == "CAP2") & (ef.conv == "R")
            & (ef.f == 0.00) & (ef.gross == 0.75)].iloc[0]
    d10 = max(abs(h.CAGR - 0.1162), abs(h.Sharpe - 1.2687) / 10, abs(h.MaxDD + 0.1481),
              abs(h.OOS_CAGR - 0.1277), abs(h.OOS_Sharpe - 1.3318) / 10)
    gate("G10 reproduces the committed CAP2 U56 headline (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f},"
         f" turnover {e0.turnover_yr:.2f}x (committed 3.51x) -> max|d| {d10:.2e}", "< 1e-3", d10 < 1e-3)

    # ---------------------------------------------------------------- A. the full ladder
    say(f"\n=== A. THE FULL LADDER AT {HEADLINE_RUNG:.0f} bps, gross 0.75, cap CAP2 — every point, both conventions ===")
    say("  panel conv    f |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | 4a 4b | H1/H2/OOS/DD/CAGR | keep  maxw  turn/yr")
    for pname in panels:
        for conv in CONVENTIONS:
            for f in FVALS:
                r = df[(df.panel == pname) & (df.arm == "EXT") & (df.cap == "CAP2") & (df.conv == conv)
                       & (df.f == f) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                e = ef[(ef.panel == pname) & (ef.arm == "EXT") & (ef.cap == "CAP2") & (ef.conv == conv)
                       & (ef.f == f) & (ef.gross == 0.75)].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  {pname:5s}  {conv}  {f:4.2f} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {e.n_keep:5.1f} {e.mean_max_name_w:5.2%} {e.turnover_yr:7.2f}"
                    + ("   <= CAP2 (anchor)" if f == 0.00 else ""))

    # ---------------------------------------------------------------- B. the exchange rate
    say("\n=== B. DOES THE TRIM BUY `L_DD` WITHOUT PAYING `L_CAGR`?  deltas vs the CAP2 anchor (10 bps, g=0.75, CAP2) ===")
    say("    ('pp of CAGR given up per pp of drawdown bought'; < 1.0 is better than the one-for-one")
    say("     exchange idea 2381 measured for every pure exposure dial.)")
    xr = []
    for pname in panels:
        for conv in CONVENTIONS:
            ref = df[(df.panel == pname) & (df.arm == "EXT") & (df.cap == "CAP2") & (df.conv == conv)
                     & (df.f == 0.00) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            say(f"  {pname} conv {conv} anchor: {ref.CAGR:.2%} / {ref.Sharpe:.4f} / {ref.MaxDD:.2%}"
                f"  (m_DD {ref.m_DD:+.4f}, m_CAGR {ref.m_CAGR:+.4f})")
            for f in FVALS:
                if f == 0.00:
                    continue
                r = df[(df.panel == pname) & (df.arm == "EXT") & (df.cap == "CAP2") & (df.conv == conv)
                       & (df.f == f) & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                dd_b = r.MaxDD - ref.MaxDD
                cg_p = ref.CAGR - r.CAGR
                rate = cg_p / dd_b if abs(dd_b) > 1e-9 else np.nan
                xr.append(dict(panel=pname, conv=conv, f=f, dd_bought=dd_b, cagr_paid=cg_p, rate=rate,
                               dSharpe=r.Sharpe - ref.Sharpe, pass4b=bool(r.pass4b)))
                say(f"    f {f:4.2f}:  dCAGR {r.CAGR - ref.CAGR:+6.2%}  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}"
                    f"  dMaxDD {dd_b:+6.2%}  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}"
                    f"  |  rate {rate:7.2f}  | 4b {'Y' if r.pass4b else '.'}")
    xrd = pd.DataFrame(xr); xrd.to_csv(f"{OUT}.exchange.csv", index=False)
    fin = xrd[np.isfinite(xrd.rate)]
    say(f"  over the {len(fin)} finite cells: rate min {fin.rate.min():.2f}  median {fin.rate.median():.2f}"
        f"  max {fin.rate.max():.2f}   cells at rate < 1.0: {int((fin.rate < 1.0).sum())} of {len(fin)}")
    say(f"  cells where the trim made drawdown WORSE (dMaxDD < 0): {int((xrd.dd_bought < 0).sum())} of {len(xrd)}")
    say(f"  cells where Sharpe IMPROVED (dSharpe > 0):             {int((xrd.dSharpe > 0).sum())} of {len(xrd)}")

    # ---------------------------------------------------------------- C. the placebo
    say("\n=== C. THE CONTROL — EXTENDEDNESS TRIM vs RANDOM TRIM at the same k_t (10 bps, g=0.75, CAP2) ===")
    say("    (THE DECIDING TEST.  Same count dropped, same de-grossing, only the criterion differs.")
    say("     If EXT does not beat its own random placebo, the trim is exposure, not extendedness.)")
    say("  panel conv    f |  EXT CAGR/Sharpe/MaxDD  |  RAND mean (5 seeds)     | RAND min..max Sharpe | EXT rank")
    pl = []
    for pname in panels:
        for conv in CONVENTIONS:
            for f in FVALS:
                if f == 0.00:
                    continue
                q = df[(df.panel == pname) & (df.cap == "CAP2") & (df.conv == conv) & (df.f == f)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)]
                e = q[q.arm == "EXT"].iloc[0]
                rd = q[q.arm == "RAND"]
                rank = int((rd.Sharpe >= e.Sharpe).sum()) + 1      # 1 = EXT best of 6
                pl.append(dict(panel=pname, conv=conv, f=f, ext_Sharpe=e.Sharpe, ext_MaxDD=e.MaxDD,
                               ext_CAGR=e.CAGR, rand_Sharpe=rd.Sharpe.mean(), rand_MaxDD=rd.MaxDD.mean(),
                               rand_CAGR=rd.CAGR.mean(), rand_Sharpe_min=rd.Sharpe.min(),
                               rand_Sharpe_max=rd.Sharpe.max(), ext_rank_of_6=rank,
                               ext_beats_rand_mean=bool(e.Sharpe > rd.Sharpe.mean()),
                               ext_dd_beats_rand_mean=bool(e.MaxDD > rd.MaxDD.mean()),
                               ext_4b=bool(e.pass4b), rand_4b=int(rd.pass4b.sum())))
                say(f"  {pname:5s}  {conv}  {f:4.2f} | {e.CAGR:6.2%} {e.Sharpe:7.4f} {e.MaxDD:8.2%} |"
                    f" {rd.CAGR.mean():6.2%} {rd.Sharpe.mean():7.4f} {rd.MaxDD.mean():8.2%} |"
                    f" {rd.Sharpe.min():7.4f}..{rd.Sharpe.max():7.4f} | {rank} of 6"
                    f"   4b EXT {'Y' if e.pass4b else '.'} RAND {int(rd.pass4b.sum())}/5")
    pld = pd.DataFrame(pl); pld.to_csv(f"{OUT}.placebo.csv", index=False)
    say(f"  EXT beats the RANDOM-trim mean Sharpe in {int(pld.ext_beats_rand_mean.sum())} of {len(pld)} cells"
        f"  (chance level 0.5 -> {len(pld) / 2:.1f})")
    say(f"  EXT has a SHALLOWER MaxDD than the RANDOM-trim mean in {int(pld.ext_dd_beats_rand_mean.sum())} of {len(pld)} cells")
    say(f"  EXT is the BEST of its own 6-book bundle (rank 1) in {int((pld.ext_rank_of_6 == 1).sum())} of {len(pld)} cells"
        f"   [chance level {len(pld) / 6:.1f}];  mean rank {pld.ext_rank_of_6.mean():.2f} (chance 3.50)")

    # ---------------------------------------------------------------- D. keep counts
    de = df[df.arm == "EXT"]
    say(f"\n=== D. KEEP COUNTS OVER ALL {len(de)} EXT ROWS (5 f x 2 conv x 2 cap x 2 gross x 2 panels x 4 rungs) ===")
    say(f"  4b passes: {int(de.pass4b.sum())} of {len(de)}      4a passes: {int(de.pass4a.sum())} of {len(de)}")
    for rung in RUNGS:
        dd = de[de.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}"
            "   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~dd[k][~dd.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for f in FVALS:
        dd = de[de.f == f]
        say(f"   f {f:4.2f}: 4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}")
    for conv in CONVENTIONS:
        dd = de[de.conv == conv]
        say(f"   conv {conv}: 4b {int(dd.pass4b.sum()):3d}/{len(dd)}   4a {int(dd.pass4a.sum()):3d}/{len(dd)}")

    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same arm, cap, conv, f, gross, rung):")
    jt = []
    for cn in CAPS:
        for conv in CONVENTIONS:
            for f in FVALS:
                for g in GROSSES:
                    for rung in RUNGS:
                        q = de[(de.cap == cn) & (de.conv == conv) & (de.f == f) & (de.gross == g)
                               & (de.cost_bps == rung)]
                        u = q[q.panel == "U56"].iloc[0]; b = q[q.panel == "B136"].iloc[0]
                        jt.append(dict(cap=cn, conv=conv, f=f, gross=g, cost_bps=rung,
                                       joint=bool(u.pass4b and b.pass4b)))
    jf = pd.DataFrame(jt); jf.to_csv(f"{OUT}.joint.csv", index=False)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells"
        f"   [CAP2 anchor f = 0.00: {int(jf[jf.f == 0.00].joint.sum())} of {len(jf[jf.f == 0.00])}]")
    for conv in CONVENTIONS:
        say(f"   conv {conv}: " + "  ".join(
            f"f {f:4.2f} {int(jf[(jf.conv == conv) & (jf.f == f)].joint.sum())}/{len(jf[(jf.conv == conv) & (jf.f == f)])}"
            for f in FVALS))
    say("   joint 4b at the LIVE gross 0.75, cap CAP2 only: " + "  ".join(
        f"{conv}/f{f:4.2f} {int(jf[(jf.conv == conv) & (jf.f == f) & (jf.gross == 0.75) & (jf.cap == 'CAP2')].joint.sum())}/4"
        for conv in CONVENTIONS for f in FVALS))

    say("\n  4b PASSES WITH f > 0.00 (the DEVICE passing, not the anchor) — every one, listed:")
    pb = de[(de.pass4b) & (de.f > 0.00)]
    if len(pb) == 0:
        say("    NONE")
    else:
        for _, r in pb.iterrows():
            say(f"    {r.panel:5s} {r.cap} conv {r.conv} f {r.f:4.2f} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
                f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  halves {r.H1:.4f}/{r.H2:.4f}"
                f"  OOS {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}")

    say("\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse) — every one, listed:")
    pa = de[de.pass4a]
    if len(pa) == 0:
        say("    NONE")
    else:
        for _, r in pa.iterrows():
            say(f"    {r.panel:5s} {r.cap} conv {r.conv} f {r.f:4.2f} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
                f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  halves {r.H1:.4f}/{r.H2:.4f}"
                f"  4b {'Y' if r.pass4b else '.'}")

    # ---------------------------------------------------------------- E. the device's own bill
    say("\n=== E. THE DEVICE'S OWN BILL, MEASURED NOT ASSUMED (EXT, CAP2, g=0.75, 10 bps) ===")
    say("  panel conv    f | N_in  N_keep  held | risk gross  mean SHY | max name w (mean/max) | turn/yr  vs CAP2 | real vol")
    for pname in panels:
        for conv in CONVENTIONS:
            a = ef[(ef.panel == pname) & (ef.arm == "EXT") & (ef.cap == "CAP2") & (ef.conv == conv)
                   & (ef.f == 0.00) & (ef.gross == 0.75)].iloc[0]
            for f in FVALS:
                e = ef[(ef.panel == pname) & (ef.arm == "EXT") & (ef.cap == "CAP2") & (ef.conv == conv)
                       & (ef.f == f) & (ef.gross == 0.75)].iloc[0]
                say(f"  {pname:5s}  {conv}  {f:4.2f} | {e.n_in:5.1f} {e.n_keep:6.1f} {e.nheld:6.1f} |"
                    f" {e.mean_risk_gross:10.3f} {e.mean_shy:9.3f} | {e.mean_max_name_w:8.2%} / {e.max_name_w:6.2%} |"
                    f" {e.turnover_yr:7.2f} {e.turnover_yr - a.turnover_yr:+7.2f} | {e.real_vol:8.4f}")

    # ---------------------------------------------------------------- F. rule 8
    say("\n=== F. RULE 8 — f chosen on <= 2016-12-31 ONLY, 2017-2026 read ONCE ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run(px, rules_v2_weights(px, band=BAND, gross=0.75)), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for cn in CAPS:
            for conv in CONVENTIONS:
                for g in GROSSES:
                    for rung in RUNGS:
                        dd = de[(de.panel == pname) & (de.cap == cn) & (de.conv == conv)
                                & (de.gross == g) & (de.cost_bps == rung)]
                        inc = dd[dd.f == 0.00].iloc[0]
                        for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                            pk = dd.loc[dd[col].idxmax()]
                            wf.append(dict(panel=pname, cap=cn, conv=conv, gross=g, cost_bps=rung,
                                           chooser=chooser, pick_f=float(pk.f),
                                           pick_is_cap2=bool(pk.f == 0.00), full4b=bool(pk.pass4b),
                                           OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                           OOS_MaxDD=pk.OOS_MaxDD,
                                           inc_OOS_CAGR=inc.OOS_CAGR, inc_OOS_Sharpe=inc.OOS_Sharpe,
                                           inc_OOS_MaxDD=inc.OOS_MaxDD,
                                           base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos),
                                           base_OOS_MaxDD=maxdd(b_oos),
                                           spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos),
                                           spy_OOS_MaxDD=maxdd(spy_oos)))
                            if cn == "CAP2" and g == 0.75:
                                say(f"  {pname:5s} conv {conv} g{g:.2f} {rung:5.1f}bps {chooser:11s} -> f {pk.f:4.2f} |"
                                    f" OOS {pk.OOS_CAGR:6.2%} / {pk.OOS_Sharpe:.4f} / {pk.OOS_MaxDD:7.2%} |"
                                    f" CAP2 anchor OOS {inc.OOS_CAGR:6.2%} / {inc.OOS_Sharpe:.4f} / {inc.OOS_MaxDD:7.2%} |"
                                    f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} / {maxdd(b_oos):7.2%} |"
                                    f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} / {maxdd(spy_oos):7.2%} |"
                                    f" full 4b {'Y' if pk.pass4b else '.'}")
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  {len(wfd)} picks (2 panels x 2 caps x 2 conv x 2 gross x 4 rungs x 2 choosers).")
    say(f"   picks landing on the CAP2 ANCHOR (f = 0.00, i.e. NO trim):   {int(wfd.pick_is_cap2.sum())} of {len(wfd)}")
    say(f"   picks beating SPY's OOS Sharpe:                      {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:            {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the CAP2 ANCHOR's own OOS Sharpe:      {int((wfd.OOS_Sharpe > wfd.inc_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks with SHALLOWER OOS MaxDD than the CAP2 anchor: {int((wfd.OOS_MaxDD > wfd.inc_OOS_MaxDD).sum())} of {len(wfd)}")
    say(f"   picks with HIGHER OOS CAGR than the CAP2 anchor:     {int((wfd.OOS_CAGR > wfd.inc_OOS_CAGR).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:                {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution over f: " + "  ".join(f"{f:4.2f}:{int((wfd.pick_f == f).sum())}" for f in FVALS))
    agree = both4b = 0
    for cn in CAPS:
        for conv in CONVENTIONS:
            for g in GROSSES:
                for rung in RUNGS:
                    for ch in ("C_ISSHARPE", "C_ISCALMAR"):
                        q = wfd[(wfd.cap == cn) & (wfd.conv == conv) & (wfd.gross == g)
                                & (wfd.cost_bps == rung) & (wfd.chooser == ch)]
                        u = q[q.panel == "U56"].iloc[0]; b = q[q.panel == "B136"].iloc[0]
                        if u.pick_f == b.pick_f:
                            agree += 1
                            both4b += int(bool(u.full4b and b.full4b))
    say(f"   U56 and B136 agree on f in {agree} of 64 (cap x conv x gross x rung x chooser) cells")
    say(f"   cells where both panels agree AND both carry a full-sample 4b: {both4b} of 64")

    gf = pd.DataFrame(GATES); gf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gf.pass_.sum())} of {len(gf)} pass ===")
    for _, r in gf[~gf.pass_].iterrows():
        say(f"    FAILED: {r.gate} -> {r.value}")
    say(f"\nwrote {OUT}.grid.csv / .exposure.csv / .exchange.csv / .placebo.csv / .joint.csv /"
        f" .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
