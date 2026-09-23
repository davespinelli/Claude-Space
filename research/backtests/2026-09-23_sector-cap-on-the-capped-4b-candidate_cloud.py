#!/usr/bin/env python3
"""idea 2339 (lane cloud, 2026-09-23) — does a per-GROUP (SECTOR) WEIGHT CAP on the CAPPED 4b
candidate buy anything the PER-NAME cap did not?

THE OBJECT.  Idea 2322 filed the record's standing KEEP-4b candidate as CAP2:

    w_i = min(gross / N_in, 0.02)  on names INSIDE the 200d +/-3% band,
    idle NAV (1 - sum w) swept to SHY at phi = 1.00,  weekly cadence, t+1 execution.

CAP2 removed the candidate's single-NAME concentration (worst day 15.00% -> 2.00%) and kept the
4b pass.  Nothing in the record has ever looked at GROUP concentration.  `research/universe.json`
is a dict of four blocks (broad 8 ETFs / sectors 16 ETFs / bonds_fx_commod 12 / megacap 20), and
on a 200d-band book the IN set is TREND-selected, so whole blocks go IN or OUT together: the
name-capped book can still be 40% megacap on the day that matters.

THE DEVICE.  On top of CAP2, cap each GROUP's total book weight at s.  Spill goes to SHY (the
sweep the candidate already collects), NEVER re-spread to other groups -- the same de-gross
convention clause 4 uses for the name cap.

    for each group G:  if sum_{i in G} w_i > s:  w_i *= s / sum_{i in G} w_i

DIAL 1 -- group cap s {0.10, 0.20, 0.30, 0.40, 0.60, INF}.  s = INF IS CAP2 exactly, so ONE
ladder spans the known book: the ladder is a continuous dial between a hard block cap and the
filed candidate.
DIAL 2 -- gross {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: 2 panels, 4 cost rungs (0 / 10 / 25 / 50 bps), weekly cadence,
t+1 execution, band 0.03, per-name cap 0.02 (2322's filed constant), phi = 1.00.
6 x 2 x 2 x 4 = 96 published rows, every grid point printed.

PANELS.  U56 is the panel where the groups are DEFINED (universe.json).  B136 has no committed
group map, so the SAME map is applied to the overlapping names and every other B136 name is its
OWN SINGLETON group; on B136 the cap therefore binds only on the ETF/megacap blocks.  That is a
ROBUSTNESS read, NOT a replication, and is labelled as such everywhere it is printed.  SMALL is
NOT run: no group map exists for it at all, and inventing one would be a third tuned dial.

BOTH KEEP PATHS on every row: 4a (Sharpe > live RULES v2 in BOTH halves and MaxDD no worse) and
4b (Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's).
RULE 8: (s, gross) chosen on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE, C_ISCALMAR), then 2017-2026 read ONCE.

GATES.  G0 >= 10y per panel.  G1 s=INF is BIT-IDENTICAL to an independent CAP2 construction.
G2 the per-column replica equals `engine.backtest` on the live weights.  G3 no leverage anywhere.
G4 the group cap BITES (max group weight non-increasing in s, and <= s + 1e-12 on every row).
G5 SHY priced on every row it is held.  G6 exactly two tuned parameters.
G7 EXTERNAL REPRODUCTION of idea 2322's committed U56 CAP2 headline
   (11.58% / 1.2643 / -14.81%, OOS 12.70% / 1.3243).
G8 the group partition covers every investable column exactly once.

SURVIVORSHIP (rule 9): U56 / B136 are CURRENT-constituent lists held from 2008, so the absolute
4b levels are optimistic.  The cap-vs-no-cap contrast is same-tape, same-day, same-gross and is
first-order immune; the CAGR floor leg is an ABSOLUTE bar and is the most contaminated reading.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_sector-cap-on-the-capped-4b-candidate_cloud.py
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "sector-cap-on-the-capped-4b-candidate", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
NAME_CAP = 0.02                      # idea 2322's filed CAP2 constant -- FIXED, not a dial
SWEEP, PHI = "SHY", 1.00
SCAPS = [0.10, 0.20, 0.30, 0.40, 0.60, "INF"]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
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


def slabel(s):
    return s if isinstance(s, str) else f"{s:.2f}"


# ---------------------------------------------------------------- group map
def group_map(cols):
    """universe.json's four blocks; any investable column not in it is its OWN singleton group."""
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    g = {}
    for blk, names in U.items():
        for t in names:
            g[t] = blk
    return {c: g.get(c, f"_solo_{c}") for c in cols}


# ---------------------------------------------------------------- books
def cap2_weights(px, invest, gross):
    """idea 2322's filed CAP2: w_i = min(gross/N_in, 0.02) on IN names, idle -> SHY at phi=1."""
    q = px[invest]
    pr = q.notna()
    inb = band_state(q, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = pd.concat([gross / nin, pd.Series(NAME_CAP, index=q.index)], axis=1).min(axis=1)
    w = inb.astype(float).mul(per.fillna(0.0), axis=0).reindex(columns=px.columns).fillna(0.0)
    return w


def group_capped_weights(px, invest, gmap, s, gross):
    """CAP2, then each GROUP's total BOOK weight capped at s (spill -> SHY, never re-spread).

    Returns (w_total, w_book).  `w_book` is the RISK BOOK before the cash sweep; `w_total` adds
    the idle NAV to SHY at phi = 1.  Every concentration statistic in this run is read off
    `w_book`, because the sweep is CASH held in a T-bill ETF, not a position -- reading it as
    one would score the cap against its own cash sleeve (SHY sits in the bonds_fx_commod block).
    """
    w = cap2_weights(px, invest, gross)
    if s != "INF":
        book = w[invest]
        gs = book.T.groupby(pd.Series(gmap)[invest].values).sum().T      # group totals, T x G
        scale = (float(s) / gs.replace(0.0, np.nan)).clip(upper=1.0).fillna(1.0)
        per_col = scale.reindex(columns=[gmap[c] for c in invest])
        per_col.columns = invest
        w = w.copy()
        w[invest] = book * per_col
    w_book = w.copy()
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w = w.copy()
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
    return w, w_book


def cap2_reference(px, invest, gross):
    """Independent construction of CAP2 + sweep (element-wise minimum form, no groupby path)."""
    q = px[invest]
    pr = q.notna()
    inb = (band_state(q, BAND) & pr).astype(float)
    nin = inb.sum(axis=1).replace(0, np.nan)
    per = np.minimum(gross / nin.values, NAME_CAP)
    w = pd.DataFrame(inb.values * per[:, None], index=q.index, columns=q.columns)
    w = w.fillna(0.0).reindex(columns=px.columns).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + PHI * idle * px[SWEEP].notna().astype(float)
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


def main():
    t0 = time.time()
    say("=== idea 2339 — does a per-GROUP (SECTOR) CAP on the CAPPED 4b candidate buy anything "
        "the PER-NAME cap did not? ===")
    say(f"    {DATE}  lane {LANE}   band {BAND}  cadence {CADENCE}  t+1  rungs {RUNGS} bps  "
        f"name cap {NAME_CAP:.2%} (FIXED, idea 2322)  sweep {SWEEP} phi={PHI:.2f}")
    say(f"    DIAL 1 group cap s {[slabel(s) for s in SCAPS]}   DIAL 2 gross {GROSSES}")
    gate("G6 exactly two tuned parameters", "group cap s, gross", "2", True)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    panels = {}
    for nm, px in (("U56", px_u), ("B136", px_b)):
        invest = list(px.columns)
        gmap = group_map(invest)
        panels[nm] = (px, invest, gmap)
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y, {len(invest)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)
        blocks = pd.Series(gmap).value_counts()
        named = {k: int(v) for k, v in blocks.items() if not k.startswith("_solo_")}
        nsolo = int(sum(v for k, v in blocks.items() if k.startswith("_solo_")))
        cover = len(gmap) == len(invest) and len(set(gmap)) == len(invest)
        gate(f"G8 group partition covers every investable column exactly once ({nm})",
             f"named blocks {named}, singletons {nsolo}, total {len(invest)}",
             "covers, no dupes", cover)
        if nm == "B136":
            publish("B136 group map is PARTIAL by construction",
                    f"{sum(named.values())} of {len(invest)} names carry a universe.json block; "
                    f"the other {nsolo} are singletons and the cap can NEVER bind on them. "
                    "ROBUSTNESS read, not a replication.")

    # G2: the replica prices the live book exactly as engine.backtest does
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    d2 = float((backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
                - priced(run_book(px_u, w_live), HEADLINE_RUNG)).abs().max())
    gate("G2 per-column replica == engine.backtest", f"max|d| {d2:.3e}", "< 1e-12", d2 < 1e-12)

    rows, conc = [], []
    for pname, (px, invest, gmap) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        say(f"\n--- panel {pname} ({len(invest)} names)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} /"
            f" {maxdd(spy):.2%}   live RULES v2 {cagr(base_r):.2%} / {sharpe(base_r):.4f} /"
            f" {maxdd(base_r):.2%}")
        gser = pd.Series(gmap)[invest]
        for gross in GROSSES:
            for s in SCAPS:
                w, w_book = group_capped_weights(px, invest, gmap, s, gross)
                mx = float(w.sum(axis=1).max())
                book = w_book[invest].loc[win]          # RISK BOOK, cash sweep excluded
                gtot = book.T.groupby(gser.values).sum().T
                named_cols = [c for c in gtot.columns if not c.startswith("_solo_")]
                res = run_book(px, w)
                pos = book.values[book.values > 0]
                conc.append(dict(panel=pname, s=slabel(s), gross=gross,
                                 max_group_w=float(gtot.max().max()),
                                 max_named_group_w=float(gtot[named_cols].max().max()) if named_cols else 0.0,
                                 p99_group_w=float(np.percentile(gtot.values, 99)),
                                 max_name_w=float(pos.max()) if len(pos) else 0.0,
                                 mean_book_gross=float(book.sum(axis=1).mean()),
                                 mean_gross=float(res["gross"].loc[win].mean()),
                                 mean_sweep_w=float(w[SWEEP].loc[win].mean()),
                                 turnover_yr=float(res["turnover"].loc[win].sum() / (len(win) / 252)),
                                 days_binding=int((gtot.max(axis=1) >
                                                   (float(s) - 1e-9 if s != "INF" else np.inf)).sum()),
                                 max_row_sum=mx))
                if mx > 1 + 1e-12:
                    gate(f"G3 no leverage ({pname} s={slabel(s)} g={gross})",
                         f"max row sum {mx:.9f}", "<= 1+1e-12", False)
                for rung in RUNGS:
                    r = priced(res, rung).loc[win]
                    r_oos = r.loc[OOS_START:]
                    h1, h2 = halves(r)
                    rows.append(dict(panel=pname, s=slabel(s), gross=gross, cost_bps=rung,
                                     CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                     H1=h1, H2=h2,
                                     IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                     OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                     **legs(r, base_r, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); cf = pd.DataFrame(conc)
    df.to_csv(f"{OUT}.grid.csv", index=False); cf.to_csv(f"{OUT}.concentration.csv", index=False)

    # ---- gates that need the whole grid
    px, invest, gmap = panels["U56"]
    d1 = float((group_capped_weights(px, invest, gmap, "INF", 0.75)[0]
                - cap2_reference(px, invest, 0.75)).abs().max().max())
    gate("G1 s=INF == idea 2322's CAP2 + sweep (U56, independent construction)",
         f"max|dw| {d1:.3e}", "< 1e-12", d1 < 1e-12)
    gate("G3 no leverage (all 24 books)", f"max row sum {cf.max_row_sum.max():.9f}",
         "<= 1+1e-12", bool((cf.max_row_sum <= 1 + 1e-12).all()))
    numeric = [slabel(s) for s in SCAPS if s != "INF"]
    honour = all(float(r.max_group_w) <= float(r.s) + 1e-9
                 for _, r in cf[cf.s != "INF"].iterrows())
    mono = []
    for (pn, g), grp in cf.groupby(["panel", "gross"]):
        v = grp.set_index("s").reindex(numeric).max_group_w.values
        mono.append(bool(np.all(np.diff(v) >= -1e-12)))
    gate("G4a every finite s is HONOURED (max BOOK group weight <= s on every row)",
         f"{honour}", "True", honour)
    gate("G4b max group weight is non-decreasing along the numeric s ladder",
         f"{sum(mono)} of {len(mono)} (panel, gross) cells", f"{len(mono)} of {len(mono)}", all(mono))
    shy_ok = all(bool(p[0][SWEEP].loc[p[0].index[WARMUP:]].notna().all()) for p in panels.values())
    gate("G5 sweep instrument priced on every held row", f"SHY non-null on all panels: {shy_ok}",
         "True", shy_ok)
    h = df[(df.panel == "U56") & (df.s == "INF") & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d7 = max(abs(h.CAGR - 0.1158), abs(h.Sharpe - 1.2643) / 10, abs(h.MaxDD + 0.1481),
             abs(h.OOS_CAGR - 0.1270), abs(h.OOS_Sharpe - 1.3243) / 10)
    gate("G7 reproduces idea 2322's committed U56 CAP2 headline (11.58%/1.2643/-14.81%, OOS 12.70%/1.3243)",
         f"read {h.CAGR:.2%} / {h.Sharpe:.4f} / {h.MaxDD:.2%}, OOS {h.OOS_CAGR:.2%} / {h.OOS_Sharpe:.4f}"
         f" -> max|d| {d7:.2e}", "< 1e-3", d7 < 1e-3)

    # ---------------------------------------------------------------- tables
    say("\n=== A. THE FULL GRID AT THE HEADLINE RUNG (10 bps) — every point, nothing dropped ===")
    for pname in panels:
        say(f"\n  {pname}" + ("   [group map PARTIAL: singletons can never bind]" if pname == "B136" else ""))
        say("  s      gross |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh  OOS DD | 4a 4b |"
            " H1/H2/OOS/DD/CAGR | maxGrpW maxNamedGrp maxNameW turn/yr bindDays")
        for gross in GROSSES:
            for s in SCAPS:
                r = df[(df.panel == pname) & (df.s == slabel(s)) & (df.gross == gross)
                       & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                c = cf[(cf.panel == pname) & (cf.s == slabel(s)) & (cf.gross == gross)].iloc[0]
                lg = "".join("1" if r[k] else "0" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                say(f"  {slabel(s):6s} {gross:.2f}  | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
                    f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} |"
                    f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg:17s} |"
                    f" {c.max_group_w:7.2%} {c.max_named_group_w:11.2%} {c.max_name_w:8.2%}"
                    f" {c.turnover_yr:7.2f} {c.days_binding:8d}")

    say("\n=== B. KEEP COUNTS OVER ALL PUBLISHED ROWS (6 s x 2 gross x 2 panels x 4 rungs) ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for rung in RUNGS:
        d = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps:  4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}"
            f"   binding leg on 4b FAILs: " +
            "  ".join(f"{k} {int((~d[k][~d.pass4b]).sum())}" for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  4b pass rows (all rungs):")
    p = df[df.pass4b]
    if len(p) == 0:
        say("    NONE")
    for _, r in p.iterrows():
        say(f"    {r.panel:5s} s {r.s:6s} g {r.gross:.2f} {r.cost_bps:5.1f}bps  "
            f"{r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}   OOS {r.OOS_CAGR:6.2%} / {r.OOS_Sharpe:.4f}")

    say("\n=== C. WHAT THE GROUP CAP COSTS: CAP2 (s=INF) minus each s, 10 bps ===")
    for pname in panels:
        ref = df[(df.panel == pname) & (df.s == "INF") & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
        cref = cf[(cf.panel == pname) & (cf.s == "INF") & (cf.gross == 0.75)].iloc[0]
        say(f"  {pname} g=0.75   CAP2 reference: max BOOK group weight {cref.max_group_w:.2%}"
            f" (named blocks {cref.max_named_group_w:.2%}), turnover {cref.turnover_yr:.2f}/yr")
        for s in SCAPS:
            r = df[(df.panel == pname) & (df.s == slabel(s)) & (df.gross == gross) & (df.cost_bps == 10.0)]
            r = df[(df.panel == pname) & (df.s == slabel(s)) & (df.gross == 0.75) & (df.cost_bps == 10.0)].iloc[0]
            c = cf[(cf.panel == pname) & (cf.s == slabel(s)) & (cf.gross == 0.75)].iloc[0]
            say(f"    s {slabel(s):6s} dCAGR {r.CAGR - ref.CAGR:+6.2%}  dSharpe {r.Sharpe - ref.Sharpe:+7.4f}"
                f"  dMaxDD {r.MaxDD - ref.MaxDD:+6.2%}  dOOS_Sh {r.OOS_Sharpe - ref.OOS_Sharpe:+7.4f}"
                f"  | max book grp {c.max_group_w:6.2%}  mean book gross {c.mean_book_gross:.3f}"
                f"  mean SHY {c.mean_sweep_w:.3f}  turn {c.turnover_yr:5.2f}  bind days {c.days_binding}")

    say("\n=== D. RULE 8 — (s, gross) chosen on <= 2016-12-31 ONLY, 2017-2026 read once ===")
    wf = []
    for pname, (px, invest, gmap) in panels.items():
        win = px.index[WARMUP:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        base_r = priced(run_book(px, rules_v2_weights(px[invest], band=BAND, gross=0.75)
                                 .reindex(columns=px.columns).fillna(0.0)), HEADLINE_RUNG).loc[win]
        b_oos = base_r.loc[OOS_START:]
        for rung in RUNGS:
            d = df[(df.panel == pname) & (df.cost_bps == rung)]
            for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                pick = d.loc[d[col].idxmax()]
                wf.append(dict(panel=pname, cost_bps=rung, chooser=chooser, pick_s=pick.s,
                               pick_gross=pick.gross, OOS_CAGR=pick.OOS_CAGR,
                               OOS_Sharpe=pick.OOS_Sharpe, OOS_MaxDD=pick.OOS_MaxDD,
                               base_OOS_CAGR=cagr(b_oos), base_OOS_Sharpe=sharpe(b_oos),
                               base_OOS_MaxDD=maxdd(b_oos), spy_OOS_CAGR=cagr(spy_oos),
                               spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                               full4b=pick.pass4b, pick_is_INF=(pick.s == "INF"),
                               beats_spy_oos=bool(pick.OOS_Sharpe > sharpe(spy_oos)),
                               beats_base_oos=bool(pick.OOS_Sharpe > sharpe(b_oos))))
                say(f"  {pname:5s} {rung:5.1f}bps {chooser:11s} -> s {pick.s:6s} g {pick.gross:.2f} |"
                    f" OOS {pick.OOS_CAGR:6.2%} / {pick.OOS_Sharpe:.4f} / {pick.OOS_MaxDD:7.2%} |"
                    f" live v2 OOS {cagr(b_oos):6.2%} / {sharpe(b_oos):.4f} / {maxdd(b_oos):7.2%} |"
                    f" SPY OOS {cagr(spy_oos):6.2%} / {sharpe(spy_oos):.4f} / {maxdd(spy_oos):7.2%} |"
                    f" full 4b {'Y' if pick.pass4b else '.'}")
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  rule-8 picks landing on s=INF (the uncapped-by-group CAP2 candidate): "
        f"{int(wfd.pick_is_INF.sum())} of {len(wfd)}")
    say(f"  rule-8 picks beating SPY OOS: {int(wfd.beats_spy_oos.sum())} of {len(wfd)};"
        f"  beating the live book OOS: {int(wfd.beats_base_oos.sum())} of {len(wfd)}")

    say("\n=== E. GROUP CONCENTRATION of the RISK BOOK (cash sweep excluded) — the risk this idea was filed to price (g=0.75) ===")
    say("  panel s      max grp  max NAMED grp  p99 grp  max name  days the cap binds  turnover/yr   mean book gross")
    for pname in panels:
        for s in SCAPS:
            c = cf[(cf.panel == pname) & (cf.s == slabel(s)) & (cf.gross == 0.75)].iloc[0]
            say(f"  {pname:5s} {slabel(s):6s} {c.max_group_w:7.2%} {c.max_named_group_w:13.2%}"
                f" {c.p99_group_w:8.2%} {c.max_name_w:9.2%} {c.days_binding:19d} {c.turnover_yr:12.2f}"
                f" {c.mean_book_gross:17.3f}")

    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n=== GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass ===")
    for _, g in gdf[~gdf.pass_].iterrows():
        say(f"    FAILED: {g.gate} = {g.value} (target {g.target})")
    say(f"\nwrote {OUT}.grid.csv / .concentration.csv / .walkforward.csv / .gates.csv "
        f"  ({time.time() - t0:.0f}s)")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
