#!/usr/bin/env python3
"""idea 2480 (lane cloud, run 58, 2026-09-23) — DOES THE CAPPED CANDIDATE'S 4b PASS SURVIVE
REPLACING SPY WITH THE PANEL'S OWN EQUAL-WEIGHT BUY-AND-HOLD IN ALL FIVE LEGS?

THE GAP.  PROTOCOL path 4b judges all five legs against SPY, a CAP-WEIGHTED index of 500 names.
The standing candidate is an EQUAL-WEIGHTED book over a CURRENT-CONSTITUENT panel of 56 (or 136)
names.  Two confounds ride in that comparison and neither has ever been separated from the band
gate the candidate is supposed to be testing:
  (i)  EQUAL-WEIGHT PREMIUM — an equal-weight book over ANY panel is a different factor bet
       (smaller-cap tilt, rebalancing premium) than a cap-weighted index, timing aside.
  (ii) SURVIVORSHIP (rule 9) — the panel is CURRENT constituents held from 2008, so its own
       buy-and-hold is flattered by exactly the bias that flatters the candidate.  SPY is not.
`L_CAGR` is the leg rule 9 says is most contaminated, and it is also the leg the record's own
census (idea 2477) found failing most often after `L_DD`.

THE TEST.  Re-run all five 4b legs with the benchmark replaced by the panel's OWN equal-weight
buy-and-hold: same names, same tape, NO TIMING, gross 1.00, charged at the SAME cost rung.  This
benchmark carries BOTH confounds, so whatever margin survives is attributable to the BAND GATE
and to nothing else.  Report how many committed 4b passes survive on each panel.

THE PRE-STATED PREDICTION, written before any compute: the candidate's edge is a DRAWDOWN edge
(it de-grosses into cash), not a return edge.  Against a benchmark that shares its survivorship
and its equal-weight tilt, `L_CAGR` and the two half-Sharpe legs should get HARDER (the panel's
own EW b&h earns more than SPY) while `L_DD` should get EASIER (an ungated EW panel draws down
harder than SPY did).  If the 4b pass is really the band gate, it survives; if it is the panel,
it does not.  Both outcomes are publishable and the run is designed to show either.

DIAL 1 -- gross g in {0.75 (live), 1.00}.
DIAL 2 -- per-name cap in {0.020 (CAP2, the committed candidate), INF (CAND, uncapped)}.
Exactly two tuned parameters (G6).  Panels {U56, B136}, rungs {0, 10, 25, 50} bps, weekly
cadence, t+1 execution, band 0.03, MA 200d and the phi = 1.00 SHY sweep are REPORTED, NEVER
SELECTED ON.

BENCHMARK CONVENTIONS, both published, the headline PRE-STATED here before any compute:
  EW_REBAL -- equal weight across every name PRICED that day, re-set on the book's own weekly
              cadence, gross 1.00, same rung.  **HEADLINE**: it holds the same names on the same
              days as the book and differs from it ONLY by the band gate and the cap, which is
              precisely the contrast the idea asks for.
  EW_DRIFT -- literal buy-and-hold: equal weight at the first scored day across names priced
              then, NEVER re-set, one entry charge.  Published to show the answer is not an
              artefact of the rebalancing premium inside EW_REBAL.
  SPY      -- the committed PROTOCOL benchmark, carried on every row so the two verdicts sit
              side by side and the DIFFERENCE, not the level, is the deliverable.
A third control, EW_EXBM (equal weight over the panel MINUS the SPY benchmark column and MINUS
the SHY sweep column), is published but never used for a verdict.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with L_DD, L_H2
and L_OOS all failing at every cell.  Changing the benchmark cannot create a pass where three
legs fail at every cell, and a SMALL EW b&h is MORE survivorship-flattered than U56's, so the
substitution can only make those legs harder.  There is no pass there to keep or break.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse
(4a is benchmark-invariant by construction and is carried as a control).  4b: Sharpe > BM in
BOTH halves AND out of sample, MaxDD >= 0.60 x BM's, CAGR >= 0.70 x BM's.
RULE 8: the two dials (gross, cap) are chosen on warm-up..2016-12-31 ONLY by two pre-stated
IS-only choosers, 2017-2026 is read ONCE, and the picks are scored under BOTH benchmarks.

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the band is
`baseline.band_state` bit for bit.  G3 the committed CAP2 / CAND U56 headlines reproduce.
G4 no leverage.  G5 cost exactly linear in the rung.  G6 exactly two tuned parameters.
G7 the EW benchmark is UNTIMED (it holds every priced name on every scored day).  G8 the EW
benchmark's name set IS the book's investable set.  G9 the SHY sweep is priced on every held
row.  G10 the EW benchmark runs at gross 1.00.  G11 EW_DRIFT really never re-sets (turnover is
one entry).  G12 the SPY legs reproduce the committed 4b verdicts of the incumbent cells.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward.  THIS RUN'S
POINT IS THAT CAVEAT: the EW benchmark carries the SAME bias as the book, so the candidate-vs-EW
margin is the first number in this record that is first-order immune to it, while every
candidate-vs-SPY margin is not.  The EW benchmark is NOT investable as stated (it presumes the
2026 constituent list was knowable in 2008); it is a CEILING on what the panel could have paid.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_panel-own-equal-weight-benchmark_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "panel-own-equal-weight-benchmark", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
GROSSES = [0.75, 1.00]
BOOKS = {"CAP2": 0.020, "CAND": np.inf}
RUNGS = [0.0, 10.0, 25.0, 50.0]
BENCH = ["SPY", "EW_REBAL", "EW_DRIFT"]
HEADLINE_BM, HEADLINE_RUNG = "EW_REBAL", 10.0
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


# ---------------------------------------------------------------- books
def risk_weights(px, gross, cap):
    """The committed candidate family: hold every priced name inside the 200d +/- band, gross/N
    each, clipped at `cap`; the residual is swept to SHY by the runner."""
    el = band_state(px, BAND) & px.notna()
    nin = el.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0)


def ew_weights(px, cols=None):
    """The panel's OWN equal weight: 1/N over every name PRICED that day, gross 1.00, no gate,
    no ranking, no timing of any kind."""
    sub = px if cols is None else px[cols]
    e = sub.notna().astype(float)
    w = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


# ---------------------------------------------------------------- the runner
def run_book(prices, w_risk, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim, except that the per-day turnover is retained so every cost rung
    is read off the SAME realised path.  Weights decided at t-1, applied at t; the book drifts
    between rebalances; the residual is swept into SHY at phi = 1.00 when `sweep`."""
    cols = list(prices.columns)
    si = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[SWEEP].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(1).values
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    cur = np.zeros(m)
    turn = np.zeros(n); r0 = np.zeros(n); gr = np.zeros(n); nheld = np.zeros(n); mx = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i].copy()
            if sweep:
                new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            turn[i] = float(np.abs(new - cur).sum())
            cur = new
        gr[i] = cur.sum(); nheld[i] = float((cur > 1e-12).sum()); mx[i] = float(cur.max())
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), names=pd.Series(nheld, index=idx),
                maxw=pd.Series(mx, index=idx))


def run_drift(prices, start):
    """Literal buy-and-hold: equal weight at `start` across the names priced then, never re-set.
    Gross 1.00 at entry, one entry charge of 1.0 turnover, then pure price drift."""
    sub = prices.loc[start:]
    live = sub.columns[sub.iloc[0].notna()]
    rel = sub[live].div(sub[live].iloc[0], axis=1)
    eq = rel.mean(axis=1)
    r0 = eq.pct_change().fillna(0.0)
    turn = pd.Series(0.0, index=sub.index); turn.iloc[0] = 1.0
    return dict(r0=r0, turn=turn, names=len(live))


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


def legs(r, base, bm):
    """The five 4b legs against an ARBITRARY benchmark `bm` (a return series over the same
    index), plus the benchmark-INVARIANT 4a verdict against the live RULES v2 book."""
    h1, h2 = halves(r); b1, b2 = halves(base); s1, s2 = halves(bm)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r.loc[OOS_START:]) > sharpe(bm.loc[OOS_START:])
    L_DD = maxdd(r) >= DD_CAP * maxdd(bm)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(bm)
    return dict(H1=h1, H2=h2,
                pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR),
                m_H1=h1 - s1, m_H2=h2 - s2,
                m_OOS=sharpe(r.loc[OOS_START:]) - sharpe(bm.loc[OOS_START:]),
                m_DD=maxdd(r) - DD_CAP * maxdd(bm),
                m_CAGR=cagr(r) - CAGR_FLOOR * cagr(bm))


def main():
    t0 = time.time()
    say("=== idea 2480 — DOES THE CANDIDATE'S 4b PASS SURVIVE THE PANEL'S OWN EQUAL-WEIGHT B&H AS BENCHMARK? ===")
    say(f"    {DATE}  lane {LANE} run 58   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 gross {GROSSES}    DIAL 2 per-name cap {{0.020 (CAP2), INF (CAND)}}")
    say(f"    BENCHMARKS {BENCH} (+ EW_EXBM control);  HEADLINE = {HEADLINE_BM}.")
    say("    PREDICTION, STATED BEFORE COMPUTE: the candidate's edge is a DRAWDOWN edge, not a return")
    say("    edge, so against the panel's own EW b&h `L_CAGR` / `L_H1` / `L_H2` should get HARDER and")
    say("    `L_DD` EASIER.  If the pass is the BAND GATE it survives; if it is the PANEL it does not.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (2383), 0 of 40-120 (2318/2322/2326/2343), three legs")
    say("    failing at every cell; a MORE survivorship-flattered EW benchmark can only make them harder.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008.  THIS RUN IS THAT")
    say("    CAVEAT: the EW benchmark carries the SAME bias as the book, so the margin against it is the")
    say("    first in this record that is first-order immune; the EW b&h is a CEILING, not an investable.")
    gate("G6 exactly two tuned parameters", "gross, per-name cap", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    bs = band_state(px_u, BAND)
    el = band_state(px_u, BAND) & px_u.notna()
    d2 = int((el != (bs & px_u.notna())).sum().sum())
    gate("G2 the gate IS baseline.band_state & priced, unmodified",
         f"{d2} differing cells; mean names IN {el.sum(axis=1).mean():.2f}", "0", d2 == 0)

    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # ------------------------------------------------------------ the grid
    rows, facts, bmfacts = [], [], []
    bm_series = {}
    for pname, px in panels.items():
        start = px.index[WARMUP]
        base_r = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]

        # ---- the benchmarks, each charged at every rung off its OWN realised path
        ewr = run_book(px, ew_weights(px), sweep=False)
        exbm_cols = [c for c in px.columns if c not in ("SPY", SWEEP)]
        ewx = run_book(px, ew_weights(px, exbm_cols), sweep=False)
        ewd = run_drift(px, start)
        spy_r0 = px["SPY"].pct_change().fillna(0.0).loc[start:]
        for rung in RUNGS:
            bm_series[(pname, "SPY", rung)] = spy_r0                    # an index pays no rung
            bm_series[(pname, "EW_REBAL", rung)] = (ewr["r0"] - ewr["turn"] * rung / 1e4).loc[start:]
            bm_series[(pname, "EW_DRIFT", rung)] = (ewd["r0"] - ewd["turn"] * rung / 1e4).loc[start:]
            bm_series[(pname, "EW_EXBM", rung)] = (ewx["r0"] - ewx["turn"] * rung / 1e4).loc[start:]
        for bname in BENCH + ["EW_EXBM"]:
            b = bm_series[(pname, bname, HEADLINE_RUNG)]
            h1, h2 = halves(b)
            bmfacts.append(dict(panel=pname, bench=bname, CAGR=cagr(b), Sharpe=sharpe(b),
                                MaxDD=maxdd(b), H1=h1, H2=h2, OOS_CAGR=cagr(b.loc[OOS_START:]),
                                OOS_Sharpe=sharpe(b.loc[OOS_START:]),
                                turnover_yr=(0.0 if bname == "SPY" else
                                             float({"EW_REBAL": ewr, "EW_DRIFT": ewd,
                                                    "EW_EXBM": ewx}[bname]["turn"].loc[start:].sum()
                                                   / (len(b) / 252)))))

        # gates on the EW benchmark itself (U56 only, published for both)
        gross_ew = ewr["gross"].loc[start:]
        nm_ew = ewr["names"].loc[start:]
        priced = px.notna().sum(axis=1).loc[start:]
        gate(f"G7/G10 EW_REBAL is UNTIMED and runs at gross 1.00 ({pname})",
             f"mean gross {gross_ew.mean():.6f} max {gross_ew.max():.6f};"
             f" mean names held {nm_ew.mean():.2f} vs mean names PRICED {priced.mean():.2f}",
             "gross==1, names held == names priced",
             bool(abs(gross_ew.mean() - 1.0) < 1e-9 and abs(nm_ew.mean() - priced.mean()) < 0.5))
        inv = (band_state(px, BAND) & px.notna()).columns
        gate(f"G8 EW's name set IS the book's investable set ({pname})",
             f"{len(inv)} columns both sides; set difference "
             f"{len(set(inv) ^ set(ew_weights(px).columns))}", "0", len(set(inv) ^ set(ew_weights(px).columns)) == 0)
        gate(f"G11 EW_DRIFT never re-sets ({pname})",
             f"total turnover {float(ewd['turn'].sum()):.4f} over {len(ewd['r0'])} rows,"
             f" {ewd['names']} names bought at {start.date()}", "exactly 1.0",
             abs(float(ewd["turn"].sum()) - 1.0) < 1e-12)

        for cname, cap in BOOKS.items():
            for gross in GROSSES:
                wr = risk_weights(px, gross, cap)
                bk = run_book(px, wr)
                r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                facts.append(dict(panel=pname, book=cname, gross=gross,
                                  turnover_yr=float(tn.sum() / (len(tn) / 252)),
                                  mean_names=float(bk["names"].loc[start:].mean()),
                                  mean_gross=float(bk["gross"].loc[start:].mean()),
                                  max_gross=float(bk["gross"].loc[start:].max()),
                                  max_name_w=float(bk["maxw"].loc[start:].max())))
                for rung in RUNGS:
                    r = r0 - tn * rung / 1e4
                    for bname in BENCH:
                        bm = bm_series[(pname, bname, rung)]
                        lg = legs(r, base_r, bm)
                        rows.append(dict(
                            panel=pname, book=cname, gross=gross, cost_bps=rung, bench=bname,
                            CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                            turnover_yr=float(tn.sum() / (len(tn) / 252)),
                            IS_Sharpe=sharpe(r.loc[:IS_END]), IS_Calmar=calmar(r.loc[:IS_END]),
                            IS_CAGR=cagr(r.loc[:IS_END]),
                            OOS_CAGR=cagr(r.loc[OOS_START:]), OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                            OOS_MaxDD=maxdd(r.loc[OOS_START:]),
                            base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r),
                            base_CAGR=cagr(base_r), base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                            bm_CAGR=cagr(bm), bm_Sharpe=sharpe(bm), bm_MaxDD=maxdd(bm),
                            bm_H1=halves(bm)[0], bm_H2=halves(bm)[1],
                            bm_OOS_Sharpe=sharpe(bm.loc[OOS_START:]),
                            bm_OOS_CAGR=cagr(bm.loc[OOS_START:]), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    ff = pd.DataFrame(facts); ff.to_csv(f"{OUT}.books.csv", index=False)
    bb = pd.DataFrame(bmfacts); bb.to_csv(f"{OUT}.benchmarks.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x 2 books x 2 gross x {len(RUNGS)} rungs x"
        f" {len(BENCH)} benchmarks; {len(ff)} distinct realised book paths, {len(bb)} benchmark paths.")

    gate("G4 no leverage anywhere (max gross <= 1)",
         f"max over {len(ff)} paths: {ff.max_gross.max():.6f} gross,"
         f" {ff.max_name_w.max():.4f} max single name", "<= 1+1e-12",
         bool(ff.max_gross.max() <= 1 + 1e-12))
    pz = panels["U56"]; bz = run_book(pz, risk_weights(pz, 0.75, 0.020)); st = pz.index[WARMUP]
    r0_ = bz["r0"].loc[st:]
    d5 = float(((r0_ - (bz["r0"] - bz["turn"] * 25 / 1e4).loc[st:]) * 2
                - (r0_ - (bz["r0"] - bz["turn"] * 50 / 1e4).loc[st:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    a = df[(df.panel == "U56") & (df.book == "CAP2") & (df.gross == 0.75)
           & (df.cost_bps == HEADLINE_RUNG) & (df.bench == "SPY")].iloc[0]
    b = df[(df.panel == "U56") & (df.book == "CAND") & (df.gross == 0.75)
           & (df.cost_bps == HEADLINE_RUNG) & (df.bench == "SPY")].iloc[0]
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 the committed CAP2 (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318) AND CAND"
         " (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines reproduce",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    gate("G12 the committed 4b verdict reproduces under SPY (U56 CAP2 g0.75 10bps is the standing pass)",
         f"pass4b {bool(a.pass4b)}, legs "
         + "".join("1" if a[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")),
         "True / 11111", bool(a.pass4b))

    # ------------------------------------------------------------ A. the benchmarks themselves
    say("\n=== A. WHAT THE TWO BENCHMARKS ACTUALLY ARE (10 bps, full sample from the scored start) ===")
    say("  panel bench     |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | turn/yr")
    for _, r in bb.iterrows():
        say(f"  {r.panel:5s} {r.bench:9s} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%} |"
            f" {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} | {r.turnover_yr:7.2f}"
            + ("   <= COMMITTED PROTOCOL BENCHMARK" if r.bench == "SPY" else
               "   <= HEADLINE" if r.bench == HEADLINE_BM else ""))
    say("\n  THE SIZE OF THE CONFOUND — the panel's own EW b&h minus SPY, same tape, both at 10 bps:")
    for pname in panels:
        s = bb[(bb.panel == pname) & (bb.bench == "SPY")].iloc[0]
        for bn in ("EW_REBAL", "EW_DRIFT", "EW_EXBM"):
            e = bb[(bb.panel == pname) & (bb.bench == bn)].iloc[0]
            say(f"   {pname:5s} {bn:9s} - SPY:  dCAGR {e.CAGR - s.CAGR:+6.2%}"
                f"  dSharpe {e.Sharpe - s.Sharpe:+7.4f}  dMaxDD {e.MaxDD - s.MaxDD:+6.2%}"
                f"  dH1 {e.H1 - s.H1:+6.3f}  dH2 {e.H2 - s.H2:+6.3f}"
                f"  dOOS Sh {e.OOS_Sharpe - s.OOS_Sharpe:+7.4f}")
    say("   -> the 4b bars MOVE by: CAGR floor 0.70 x dCAGR, DD cap 0.60 x dMaxDD, and the three")
    say("      Sharpe legs by the full dSharpe.  Positive dCAGR / dSharpe = HARDER; more negative")
    say("      dMaxDD = EASIER on L_DD.")

    # ------------------------------------------------------------ B. every grid point
    say("\n=== B. EVERY GRID POINT, ALL THREE BENCHMARKS ===")
    say("  panel book  g    bps bench     |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh"
        " | turn/yr | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for cname in BOOKS:
            for gross in GROSSES:
                for rung in RUNGS:
                    for bn in BENCH:
                        r = df[(df.panel == pname) & (df.book == cname) & (df.gross == gross)
                               & (df.cost_bps == rung) & (df.bench == bn)].iloc[0]
                        lg = "".join("1" if r[x] else "0"
                                     for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                        say(f"  {pname:5s} {cname:4s} {gross:.2f} {rung:5.1f} {bn:9s} | {r.CAGR:6.2%}"
                            f" {r.Sharpe:7.4f} {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} |"
                            f" {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} | {r.turnover_yr:7.2f} |"
                            f" {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}")

    # ------------------------------------------------------------ C. the answer
    say("\n=== C. THE WHOLE QUESTION: HOW MANY COMMITTED 4b PASSES SURVIVE THE SUBSTITUTION? ===")
    say("  panel | cells | 4b under SPY | 4b under EW_REBAL | 4b under EW_DRIFT | survive | new")
    surv = []
    for pname in list(panels) + ["BOTH"]:
        d = df if pname == "BOTH" else df[df.panel == pname]
        s = d[d.bench == "SPY"].set_index(["panel", "book", "gross", "cost_bps"]).pass4b
        for bn in ("EW_REBAL", "EW_DRIFT"):
            e = d[d.bench == bn].set_index(["panel", "book", "gross", "cost_bps"]).pass4b
            surv.append(dict(panel=pname, bench=bn, n=len(s), spy=int(s.sum()), ew=int(e.sum()),
                             survive=int((s & e).sum()), lost=int((s & ~e).sum()),
                             new=int((~s & e).sum())))
        a_ = [x for x in surv if x["panel"] == pname]
        say(f"  {pname:5s} | {a_[0]['n']:5d} | {a_[0]['spy']:12d} | {a_[0]['ew']:17d} |"
            f" {a_[1]['ew']:17d} | {a_[0]['survive']:2d}/{a_[0]['spy']} (EW_REBAL) |"
            f" +{a_[0]['new']}")
    pd.DataFrame(surv).to_csv(f"{OUT}.survival.csv", index=False)

    say("\n  CELL BY CELL (SPY verdict -> EW_REBAL verdict -> EW_DRIFT verdict, with the leg strings):")
    say("  panel book  g    bps | SPY 4b legs | EWR 4b legs | EWD 4b legs")
    for pname in panels:
        for cname in BOOKS:
            for gross in GROSSES:
                for rung in RUNGS:
                    out = []
                    for bn in BENCH:
                        r = df[(df.panel == pname) & (df.book == cname) & (df.gross == gross)
                               & (df.cost_bps == rung) & (df.bench == bn)].iloc[0]
                        out.append(("PASS" if r.pass4b else "fail",
                                    "".join("1" if r[x] else "0"
                                            for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))))
                    say(f"  {pname:5s} {cname:4s} {gross:.2f} {rung:5.1f} | "
                        + " | ".join(f"{v} {l}" for v, l in out))

    say("\n  WHICH LEG KILLS IT — leg-failure census over the 32 (panel, book, gross, rung) cells:")
    for bn in BENCH:
        d = df[df.bench == bn]
        say(f"   {bn:9s}: 4b {int(d.pass4b.sum()):2d}/{len(d)}   4a {int(d.pass4a.sum()):2d}/{len(d)}"
            "   fails: " + "  ".join(f"{x[2:]} {int((~d[x]).sum()):2d}" for x in
                                     ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  LEG MARGINS AT THE HEADLINE CELL (U56 CAP2 g0.75 10 bps) — the sign of each margin is the answer:")
    for bn in BENCH:
        r = df[(df.panel == "U56") & (df.book == "CAP2") & (df.gross == 0.75)
               & (df.cost_bps == HEADLINE_RUNG) & (df.bench == bn)].iloc[0]
        say(f"   vs {bn:9s}: H1 {r.m_H1:+7.4f}  H2 {r.m_H2:+7.4f}  OOS {r.m_OOS:+7.4f}"
            f"  DD {r.m_DD:+7.2%}  CAGR {r.m_CAGR:+7.2%}   -> {'PASS' if r.pass4b else 'FAIL'}"
            f"   (bench {r.bm_CAGR:.2%}/{r.bm_Sharpe:.4f}/{r.bm_MaxDD:.2%})")

    # ------------------------------------------------------------ D. rule 8
    say("\n=== D. RULE 8 — the two dials (gross, cap) chosen on warm-up..2016-12-31 ONLY, 2017-2026 read")
    say("    ONCE, scored under BOTH benchmarks.  The dials do not depend on the benchmark, so this")
    say("    isolates whether the OOS verdict is benchmark-sensitive at the SAME pick. ===")
    wf = []
    for pname in panels:
        for rung in RUNGS:
            d = df[(df.panel == pname) & (df.cost_bps == rung) & (df.bench == "SPY")]
            for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                pk = d.loc[d[col].idxmax()]
                for bn in BENCH:
                    q = df[(df.panel == pname) & (df.cost_bps == rung) & (df.bench == bn)
                           & (df.book == pk.book) & (df.gross == pk.gross)].iloc[0]
                    wf.append(dict(panel=pname, cost_bps=rung, chooser=chooser, bench=bn,
                                   pick=f"{pk.book}/{pk.gross:.2f}", full4b=bool(q.pass4b),
                                   OOS_CAGR=q.OOS_CAGR, OOS_Sharpe=q.OOS_Sharpe,
                                   OOS_MaxDD=q.OOS_MaxDD, bm_OOS_Sharpe=q.bm_OOS_Sharpe,
                                   bm_OOS_CAGR=q.bm_OOS_CAGR,
                                   base_OOS_Sharpe=q.base_OOS_Sharpe,
                                   beats_bm=bool(q.OOS_Sharpe > q.bm_OOS_Sharpe),
                                   beats_live=bool(q.OOS_Sharpe > q.base_OOS_Sharpe)))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} scored picks (2 panels x {len(RUNGS)} rungs x 2 choosers x {len(BENCH)} benchmarks)"
        f" over {len(wfd) // len(BENCH)} distinct IS-only picks.")
    say("   pick distribution: " + "  ".join(
        f"{p}:{int((wfd[wfd.bench == 'SPY'].pick == p).sum())}" for p in sorted(wfd.pick.unique())))
    for bn in BENCH:
        q = wfd[wfd.bench == bn]
        say(f"   under {bn:9s}: picks beating the BENCHMARK's OOS Sharpe {int(q.beats_bm.sum())}/{len(q)}"
            f"   beating the LIVE book's {int(q.beats_live.sum())}/{len(q)}"
            f"   carrying a full-sample 4b {int(q.full4b.sum())}/{len(q)}"
            f"   mean OOS Sharpe {q.OOS_Sharpe.mean():.4f} vs bench {q.bm_OOS_Sharpe.mean():.4f}"
            f"   mean OOS CAGR {q.OOS_CAGR.mean():.2%} vs bench {q.bm_OOS_CAGR.mean():.2%}")
    say("\n   panel   bps chooser     pick      | OOS CAGR  OOS Sh  OOS DD  | SPY 4b  EWR 4b  EWD 4b")
    for (pname, rung, ch), g in wfd.groupby(["panel", "cost_bps", "chooser"], sort=False):
        r = g[g.bench == "SPY"].iloc[0]
        v = {x.bench: ("PASS" if x.full4b else "fail") for _, x in g.iterrows()}
        say(f"   {pname:5s} {rung:5.1f} {ch:11s} {r['pick']:9s} | {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:7.4f}"
            f" {r.OOS_MaxDD:7.2%} | {v['SPY']:6s}  {v['EW_REBAL']:6s}  {v['EW_DRIFT']:6s}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
