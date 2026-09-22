#!/usr/bin/env python3
"""idea 2326 (lane cloud, 2026-09-22) — does a MINIMUM BREADTH FLOOR on N_in beat the PER-NAME CAP
at the same job?

THE OBJECT.  Idea 2300 filed `RG100 + phi = 1.00` as the record's standing 4b candidate: every
name INSIDE the 200d +/-3% band held at `gross / N_in` of NAV, the residual `1 - sum(w)` swept to
SHY.  Its published risk is what the re-gross does when BREADTH COLLAPSES: with three names IN,
the book puts a third of gross into each.  Idea 2322 fixed that from the NAME side with a cap
(`w_i = min(gross / N_in, cap)`) and found a 2.0% cap clears 4b on both large-cap panels.  This
run prices the mirror fix, from the DAY side:

    if N_in < m:  w_i = gross / N_t   on IN names   (fall back to the de-grossed live book)
    else:         w_i = gross / N_in  on IN names   (the candidate's full re-gross)
    either way:   idle NAV -> SHY at phi = 1.00, charged the same turnover as any other leg

The two devices cut the same tail differently: the CAP binds name-by-name and is ALWAYS on, the
FLOOR binds day-by-day and is OFF in normal breadth.  If the floor holds the 4b pass it is the
cheaper fix, because it spends nothing on the 99% of days where breadth is healthy.

DIAL 1 -- breadth floor m {1, 3, 5, 8, 12, 20, INF}.  m = 1 IS the candidate (gate G2); m = INF
is the de-grossed live book with the sweep attached (gate G3), so one sweep prices the whole
family between the two known books.
DIAL 2 -- gross {0.75 (live), 1.00}.

REFERENCE BOOKS, COMPUTED AND REPORTED BUT NEVER SELECTED ON AND NEVER COUNTED AS A DIAL:
  CAP2      = idea 2322's committed headline device, `w_i = min(gross / N_in, 0.02)` + phi = 1.
  FLOORCAP  = the floor at each m WITH that same 2.0% cap attached.  The cap value is INHERITED
              from a committed result, not tuned here; the family is published as a by-product so
              the "which fix, or both?" question is answered with numbers rather than asserted.

REPORTED, NEVER SELECTED ON: 3 panels (U56 / B136 / SMALL), 4 cost rungs (0 / 10 / 25 / 50 bps),
weekly cadence, t+1 execution, band 0.03 (the live clause-2 constant), sweep instrument SHY.
15 books x 2 gross x 3 panels = 90 books, every one published at every rung = 360 rows.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
RULE 8: (m, gross) chosen on warm-up..2016-12-31 ONLY over the FLOOR family by two pre-stated
IS-only choosers (C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

SURVIVORSHIP.  U56 (research/universe.json) and B136 (research/universe_broad.json) are
CURRENT-CONSTITUENT lists; SMALL (data/prices_small.csv.gz) is a current screen of sub-$2B names
with the `max_1d_move >= 1.0` tickers dropped per data/SMALL_PANEL_README.md.  Absolute CAGRs are
survivorship-optimistic on all three panels and any 4b verdict inherits that bias.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-22_minimum-breadth-floor-vs-per-name-cap_cloud.py
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

DATE, SLUG, LANE = "2026-09-22", "minimum-breadth-floor-vs-per-name-cap", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
FLOORS = [1, 3, 5, 8, 12, 20, "INF"]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG, LIVE_GROSS = 10.0, 0.75
REF_CAP = 0.02                      # idea 2322's committed headline cap — inherited, NOT tuned
SWEEP = "SHY"
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


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUB   {name}: {value}")


def mlabel(m):
    return "INF" if m == "INF" else f"{int(m):d}"


# ---------------------------------------------------------------- books
def breadth_parts(px, invest):
    """N_t (names priced), N_in (names inside the band), and the IN mask, on the panel."""
    q = px[invest]
    pr = q.notna()
    N = pr.sum(axis=1).replace(0, np.nan)
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    return N, nin, inb


def floor_weights(px, invest, m, gross, cap=None):
    """w_i = gross / N_in on IN names when N_in >= m, else the de-grossed gross / N_t; idle -> SHY.
    cap, when given, additionally holds every name to `min(per, cap)` (the FLOORCAP by-product)."""
    N, nin, inb = breadth_parts(px, invest)
    rg = gross / nin                                    # the candidate's re-grossed per-name weight
    dg = gross / N                                      # the live de-grossed per-name weight
    if m == "INF":
        per = dg
    elif m <= 1:
        per = rg
    else:
        per = rg.where(nin >= m, dg)
    if cap is not None:
        per = pd.concat([per, pd.Series(float(cap), index=per.index)], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0)
    w = w.reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def cap_weights(px, invest, cap, gross):
    """Idea 2322's device: w_i = min(gross / N_in, cap) on IN names, idle -> SHY (phi = 1.00)."""
    N, nin, inb = breadth_parts(px, invest)
    per = pd.concat([gross / nin, pd.Series(float(cap), index=px.index)], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def rg100_reference(px, invest, gross):
    """Independent construction of idea 2300's RG100 + phi = 1.00 (scale form, not the min form)."""
    N, nin, inb = breadth_parts(px, invest)
    q = px[invest]
    e = pd.DataFrame(1.0, index=q.index, columns=q.columns).where(q.notna(), 0.0)
    dg = (gross * e.div(N, axis=0).fillna(0.0)).where(inb, 0.0)
    scale = (N / nin).replace([np.inf, -np.inf], np.nan).fillna(1.0)
    w = dg.mul(scale, axis=0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def dg_reference(px, invest, gross):
    """The LIVE de-grossed band book with the same sweep attached."""
    w = rules_v2_weights(px[invest], band=BAND, gross=gross).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


def run_book(prices, weights, freq=CADENCE):
    """Replica of engine.backtest keeping zero-cost returns + turnover so every cost rung is
    priced from one pass.  Un-invested residual drifts at 0% (engine's convention)."""
    rets = prices.pct_change().fillna(0.0)
    w_target = weights.reindex(prices.index).fillna(0.0).shift(1)
    key = prices.index.to_period(freq)
    s = pd.Series(key, index=prices.index)
    mask = (s != s.shift(-1)).shift(1, fill_value=False)
    held = np.zeros((len(prices.index), len(prices.columns)))
    cur = np.zeros(len(prices.columns))
    turnover = np.zeros(len(prices.index))
    gross_s = np.zeros(len(prices.index))
    wt = w_target.values
    rv = rets.values
    for i in range(len(prices.index)):
        if mask.iloc[i] or i == 0:
            new = wt[i]
            turnover[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        gross_s[i] = cur.sum()
        growth = cur * (1 + rv[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    r0 = pd.Series((held * rv).sum(axis=1), index=prices.index)
    return dict(r0=r0, turnover=pd.Series(turnover, index=prices.index),
                gross=pd.Series(gross_s, index=prices.index))


def priced(res, bps):
    return res["r0"] - res["turnover"] * bps / 1e4


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    eq = (1 + r).cumprod()
    return float(eq.iloc[-1] ** (252 / len(r)) - 1)


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
    h1, h2 = halves(r)
    b1, b2 = halves(base)
    p4a = (h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))
    s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(pass4a=bool(p4a), pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS), L_DD=bool(L_DD),
                L_CAGR=bool(L_CAGR))


# ---------------------------------------------------------------- panels
def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    dropped = len(px.columns) - len(keep)
    px = px[keep]
    shy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)[SWEEP]
    px = pd.concat([px, shy.reindex(px.index, method="ffill").rename(SWEEP)], axis=1)
    return px, dropped


def main():
    t0 = time.time()
    say("=== idea 2326 — does a MINIMUM BREADTH FLOOR on N_in beat the PER-NAME CAP at the same job? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 breadth floor m {[mlabel(m) for m in FLOORS]}   DIAL 2 gross {GROSSES}")
    say(f"    reference books (reported, never selected on, never a dial): CAP2 = idea 2322's cap {REF_CAP:.1%};"
        f" FLOORCAP = floor(m) + that same cap")
    gate("G8 exactly two tuned parameters", "breadth floor m, gross", "2", True)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    px_s, dropped = small_panel()
    gate("G7 dropped-ticker rule bit (SMALL)", f"{dropped} names dropped (max_1d_move >= 1.0)",
         ">= 1", dropped >= 1)

    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b), ("SMALL", px_s)):
        invest = [c for c in px.columns if c not in ("SPY", SWEEP)] if nm == "SMALL" else list(px.columns)
        panels[nm] = (px, invest)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} investable, {len(px)} rows, "
             f"scored {px.index[WARMUP].date()}..{px.index[-1].date()}", ">= 10y", yrs >= 10)

    # G1: the replica prices the live book exactly as engine.backtest does
    w_live = rules_v2_weights(px_u, band=BAND, gross=LIVE_GROSS)
    res_live = run_book(px_u, w_live)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    d1 = float((r_eng - priced(res_live, HEADLINE_RUNG)).abs().max())
    gate("G1 per-column replica == engine.backtest", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    rows, shape = [], []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=LIVE_GROSS)
                                 .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        N, nin, inb = breadth_parts(px, invest)
        say(f"\n--- panel {pname} ({len(invest)} names)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}"
            f"   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} / {maxdd(base_r):.2%}")
        say(f"    breadth on the scored window: N_in median {nin.loc[win].median():.0f}, "
            f"p05 {nin.loc[win].quantile(0.05):.0f}, min {nin.loc[win].min():.0f}, N_t {N.loc[win].median():.0f}")
        books = []
        for gross in GROSSES:
            for m in FLOORS:
                books.append((f"FLOOR", mlabel(m), gross, floor_weights(px, invest, m, gross)))
            books.append(("CAP2", f"cap{REF_CAP:.3f}", gross, cap_weights(px, invest, REF_CAP, gross)))
            for m in FLOORS:
                books.append(("FLOORCAP", mlabel(m), gross,
                              floor_weights(px, invest, m, gross, cap=REF_CAP)))
        for fam, lab, gross, w in books:
            res = run_book(px, w)
            nm_w = w.drop(columns=[SWEEP]).loc[win]
            pos = nm_w.values[nm_w.values > 0]
            if fam == "CAP2":
                binds = np.nan                       # the cap is always on; it has no binding DAY
            else:
                thr = np.inf if lab == "INF" else float(lab)
                binds = float((nin.loc[win] < thr).mean())
            shape.append(dict(panel=pname, family=fam, m=lab, gross=gross,
                              max_name_w=float(pos.max()) if len(pos) else 0.0,
                              p99_name_w=float(np.percentile(pos, 99)) if len(pos) else 0.0,
                              med_name_w=float(np.median(pos)) if len(pos) else 0.0,
                              mean_gross=float(res["gross"].loc[win].mean()),
                              mean_sweep_w=float(w[SWEEP].loc[win].mean()),
                              turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                              bind_share=binds, max_row_sum=float(w.sum(axis=1).max())))
            for rung in RUNGS:
                r = priced(res, rung).loc[win]
                r_oos = r.loc[OOS_START:]
                h1, h2 = halves(r)
                rows.append(dict(panel=pname, family=fam, m=lab, gross=gross, cost_bps=rung,
                                 CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                 H1=h1, H2=h2, IS_Sharpe=sharpe(r.loc[:IS_END]),
                                 IS_Calmar=calmar(r.loc[:IS_END]), OOS_CAGR=cagr(r_oos),
                                 OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                 **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows)
    sf = pd.DataFrame(shape)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    sf.to_csv(f"{OUT}.shape.csv", index=False)

    # ---- structural gates on the two known ends of the floor ladder
    px, invest = panels["U56"]
    d2 = float((floor_weights(px, invest, 1, LIVE_GROSS) - rg100_reference(px, invest, LIVE_GROSS)).abs().max().max())
    gate("G2 m=1 == idea 2300's RG100 + phi=1 (U56, independent construction)", f"max|dw| {d2:.3e}",
         "< 1e-12", d2 < 1e-12)
    d3 = float((floor_weights(px, invest, "INF", LIVE_GROSS) - dg_reference(px, invest, LIVE_GROSS)).abs().max().max())
    gate("G3 m=INF == the live de-grossed book + sweep (U56)", f"max|dw| {d3:.3e}", "< 1e-12", d3 < 1e-12)
    gate("G4 no leverage (all 90 books)", f"max row sum {sf.max_row_sum.max():.9f}", "<= 1+1e-12",
         bool((sf.max_row_sum <= 1 + 1e-12).all()))
    shy_ok = all(bool(p[SWEEP].loc[p.index[WARMUP:]].notna().all()) for p, _ in panels.values())
    gate("G6 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}",
         "True", shy_ok)

    # G5 the floor dial bites: binding-day share is non-decreasing in m, and concentration falls
    fl = sf[sf.family == "FLOOR"]
    mono, ends = [], []
    for (pn, g), grp in fl.groupby(["panel", "gross"]):
        grp = grp.set_index("m").reindex([mlabel(m) for m in FLOORS])
        v = grp.bind_share.values
        mono.append(bool(np.all(np.diff(v) >= -1e-12)))
        ends.append(f"{pn}/g{g:.2f} {v[0]:.4f}->{v[-2]:.4f} (m=20)")
    gate("G5 binding-day share non-decreasing along the floor ladder",
         f"{sum(mono)} of {len(mono)} (panel, gross) cells", "6 of 6", all(mono))
    publish("G5b binding-day share, m=1 -> m=20", "  ".join(ends))

    # G9 / G10 external reproductions of the two committed headline cells
    h = df[(df.panel == "U56") & (df.family == "FLOOR") & (df.m == "1") & (df.gross == LIVE_GROSS)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d9 = max(abs(h.CAGR - 0.1255), abs(h.Sharpe - 1.1896) / 10, abs(h.MaxDD + 0.1739),
             abs(h.OOS_CAGR - 0.1377), abs(h.OOS_Sharpe - 1.2332) / 10)
    gate("G9 reproduces idea 2300's committed U56 headline (12.55%/1.1896/-17.39%, OOS 13.77%/1.2332)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d9:.2e}", "< 2e-3", d9 < 2e-3)
    c = df[(df.panel == "U56") & (df.family == "CAP2") & (df.gross == LIVE_GROSS)
           & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d10 = max(abs(c.CAGR - 0.1158), abs(c.Sharpe - 1.2643) / 10, abs(c.MaxDD + 0.1481),
              abs(c.H1 - 1.3042) / 10, abs(c.H2 - 1.2363) / 10,
              abs(c.OOS_CAGR - 0.1270), abs(c.OOS_Sharpe - 1.3243) / 10)
    gate("G10 reproduces idea 2322's committed U56 cap-2.0% headline "
         "(11.58%/1.2643/-14.81%, 1.3042/1.2363, OOS 12.70%/1.3243)",
         f"read {c.CAGR:.2%} / {c.Sharpe:.4f} / {c.MaxDD:.2%}, {c.H1:.4f}/{c.H2:.4f}, "
         f"OOS {c.OOS_CAGR:.2%} / {c.OOS_Sharpe:.4f} -> max|d| {d10:.2e}", "< 2e-3", d10 < 2e-3)

    # ---------------------------------------------------------------- A. the grid
    say("\n=== A. THE FULL GRID AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        say(f"\n  {pname}")
        say("  family    m      gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b | legs H1/H2/OOS/DD/CAGR | maxw  p99w  bind%  turn/yr")
        for gross in GROSSES:
            for fam in ("FLOOR", "CAP2", "FLOORCAP"):
                d = df[(df.panel == pname) & (df.family == fam) & (df.gross == gross)
                       & (df.cost_bps == HEADLINE_RUNG)]
                for _, r in d.iterrows():
                    s = sf[(sf.panel == pname) & (sf.family == fam) & (sf.m == r.m)
                           & (sf.gross == gross)].iloc[0]
                    lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    bs = "  --" if not np.isfinite(s.bind_share) else f"{s.bind_share:5.2%}"
                    say(f"  {fam:9s} {r.m:6s} {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                        f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                        f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:22s} |"
                        f" {s.max_name_w:5.2%} {s.p99_name_w:5.2%} {bs:>6s} {s.turnover_yr:7.2f}")

    say("\n=== B. KEEP COUNTS OVER ALL PUBLISHED ROWS ===")
    say(f"  rows {len(df)}   4b passes {int(df.pass4b.sum())}   4a passes {int(df.pass4a.sum())}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for fam in ("FLOOR", "CAP2", "FLOORCAP"):
        d = df[df.family == fam]
        say(f"   {fam:9s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")
    for pname in panels:
        d = df[df.panel == pname]
        say(f"   {pname:9s}: 4b {int(d.pass4b.sum()):3d}/{len(d)}   4a {int(d.pass4a.sum()):3d}/{len(d)}")

    say("\n=== C. THE HEAD-TO-HEAD — FLOOR vs CAP at the same job (U56 / B136, gross 0.75, 10 bps) ===")
    say("  the question the idea asks: does the floor hold the candidate's 4b pass while cutting the")
    say("  concentration the re-gross adds, and does it do so more cheaply than the always-on cap?")
    for pname in ("U56", "B136", "SMALL"):
        say(f"\n  {pname}")
        say("  book                |   CAGR   Sharpe    MaxDD | OOS CAGR  OOS Sh | 4b | max name w  p99   bind%  turn/yr")
        for fam, lab in [("FLOOR", "1")] + [("FLOOR", mlabel(m)) for m in FLOORS[1:]] + [("CAP2", f"cap{REF_CAP:.3f}")]:
            r = df[(df.panel == pname) & (df.family == fam) & (df.m == lab) & (df.gross == LIVE_GROSS)
                   & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
            s = sf[(sf.panel == pname) & (sf.family == fam) & (sf.m == lab) & (sf.gross == LIVE_GROSS)].iloc[0]
            nmb = ("the candidate (m=1)" if (fam, lab) == ("FLOOR", "1") else
                   "de-grossed (m=INF)" if lab == "INF" else
                   f"cap {REF_CAP:.1%} (idea 2322)" if fam == "CAP2" else f"floor m={lab}")
            bs = "  --" if not np.isfinite(s.bind_share) else f"{s.bind_share:5.2%}"
            say(f"  {nmb:19s} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} |"
                f" {'Y' if r.pass4b else '.'}  | {s.max_name_w:9.2%} {s.p99_name_w:6.2%} {bs:>6s} {s.turnover_yr:7.2f}")

    say("\n=== D. RULE 8 — (m, gross) chosen on <= 2016-12-31 ONLY over the FLOOR family, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_oos = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=LIVE_GROSS)
                                   .reindex(columns=px.columns).fillna(0.0)),
                          HEADLINE_RUNG).loc[win].loc[OOS_START:]
        for rung in RUNGS:
            d = df[(df.panel == pname) & (df.cost_bps == rung) & (df.family == "FLOOR")]
            cp = df[(df.panel == pname) & (df.cost_bps == rung) & (df.family == "CAP2")
                    & (df.gross == LIVE_GROSS)].iloc[0]
            for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                pick = d.loc[d[col].idxmax()]
                wf.append(dict(panel=pname, cost_bps=rung, chooser=chooser, pick_m=pick.m,
                               pick_gross=pick.gross, OOS_CAGR=pick.OOS_CAGR,
                               OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                               pass4b_full=bool(pick.pass4b),
                               cap_OOS_CAGR=cp.OOS_CAGR, cap_OOS_Sharpe=cp.OOS_Sharpe,
                               cap_OOS_MaxDD=cp.OOS_MaxDD,
                               base_OOS_CAGR=cagr(base_oos), base_OOS_Sharpe=sharpe(base_oos),
                               base_OOS_MaxDD=maxdd(base_oos), spy_OOS_CAGR=cagr(spy_oos),
                               spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                               pick_is_candidate=bool(pick.m == "1"),
                               beats_cap_OOS_Sharpe=bool(pick.OOS_Sharpe > cp.OOS_Sharpe),
                               on_endpoint=bool(pick.m in ("1", "INF")))
                          )
                say(f"  {pname:5s} {rung:5.1f}bps {chooser:11s} -> m {pick.m:4s} g {pick.gross:.2f} |"
                    f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                    f" CAP2 g0.75 OOS {cp.OOS_CAGR:6.2%} / {cp.OOS_Sharpe:.4f} |"
                    f" live v2 OOS {cagr(base_oos):6.2%} / {sharpe(base_oos):.4f} |"
                    f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} | full-sample 4b "
                    f"{'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on m=1 (the uncapped, unfloored candidate): "
        f"{int(wfd.pick_is_candidate.sum())} of {len(wfd)}")
    say(f"  rule-8 picks sitting on a ladder ENDPOINT (m=1 or m=INF): "
        f"{int(wfd.on_endpoint.sum())} of {len(wfd)}")
    say(f"  rule-8 picks whose OOS Sharpe beats idea 2322's CAP2 book: "
        f"{int(wfd.beats_cap_OOS_Sharpe.sum())} of {len(wfd)}")
    say(f"  rule-8 picks that also pass 4b on the full sample: "
        f"{int(wfd.pass4b_full.sum())} of {len(wfd)}")

    say("\n=== E. WHAT THE FLOOR COSTS AND WHAT IT BUYS (deltas against the candidate m=1, U56 g=0.75, 10 bps) ===")
    ref = df[(df.panel == "U56") & (df.family == "FLOOR") & (df.m == "1") & (df.gross == LIVE_GROSS)
             & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    for fam, lab in [("FLOOR", mlabel(m)) for m in FLOORS] + [("CAP2", f"cap{REF_CAP:.3f}")]:
        r = df[(df.panel == "U56") & (df.family == fam) & (df.m == lab) & (df.gross == LIVE_GROSS)
               & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
        s = sf[(sf.panel == "U56") & (sf.family == fam) & (sf.m == lab) & (sf.gross == LIVE_GROSS)].iloc[0]
        say(f"  {fam:9s} {lab:6s} dCAGR {r.CAGR - ref.CAGR:+6.2%}  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}"
            f"  dMaxDD {r.MaxDD - ref.MaxDD:+6.2%}  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}"
            f"  | max name w {s.max_name_w:5.2%}  mean gross {s.mean_gross:.3f}  mean SHY {s.mean_sweep_w:.3f}")

    gdf = pd.DataFrame(GATES)
    gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .shape.csv / .walkforward.csv / .gates.csv   ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
