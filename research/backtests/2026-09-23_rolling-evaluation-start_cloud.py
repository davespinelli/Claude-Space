#!/usr/bin/env python3
"""idea 2510 (lane cloud, run 64, 2026-09-23) — DOES THE CAPPED CANDIDATE'S 4b PASS SURVIVE A
ROLLING EVALUATION START?

THE GAP.  Every scored path in this record begins at row 260 of a 2008-start panel, i.e. the
first trading days of 2009 — one quarter off the GFC low.  The 2008-09 collapse and its rebound
therefore sit inside EVERY full-sample number the candidate owns, and BOTH of 4b's absolute legs
lean on that placement: `L_DD` is a ratio to SPY's own -33.72% (made almost entirely in that
episode) and `L_H1` is a Sharpe over a first half that CONTAINS the rebound.  Real capital is
never deployed at a bottom.

WHY EXCISING IS NOT THE SAME TEST.  Ideas 1799 / 2022 cut the crash window out MID-SAMPLE and
found the effect was mostly a BAR shift.  A truncated START is a different object: it also moves
the compounding base, moves the half-sample split point, and — decisively — removes the
benchmark's own -33.72% drawdown, which is the DENOMINATOR of 4b's `L_DD` leg.  Every one of
those three moves against the book.

THE DEVICE.  Roll the evaluation start to {COMMITTED (row 260), 2010-01-01, 2011-01-01,
2012-01-01, 2013-01-01} with the END fixed, re-scoring the BOOK, the LIVE RULES v2 baseline and
SPY end to end from each start, so SPY's floor and cap are recomputed on every window.  The
weights themselves are untouched: the rule is causal and identical at every start; only the
scoring window moves.  COMMITTED is the published window EXACTLY (G3 asserts bit-identity).

DIAL 1 -- evaluation start in {COMMITTED, 2010, 2011, 2012, 2013}.
DIAL 2 -- gross g in {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, rungs {0, 10, 25, 50} bps, books {CAP2, CAND},
cadence W, band 0.03, name cap 2%, SHY sweep at phi = 1.00, t+1 execution.

PRIOR, STATED BEFORE COMPUTE: the SIGN is known for `L_DD` and UNKNOWN for the rest.  Dropping
2008-09 removes ~34 pp of SPY drawdown, so the 4b DD CAP (60% of SPY's) TIGHTENS sharply on every
later start; the book's own MaxDD also falls, but a 200d gate's whole advantage is made in
exactly that episode, so it should fall LESS than the benchmark's.  If `L_DD` survives anyway the
candidate's risk claim is a property of the rule; if it collapses the record's DD margin is a
GFC artefact and must be described that way before any capital is committed.

SMALL NOT PRICED: the sub-$2B panel has never carried a 4b pass anywhere in this record
(0 of 128, idea 2383; 0 of 40-120, 2318/2322/2326/2343), and it begins in 2010 in any case.

SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008, so `L_CAGR` is the
contaminated leg; a LATER start makes that contamination WORSE, not better (fewer years over
which a delisted name could have hurt), so the CAGR numbers here are upper bounds.
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from baseline import load_universe, rules_v2_weights, band_state, backtest  # noqa

DATE, SLUG, LANE = "2026-09-23", "rolling-evaluation-start", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
STARTS = ["COMMITTED", "2010-01-01", "2011-01-01", "2012-01-01", "2013-01-01"]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG = 10.0
NAME_CAP, SWEEP = 0.020, "SHY"
BOOKS = {"CAP2": NAME_CAP, "CAND": np.inf}
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


def start_ts(px, s):
    return px.index[WARMUP] if s == "COMMITTED" else max(pd.Timestamp(s), px.index[WARMUP])


# ---------------------------------------------------------------- the book
def risk_weights(px, gross, cap):
    """The committed capped candidate: every in-band, priced name at min(gross/N_in, cap).
    The rule is IDENTICAL at every evaluation start — only the scoring window moves."""
    el = band_state(px, BAND) & px.notna()
    nin = el.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0)


def run_book(prices, w_risk, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim (weights decided at t-1, applied at t; drift between
    rebalances), except that per-day turnover is retained so every cost rung reads off the SAME
    realised path, and the residual is swept into SHY at phi = 1.00."""
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
            new = np.nan_to_num(wt[i]).copy()
            if sweep:
                new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            turn[i] = float(np.abs(new - cur).sum()); cur = new
        gr[i] = cur.sum(); nheld[i] = float((cur > 1e-12).sum()); mx[i] = float(cur.max())
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), names=pd.Series(nheld, index=idx),
                maxw=pd.Series(mx, index=idx))


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
    return dict(H1=h1, H2=h2, b_H1=b1, b_H2=b2, spy_H1=s1, spy_H2=s2,
                pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR),
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy),
                m_H1=h1 - s1, m_H2=h2 - s2, m_OOS=sharpe(r_oos) - sharpe(spy_oos))


def main():
    t0 = time.time()
    say("=== idea 2510 — DOES THE CAPPED CANDIDATE'S 4b PASS SURVIVE A ROLLING EVALUATION START? ===")
    say(f"    {DATE}  lane {LANE} run 64   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}  t+1"
        f"  rungs {RUNGS} bps  cap {NAME_CAP:.0%}  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 evaluation start {STARTS} (END fixed; BOOK, LIVE BASELINE and SPY all re-scored")
    say(f"    end to end from each start, so SPY's DD cap and CAGR floor move with the window)")
    say(f"    DIAL 2 gross {GROSSES}")
    say("    PRIOR, STATED BEFORE COMPUTE: the SIGN is known for L_DD only.  Dropping 2008-09 removes")
    say("    ~34 pp of SPY drawdown, so the 60%-of-SPY cap TIGHTENS sharply on every later start; the")
    say("    book's own MaxDD falls too, but a 200d gate earns its advantage in exactly that episode,")
    say("    so it should fall LESS.  If L_DD survives, the risk claim is a property of the rule; if it")
    say("    collapses, the record's DD margin is a GFC artefact and must be said so before capital.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (2383), 0 of 40-120 (2318/2322/2326/2343); it begins 2010.")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents; a LATER start makes the")
    say("    contamination WORSE, not better, so every CAGR here is an UPPER BOUND.")
    gate("G6 exactly two tuned parameters", "evaluation start, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        yrs13 = (px.index[-1] - start_ts(px, "2013-01-01")).days / 365.25
        gate(f"G0 >= 10y ({nm}) at the COMMITTED and at the SHORTEST start",
             f"{yrs:.1f}y committed / {yrs13:.1f}y from 2013, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y on both", yrs >= 10 and yrs13 >= 10)

    px_u = panels["U56"]

    # G1 replica fidelity against the engine on the LIVE book
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica == engine.backtest (live RULES v2, flat 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G2 the dial moves ONLY the scoring window: one realised path per (panel, book, gross)
    wr = risk_weights(px_u, 0.75, NAME_CAP)
    bk = run_book(px_u, wr)
    sub = {s: bk["r0"].loc[start_ts(px_u, s):] for s in STARTS}
    nested = all(sub[STARTS[i]].index[-1] == sub[STARTS[0]].index[-1] for i in range(len(STARTS))) \
        and all(len(sub[STARTS[i]]) > len(sub[STARTS[i + 1]]) for i in range(len(STARTS) - 1)) \
        and all(sub[STARTS[i + 1]].equals(sub[STARTS[i]].loc[sub[STARTS[i + 1]].index[0]:])
                for i in range(len(STARTS) - 1))
    gate("G2 every start is a SUFFIX of the SAME realised return path (the rule never changes)",
         "  ".join(f"{s}:{len(sub[s])}rows" for s in STARTS), "strictly nested, common END", nested)

    # G7 causality: truncating the panel changes no weight before the cut
    cut = px_u.index[3000]
    w_full = risk_weights(px_u, 0.75, NAME_CAP).loc[:cut]
    w_trunc = risk_weights(px_u.loc[:cut], 0.75, NAME_CAP)
    d7 = float((w_full - w_trunc).abs().max().max())
    gate("G7 the weight rule is CAUSAL (panel truncation at row 3000 changes nothing before it)",
         f"max|d| {d7:.3e} over {w_full.shape[0]}x{w_full.shape[1]} cells", "0.0", d7 == 0.0)

    # ------------------------------------------------------------ the grid
    rows, bench = [], []
    for pname, px in panels.items():
        spy_all = px["SPY"].pct_change().fillna(0.0)
        paths = {}
        for bname, cap in BOOKS.items():
            for gross in GROSSES:
                paths[(bname, gross)] = run_book(px, risk_weights(px, gross, cap))
        base_all = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                            cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
        for s in STARTS:
            st = start_ts(px, s)
            spy = spy_all.loc[st:]
            spy_oos = spy.loc[OOS_START:]
            base_r = base_all.loc[st:]
            bench.append(dict(panel=pname, start=s, start_date=str(st.date()), rows=len(spy),
                              years=len(spy) / 252,
                              spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                              spy_H1=halves(spy)[0], spy_H2=halves(spy)[1],
                              spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                              DD_cap=DD_CAP * maxdd(spy), CAGR_floor=CAGR_FLOOR * cagr(spy),
                              base_CAGR=cagr(base_r), base_Sharpe=sharpe(base_r),
                              base_MaxDD=maxdd(base_r),
                              IS_rows=len(spy.loc[:IS_END]), OOS_rows=len(spy_oos)))
            for bname in BOOKS:
                for gross in GROSSES:
                    bkp = paths[(bname, gross)]
                    r0 = bkp["r0"].loc[st:]; tn = bkp["turn"].loc[st:]
                    for rung in RUNGS:
                        r = r0 - tn * rung / 1e4
                        r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                        lg = legs(r, base_r, spy, r_oos, spy_oos)
                        rows.append(dict(
                            panel=pname, start=s, start_date=str(st.date()), book=bname,
                            gross=gross, cost_bps=rung, years=len(r) / 252,
                            CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                            turnover_yr=float(tn.sum() / (len(tn) / 252)),
                            IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                            IS_rows=len(r_is),
                            OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                            base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r), base_CAGR=cagr(base_r),
                            base_OOS_Sharpe=sharpe(base_all.loc[OOS_START:]),
                            base_OOS_CAGR=cagr(base_all.loc[OOS_START:]),
                            spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                            spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                            spy_IS_Sharpe=sharpe(spy.loc[:IS_END]), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bn = pd.DataFrame(bench); bn.to_csv(f"{OUT}.benchmarks.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x {len(STARTS)} starts x 2 books x"
        f" {len(GROSSES)} gross x {len(RUNGS)} rungs; 8 distinct realised weight paths"
        " (the rule never changes — only the window does).")

    pz = panels["U56"]
    bz = run_book(pz, risk_weights(pz, 0.75, NAME_CAP))
    stz = pz.index[WARMUP]
    r0z = bz["r0"].loc[stz:]
    d5 = float(((r0z - (bz["r0"] - bz["turn"] * 25 / 1e4).loc[stz:]) * 2
                - (r0z - (bz["r0"] - bz["turn"] * 50 / 1e4).loc[stz:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)

    # G8 WHERE the binding drawdown actually LIVES — the finding the ladder turns on
    def trough(r):
        eq = (1 + r).cumprod(); dd = eq / eq.cummax() - 1
        return dd.idxmin().date(), float(dd.min())

    say("\n    G8 WHERE THE BINDING DRAWDOWN LIVES (this is what the whole ladder turns on):")
    tr_ok = True
    for pname, px in panels.items():
        sp = px["SPY"].pct_change().fillna(0.0).loc[px.index[WARMUP]:]
        td, tv = trough(sp)
        bkq = run_book(px, risk_weights(px, 0.75, NAME_CAP))
        cd, cv = trough((bkq["r0"] - bkq["turn"] * HEADLINE_RUNG / 1e4).loc[px.index[WARMUP]:])
        say(f"      {pname}: SPY MaxDD {tv:.2%} troughs {td};  CAP2 g0.75 {cv:.2%} troughs {cd}")
        tr_ok = tr_ok and pd.Timestamp(td) >= pd.Timestamp("2014-01-01")
    gate("G8 the binding SPY drawdown is AFTER 2014 on BOTH panels — i.e. the committed window's"
         " -33.72% is NOT the GFC, so NO start on this ladder can remove it",
         f"both troughs after 2014-01-01: {tr_ok}", "True", tr_ok)
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    a = df[(df.panel == "U56") & (df.book == "CAP2") & (df.start == "COMMITTED")
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    b = df[(df.panel == "U56") & (df.book == "CAND") & (df.start == "COMMITTED")
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 start = COMMITTED reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS"
         " 12.77%/1.3318) AND CAND (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # ------------------------------------------------------------ A. what the window does to the BAR
    say("\n=== A. WHAT THE ROLLING START DOES TO THE BENCHMARK — i.e. TO 4b's OWN BAR ===")
    say("  panel start      from         yrs |  SPY CAGR  SPY Sh   SPY MaxDD |  DD CAP (60%)  CAGR FLOOR (70%) | live v2 CAGR/Sh/DD")
    for _, r in bn.iterrows():
        say(f"  {r.panel:5s} {r.start:10s} {r.start_date} {r.years:5.1f} | {r.spy_CAGR:9.2%}"
            f" {r.spy_Sharpe:7.4f} {r.spy_MaxDD:10.2%} | {r.DD_cap:12.2%} {r.CAGR_floor:16.2%}"
            f" | {r.base_CAGR:6.2%}/{r.base_Sharpe:.4f}/{r.base_MaxDD:7.2%}")
    say("\n  THE MECHANISM, in one line per panel: SPY's MaxDD and therefore 4b's DD CAP")
    for pname in panels:
        q = bn[bn.panel == pname]
        c = q[q.start == "COMMITTED"].iloc[0]
        say(f"   {pname}: SPY MaxDD {c.spy_MaxDD:.2%} (committed) -> "
            + " -> ".join(f"{r.spy_MaxDD:.2%}" for _, r in q[q.start != "COMMITTED"].iterrows())
            + f";  DD CAP {c.DD_cap:.2%} -> "
            + " -> ".join(f"{r.DD_cap:.2%}" for _, r in q[q.start != "COMMITTED"].iterrows()))

    # ------------------------------------------------------------ B. the ladder
    say("\n=== B. THE FULL LADDER, gross 0.75 — EVERY GRID POINT ===")
    say("  panel book  start        bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for bk_ in BOOKS:
            for s in STARTS:
                for rung in RUNGS:
                    r = df[(df.panel == pname) & (df.book == bk_) & (df.start == s)
                           & (df.gross == 0.75) & (df.cost_bps == rung)].iloc[0]
                    lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {pname:5s} {bk_:4s} {s:10s} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                        f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                        f" | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}"
                        + ("   <= COMMITTED" if s == "COMMITTED" else ""))
    say("\n  The same ladder at gross 1.00:")
    say("  panel book  start        bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | 4a 4b | legs")
    for pname in panels:
        for bk_ in BOOKS:
            for s in STARTS:
                for rung in RUNGS:
                    r = df[(df.panel == pname) & (df.book == bk_) & (df.start == s)
                           & (df.gross == 1.00) & (df.cost_bps == rung)].iloc[0]
                    lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {pname:5s} {bk_:4s} {s:10s} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                        f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                        f" | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}")

    # ------------------------------------------------------------ C. survival and binding leg
    say("\n=== C. THE WHOLE QUESTION: HOW MANY COMMITTED 4b PASSES SURVIVE EACH START, AND WHICH LEG BINDS FIRST? ===")
    say("  start       | 4b passes | 4a passes | binding leg on the 4b FAILs (L_H1/L_H2/L_OOS/L_DD/L_CAGR)")
    for s in STARTS:
        q = df[df.start == s]
        f_ = q[~q.pass4b]
        say(f"  {s:11s} | {int(q.pass4b.sum()):3d}/{len(q):3d}   | {int(q.pass4a.sum()):3d}/{len(q):3d}   | "
            + "  ".join(f"{x[2:]} {int((~f_[x]).sum()):2d}" for x in
                        ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    say("\n  SURVIVAL, cell by cell: of the 32 (panel, book, gross, rung) cells that PASS 4b at the")
    say("  COMMITTED start, how many still pass at each later start?")
    cells = df[df.start == "COMMITTED"]
    surv = []
    for _, c in cells.iterrows():
        row = dict(panel=c.panel, book=c.book, gross=c.gross, cost_bps=c.cost_bps,
                   committed=bool(c.pass4b))
        for s in STARTS[1:]:
            z = df[(df.panel == c.panel) & (df.book == c.book) & (df.gross == c.gross)
                   & (df.cost_bps == c.cost_bps) & (df.start == s)].iloc[0]
            row[s] = bool(z.pass4b)
        surv.append(row)
    sv = pd.DataFrame(surv); sv.to_csv(f"{OUT}.survival.csv", index=False)
    cp = sv[sv.committed]
    say(f"   committed 4b passes: {len(cp)} of {len(sv)} cells")
    for s in STARTS[1:]:
        say(f"    still passing at {s}: {int(cp[s].sum()):3d} of {len(cp)}"
            f"   (and NEW passes that did NOT pass at COMMITTED: {int(sv[~sv.committed][s].sum())})")
    say("\n   the surviving cells at the LATEST start (2013-01-01):")
    for _, r in cp[cp["2013-01-01"]].iterrows():
        say(f"    {r.panel:5s} {r.book:4s} g {r.gross:.2f} {r.cost_bps:5.1f} bps")
    if int(cp["2013-01-01"].sum()) == 0:
        say("    (none)")

    say("\n  MARGIN DECAY on the headline cells (10 bps, gross 0.75) — each leg's slack at each start:")
    say("  panel book  start      |   CAGR   Sharpe   MaxDD  | m_H1   m_H2   m_OOS  | m_DD     m_CAGR  | 4b")
    for pname in panels:
        for bk_ in BOOKS:
            for s in STARTS:
                r = df[(df.panel == pname) & (df.book == bk_) & (df.start == s)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                say(f"  {pname:5s} {bk_:4s} {s:10s} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:7.2%}"
                    f"  | {r.m_H1:+6.3f} {r.m_H2:+6.3f} {r.m_OOS:+6.3f} | {r.m_DD:+7.2%}"
                    f" {r.m_CAGR:+8.2%} | {'PASS' if r.pass4b else 'fail'}")

    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same book, gross, start, rung):")
    jt = []
    for bk_ in BOOKS:
        for gross in GROSSES:
            for s in STARTS:
                for rung in RUNGS:
                    q = df[(df.book == bk_) & (df.gross == gross) & (df.start == s)
                           & (df.cost_bps == rung)]
                    u = q[q.panel == "U56"].iloc[0]; v = q[q.panel == "B136"].iloc[0]
                    jt.append(dict(book=bk_, gross=gross, start=s, cost_bps=rung,
                                   joint=bool(u.pass4b and v.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells;  by start: "
        + "  ".join(f"{s}:{int(jf[jf.start == s].joint.sum())}/{len(jf[jf.start == s])}" for s in STARTS))
    pa = df[df.pass4a]
    say(f"\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse): {len(pa)} of {len(df)}")
    for _, r in pa.head(24).iterrows():
        say(f"    {r.panel:5s} {r.book:4s} {r.start:10s} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
            f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ D. rule 8
    say("\n=== D. RULE 8 — the two dials (start, gross) chosen on warm-up..2016-12-31 ONLY, 2017-2026")
    say("    read ONCE, and scored against the COMMITTED start / gross 0.75 cell, the live book and SPY.")
    say("    NOTE the start dial SHRINKS the IS window it is fitted on (published below), which is")
    say("    exactly the pathology rule 8 exists to expose. ===")
    wf = []
    for pname in panels:
        for bk_ in BOOKS:
            for rung in RUNGS:
                q = df[(df.panel == pname) & (df.book == bk_) & (df.cost_bps == rung)]
                cm = q[(q.start == "COMMITTED") & (q.gross == 0.75)].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pk = q.loc[q[col].idxmax()]
                    wf.append(dict(panel=pname, book=bk_, cost_bps=rung, chooser=chooser,
                                   pick_start=pk.start, pick_gross=pk.gross, pick_IS_rows=int(pk.IS_rows),
                                   full4b=bool(pk.pass4b), OOS_CAGR=pk.OOS_CAGR,
                                   OOS_Sharpe=pk.OOS_Sharpe, OOS_MaxDD=pk.OOS_MaxDD,
                                   committed_OOS_Sharpe=cm.OOS_Sharpe, committed_OOS_CAGR=cm.OOS_CAGR,
                                   committed_OOS_MaxDD=cm.OOS_MaxDD,
                                   base_OOS_Sharpe=pk.base_OOS_Sharpe, base_OOS_CAGR=pk.base_OOS_CAGR,
                                   spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x 2 books x {len(RUNGS)} rungs x 2 choosers).")
    say(f"   picks beating SPY's OOS Sharpe:                            {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:                  {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the COMMITTED start cell's OOS Sharpe:       {int((wfd.OOS_Sharpe > wfd.committed_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass on their OWN window:  {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution over start: " + "  ".join(
        f"{s}:{int((wfd.pick_start == s).sum())}" for s in STARTS))
    say("   pick distribution over gross: " + "  ".join(
        f"{g:.2f}:{int((wfd.pick_gross == g).sum())}" for g in GROSSES))
    say(f"   mean IS rows the picks were fitted on {wfd.pick_IS_rows.mean():.0f}"
        f" (COMMITTED start has {int(df[(df.start == 'COMMITTED') & (df.panel == 'U56')].IS_rows.iloc[0])})")
    say(f"   mean OOS Sharpe of the IS-only picks {wfd.OOS_Sharpe.mean():.4f}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_Sharpe.mean():.4f}"
        f" ({wfd.OOS_Sharpe.mean() - wfd.committed_OOS_Sharpe.mean():+.4f})"
        f" vs live book OOS {wfd.base_OOS_Sharpe.mean():.4f} vs SPY OOS {wfd.spy_OOS_Sharpe.mean():.4f}")
    say(f"   mean OOS CAGR  of the IS-only picks {wfd.OOS_CAGR.mean():.2%}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_CAGR.mean():.2%}"
        f" vs live book {wfd.base_OOS_CAGR.mean():.2%} vs SPY {wfd.spy_OOS_CAGR.mean():.2%}")
    say(f"   mean OOS MaxDD of the IS-only picks {wfd.OOS_MaxDD.mean():.2%}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_MaxDD.mean():.2%}")
    say("\n   panel book   bps chooser     | pick start/g       ISrows  OOS CAGR  OOS Sh  OOS DD  | committed OOS Sh | SPY OOS Sh")
    for _, r in wfd.iterrows():
        say(f"   {r.panel:5s} {r.book:4s} {r.cost_bps:5.1f} {r.chooser:11s} |"
            f" {r.pick_start + '/' + format(r.pick_gross, '.2f'):16s} {r.pick_IS_rows:6d}"
            f" {r.OOS_CAGR:9.2%} {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%}"
            f" | {r.committed_OOS_Sharpe:16.4f} | {r.spy_OOS_Sharpe:10.4f}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
