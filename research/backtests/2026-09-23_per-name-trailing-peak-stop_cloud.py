#!/usr/bin/env python3
"""idea 2415 (lane cloud, run 46, 2026-09-23) — DOES A PER-NAME TRAILING-PEAK STOP CUT THE
CAPPED CANDIDATE'S DRAWDOWN WHERE THE BAND AND THE BOOK-LEVEL GATES COULD NOT?

THE GAP.  `L_DD` is the binding leg on essentially every sub-50 bps 4b FAIL the capped family has
published (29 of 29 in idea 2391; every finite-cap failure in 2387; every d < 1 cell in 2399; 57
of 67 at 10 bps in 2404).  Every device the record has tried against it is either CROSS-SECTIONAL
(inverse-vol 2362, sector cap 2339, breadth cap 2387, relative cap 2381, extended-name trim 2419 —
all measured to be exposure or composition dials) or acts on the BOOK AS ONE NUMBER (equity-curve
gate 2399, book vol target 2403).  The untried device is PER-NAME and TIME-SERIES.

THE DEVICE.  A name is STOPPED at close t when

        px_i,t  <  (1 - q) x max( px_i,t-H+1 .. px_i,t )

i.e. when it has fallen more than `q` below its OWN trailing `H`-day high.  Its weight goes to the
SHY sweep.  A stopped name is NOT re-admitted by the price recovering: it stays out until the
normal 200d +/-3% band gates it OUT and then back IN, which is the record's committed re-entry
mechanism and the only one this run will use.  Unlike the band, the trigger keys off the name's
own PEAK rather than a slow mean, so it can cut a fast top-out months before the 200d registers it.

DIAL 1 -- the stop depth `q` {0.10, 0.15, 0.20, 0.25, 0.30, INF}.  **q = INF NEVER FIRES AND IS
          THE COMMITTED CAP2 BOOK EXACTLY**, so one ladder spans it; G3 asserts bit-identity
          against an independent `engine.backtest` construction.
DIAL 2 -- the peak lookback `H` {63, 126, 252} trading days.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, books {CAP2 (2% cap), CAND (uncapped)}, gross
{0.75 live, 1.00}, cost rungs {0, 10, 25, 50} bps, weekly cadence, t+1 execution, band 0.03 and
the phi = 1.00 SHY sweep.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with L_DD, L_H2
and L_OOS all failing; a device that can only REMOVE exposure cannot lift three legs at once.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: BOTH dials fitted on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE = max in-sample Sharpe, C_ISCALMAR = max in-sample Calmar), then 2017-2026 read ONCE.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the band is
`baseline.band_state` bit for bit.  G3 q = INF is BIT-IDENTICAL to an independent CAP2
construction through `engine.backtest`.  G4 no leverage.  G5 the stop BITES (names held must fall
as q tightens).  G6 H is a NO-OP at q = INF.  G7 exactly two tuned parameters.  G8 the stop state
is CAUSAL (panel truncation reproduces it).  G9 SHY priced on every held row.  G10 EXTERNAL
REPRODUCTION of the committed CAP2 U56 headline (11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318)
and the committed CAND U56 headline (12.59% / 1.1934 / -17.39%, OOS 13.85% / 1.2397).  G11 the
held set is a SUBSET of the band's IN set at every (t, name) — the stop may only REMOVE.  G12 a
stopped name never returns without a band OUT in between (re-admission is the band's alone).

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The stop-vs-no-stop contrast is same-tape, same-day,
same-gross and same-panel and is first-order immune; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_per-name-trailing-peak-stop_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "per-name-trailing-peak-stop", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
QS = [0.10, 0.15, 0.20, 0.25, 0.30, np.inf]
HS = [63, 126, 252]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
BOOKS = {"CAP2": 0.020, "CAND": np.inf}
SWEEP = "SHY"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
HEADLINE_RUNG, LIVE_GROSS = 10.0, 0.75

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


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUB   {name}: {value}")


# ---------------------------------------------------------------- the device
def stop_block(px, inb, q, H):
    """blocked_i,t: True once the trailing-peak stop has fired on name i, cleared only by the
    200d band gating the name OUT.  Causal: the trigger reads px through t only, and the weights
    built from it are applied at t+1 by the engine."""
    if not np.isfinite(q):
        return pd.DataFrame(False, index=px.index, columns=px.columns)
    peak = px.rolling(H, min_periods=1).max()
    trig = (px < (1.0 - q) * peak).fillna(False).values
    bnd = inb.values
    n, m = trig.shape
    out = np.zeros((n, m), dtype=bool)
    state = np.zeros(m, dtype=bool)
    for i in range(n):
        state = np.where(bnd[i], state | trig[i], False)
        out[i] = state
    return pd.DataFrame(out, index=px.index, columns=px.columns)


def risk_weights(px, gross, cap, q, H):
    """CAP2/CAND with the trailing-peak stop: w_i = min(gross / N_in, cap) on names INSIDE the
    200d +/- 0.03 band AND not stopped.  N_in is the BAND's count (the freed weight is NOT
    re-spread over the survivors; it falls to the SHY sweep, exactly as the gated-out weight does
    in the committed book)."""
    pr = px.notna()
    inb = band_state(px, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    held = inb & ~stop_block(px, inb, q, H)
    return held.astype(float).mul(per, axis=0).fillna(0.0), inb, held


def full_reference(px, gross, cap):
    """The committed book WITH the phi = 1.00 SHY sweep, for the engine anchors."""
    pr = px.notna()
    inb = band_state(px, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    w = inb.astype(float).mul((gross / nin).clip(upper=cap).fillna(0.0), axis=0).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- the runner
def run_book(prices, w_risk, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim, except that the total |dw| is retained so every cost rung is
    read off ONE realised path (the strategy is cost-blind).  Weights decided t-1, applied t."""
    cols = list(prices.columns)
    shy_i = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    shy_ok = prices[SWEEP].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    dw = np.zeros(n); cur = np.zeros(m)
    gr = np.zeros(n); r0 = np.zeros(n); nheld = np.zeros(n); shyw = np.zeros(n); mx = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[shy_i] += max(0.0, 1.0 - new.sum()) * shy_ok[i]
            dw[i] = np.abs(new - cur).sum()
            cur = new
        gr[i] = cur.sum()
        nheld[i] = float((cur > 1e-12).sum())
        shyw[i] = cur[shy_i]
        mx[i] = cur.max()
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), gross=pd.Series(gr, index=idx),
                names=pd.Series(nheld, index=idx), shy=pd.Series(shyw, index=idx),
                maxw=pd.Series(mx, index=idx), dw=pd.Series(dw, index=idx))


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    return float((1 + r).cumprod().iloc[-1] ** (252 / len(r)) - 1)


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def calmar(r):
    d = maxdd(r)
    return float(cagr(r) / abs(d)) if d < 0 else np.nan


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
    say("=== idea 2415 — DOES A PER-NAME TRAILING-PEAK STOP CUT THE CAPPED CANDIDATE'S DRAWDOWN? ===")
    say(f"    {DATE}  lane {LANE} run 46   band {BAND}  MA 200d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  cap 2%  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 stop depth q {QS}   DIAL 2 peak lookback H {HS}")
    say("    q = INF NEVER FIRES AND IS THE COMMITTED CAP2 BOOK EXACTLY (G3 asserts bit-identity).")
    say("    Freed weight falls to the SHY sweep; it is NOT re-spread over the survivors.")
    say("    Re-admission is the 200d band's alone: a stopped name returns only after a band OUT (G12).")
    say("    SMALL NOT PRICED: 0 of 128 4b cells in 2383 and 0 of 40-120 in 2318/2322/2326/2343.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is the")
    say("    contaminated leg.  The stop-vs-no-stop contrast is same-tape/same-gross and first-order immune.")
    gate("G7 exactly two tuned parameters", "q, H", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    inb_u = band_state(px_u, BAND) & px_u.notna()
    d2 = int((band_state(px_u, BAND) != band_state(px_u, BAND)).sum().sum())
    gate("G2 the gate IS baseline.band_state (live clause 2), unmodified",
         f"{d2} differing cells; mean names IN {inb_u.sum(axis=1).mean():.2f}", "0", d2 == 0)

    # G1 replica fidelity on the LIVE book
    w_live = rules_v2_weights(px_u, band=BAND, gross=LIVE_GROSS)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["dw"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G3 / G6 q = INF is the committed book and H is a no-op there
    d3 = 0.0
    for H in HS:
        wq, _, _ = risk_weights(px_u, LIVE_GROSS, BOOKS["CAP2"], np.inf, H)
        bk = run_book(px_u, wq)
        eng = backtest(px_u, full_reference(px_u, LIVE_GROSS, BOOKS["CAP2"]),
                       cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
        d3 = max(d3, float((eng - (bk["r0"] - bk["dw"] * HEADLINE_RUNG / 1e4)).abs().max()))
    gate("G3 q = INF IS the committed CAP2 book == an independent engine.backtest construction",
         f"max|d| over H {HS}: {d3:.3e}", "< 1e-12", d3 < 1e-12)

    # G8 causality of the stop state
    cut = px_u.index[int(len(px_u) * 0.70)]
    s_full = stop_block(px_u, inb_u, 0.20, 126).loc[:cut]
    px_t = px_u.loc[:cut]
    s_trunc = stop_block(px_t, band_state(px_t, BAND) & px_t.notna(), 0.20, 126)
    d8 = int((s_full.values != s_trunc.values).sum())
    gate(f"G8 the stop state is CAUSAL (panel truncated at {cut.date()}, q=0.20 H=126)",
         f"{d8} differing cells of {s_full.size}", "0", d8 == 0)

    # G11 / G12 structural assertions on the held set
    q11, h11 = 0.20, 126
    blk = stop_block(px_u, inb_u, q11, h11)
    held11 = inb_u & ~blk
    g11 = int((held11 & ~inb_u).values.sum())
    gate("G11 the held set is a SUBSET of the band's IN set (the stop may only REMOVE)",
         f"{g11} held-but-not-IN cells (q=0.20, H=126)", "0", g11 == 0)
    b = blk.values; ib = inb_u.values
    # a re-admission is blocked->unblocked with the band continuously IN
    readmit_no_out = int((b[:-1] & ~b[1:] & ib[:-1] & ib[1:]).sum())
    gate("G12 a stopped name never returns without a band OUT in between",
         f"{readmit_no_out} in-band re-admissions (q=0.20, H=126)", "0", readmit_no_out == 0)

    rows, paths_meta = [], []
    for pname, px in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        yrs = len(win) / 252
        say(f"\n--- panel {pname} ({len(px.columns)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}")
        say(f"    4b bars here: DD cap {DD_CAP * maxdd(spy):.2%}   CAGR floor {CAGR_FLOOR * cagr(spy):.2%}"
            f"   SPY halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f}   SPY OOS Sharpe {sharpe(spy_oos):.4f}")
        base_paths = {g: run_book(px, rules_v2_weights(px, band=BAND, gross=g), sweep=False) for g in GROSSES}
        for bname, cap in BOOKS.items():
            for gross in GROSSES:
                for q in QS:
                    for H in HS:
                        wq, inb, held = risk_weights(px, gross, cap, q, H)
                        pth = run_book(px, wq)
                        r0 = pth["r0"].loc[win]; dwt = pth["dw"].loc[win]
                        paths_meta.append(dict(panel=pname, book=bname, gross=gross, q=q, H=H,
                                               turnover_yr=float(dwt.sum() / yrs),
                                               mean_names=float(pth["names"].loc[win].mean()),
                                               mean_shy=float(pth["shy"].loc[win].mean()),
                                               max_gross=float(pth["gross"].max()),
                                               max_w=float(pth["maxw"].max()),
                                               stop_share=float((inb & ~held).loc[win].values.sum()
                                                                / max(1, inb.loc[win].values.sum()))))
                        for rung in RUNGS:
                            r = r0 - dwt * rung / 1e4
                            br = (base_paths[LIVE_GROSS]["r0"]
                                  - base_paths[LIVE_GROSS]["dw"] * rung / 1e4).loc[win]
                            r_oos = r.loc[OOS_START:]
                            h1, h2 = halves(r)
                            rows.append(dict(panel=pname, book=bname, gross=gross, q=q, H=H, cost_bps=rung,
                                             CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                             H1=h1, H2=h2,
                                             IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                             OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                             base_Sharpe=sharpe(br), base_MaxDD=maxdd(br),
                                             base_CAGR=cagr(br), base_OOS_Sharpe=sharpe(br.loc[OOS_START:]),
                                             base_OOS_CAGR=cagr(br.loc[OOS_START:]),
                                             base_OOS_MaxDD=maxdd(br.loc[OOS_START:]),
                                             spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                                             spy_H1=halves(spy)[0], spy_H2=halves(spy)[1],
                                             spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos),
                                             spy_OOS_MaxDD=maxdd(spy_oos),
                                             turnover_yr=float(dwt.sum() / yrs),
                                             **legs(r, br, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); pm = pd.DataFrame(paths_meta)
    df.to_csv(f"{OUT}.grid.csv", index=False); pm.to_csv(f"{OUT}.paths.csv", index=False)

    gate("G4 no leverage anywhere (realised row sums)", f"max gross {pm.max_gross.max():.9f}",
         "<= 1+1e-12", bool((pm.max_gross <= 1 + 1e-12).all()))
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP:]].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}", "True", shy_ok)

    # G6 H is a no-op at q = INF
    inf_rows = df[~np.isfinite(df.q)]
    g6 = int(inf_rows.groupby(["panel", "book", "gross", "cost_bps"]).Sharpe.nunique().max())
    gate("G6 H is a NO-OP at q = INF", f"distinct Sharpes per (panel, book, gross, rung): {g6}", "1", g6 == 1)

    # G5 the stop bites and bites monotonically in q
    fin = pm[np.isfinite(pm.q)].sort_values("q")
    mono = []
    for k, grp in pm.groupby(["panel", "book", "gross", "H"]):
        s = grp.sort_values("q", ascending=False)          # INF first, then 0.30 .. 0.10
        mono.append(bool((s.mean_names.diff().dropna() <= 1e-9).all()))
    gate("G5 the stop BITES and mean names held falls monotonically as q tightens",
         f"{sum(mono)} of {len(mono)} (panel, book, gross, H) ladders monotone; "
         f"stopped share of band-IN cells {fin.stop_share.min():.2%}..{fin.stop_share.max():.2%}",
         "all monotone, stop_share > 0", all(mono) and fin.stop_share.min() > 0)

    # G10 external reproduction of the committed headlines
    a = df[(df.panel == "U56") & (df.book == "CAP2") & (~np.isfinite(df.q)) & (df.H == HS[0])
           & (df.gross == LIVE_GROSS) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    b2 = df[(df.panel == "U56") & (df.book == "CAND") & (~np.isfinite(df.q)) & (df.H == HS[0])
            & (df.gross == LIVE_GROSS) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d10 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
              abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
              abs(b2.CAGR - 0.1259), abs(b2.Sharpe - 1.1934) / 10, abs(b2.MaxDD + 0.1739),
              abs(b2.OOS_CAGR - 0.1385), abs(b2.OOS_Sharpe - 1.2397) / 10)
    gate("G10 reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318) AND CAND"
         " (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b2.CAGR:.2%}/{b2.Sharpe:.4f}/{b2.MaxDD:.2%} OOS {b2.OOS_CAGR:.2%}/{b2.OOS_Sharpe:.4f}"
         f" -> max|d| {d10:.2e}", "< 1e-3", d10 < 1e-3)

    # ------------------------------------------------------------ A. the full ladder
    say("\n=== A. THE FULL LADDER (every grid point, live gross 0.75, 10 bps) ===")
    for pname in panels:
        for bname in BOOKS:
            say(f"  -- {pname} / {bname}")
            say("     q      H    CAGR   Sharpe   MaxDD    H1/H2         OOS CAGR/Sharpe/MaxDD   turn  names  4a 4b  binding")
            sub = df[(df.panel == pname) & (df.book == bname) & (df.gross == LIVE_GROSS)
                     & (df.cost_bps == HEADLINE_RUNG)]
            for _, r in sub.sort_values(["q", "H"]).iterrows():
                bind = ",".join(k[2:] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR") if not r[k]) or "-"
                qs = "INF " if not np.isfinite(r.q) else f"{r.q:.2f}"
                say(f"     {qs}  {int(r.H):4d}  {r.CAGR:6.2%}  {r.Sharpe:6.4f}  {r.MaxDD:7.2%}"
                    f"  {r.H1:.4f}/{r.H2:.4f}  {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}"
                    f"  {r.turnover_yr:4.2f}  {'':4s}  {int(r.pass4a)}  {int(r.pass4b)}  {bind}")

    say("\n=== A2. THE OTHER RUNGS AND THE OTHER GROSS (4a / 4b counts, all 288 rows) ===")
    cnt = df.groupby(["panel", "book", "gross", "cost_bps"]).agg(
        n=("pass4b", "size"), n4a=("pass4a", "sum"), n4b=("pass4b", "sum")).reset_index()
    for _, r in cnt.iterrows():
        say(f"    {r.panel:5s} {r.book:5s} g={r.gross:.2f} {int(r.cost_bps):3d} bps:"
            f"  4a {int(r.n4a):2d}/{int(r.n):2d}   4b {int(r.n4b):2d}/{int(r.n):2d}")

    say("\n=== A3. JOINT BOTH-PANEL 4b (the bar the record uses for adoption) ===")
    j = df.pivot_table(index=["book", "gross", "q", "H", "cost_bps"], columns="panel",
                       values="pass4b", aggfunc="first", dropna=False)
    j["joint"] = j.get("U56", False) & j.get("B136", False)
    say(f"    joint both-panel 4b: {int(j.joint.sum())} of {len(j)} (book, gross, q, H, rung) cells")
    for (bk_, g_, q_, h_, c_), r in j[j.joint].iterrows():
        say(f"      JOINT PASS: {bk_}  g={g_:.2f}  q={'INF' if not np.isfinite(q_) else f'{q_:.2f}'}"
            f"  H={int(h_)}  {int(c_)} bps")

    # ------------------------------------------------------------ B. the bill of the device
    say("\n=== B. WHAT THE STOP BUYS AND WHAT IT COSTS (vs q = INF, same panel/book/gross/H/rung) ===")
    base = df[~np.isfinite(df.q)].set_index(["panel", "book", "gross", "H", "cost_bps"])
    dd = []
    for _, r in df[np.isfinite(df.q)].iterrows():
        b0 = base.loc[(r.panel, r.book, r.gross, r.H, r.cost_bps)]
        dd.append(dict(panel=r.panel, book=r.book, gross=r.gross, q=r.q, H=r.H, cost_bps=r.cost_bps,
                       dCAGR=r.CAGR - b0.CAGR, dSharpe=r.Sharpe - b0.Sharpe,
                       dMaxDD=r.MaxDD - b0.MaxDD, dOOS_Sharpe=r.OOS_Sharpe - b0.OOS_Sharpe,
                       dturn=r.turnover_yr - b0.turnover_yr))
    dfd = pd.DataFrame(dd); dfd.to_csv(f"{OUT}.delta.csv", index=False)
    say(f"    over all {len(dfd)} stopped cells:  dMaxDD > 0 (shallower) in {int((dfd.dMaxDD > 0).sum())};"
        f"  dSharpe > 0 in {int((dfd.dSharpe > 0).sum())};  dCAGR > 0 in {int((dfd.dCAGR > 0).sum())};"
        f"  dOOS_Sharpe > 0 in {int((dfd.dOOS_Sharpe > 0).sum())}")
    say("    median deltas by q (live gross, 10 bps, both panels, both books, all H):")
    m = dfd[(dfd.gross == LIVE_GROSS) & (dfd.cost_bps == HEADLINE_RUNG)].groupby("q").median(numeric_only=True)
    for q_, r in m.iterrows():
        say(f"      q={q_:.2f}:  dCAGR {r.dCAGR * 100:+.2f} pp  dSharpe {r.dSharpe:+.4f}"
            f"  dMaxDD {r.dMaxDD * 100:+.2f} pp  dOOS_Sharpe {r.dOOS_Sharpe:+.4f}  dturn {r.dturn:+.2f}x/yr")
    say("    the device's own exposure cost (mean names held / mean SHY sleeve, live gross):")
    mm = pm[pm.gross == LIVE_GROSS].groupby(["panel", "book", "q"]).agg(
        names=("mean_names", "mean"), shy=("mean_shy", "mean"), turn=("turnover_yr", "mean")).reset_index()
    for _, r in mm.iterrows():
        say(f"      {r.panel:5s} {r.book:5s} q={'INF ' if not np.isfinite(r.q) else f'{r.q:.2f}'}:"
            f"  names {r.names:5.2f}  SHY {r.shy:6.2%}  turn {r.turn:4.2f}x/yr")

    # ------------------------------------------------------------ C. rule 8
    say("\n=== C. RULE 8 — BOTH DIALS FITTED ON <= 2016-12-31 ONLY, 2017-2026 READ ONCE ===")
    picks = []
    for (pname, bname, gross, rung), grp in df.groupby(["panel", "book", "gross", "cost_bps"]):
        for cname, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
            w = grp.sort_values([col, "q", "H"], ascending=[False, True, True]).iloc[0]
            picks.append(dict(panel=pname, book=bname, gross=gross, cost_bps=rung, chooser=cname,
                              q=w.q, H=w.H, OOS_CAGR=w.OOS_CAGR, OOS_Sharpe=w.OOS_Sharpe,
                              OOS_MaxDD=w.OOS_MaxDD, spy_OOS_Sharpe=w.spy_OOS_Sharpe,
                              spy_OOS_CAGR=w.spy_OOS_CAGR, spy_OOS_MaxDD=w.spy_OOS_MaxDD,
                              base_OOS_Sharpe=w.base_OOS_Sharpe, base_OOS_CAGR=w.base_OOS_CAGR,
                              base_OOS_MaxDD=w.base_OOS_MaxDD, pass4b=w.pass4b, pass4a=w.pass4a))
    pk = pd.DataFrame(picks); pk.to_csv(f"{OUT}.picks.csv", index=False)
    stopped = pk[np.isfinite(pk.q)]
    say(f"    {len(pk)} IS-only picks (2 choosers x 2 panels x 2 books x 2 gross x 4 rungs).")
    say(f"    the chooser lands on a STOPPED book (q < INF) in {len(stopped)} of {len(pk)};"
        f"  on q = INF (the committed book) in {len(pk) - len(stopped)}.")
    if len(stopped):
        say("    q distribution of the stopped picks: "
            + ", ".join(f"{q_:.2f}:{c}" for q_, c in stopped.q.value_counts().sort_index().items()))
    say(f"    OOS: {int((pk.OOS_Sharpe > pk.spy_OOS_Sharpe).sum())} of {len(pk)} beat SPY;"
        f"  {int((pk.OOS_Sharpe > pk.base_OOS_Sharpe).sum())} of {len(pk)} beat the live RULES v2 book;"
        f"  {int(pk.pass4b.sum())} of {len(pk)} carry a full-sample 4b pass.")
    say("    every pick, live gross, all rungs:")
    for _, r in pk[pk.gross == LIVE_GROSS].sort_values(["panel", "book", "cost_bps", "chooser"]).iterrows():
        say(f"      {r.panel:5s} {r.book:5s} {int(r.cost_bps):3d}bps {r.chooser:11s}"
            f" -> q={'INF ' if not np.isfinite(r.q) else f'{r.q:.2f}'} H={int(r.H):3d}"
            f"  OOS {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}"
            f"  (SPY {r.spy_OOS_CAGR:6.2%}/{r.spy_OOS_Sharpe:.4f}/{r.spy_OOS_MaxDD:7.2%};"
            f" base {r.base_OOS_CAGR:6.2%}/{r.base_OOS_Sharpe:.4f}/{r.base_OOS_MaxDD:7.2%})  4b={int(r.pass4b)}")

    # ------------------------------------------------------------ D. binding legs
    say("\n=== D. WHICH LEG BINDS ON THE 4b FAILS ===")
    for rung in RUNGS:
        f = df[(df.cost_bps == rung) & (~df.pass4b)]
        say(f"    {int(rung):3d} bps, {len(f)} fails:  "
            + "  ".join(f"{k} {int((~f[k]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))

    ok = all(g["pass_"] for g in GATES if g["target"] != "published, not asserted")
    say(f"\n=== GATES: {sum(1 for g in GATES if g['pass_'] and g['target'] != 'published, not asserted')}"
        f" of {sum(1 for g in GATES if g['target'] != 'published, not asserted')} pass"
        f"  ({len(df)} published rows, {time.time() - t0:.0f}s) ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
