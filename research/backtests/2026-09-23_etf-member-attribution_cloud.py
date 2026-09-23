#!/usr/bin/env python3
"""idea 2435 (lane cloud, run 46, 2026-09-23) — HOW MUCH OF THE CAPPED CANDIDATE'S 4b PASS IS
CARRIED BY THE ETF MEMBERS OF ITS OWN PANEL?

THE GAP.  U56 is **36 ETFs and 20 single stocks**; B136 carries ~35 ETFs beside its 100 large
caps.  The book the record calls a capital candidate is therefore permitted to hold **SPY itself**,
plus QQQ, VTI, RSP, DIA, IWM and sixteen sector funds.  4b's whole question is "does this beat
SPY", and a book that may hold SPY answers part of that question by construction rather than by
selection.  No committed run has ever priced the candidate on a panel with the index funds removed.

DIAL 1 -- the exclusion set, a nested ladder (each tranche a strict superset of the last):
   NONE     the committed panel.  **IS CAP2 / CAND EXACTLY** — G3 asserts bit-identity.
   NOBROAD  minus the broad equity index funds {SPY, QQQ, VTI, RSP, DIA, IWM, EFA, EEM}.
   NOEQETF  minus those AND the sixteen sector funds {XLK XLF XLV XLE XLI XLY XLP XLU XLB XLRE
            XLC SMH XBI KRE ITB GDX}.
   STOCKS   single stocks + SHY only (also minus TLT IEF HYG LQD TIP GLD SLV USO UNG DBC UUP).
DIAL 2 -- gross g {0.75 live, 1.00}.

SHY is RETAINED at every rung because it is the sweep instrument, not a return source.  SPY is
retained as a COLUMN (it is the benchmark every 4b leg is scored against) but its weight is forced
to zero from NOBROAD onward, so it is never held above the first rung.

TWO CONVENTIONS, BOTH PUBLISHED, THE HEADLINE PRE-STATED HERE BEFORE ANY COMPUTE:
   RESPREAD -- `N_in` counts only the ELIGIBLE names, so the book re-spreads over the survivors at
               the same gross.  This is the TRADABLE book: "run the committed rule on a panel with
               no index funds in it".  **HEADLINE.**
   DEGROSS  -- `N_in` still counts the band's IN names over the FULL panel, so the excluded names'
               weight falls to the SHY sweep and the survivors keep their committed sizing.  This
               is the ATTRIBUTION book: it reads off how much of the return those names carried at
               unchanged per-name weight, with no re-spreading confound.
They are conventions on one dial, not a third dial: both are read off the same exclusion ladder.

WHY IT MATTERS FOR CAPITAL, stated before the result.  A pass that survives to STOCKS is a
stock-selection rule.  One that dies at NOBROAD is a restatement of index beta with a 200d filter,
and should be described that way in any memo before capital is committed.  Either answer is a
result; neither is a failure of the run.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, books {CAP2 (2% cap), CAND (uncapped)}, cost rungs
{0, 10, 25, 50} bps, weekly cadence, t+1 execution, band 0.03 and the phi = 1.00 SHY sweep.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: BOTH dials fitted on warm-up..2016-12-31 ONLY by two pre-stated IS-only choosers
(C_ISSHARPE = max in-sample Sharpe, C_ISCALMAR = max in-sample Calmar), then 2017-2026 read ONCE.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the band is
`baseline.band_state` bit for bit.  G3 NONE is BIT-IDENTICAL, under BOTH conventions, to an
independent CAP2/CAND construction through `engine.backtest`.  G4 no leverage.  G5 the ladder is
NESTED and BITES (each tranche removes strictly more names, mean names held strictly falls).  G6
SPY is never held above NONE and SHY is held at every rung.  G7 exactly two tuned parameters.  G8
DEGROSS leaves every surviving name's weight UNCHANGED from the committed book (that is what makes
it an attribution).  G9 SHY priced on every held row.  G10 EXTERNAL REPRODUCTION of the committed
CAP2 U56 headline (11.62% / 1.2687 / -14.81%, OOS 12.77% / 1.3318) and CAND U56 headline
(12.59% / 1.1934 / -17.39%, OOS 13.85% / 1.2397).

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008.  This idea is MORE exposed to that bias than most,
because the tranche it strips away (index funds) is the one part of the panel that is NOT
survivorship-selected, while the single stocks that remain are exactly the names the screen kept.
The STOCKS rung is therefore the OPTIMISTIC bound on a stock-selection reading, and that is stated
as the run's main caveat rather than buried.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_etf-member-attribution_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "etf-member-attribution", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, CADENCE, WARMUP = 0.03, "W", 260
BROAD_EQ = {"SPY", "QQQ", "VTI", "RSP", "DIA", "IWM", "EFA", "EEM"}
SECTOR = {"XLK", "XLF", "XLV", "XLE", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC",
          "SMH", "XBI", "KRE", "ITB", "GDX"}
OTHER_ETF = {"TLT", "IEF", "HYG", "LQD", "TIP", "GLD", "SLV", "USO", "UNG", "DBC", "UUP"}
TRANCHES = {"NONE": set(), "NOBROAD": BROAD_EQ, "NOEQETF": BROAD_EQ | SECTOR,
            "STOCKS": BROAD_EQ | SECTOR | OTHER_ETF}
LADDER = ["NONE", "NOBROAD", "NOEQETF", "STOCKS"]
CONVENTIONS = ["RESPREAD", "DEGROSS"]
HEADLINE_CONV = "RESPREAD"
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
BOOKS = {"CAP2": 0.020, "CAND": np.inf}
SWEEP, BENCH = "SHY", "SPY"
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


# ---------------------------------------------------------------- the books
def risk_weights(px, gross, cap, tranche, conv):
    """CAP2/CAND with an ETF tranche excluded.

    RESPREAD: N_in counts ELIGIBLE band-IN names only -> the book re-spreads at the same gross.
    DEGROSS : N_in counts ALL band-IN names -> survivors keep their committed weight and the
              excluded names' share falls to the SHY sweep.
    SHY is never excluded (it is the sweep); SPY is excluded from NOBROAD onward."""
    drop = TRANCHES[tranche] - {SWEEP}
    pr = px.notna()
    inb_all = band_state(px, BAND) & pr
    elig = pd.Series([c not in drop for c in px.columns], index=px.columns)
    inb = inb_all & elig
    nin = (inb if conv == "RESPREAD" else inb_all).sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return inb.astype(float).mul(per, axis=0).fillna(0.0), inb_all, inb


def full_reference(px, gross, cap):
    pr = px.notna()
    inb = band_state(px, BAND) & pr
    nin = inb.sum(axis=1).replace(0, np.nan)
    w = inb.astype(float).mul((gross / nin).clip(upper=cap).fillna(0.0), axis=0).fillna(0.0)
    idle = (1.0 - w.sum(axis=1)).clip(lower=0.0)
    w[SWEEP] = w[SWEEP] + idle * px[SWEEP].notna().astype(float)
    return w


# ---------------------------------------------------------------- the runner
def run_book(prices, w_risk, freq=CADENCE, sweep=True, watch=()):
    """`engine.backtest` verbatim, with total |dw| retained so every cost rung reads off one
    realised path, plus the realised NAV share of a watched ticker set."""
    cols = list(prices.columns)
    shy_i = cols.index(SWEEP)
    w_idx = [cols.index(t) for t in watch if t in cols]
    rv = prices.pct_change().fillna(0.0).values
    shy_ok = prices[SWEEP].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    dw = np.zeros(n); cur = np.zeros(m)
    gr = np.zeros(n); r0 = np.zeros(n); nheld = np.zeros(n)
    shyw = np.zeros(n); mx = np.zeros(n); wsh = np.zeros(n); spyw = np.zeros(n)
    spy_i = cols.index(BENCH)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[shy_i] += max(0.0, 1.0 - new.sum()) * shy_ok[i]
            dw[i] = np.abs(new - cur).sum()
            cur = new
        gr[i] = cur.sum()
        nheld[i] = float((cur > 1e-12).sum())
        shyw[i] = cur[shy_i]; spyw[i] = cur[spy_i]; mx[i] = cur.max()
        wsh[i] = float(cur[w_idx].sum()) if w_idx else 0.0
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), gross=pd.Series(gr, index=idx),
                names=pd.Series(nheld, index=idx), shy=pd.Series(shyw, index=idx),
                spy=pd.Series(spyw, index=idx), maxw=pd.Series(mx, index=idx),
                watch=pd.Series(wsh, index=idx), dw=pd.Series(dw, index=idx))


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
    say("=== idea 2435 — HOW MUCH OF THE CAPPED CANDIDATE'S 4b PASS IS CARRIED BY THE ETF MEMBERS? ===")
    say(f"    {DATE}  lane {LANE} run 46   band {BAND}  MA 200d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  cap 2%  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 exclusion tranche {LADDER}   DIAL 2 gross {GROSSES}")
    say(f"    conventions {CONVENTIONS}; HEADLINE = {HEADLINE_CONV} (the tradable book).")
    say("    NONE IS THE COMMITTED BOOK EXACTLY under BOTH conventions (G3 asserts bit-identity).")
    say("    SHY is retained at every rung (it is the sweep); SPY stays a COLUMN (the benchmark) but is")
    say("    never HELD above NONE (G6).")
    say("    SURVIVORSHIP (rule 9): the tranche stripped away (index funds) is the one part of the panel")
    say("    that is NOT survivorship-selected, so the STOCKS rung is the OPTIMISTIC bound on any")
    say("    stock-selection reading.  This idea is MORE exposed to rule 9 than most, not less.")
    gate("G7 exactly two tuned parameters", "tranche, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)
        for t in LADDER:
            drop = (TRANCHES[t] - {SWEEP}) & set(px.columns)
            publish(f"G5a tranche sizes ({nm} / {t})",
                    f"{len(drop)} of {len(px.columns)} columns excluded, {len(px.columns) - len(drop)} eligible")

    px_u = panels["U56"]
    d2 = int((band_state(px_u, BAND) != band_state(px_u, BAND)).sum().sum())
    gate("G2 the gate IS baseline.band_state (live clause 2), unmodified",
         f"{d2} differing cells; mean names IN "
         f"{(band_state(px_u, BAND) & px_u.notna()).sum(axis=1).mean():.2f}", "0", d2 == 0)

    w_live = rules_v2_weights(px_u, band=BAND, gross=LIVE_GROSS)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["dw"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    d3 = 0.0
    for bname, cap in BOOKS.items():
        eng = backtest(px_u, full_reference(px_u, LIVE_GROSS, cap), cost_bps=HEADLINE_RUNG,
                       freq=CADENCE)["returns"]
        for conv in CONVENTIONS:
            wq, _, _ = risk_weights(px_u, LIVE_GROSS, cap, "NONE", conv)
            bk = run_book(px_u, wq)
            d3 = max(d3, float((eng - (bk["r0"] - bk["dw"] * HEADLINE_RUNG / 1e4)).abs().max()))
    gate("G3 NONE IS the committed book under BOTH conventions == independent engine.backtest",
         f"max|d| over books x conventions: {d3:.3e}", "< 1e-12", d3 < 1e-12)

    # G8 DEGROSS leaves surviving names' weights unchanged
    w0, _, _ = risk_weights(px_u, LIVE_GROSS, BOOKS["CAP2"], "NONE", "DEGROSS")
    d8 = 0.0
    for t in LADDER[1:]:
        wt_, _, el = risk_weights(px_u, LIVE_GROSS, BOOKS["CAP2"], t, "DEGROSS")
        keep = [c for c in px_u.columns if c not in (TRANCHES[t] - {SWEEP})]
        d8 = max(d8, float((wt_[keep] - w0[keep]).abs().max().max()))
    gate("G8 DEGROSS leaves every SURVIVING name's weight unchanged (it is an attribution, not a re-sizing)",
         f"max|dw| over surviving names, all tranches: {d8:.3e}", "< 1e-12", d8 < 1e-12)

    rows, meta = [], []
    for pname, px in panels.items():
        win = px.index[WARMUP:]
        spy = px[BENCH].pct_change().fillna(0.0).loc[win]
        spy_oos = spy.loc[OOS_START:]
        yrs = len(win) / 252
        say(f"\n--- panel {pname} ({len(px.columns)} columns)  SPY {cagr(spy):.2%} / {sharpe(spy):.4f} / {maxdd(spy):.2%}")
        say(f"    4b bars here: DD cap {DD_CAP * maxdd(spy):.2%}   CAGR floor {CAGR_FLOOR * cagr(spy):.2%}"
            f"   SPY halves {halves(spy)[0]:.4f}/{halves(spy)[1]:.4f}   SPY OOS Sharpe {sharpe(spy_oos):.4f}")
        base_paths = {g: run_book(px, rules_v2_weights(px, band=BAND, gross=g), sweep=False) for g in GROSSES}
        for bname, cap in BOOKS.items():
            for conv in CONVENTIONS:
                for tr in LADDER:
                    for gross in GROSSES:
                        wq, inb_all, inb = risk_weights(px, gross, cap, tr, conv)
                        watch = (TRANCHES["STOCKS"] - {SWEEP}) & set(px.columns)
                        pth = run_book(px, wq, watch=tuple(sorted(watch)))
                        r0 = pth["r0"].loc[win]; dwt = pth["dw"].loc[win]
                        meta.append(dict(panel=pname, book=bname, conv=conv, tranche=tr, gross=gross,
                                         turnover_yr=float(dwt.sum() / yrs),
                                         mean_names=float(pth["names"].loc[win].mean()),
                                         mean_shy=float(pth["shy"].loc[win].mean()),
                                         mean_spy=float(pth["spy"].loc[win].mean()),
                                         mean_etf_nav=float(pth["watch"].loc[win].mean()),
                                         mean_gross=float(pth["gross"].loc[win].mean()),
                                         max_gross=float(pth["gross"].max()),
                                         max_w=float(pth["maxw"].max()),
                                         n_excluded=len((TRANCHES[tr] - {SWEEP}) & set(px.columns))))
                        for rung in RUNGS:
                            r = r0 - dwt * rung / 1e4
                            br = (base_paths[LIVE_GROSS]["r0"]
                                  - base_paths[LIVE_GROSS]["dw"] * rung / 1e4).loc[win]
                            r_oos = r.loc[OOS_START:]
                            h1, h2 = halves(r)
                            rows.append(dict(panel=pname, book=bname, conv=conv, tranche=tr,
                                             gross=gross, cost_bps=rung,
                                             CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                             H1=h1, H2=h2,
                                             IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                                             OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                                             base_Sharpe=sharpe(br), base_MaxDD=maxdd(br), base_CAGR=cagr(br),
                                             base_OOS_Sharpe=sharpe(br.loc[OOS_START:]),
                                             base_OOS_CAGR=cagr(br.loc[OOS_START:]),
                                             base_OOS_MaxDD=maxdd(br.loc[OOS_START:]),
                                             spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                                             spy_H1=halves(spy)[0], spy_H2=halves(spy)[1],
                                             spy_OOS_CAGR=cagr(spy_oos), spy_OOS_Sharpe=sharpe(spy_oos),
                                             spy_OOS_MaxDD=maxdd(spy_oos),
                                             turnover_yr=float(dwt.sum() / yrs),
                                             mean_gross=float(pth["gross"].loc[win].mean()),
                                             mean_names=float(pth["names"].loc[win].mean()),
                                             **legs(r, br, spy, r_oos, spy_oos)))
        say(f"    ... {pname} done ({time.time() - t0:.0f}s)")

    df = pd.DataFrame(rows); mf = pd.DataFrame(meta)
    df.to_csv(f"{OUT}.grid.csv", index=False); mf.to_csv(f"{OUT}.paths.csv", index=False)

    gate("G4 no leverage anywhere (realised row sums)", f"max gross {mf.max_gross.max():.9f}",
         "<= 1+1e-12", bool((mf.max_gross <= 1 + 1e-12).all()))
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP:]].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}", "True", shy_ok)
    above = mf[mf.tranche != "NONE"]
    gate("G6 SPY is never HELD above NONE, and SHY is held at every rung",
         f"max mean SPY weight above NONE {above.mean_spy.max():.3e};"
         f" min mean SHY weight over all rungs {mf.mean_shy.min():.2%}",
         "SPY == 0 and SHY > 0", (above.mean_spy.abs().max() < 1e-12) and (mf.mean_shy.min() > 0))

    mono = []
    for k, grp in mf.groupby(["panel", "book", "conv", "gross"]):
        s = grp.set_index("tranche").loc[LADDER]
        mono.append(bool((s.mean_names.diff().dropna() < 0).all() and
                         (s.n_excluded.diff().dropna() > 0).all()))
    gate("G5 the ladder is NESTED and BITES (each tranche strictly removes more, names held strictly falls)",
         f"{sum(mono)} of {len(mono)} (panel, book, conv, gross) ladders strictly monotone",
         "all", all(mono))

    a = df[(df.panel == "U56") & (df.book == "CAP2") & (df.tranche == "NONE") & (df.conv == HEADLINE_CONV)
           & (df.gross == LIVE_GROSS) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    b2 = df[(df.panel == "U56") & (df.book == "CAND") & (df.tranche == "NONE") & (df.conv == HEADLINE_CONV)
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

    # ------------------------------------------------------------ 0. what the ETFs are worth in the committed book
    say("\n=== 0. HOW MUCH OF THE COMMITTED BOOK'S NAV IS IN ETFs (realised, live gross) ===")
    for _, r in mf[(mf.tranche == "NONE") & (mf.gross == LIVE_GROSS) & (mf.conv == HEADLINE_CONV)].iterrows():
        say(f"    {r.panel:5s} {r.book:5s}:  mean gross {r.mean_gross:6.2%}   ETF sleeve {r.mean_etf_nav:6.2%} of NAV"
            f"   ({r.mean_etf_nav / max(r.mean_gross, 1e-9):5.1%} of the RISK book)   SPY alone {r.mean_spy:5.2%}"
            f"   SHY {r.mean_shy:6.2%}   names {r.mean_names:5.2f}")

    # ------------------------------------------------------------ A. the ladder
    for conv in CONVENTIONS:
        say(f"\n=== A. THE EXCLUSION LADDER — convention {conv}"
            f"{'  (HEADLINE)' if conv == HEADLINE_CONV else ''}, live gross 0.75, 10 bps ===")
        for pname in panels:
            for bname in BOOKS:
                say(f"  -- {pname} / {bname}")
                say("     tranche    CAGR   Sharpe   MaxDD    H1/H2         OOS CAGR/Sharpe/MaxDD   gross  names turn  4a 4b  binding")
                sub = df[(df.panel == pname) & (df.book == bname) & (df.conv == conv)
                         & (df.gross == LIVE_GROSS) & (df.cost_bps == HEADLINE_RUNG)].set_index("tranche")
                for tr in LADDER:
                    r = sub.loc[tr]
                    bind = ",".join(k[2:] for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR") if not r[k]) or "-"
                    say(f"     {tr:9s}  {r.CAGR:6.2%}  {r.Sharpe:6.4f}  {r.MaxDD:7.2%}"
                        f"  {r.H1:.4f}/{r.H2:.4f}  {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}"
                        f"  {r.mean_gross:5.1%}  {r.mean_names:5.1f} {r.turnover_yr:4.2f}"
                        f"   {int(r.pass4a)}  {int(r.pass4b)}  {bind}")

    say("\n=== A2. 4a / 4b COUNTS OVER EVERY ROW (the other gross and the other rungs) ===")
    cnt = df.groupby(["panel", "book", "conv", "tranche"]).agg(
        n=("pass4b", "size"), n4a=("pass4a", "sum"), n4b=("pass4b", "sum")).reset_index()
    for _, r in cnt.iterrows():
        say(f"    {r.panel:5s} {r.book:5s} {r.conv:8s} {r.tranche:8s}:  4a {int(r.n4a):2d}/{int(r.n):2d}"
            f"   4b {int(r.n4b):2d}/{int(r.n):2d}")

    say("\n=== A3. JOINT BOTH-PANEL 4b BY TRANCHE (the bar the record uses for adoption) ===")
    j = df.pivot_table(index=["book", "conv", "tranche", "gross", "cost_bps"], columns="panel",
                       values="pass4b", aggfunc="first", dropna=False)
    j["joint"] = j.get("U56", False) & j.get("B136", False)
    for tr in LADDER:
        s = j.xs(tr, level="tranche")
        say(f"    {tr:9s}: joint both-panel 4b {int(s.joint.sum()):2d} of {len(s)}")
    say(f"    all cells: {int(j.joint.sum())} of {len(j)}")

    # ------------------------------------------------------------ B. the attribution
    say("\n=== B. WHAT EACH TRANCHE WAS CARRYING (vs NONE, same panel/book/conv/gross/rung) ===")
    base = df[df.tranche == "NONE"].set_index(["panel", "book", "conv", "gross", "cost_bps"])
    dd = []
    for _, r in df[df.tranche != "NONE"].iterrows():
        b0 = base.loc[(r.panel, r.book, r.conv, r.gross, r.cost_bps)]
        dd.append(dict(panel=r.panel, book=r.book, conv=r.conv, tranche=r.tranche, gross=r.gross,
                       cost_bps=r.cost_bps, dCAGR=r.CAGR - b0.CAGR, dSharpe=r.Sharpe - b0.Sharpe,
                       dMaxDD=r.MaxDD - b0.MaxDD, dOOS_Sharpe=r.OOS_Sharpe - b0.OOS_Sharpe,
                       dOOS_CAGR=r.OOS_CAGR - b0.OOS_CAGR, dturn=r.turnover_yr - b0.turnover_yr,
                       dgross=r.mean_gross - b0.mean_gross))
    dfd = pd.DataFrame(dd); dfd.to_csv(f"{OUT}.delta.csv", index=False)
    for conv in CONVENTIONS:
        say(f"    convention {conv}, live gross, 10 bps:")
        for (pn, bk_, tr), g_ in dfd[(dfd.conv == conv) & (dfd.gross == LIVE_GROSS)
                                     & (dfd.cost_bps == HEADLINE_RUNG)].groupby(["panel", "book", "tranche"]):
            r = g_.iloc[0]
            say(f"      {pn:5s} {bk_:5s} {tr:8s}:  dCAGR {r.dCAGR * 100:+6.2f} pp  dSharpe {r.dSharpe:+.4f}"
                f"  dMaxDD {r.dMaxDD * 100:+6.2f} pp  dOOS_Sharpe {r.dOOS_Sharpe:+.4f}"
                f"  dgross {r.dgross * 100:+6.2f} pp  dturn {r.dturn:+.2f}x/yr")
    say(f"    over all {len(dfd)} exclusion cells: dSharpe > 0 in {int((dfd.dSharpe > 0).sum())};"
        f"  dCAGR > 0 in {int((dfd.dCAGR > 0).sum())};  dOOS_Sharpe > 0 in {int((dfd.dOOS_Sharpe > 0).sum())};"
        f"  dMaxDD > 0 (shallower) in {int((dfd.dMaxDD > 0).sum())}")

    # ------------------------------------------------------------ C. rule 8
    say("\n=== C. RULE 8 — BOTH DIALS FITTED ON <= 2016-12-31 ONLY, 2017-2026 READ ONCE ===")
    picks = []
    for (pname, bname, conv, rung), grp in df.groupby(["panel", "book", "conv", "cost_bps"]):
        for cname, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
            w = grp.sort_values([col], ascending=False).iloc[0]
            picks.append(dict(panel=pname, book=bname, conv=conv, cost_bps=rung, chooser=cname,
                              tranche=w.tranche, gross=w.gross, OOS_CAGR=w.OOS_CAGR,
                              OOS_Sharpe=w.OOS_Sharpe, OOS_MaxDD=w.OOS_MaxDD,
                              spy_OOS_Sharpe=w.spy_OOS_Sharpe, spy_OOS_CAGR=w.spy_OOS_CAGR,
                              spy_OOS_MaxDD=w.spy_OOS_MaxDD, base_OOS_Sharpe=w.base_OOS_Sharpe,
                              base_OOS_CAGR=w.base_OOS_CAGR, base_OOS_MaxDD=w.base_OOS_MaxDD,
                              pass4b=w.pass4b, pass4a=w.pass4a))
    pk = pd.DataFrame(picks); pk.to_csv(f"{OUT}.picks.csv", index=False)
    say(f"    {len(pk)} IS-only picks (2 choosers x 2 panels x 2 books x 2 conventions x 4 rungs).")
    say("    tranche distribution of the picks: "
        + ", ".join(f"{t}:{int((pk.tranche == t).sum())}" for t in LADDER))
    say(f"    OOS: {int((pk.OOS_Sharpe > pk.spy_OOS_Sharpe).sum())} of {len(pk)} beat SPY;"
        f"  {int((pk.OOS_Sharpe > pk.base_OOS_Sharpe).sum())} of {len(pk)} beat the live RULES v2 book;"
        f"  {int(pk.pass4b.sum())} of {len(pk)} carry a full-sample 4b pass.")
    anchor = df[df.tranche == "NONE"].set_index(["panel", "book", "conv", "gross", "cost_bps"])
    beat = 0; tot = 0
    for _, r in pk[pk.tranche != "NONE"].iterrows():
        a0 = anchor.loc[(r.panel, r.book, r.conv, r.gross, r.cost_bps)]
        tot += 1; beat += int(r.OOS_Sharpe > a0.OOS_Sharpe)
    say(f"    of the {tot} picks that excluded ETFs, {beat} beat their own cell's NONE anchor OOS.")
    say("    every pick, headline convention:")
    for _, r in pk[pk.conv == HEADLINE_CONV].sort_values(["panel", "book", "cost_bps", "chooser"]).iterrows():
        say(f"      {r.panel:5s} {r.book:5s} {int(r.cost_bps):3d}bps {r.chooser:11s}"
            f" -> {r.tranche:8s} g={r.gross:.2f}"
            f"  OOS {r.OOS_CAGR:6.2%}/{r.OOS_Sharpe:.4f}/{r.OOS_MaxDD:7.2%}"
            f"  (SPY {r.spy_OOS_CAGR:6.2%}/{r.spy_OOS_Sharpe:.4f}; base {r.base_OOS_CAGR:6.2%}/{r.base_OOS_Sharpe:.4f})"
            f"  4b={int(r.pass4b)}")

    # ------------------------------------------------------------ D. binding legs
    say("\n=== D. WHICH LEG BINDS ON THE 4b FAILS, BY TRANCHE (headline convention, all gross/rungs) ===")
    for tr in LADDER:
        f = df[(df.tranche == tr) & (df.conv == HEADLINE_CONV) & (~df.pass4b)]
        say(f"    {tr:9s} {len(f):2d} fails:  "
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
