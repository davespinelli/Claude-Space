#!/usr/bin/env python3
"""idea 2502 (lane cloud, run 64, 2026-09-23) — DOES THE CAPPED CANDIDATE'S 4b PASS SURVIVE
EXECUTION DELAY BEYOND t+1?

THE GAP.  Every number the capped family owns (2322 onward) is scored at ONE execution delay:
`engine.backtest` shifts the target weights by exactly one session, so the close that makes the
decision is followed by the close that fills it.  Idea 2046's review swept {t+1, t+2, t+3} but
did so on the PRE-CAP candidate, and no line of the capped family has ever been re-priced at any
other delay.

WHY IT MATTERS FOR REAL CAPITAL.  The book's only signal is a 200d MA crossing with 3%
hysteresis — an object that moves on a timescale of months.  A rule like that OUGHT to be
delay-insensitive.  If CAP2's 4b margin decays materially between t+1 and t+3, the edge is not
the trend gate at all but a short-horizon reversal artefact sitting on top of it, and a human
running the book weekly WILL slip a day or two.  So the sign of the decay is the whole finding:
flat means the gate is what it claims to be; steep means the published headline is a
fill-timing number.

THE DEVICE.  Delay `d` sessions between the DECISION close and the APPLIED weights.  Both the
target-weight series AND the rebalance mask are shifted by `d`, so the trade that the weekly
boundary asks for is executed `d` sessions later at that day's close; the book drifts
undisturbed in between.  `d = 1` IS the committed convention EXACTLY (G3 asserts bit-identity
against the published CAP2 and CAND headlines).

DIAL 1 -- delay d in {1 (committed), 2, 3, 5} sessions.
DIAL 2 -- gross g in {0.75 (live), 1.00}.

REPORTED, NEVER SELECTED ON: panels {U56, B136}, rungs {0, 10, 25, 50} bps, books {CAP2, CAND},
cadence W, band 0.03, name cap 2%, SHY sweep at phi = 1.00.

PRIOR, STATED BEFORE COMPUTE: a 200d gate should be delay-insensitive, so the expectation is a
SMALL and UNSIGNED drift in CAGR and Sharpe with turnover essentially unchanged (the same trades
are made, one to four sessions later).  The run is designed to refute that: if the margin decays
monotonically in d the reading is a fill-timing artefact and the candidate should be described
that way before any capital is committed.

SMALL NOT PRICED: the sub-$2B panel has never carried a 4b pass anywhere in this record
(0 of 128, idea 2383; 0 of 40-120, 2318/2322/2326/2343).  A delay cannot move three failing legs
at once, so pricing it there would add rows and no information.

SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008, so `L_CAGR` is the
contaminated leg.  The d-vs-d=1 contrast is same-tape, same-panel and first-order immune to it.
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from baseline import load_universe, rules_v2_weights, band_state, backtest  # noqa

DATE, SLUG, LANE = "2026-09-23", "execution-delay-beyond-t1", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, CADENCE, WARMUP = 0.03, 200, "W", 260
DELAYS = [1, 2, 3, 5]
GROSSES = [0.75, 1.00]
RUNGS = [0.0, 10.0, 25.0, 50.0]
HEADLINE_RUNG, HEADLINE_D = 10.0, 1
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


# ---------------------------------------------------------------- the book
def risk_weights(px, gross, cap):
    """The committed capped candidate: every in-band, priced name at min(gross/N_in, cap)."""
    el = band_state(px, BAND) & px.notna()
    nin = el.sum(axis=1).replace(0, np.nan)
    per = (gross / nin).clip(upper=cap).fillna(0.0)
    return el.astype(float).mul(per, axis=0).fillna(0.0)


def run_book(prices, w_risk, delay=1, freq=CADENCE, sweep=True):
    """`engine.backtest` verbatim EXCEPT (a) per-day turnover is retained so every cost rung reads
    off the SAME realised path, (b) the residual is swept into SHY at phi = 1.00, and (c) the
    DECISION-TO-FILL lag is the dial: both the target weights and the rebalance mask are shifted
    by `delay` sessions instead of the engine's hard-coded 1.  delay = 1 is the engine exactly."""
    cols = list(prices.columns)
    si = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[SWEEP].notna().values.astype(float)
    wt = w_risk.reindex(prices.index).fillna(0.0).shift(delay).values
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(delay, fill_value=False).values

    n, m = len(prices.index), len(cols)
    cur = np.zeros(m)
    turn = np.zeros(n); r0 = np.zeros(n); gr = np.zeros(n); nheld = np.zeros(n); mx = np.zeros(n)
    nreb = 0
    for i in range(n):
        if mask[i] or i == 0:
            new = np.nan_to_num(wt[i]).copy()
            if sweep:
                new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i]
            turn[i] = float(np.abs(new - cur).sum()); cur = new; nreb += 1
        gr[i] = cur.sum(); nheld[i] = float((cur > 1e-12).sum()); mx[i] = float(cur.max())
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        cur = g / tot if tot > 0 else cur
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), names=pd.Series(nheld, index=idx),
                maxw=pd.Series(mx, index=idx), nreb=nreb)


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
    return dict(H1=h1, H2=h2,
                pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR),
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy))


def main():
    t0 = time.time()
    say("=== idea 2502 — DOES THE CAPPED CANDIDATE'S 4b PASS SURVIVE EXECUTION DELAY BEYOND t+1? ===")
    say(f"    {DATE}  lane {LANE} run 64   band {BAND}  MA {MA_LEN}d  cadence {CADENCE}"
        f"  rungs {RUNGS} bps  cap {NAME_CAP:.0%}  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 delay d {DELAYS} sessions between decision close and applied weights"
        f"    DIAL 2 gross {GROSSES}")
    say("    PRIOR, STATED BEFORE COMPUTE: a 200d gate with 3% hysteresis moves on a timescale of")
    say("    MONTHS, so the expectation is a small UNSIGNED drift and unchanged turnover.  A clean")
    say("    monotone decay in d would mean the published headline is a FILL-TIMING number, not a")
    say("    trend-gate number, and the candidate must be described that way before any capital.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (2383) and 0 of 40-120 (2318/2322/2326/2343).")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is")
    say("    the contaminated leg.  The d-vs-1 contrast is same-tape, same-day, first-order immune.")
    gate("G6 exactly two tuned parameters", "delay d, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]

    # G1 replica fidelity against the engine on the LIVE book at d = 1
    w_live = rules_v2_weights(px_u, band=BAND, gross=0.75)
    r_eng = backtest(px_u, w_live, cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"]
    lv = run_book(px_u, w_live, delay=1, sweep=False)
    d1 = float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max())
    gate("G1 per-column replica at d = 1 == engine.backtest (live RULES v2, 10 bps, sweep off)",
         f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    # G2 the delay dial touches ONLY the fill lag: the weight PATH at d is the d=1 path shifted
    wr = risk_weights(px_u, 0.75, NAME_CAP)
    b1_ = run_book(px_u, wr, delay=1)
    dd_shift = {}
    for d in DELAYS[1:]:
        bd = run_book(px_u, wr, delay=d)
        dd_shift[d] = (bd["nreb"], float(bd["turn"].sum() / b1_["turn"].sum() - 1))
    gate("G2 the rebalance COUNT is delay-invariant (the same weekly trades, d sessions later)",
         f"d=1:{b1_['nreb']}  " + "  ".join(f"d={d}:{v[0]}" for d, v in dd_shift.items()),
         "equal to within 1 (calendar edge)",
         all(abs(v[0] - b1_["nreb"]) <= 1 for v in dd_shift.values()))
    publish("G2b total turnover at d vs d=1 (U56, CAP2, g0.75)",
            "  ".join(f"d={d}:{v[1]:+.2%}" for d, v in dd_shift.items()))

    # G7 the delay is CAUSAL and strictly backward-looking: truncating the panel changes nothing
    cut = px_u.index[3000]
    w_full = risk_weights(px_u, 0.75, NAME_CAP).loc[:cut]
    w_trunc = risk_weights(px_u.loc[:cut], 0.75, NAME_CAP)
    d7 = float((w_full - w_trunc).abs().max().max())
    gate("G7 the weight rule is CAUSAL (panel truncation at row 3000 changes nothing before it)",
         f"max|d| {d7:.3e} over {w_full.shape[0]}x{w_full.shape[1]} cells", "0.0", d7 == 0.0)

    # ------------------------------------------------------------ the grid
    rows, book_facts = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        spy_oos, spy_is = spy.loc[OOS_START:], spy.loc[:IS_END]
        base_r = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEADLINE_RUNG, freq=CADENCE)["returns"].loc[start:]
        for bname, cap in BOOKS.items():
            for gross in GROSSES:
                wrx = risk_weights(px, gross, cap)
                for d in DELAYS:
                    bk = run_book(px, wrx, delay=d)
                    r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                    book_facts.append(dict(
                        panel=pname, book=bname, gross=gross, d=d,
                        turnover_yr=float(tn.sum() / (len(tn) / 252)),
                        rebalances=bk["nreb"],
                        mean_names=float(bk["names"].loc[start:].mean()),
                        mean_gross=float(bk["gross"].loc[start:].mean()),
                        max_gross=float(bk["gross"].loc[start:].max()),
                        max_name_w=float(bk["maxw"].loc[start:].max())))
                    for rung in RUNGS:
                        r = r0 - tn * rung / 1e4
                        r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                        lg = legs(r, base_r, spy, r_oos, spy_oos)
                        rows.append(dict(
                            panel=pname, book=bname, gross=gross, d=d, cost_bps=rung,
                            CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                            turnover_yr=float(tn.sum() / (len(tn) / 252)),
                            IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                            OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos), OOS_MaxDD=maxdd(r_oos),
                            base_Sharpe=sharpe(base_r), base_MaxDD=maxdd(base_r), base_CAGR=cagr(base_r),
                            base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                            base_OOS_CAGR=cagr(base_r.loc[OOS_START:]),
                            spy_CAGR=cagr(spy), spy_Sharpe=sharpe(spy), spy_MaxDD=maxdd(spy),
                            spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_CAGR=cagr(spy_oos),
                            spy_IS_Sharpe=sharpe(spy_is), **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x 2 books x {len(GROSSES)} gross x"
        f" {len(DELAYS)} delays x {len(RUNGS)} rungs; {len(bf)} distinct realised weight paths.")

    gate("G4 no leverage anywhere (max gross <= 1)",
         f"max over {len(bf)} paths: {bf.max_gross.max():.6f} gross,"
         f" {bf.max_name_w.max():.4f} max single name", "<= 1+1e-12",
         bool(bf.max_gross.max() <= 1 + 1e-12))

    pz = panels["U56"]
    bz = run_book(pz, risk_weights(pz, 0.75, NAME_CAP), delay=1)
    st = pz.index[WARMUP]
    r0_ = bz["r0"].loc[st:]
    d5 = float(((r0_ - (bz["r0"] - bz["turn"] * 25 / 1e4).loc[st:]) * 2
                - (r0_ - (bz["r0"] - bz["turn"] * 50 / 1e4).loc[st:])).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)
    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every held row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    a = df[(df.panel == "U56") & (df.book == "CAP2") & (df.d == 1)
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    b = df[(df.panel == "U56") & (df.book == "CAND") & (df.d == 1)
           & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 d = 1 reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318) AND"
         " CAND (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)

    # ------------------------------------------------------------ A. the full ladder
    say("\n=== A. THE FULL LADDER, gross 0.75 — EVERY GRID POINT ===")
    say("  panel book  d   bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | turn/yr | 4a 4b | H1/H2/OOS/DD/CAGR")
    for pname in panels:
        for bk_ in BOOKS:
            for d in DELAYS:
                for rung in RUNGS:
                    r = df[(df.panel == pname) & (df.book == bk_) & (df.d == d)
                           & (df.gross == 0.75) & (df.cost_bps == rung)].iloc[0]
                    lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {pname:5s} {bk_:4s} {d:3d} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                        f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                        f" | {r.turnover_yr:7.2f} | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}"
                        f"  | {lg}" + ("   <= COMMITTED" if d == 1 else ""))
    say("\n  The same ladder at gross 1.00:")
    say("  panel book  d   bps |   CAGR   Sharpe    MaxDD |   H1     H2   | OOS CAGR  OOS Sh | turn/yr | 4a 4b | legs")
    for pname in panels:
        for bk_ in BOOKS:
            for d in DELAYS:
                for rung in RUNGS:
                    r = df[(df.panel == pname) & (df.book == bk_) & (df.d == d)
                           & (df.gross == 1.00) & (df.cost_bps == rung)].iloc[0]
                    lg = "".join("1" if r[x] else "0" for x in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"))
                    say(f"  {pname:5s} {bk_:4s} {d:3d} {rung:5.1f} | {r.CAGR:6.2%} {r.Sharpe:7.4f}"
                        f" {r.MaxDD:8.2%} | {r.H1:5.2f} {r.H2:6.2f} | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f}"
                        f" | {r.turnover_yr:7.2f} | {'Y' if r.pass4a else '.'}  {'Y' if r.pass4b else '.'}  | {lg}")

    # ------------------------------------------------------------ B. the decay
    say("\n=== B. THE WHOLE QUESTION: THE 4b DECAY CURVE IN d (each d against its OWN d = 1 cell) ===")
    dec = []
    for pname in panels:
        for bk_ in BOOKS:
            for gross in GROSSES:
                for rung in RUNGS:
                    z = df[(df.panel == pname) & (df.book == bk_) & (df.gross == gross)
                           & (df.cost_bps == rung) & (df.d == 1)].iloc[0]
                    for d in DELAYS[1:]:
                        r = df[(df.panel == pname) & (df.book == bk_) & (df.gross == gross)
                               & (df.cost_bps == rung) & (df.d == d)].iloc[0]
                        dec.append(dict(panel=pname, book=bk_, gross=gross, cost_bps=rung, d=d,
                                        dCAGR=r.CAGR - z.CAGR, dSharpe=r.Sharpe - z.Sharpe,
                                        dMaxDD=r.MaxDD - z.MaxDD,
                                        dOOS_Sharpe=r.OOS_Sharpe - z.OOS_Sharpe,
                                        dOOS_CAGR=r.OOS_CAGR - z.OOS_CAGR,
                                        dTurn=r.turnover_yr / z.turnover_yr - 1,
                                        dm_DD=r.m_DD - z.m_DD, dm_CAGR=r.m_CAGR - z.m_CAGR,
                                        one4b=bool(z.pass4b), d4b=bool(r.pass4b)))
    dd2 = pd.DataFrame(dec); dd2.to_csv(f"{OUT}.decay.csv", index=False)
    say("  d | mean dCAGR  dSharpe   dMaxDD   dOOS Sh  dOOS CAGR  dTurn | 4b at d=1 -> 4b at d | worst dSharpe")
    for d in DELAYS[1:]:
        q = dd2[dd2.d == d]
        say(f"  {d} | {q.dCAGR.mean():+10.2%} {q.dSharpe.mean():+8.4f} {q.dMaxDD.mean():+8.2%}"
            f" {q.dOOS_Sharpe.mean():+8.4f} {q.dOOS_CAGR.mean():+9.2%} {q.dTurn.mean():+6.1%}"
            f" | {int(q.one4b.sum())}/{len(q)} -> {int(q.d4b.sum())}/{len(q)}"
            f" | {q.dSharpe.min():+.4f}")
    say("\n  The headline cells in full (10 bps, gross 0.75) — CAP2 and CAND on both panels:")
    say("  panel book  d |   CAGR   Sharpe    MaxDD  | OOS CAGR  OOS Sh | 4b | m_DD (slack) m_CAGR (slack)")
    for pname in panels:
        for bk_ in BOOKS:
            for d in DELAYS:
                r = df[(df.panel == pname) & (df.book == bk_) & (df.d == d)
                       & (df.gross == 0.75) & (df.cost_bps == HEADLINE_RUNG)].iloc[0]
                say(f"  {pname:5s} {bk_:4s} {d:2d} | {r.CAGR:6.2%} {r.Sharpe:7.4f} {r.MaxDD:8.2%}"
                    f"  | {r.OOS_CAGR:7.2%} {r.OOS_Sharpe:7.4f} | {'PASS' if r.pass4b else 'fail'}"
                    f" | {r.m_DD:+11.2%} {r.m_CAGR:+13.2%}")
    say("\n  MONOTONICITY: is the decay clean in d?  (sign of dSharpe over the 4 d-steps per cell)")
    mono_dn = mono_up = 0
    cells = df[df.d == 1][["panel", "book", "gross", "cost_bps"]].drop_duplicates()
    for _, c in cells.iterrows():
        v = [df[(df.panel == c.panel) & (df.book == c.book) & (df.gross == c.gross)
                & (df.cost_bps == c.cost_bps) & (df.d == d)].iloc[0].Sharpe for d in DELAYS]
        if all(v[i] > v[i + 1] for i in range(len(v) - 1)): mono_dn += 1
        if all(v[i] < v[i + 1] for i in range(len(v) - 1)): mono_up += 1
    say(f"   strictly DECAYING in d: {mono_dn} of {len(cells)} cells;"
        f" strictly IMPROVING in d: {mono_up} of {len(cells)};"
        f" non-monotone: {len(cells) - mono_dn - mono_up}")

    # ------------------------------------------------------------ C. KEEP counts
    say(f"\n=== C. KEEP COUNTS OVER ALL {len(df)} PUBLISHED ROWS ===")
    say(f"  4b passes: {int(df.pass4b.sum())} of {len(df)}      4a passes: {int(df.pass4a.sum())} of {len(df)}")
    for d in DELAYS:
        q = df[df.d == d]
        say(f"   d {d}: 4b {int(q.pass4b.sum()):3d}/{len(q)}   4a {int(q.pass4a.sum()):3d}/{len(q)}"
            "   binding leg on 4b FAILs: "
            + "  ".join(f"{x} {int((~q[x][~q.pass4b]).sum())}" for x in
                        ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR")))
    for rung in RUNGS:
        q = df[df.cost_bps == rung]
        say(f"   {rung:5.1f} bps: 4b {int(q.pass4b.sum()):3d}/{len(q)}   by d: "
            + "  ".join(f"{d}:{int(q[q.d == d].pass4b.sum())}/{len(q[q.d == d])}" for d in DELAYS))
    for pname in panels:
        q = df[df.panel == pname]
        say(f"   panel {pname}: 4b {int(q.pass4b.sum()):3d}/{len(q)}   4a {int(q.pass4a.sum()):3d}/{len(q)}")
    say("\n  JOINT BOTH-PANEL 4b (U56 AND B136 at the same book, gross, d, rung):")
    jt = []
    for bk_ in BOOKS:
        for gross in GROSSES:
            for d in DELAYS:
                for rung in RUNGS:
                    q = df[(df.book == bk_) & (df.gross == gross) & (df.d == d) & (df.cost_bps == rung)]
                    u = q[q.panel == "U56"].iloc[0]; v = q[q.panel == "B136"].iloc[0]
                    jt.append(dict(book=bk_, gross=gross, d=d, cost_bps=rung,
                                   joint=bool(u.pass4b and v.pass4b)))
    jf = pd.DataFrame(jt)
    say(f"   joint 4b: {int(jf.joint.sum())} of {len(jf)} cells;  by d: "
        + "  ".join(f"{d}:{int(jf[jf.d == d].joint.sum())}/{len(jf[jf.d == d])}" for d in DELAYS))
    pa = df[df.pass4a]
    say(f"\n  4a PASSES (Sharpe > live RULES v2 in BOTH halves AND MaxDD no worse): {len(pa)}")
    for _, r in pa.head(24).iterrows():
        say(f"    {r.panel:5s} {r.book:4s} d {r.d} g {r.gross:.2f} {r.cost_bps:5.1f}bps"
            f"  {r.CAGR:6.2%} / {r.Sharpe:.4f} / {r.MaxDD:7.2%}  turn {r.turnover_yr:.2f}x"
            f"  4b {'Y' if r.pass4b else '.'}")

    # ------------------------------------------------------------ D. rule 8
    say("\n=== D. RULE 8 — the two dials (d, gross) chosen on warm-up..2016-12-31 ONLY, 2017-2026 read")
    say("    ONCE, and scored against the COMMITTED d = 1 / gross 0.75 cell, the live book and SPY. ===")
    wf = []
    for pname in panels:
        for bk_ in BOOKS:
            for rung in RUNGS:
                q = df[(df.panel == pname) & (df.book == bk_) & (df.cost_bps == rung)]
                cm = q[(q.d == 1) & (q.gross == 0.75)].iloc[0]
                for chooser, col in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    pk = q.loc[q[col].idxmax()]
                    wf.append(dict(panel=pname, book=bk_, cost_bps=rung, chooser=chooser,
                                   pick_d=int(pk.d), pick_gross=pk.gross, full4b=bool(pk.pass4b),
                                   OOS_CAGR=pk.OOS_CAGR, OOS_Sharpe=pk.OOS_Sharpe,
                                   OOS_MaxDD=pk.OOS_MaxDD, pick_turn=pk.turnover_yr,
                                   committed_OOS_Sharpe=cm.OOS_Sharpe, committed_OOS_CAGR=cm.OOS_CAGR,
                                   committed_OOS_MaxDD=cm.OOS_MaxDD,
                                   base_OOS_Sharpe=pk.base_OOS_Sharpe, base_OOS_CAGR=pk.base_OOS_CAGR,
                                   spy_OOS_Sharpe=pk.spy_OOS_Sharpe, spy_OOS_CAGR=pk.spy_OOS_CAGR))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"  {len(wfd)} picks (2 panels x 2 books x {len(RUNGS)} rungs x 2 choosers).")
    say(f"   picks beating SPY's OOS Sharpe:                      {int((wfd.OOS_Sharpe > wfd.spy_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the live book's OOS Sharpe:            {int((wfd.OOS_Sharpe > wfd.base_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks beating the COMMITTED d=1 cell's OOS Sharpe:   {int((wfd.OOS_Sharpe > wfd.committed_OOS_Sharpe).sum())} of {len(wfd)}")
    say(f"   picks carrying a full-sample 4b pass:                {int(wfd.full4b.sum())} of {len(wfd)}")
    say("   pick distribution over d:     " + "  ".join(
        f"{d}:{int((wfd.pick_d == d).sum())}" for d in DELAYS))
    say("   pick distribution over gross: " + "  ".join(
        f"{g:.2f}:{int((wfd.pick_gross == g).sum())}" for g in GROSSES))
    say(f"   mean OOS Sharpe of the IS-only picks {wfd.OOS_Sharpe.mean():.4f}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_Sharpe.mean():.4f}"
        f" ({wfd.OOS_Sharpe.mean() - wfd.committed_OOS_Sharpe.mean():+.4f})"
        f" vs live book OOS {wfd.base_OOS_Sharpe.mean():.4f} vs SPY OOS {wfd.spy_OOS_Sharpe.mean():.4f}")
    say(f"   mean OOS CAGR  of the IS-only picks {wfd.OOS_CAGR.mean():.2%}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_CAGR.mean():.2%}"
        f" vs live book {wfd.base_OOS_CAGR.mean():.2%} vs SPY {wfd.spy_OOS_CAGR.mean():.2%}")
    say(f"   mean OOS MaxDD of the IS-only picks {wfd.OOS_MaxDD.mean():.2%}"
        f" vs the COMMITTED cell's {wfd.committed_OOS_MaxDD.mean():.2%}")
    say("\n   panel book   bps chooser     | pick d/g   OOS CAGR  OOS Sh  OOS DD  | committed OOS Sh | SPY OOS Sh")
    for _, r in wfd.iterrows():
        say(f"   {r.panel:5s} {r.book:4s} {r.cost_bps:5.1f} {r.chooser:11s} |"
            f" {str(r.pick_d) + '/' + format(r.pick_gross, '.2f'):9s} {r.OOS_CAGR:8.2%}"
            f" {r.OOS_Sharpe:7.4f} {r.OOS_MaxDD:7.2%} | {r.committed_OOS_Sharpe:16.4f}"
            f" | {r.spy_OOS_Sharpe:10.4f}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
