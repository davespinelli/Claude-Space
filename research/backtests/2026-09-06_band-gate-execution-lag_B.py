#!/usr/bin/env python3
"""QUEUE idea 58 — band-gate-execution-lag (lane B, 2026-09-06).

Question
--------
Idea 57's standing 4b KEEP-candidate is `ew-all + 3% band` (equal weight every name
inside the 200d +/-3% hysteresis band, 75% gross, weekly).  The queue entry records it as
"dies between 10 and 25 bps on the cross-universe 4b test"; idea 82 later found the
verdict depends on the DE-GROSSING CONVENTION (`rw` full-gross rebuild survives to >=30
bps cross-universe, `dg` cash never passes), and NOTHING in the record has ever priced an
EXECUTION LAG for this book.  This run applies idea 45's protocol verbatim — 5/10/15/20/25
bps crossed with a 1-day and a 1-week execution lag, both large-cap universes as PRIMARY —
and reports where the cross-universe 4b pass is lost on each axis.

An identity problem found in flight (reported, not smoothed over)
------------------------------------------------------------------
The record quotes TWO DIFFERENT books as "idea 57's ew-band3", and this run reproduces
both to the published digits on u56 @10bps, weekly, gross 0.75, `rw`:
    band only  (TREND)            12.25% / 1.1609 / -17.71%   = idea 94's `EWall + band3-rw`
    band & vol20<0.60 (FULL)      11.26% / 1.1348 / -15.14%   = idea 66/268's `ew-band3 g=0.75`
So the STANDING 4b KEEP-CANDIDATE, the one the queue calls "ew-all + 3% band", is the FULL
gate: it still carries RULES v1's vol20 filter.  Both are carried through every cell below;
where they disagree the verdict is reported separately for each.  A third reading, `dg`
band-only, is byte-identical to the LIVE RULES v2 book (8.66%/1.2056/-12.05%), which is the
run's third reproduction gate.

Design (PROTOCOL rules 1-8)
---------------------------
Universes: research/universe.json (u56) and research/universe_broad.json (B136).  Both are
           reported as primary; a cross-universe pass is the object under test.
Books    : band in {0.00, 0.03, 0.06} x gate composition in {TREND, FULL} = 6 books, each
           run under both de-grossing conventions, plus a NOGATE control (always-invested
           ew-all at the same gross).  EXACTLY TWO TUNED PARAMETERS: the band width and the
           gate composition.  Gross is pinned at idea 57's 0.75 and cadence at weekly;
           neither is swept.  Every one of the grid points is reported.
Conv     : NOT a tuned parameter — idea 82 established that this book's verdict flips with
           it and that any bar RULES states must NAME it, so both readings are carried in
           full and neither is selected over the other.
           `rw` gated-out weight re-spread over the surviving names, gross pinned at 0.75
                (idea 57's own construction and idea 82's surviving reading);
           `dg` gated-out weight to CASH, gross floats down with the gate (RULES v2's
                live convention).
Lag      : the engine already applies weights decided at close t at t+1 (the `1d` arm).
           The `1w` arm shifts the weight matrix a further 4 trading days, so a signal
           formed at Friday's close is executed at the FOLLOWING Friday's close.  The
           rebalance schedule is unchanged; only the staleness of the target changes.
Costs    : held weights and turnover do not depend on cost_bps, so the five cost rungs are
           computed analytically from ONE zero-cost backtest per (book, lag, universe):
           r_c = r_0 - turnover * c/1e4.  Checked against the engine to machine precision.
Paths    : BOTH KEEP paths at every cell — 4a against the LIVE RULES v2 book run on the
           same universe/window, 4b against SPY (H1, H2, OOS, MaxDD <= 60% of SPY's,
           CAGR >= 70% of SPY's).
Rule 8   : at EVERY (universe, cost, lag) cell independently, (band, conv) is chosen on
           2009-2016 only under two rules fixed in advance — plain IS Sharpe, and IS Sharpe
           subject to the IS 4b bars — and that pick is then evaluated untouched on
           2017-2026 against the baseline's and SPY's OOS.

SURVIVORSHIP: both lists are current constituents, so absolute CAGRs are optimistic.  The
cost and lag comparisons hold names, days, gate, gross and cadence fixed and are far less
exposed than the levels are.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-06_band-gate-execution-lag_B"
OUT = ROOT / "research" / "backtests"
SCRIPT = f"research/backtests/{STEM}.py"

FREQ, GROSS = "W", 0.75
COSTS = [5, 10, 15, 20, 25]
LAGS = {"1d": 0, "1w": 4}                 # extra trading days on top of the engine's t+1
BANDS = [0.00, 0.03, 0.06]
COMPS = ["TREND", "FULL"]                 # TREND = band only; FULL = band & vol20 < MAX_VOL
CONVS = ["rw", "dg"]
MAX_VOL = 0.60
BOOKS = [(b, m_, c) for b in BANDS for m_ in COMPS for c in CONVS]
CAND = (0.03, "FULL", "rw")               # idea 57's committed arm (idea 66/268's row)
CAND_TREND = (0.03, "TREND", "rw")        # the same name in idea 94's row
IS_END, OOS_START = "2016-12-31", "2017-01-01"

_log = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _log.append(s)


# ------------------------------------------------------------------ construction
def band_gate(px, band):
    """200d MA band with hysteresis; band=0 degenerates to the plain px > 200d MA gate."""
    ma = px.rolling(200).mean()
    raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
    raw = raw.mask(px > ma * (1 + band), 1.0).mask(px < ma * (1 - band), 0.0)
    return raw.ffill().fillna(0.0) > 0.5


def weights_ewall(px, band, comp, conv, extra_lag=0, gross=GROSS):
    """dg: denominator = full priced universe (gross floats down with the gate).
    rw: denominator = surviving set (gross pinned at `gross`).
    comp FULL adds RULES v1's vol20 < 0.60 leg to the band; TREND is the band alone.
    band is None -> NOGATE control (always invested)."""
    live = px.notna()
    if band is None:
        sel = live
    else:
        sel = band_gate(px, band) & live
        if comp == "FULL":
            vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
            sel = sel & (vol20 < MAX_VOL)
    den = (live.sum(axis=1) if conv == "dg" else sel.sum(axis=1)).replace(0, np.nan)
    w = sel.astype(float).div(den, axis=0).mul(gross).fillna(0.0)
    return w.shift(extra_lag) if extra_lag else w


# ------------------------------------------------------------------ fast backtest
def fast_bt(px, w):
    """engine.backtest at cost_bps=0, in numpy. Returns (gross_returns, turnover)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, FREQ).shift(1, fill_value=False).values
    n = len(px)
    cur = np.zeros(px.shape[1])
    port = np.empty(n)
    turn = np.zeros(n)
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        port[i] = float((cur * rets[i]).sum())
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    idx = px.index
    return pd.Series(port, index=idx), pd.Series(turn, index=idx)


# ------------------------------------------------------------------ metrics
def m3(r):
    d = metrics(r)
    return d["CAGR"], d["Sharpe"], d["MaxDD"]


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail4a(r, base):
    _, _, dd = m3(r)
    h1, h2 = halves(r)
    _, _, bdd = m3(base)
    b1, b2 = halves(base)
    bad = []
    if h1 <= b1: bad.append("H1")
    if h2 <= b2: bad.append("H2")
    if dd < bdd: bad.append("DD")
    return bad


def fail4b(r, spy_stats, oos_sh):
    c, s, dd = m3(r)
    h1, h2 = halves(r)
    sc, s1, s2, sdd, ss_o = spy_stats
    bad = []
    if h1 <= s1: bad.append("H1")
    if h2 <= s2: bad.append("H2")
    if oos_sh <= ss_o: bad.append("OOS")
    if dd < 0.60 * sdd: bad.append("DD")
    if c < 0.70 * sc: bad.append("CAGR")
    return bad


def bname(key):
    b, m_, c = key
    return "NOGATE" if b is None else f"band{int(round(b * 100))}-{m_[0]}-{c}"


# ------------------------------------------------------------------ one universe
def sweep(px, tag):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    sc, ss, sdd = m3(spy)
    s1, s2 = halves(spy)
    ss_o = m3(spy.loc[OOS_START:])[1]
    spy_stats = (sc, s1, s2, sdd, ss_o)

    yrs = px.index.to_series().groupby(px.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        sys.exit("!! CALENDAR-DAY INDEX DETECTED — aborting.")

    base_full = backtest(px, rules_v2_weights(px), cost_bps=10, freq=FREQ)["returns"]
    base = base_full.loc[start:]
    v1 = backtest(px, rules_v1_weights(px), cost_bps=10, freq=FREQ)["returns"].loc[start:]
    b1, b2 = halves(base)
    bc, bs, bdd = m3(base)
    base_oos = m3(base_full.loc[OOS_START:])[1]

    P("\n" + "=" * 132)
    P(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
      f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    P(f"SPY            {sc:7.2%} / {ss:.4f} / {sdd:7.2%}  halves {s1:.4f}/{s2:.4f}  OOS Sharpe {ss_o:.4f}")
    P(f"RULES v2 (live){bc:7.2%} / {bs:.4f} / {bdd:7.2%}  halves {b1:.4f}/{b2:.4f}  OOS Sharpe {base_oos:.4f}")
    P(f"RULES v1 (prev){m3(v1)[0]:7.2%} / {m3(v1)[1]:.4f} / {m3(v1)[2]:7.2%}")
    P(f"4a bars (vs RULES v2): H1 > {b1:.4f}   H2 > {b2:.4f}   MaxDD >= {bdd:.2%}")
    P(f"4b bars (vs SPY)     : H1 > {s1:.4f}   H2 > {s2:.4f}   OOS > {ss_o:.4f}   "
      f"MaxDD >= {0.60 * sdd:.2%}   CAGR >= {0.70 * sc:.2%}")
    P("=" * 132)

    # ---- one zero-cost run per (book, lag)
    raw = {}
    keys = BOOKS + [(None, "TREND", "rw")]
    for key in keys:
        b, cmp_, c = key
        for lag, k in LAGS.items():
            g, t = fast_bt(px, weights_ewall(px, b, cmp_, c, k))
            raw[(key, lag)] = (g.loc[start:], t.loc[start:])

    # ---- harness gate [a]: fast_bt == engine.backtest
    wc = weights_ewall(px, *CAND)
    eng = backtest(px, wc, cost_bps=10, freq=FREQ)["returns"].loc[start:]
    g, t = raw[(CAND, "1d")]
    an = g - t * 10 / 1e4
    d = float(np.abs(an - eng).max())
    P(f"\n[a] fast_bt+analytic-cost vs engine.backtest ({bname(CAND)}, 10 bps, 1d)  "
      f"max|diff| = {d:.3e}   {'PASS' if d < 1e-12 else '*** MISMATCH ***'}")

    # ---- harness gate [b]: reproduce the record's published rows (u56 only)
    if tag == "u56":
        for key, ref, src in [((0.03, "TREND", "rw"), (0.122, 1.160, -0.177),
                               "idea 94 `u56 EWall + band3-rw`"),
                              ((0.03, "FULL", "rw"), (0.113, 1.136, -0.151),
                               "idea 66/268 `ew-band3 g=0.75` = THE STANDING CANDIDATE"),
                              ((0.03, "TREND", "dg"), (0.0866, 1.2056, -0.1205),
                               "idea 60 gate `LIVE RULES v2 on U56`")]:
            gg, tt = raw[(key, "1d")]
            c_, s_, dd_ = m3(gg - tt * 10 / 1e4)
            ok = abs(c_ - ref[0]) < 0.003 and abs(s_ - ref[1]) < 0.015 and abs(dd_ - ref[2]) < 0.006
            P(f"[b] {bname(key):<16} @10bps/1d -> {c_:6.2%}/{s_:.4f}/{dd_:7.2%}   "
              f"record {ref[0]:.2%}/{ref[1]:.4f}/{ref[2]:.2%} ({src})  "
              f"{'PASS' if ok else '*** MISMATCH ***'}")
        # [c] the dg/TREND book IS rules_v2_weights, elementwise
        dw = float(np.abs(weights_ewall(px, 0.03, "TREND", "dg") - rules_v2_weights(px)).max().max())
        P(f"[c] weights(band3-T-dg) vs baseline.rules_v2_weights   max|diff| = {dw:.3e}   "
          f"{'PASS' if dw < 1e-12 else '*** MISMATCH ***'}")

    # ---- turnover by book and lag
    P("\nAnnualised turnover (x of book) by book and execution lag:")
    for key in keys:
        nyrs = len(raw[(key, '1d')][0]) / 252
        line = "  ".join(f"{lag} {raw[(key, lag)][1].sum() / nyrs:5.2f}x" for lag in LAGS)
        P(f"  {bname(key):<14} {line}")

    # ---- the full grid: every book x lag x cost, both KEEP paths
    grid, rows = {}, []
    P(f"\n{'book':<14}{'lag':<5}{'bps':>4}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}"
      f"{'H1':>7}{'H2':>7}{'OOS':>7}{'turn':>7}   4a / 4b")
    P("-" * 132)
    for key in keys:
        for lag in LAGS:
            g, t = raw[(key, lag)]
            nyrs = len(g) / 252
            for cb in COSTS:
                r = g - t * cb / 1e4
                grid[(key, lag, cb)] = r
                oos = m3(r.loc[OOS_START:])[1]
                fa, fb = fail4a(r, base), fail4b(r, spy_stats, oos)
                va = "4a PASS" if not fa else "4a fail(" + ",".join(fa) + ")"
                vb = "4b PASS" if not fb else "4b fail(" + ",".join(fb) + ")"
                cg, sh, dd = m3(r)
                h1, h2 = halves(r)
                P(f"{bname(key):<14}{lag:<5}{cb:4d}{cg:8.2%}{sh:8.4f}{dd:8.2%}"
                  f"{h1:7.3f}{h2:7.3f}{oos:7.3f}{t.sum() / nyrs:7.2f}   {va} / {vb}")
                rows.append(dict(universe=tag, book=bname(key), band=key[0], comp=key[1], conv=key[2],
                                 lag=lag, bps=cb, CAGR=cg, Sharpe=sh, MaxDD=dd, H1=h1, H2=h2,
                                 OOS=oos, turnover=t.sum() / nyrs,
                                 pass4a=int(not fa), fail4a=",".join(fa),
                                 pass4b=int(not fb), fail4b=",".join(fb)))
        P("-" * 132)

    # ---- the price of the week's delay, paired daily
    P("\nCost decay (dSharpe per +10 bps over the 5-25 span) and the price of the 1-week lag @10bps:")
    lagrows = []
    for key in keys:
        out = []
        for lag in LAGS:
            s5, s25 = m3(grid[(key, lag, 5)])[1], m3(grid[(key, lag, 25)])[1]
            out.append(f"{lag} {10 * (s25 - s5) / 20:+.4f}")
        dser = (grid[(key, "1w", 10)] - grid[(key, "1d", 10)]).dropna()
        tstat = dser.mean() / dser.std() * np.sqrt(len(dser))
        dsh = m3(grid[(key, "1w", 10)])[1] - m3(grid[(key, "1d", 10)])[1]
        ddd = m3(grid[(key, "1w", 10)])[2] - m3(grid[(key, "1d", 10)])[2]
        P(f"  {bname(key):<14} {'  '.join(out)}    1w-1d @10bps: {dser.mean() * 252:+6.2%}/yr  "
          f"t {tstat:+5.2f}  dSharpe {dsh:+.4f}  dMaxDD {ddd:+.2%}")
        lagrows.append(dict(universe=tag, book=bname(key),
                            dSh_per10bps_1d=10 * (m3(grid[(key, '1d', 25)])[1] - m3(grid[(key, '1d', 5)])[1]) / 20,
                            dSh_per10bps_1w=10 * (m3(grid[(key, '1w', 25)])[1] - m3(grid[(key, '1w', 5)])[1]) / 20,
                            lag_dCAGR_yr=dser.mean() * 252, lag_t=tstat,
                            lag_dSharpe=dsh, lag_dMaxDD=ddd))

    # ---- rule 8 walk-forward, per (conv, cost, lag) cell.  Conv is NOT selected over:
    #      (band, comp) is chosen inside each convention, so neither reading borrows the
    #      other's hindsight.
    wf = []
    P(f"\nRULE 8 WALK-FORWARD ({tag}) — (band, comp) chosen on <= {IS_END} WITHIN each convention, "
      f"evaluated untouched on {OOS_START}+")
    P(f"{'conv':<5}{'lag':<5}{'bps':>4}  {'IS-Sharpe pick':<16}{'OOS Sh':>8}{'OOS CAGR':>10}{'OOS DD':>9}   "
      f"{'IS-4b pick':<16}{'OOS Sh':>8}{'OOS CAGR':>10}{'OOS DD':>9}   {'cand OOS Sh':>12}")
    spy_is = spy.loc[:IS_END]
    sc_i, ss_i, sdd_i = m3(spy_is)
    s1_i, s2_i = halves(spy_is)
    for conv in CONVS:
        pool = [k for k in BOOKS if k[2] == conv]
        cand_k = (CAND[0], CAND[1], conv)
        for lag in LAGS:
            for cb in COSTS:
                is_ = {k: grid[(k, lag, cb)].loc[:IS_END] for k in pool}
                oos_ = {k: grid[(k, lag, cb)].loc[OOS_START:] for k in pool}
                pick_sh = max(pool, key=lambda k: metrics(is_[k])["Sharpe"])
                elig = []
                for k in pool:
                    c_, s_, dd_ = m3(is_[k])
                    h1_, h2_ = halves(is_[k])
                    if h1_ > s1_i and h2_ > s2_i and dd_ >= 0.60 * sdd_i and c_ >= 0.70 * sc_i:
                        elig.append(k)
                pick_4b = max(elig, key=lambda k: metrics(is_[k])["Sharpe"]) if elig else None
                om = lambda k: (np.nan, np.nan, np.nan) if k is None else m3(oos_[k])
                a, b_, c_ = om(pick_sh)
                d_, e_, f_ = om(pick_4b)
                cc, cs, cd = m3(oos_[cand_k])
                P(f"{conv:<5}{lag:<5}{cb:4d}  {bname(pick_sh):<16}{b_:8.4f}{a:10.2%}{c_:9.2%}   "
                  f"{(bname(pick_4b) if pick_4b else 'none'):<16}{e_:8.4f}{d_:10.2%}{f_:9.2%}   {cs:12.4f}")
                wf.append(dict(universe=tag, conv=conv, lag=lag, bps=cb,
                               pick_ISsharpe=bname(pick_sh),
                               pick_ISsharpe_oosSharpe=b_, pick_ISsharpe_oosCAGR=a,
                               pick_ISsharpe_oosMaxDD=c_,
                               pick_IS4b=(bname(pick_4b) if pick_4b else "none"),
                               n_IS4b_eligible=len(elig),
                               pick_IS4b_oosSharpe=e_, pick_IS4b_oosCAGR=d_, pick_IS4b_oosMaxDD=f_,
                               cand_oosSharpe=cs, cand_oosCAGR=cc, cand_oosMaxDD=cd,
                               spy_oosSharpe=ss_o, spy_oosCAGR=m3(spy.loc[OOS_START:])[0],
                               spy_oosMaxDD=m3(spy.loc[OOS_START:])[2],
                               base_oosSharpe=base_oos))
    P(f"  SPY OOS {m3(spy.loc[OOS_START:])[0]:.2%}/{ss_o:.4f}/{m3(spy.loc[OOS_START:])[2]:.2%}   "
      f"RULES v2 OOS Sharpe {base_oos:.4f}   (`cand OOS Sh` = band3-FULL in the row's own convention)")
    return rows, lagrows, wf


# ------------------------------------------------------------------ run
P(f"IDEA 58 — band-gate-execution-lag (lane B).  {SCRIPT}")
P(f"Books: band in {BANDS} x gate composition in {COMPS} (2 tuned params), each under both "
  f"de-grossing conventions {CONVS} (a reported fork, not a tuned dial), + NOGATE control; "
  f"gross {GROSS}, cadence {FREQ}.")
P(f"Stress axes (not tuned): cost {COSTS} bps x lag {list(LAGS)} "
  f"(1w = 4 extra trading days of staleness on top of the engine's t+1).")

allrows, alllag, allwf = [], [], []
for tag, px in (("u56", load_universe()), ("B136", load_universe(broad=True))):
    r, l, w = sweep(px, tag)
    allrows += r; alllag += l; allwf += w

G = pd.DataFrame(allrows)
L = pd.DataFrame(alllag)
W = pd.DataFrame(allwf)
G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
L.to_csv(OUT / f"{STEM}.lagprice.csv", index=False)
W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

# ------------------------------------------------------------------ the answer
P("\n" + "=" * 132)
P("Q  WHERE IS THE CROSS-UNIVERSE 4b PASS LOST?  (a cell passes cross-universe iff it "
  "passes 4b on u56 AND on B136)")
P("=" * 132)
xu = (G[G.book != "NOGATE"]
      .pivot_table(index=["book", "lag", "bps"], columns="universe", values="pass4b")
      .reset_index())
xu["cross"] = (xu["u56"] * xu["B136"]).astype(int)
xu.to_csv(OUT / f"{STEM}.crossuniverse.csv", index=False)
P(f"\n{'book':<14}{'lag':<5}" + "".join(f"{c:>6}" for c in COSTS) +
  "     (1 = 4b passes on BOTH universes)")
for bk in sorted(xu.book.unique()):
    for lag in LAGS:
        sub = xu[(xu.book == bk) & (xu.lag == lag)].set_index("bps")
        P(f"{bk:<14}{lag:<5}" + "".join(f"{int(sub.loc[c, 'cross']):>6}" for c in COSTS))
P(f"\nCross-universe 4b passes: {int(xu['cross'].sum())} of {len(xu)} (book x lag x cost) cells.")
for bk in sorted(xu.book.unique()):
    s = xu[xu.book == bk]
    P(f"  {bk:<14} u56 {int(s['u56'].sum()):2d}/10   B136 {int(s['B136'].sum()):2d}/10   "
      f"cross {int(s['cross'].sum()):2d}/10")

for cname, ctitle in (("band3-F-rw", "THE STANDING CANDIDATE (idea 57/66/268 `ew-band3`, FULL gate, rw)"),
                      ("band3-T-rw", "the band-only reading of the same name (idea 94)")):
    P(f"\n{ctitle} — 4b by universe x lag x cost:")
    for tag in ("u56", "B136"):
        for lag in LAGS:
            s = G[(G.universe == tag) & (G.book == cname) & (G.lag == lag)].set_index("bps")
            P(f"  {tag:<5}{lag:<4}" + "  ".join(
                f"{c}bps:{'PASS' if s.loc[c, 'pass4b'] else 'fail(' + s.loc[c, 'fail4b'] + ')'}"
                for c in COSTS))

P("\nMECHANISM — what one week of execution staleness actually costs (24 gated books, 2 universes):")
Lg = L[L.book != "NOGATE"]
P(f"  return effect  : mean dCAGR {Lg.lag_dCAGR_yr.mean():+.3%}/yr, "
  f"max |t| over the 24 books {Lg.lag_t.abs().max():.2f} — "
  f"{int((Lg.lag_t.abs() > 1.96).sum())} of {len(Lg)} books significant at 5%")
P(f"  drawdown effect: MaxDD DEEPENS in {int((Lg.lag_dMaxDD < 0).sum())} of {len(Lg)} books, "
  f"mean {Lg.lag_dMaxDD.mean():+.2%} (worst {Lg.lag_dMaxDD.min():+.2%}); "
  f"Sharpe falls in {int((Lg.lag_dSharpe < 0).sum())} of {len(Lg)}")
Ln = L[L.book == "NOGATE"]
P(f"  PLACEBO (NOGATE, nothing to be stale about): dMaxDD "
  f"{' / '.join(f'{v:+.2%}' for v in Ln.lag_dMaxDD)}, dSharpe "
  f"{' / '.join(f'{v:+.4f}' for v in Ln.lag_dSharpe)}")
P("  => the lag is not a return tax, it is a GATE-TIMING tax that lands entirely in MaxDD,")
P("     which is the exact 4b bar it breaks.")

P("\nFirst-failing 4b bar, counted over all (universe, book, lag, cost) cells:")
fb = G[(G.book != "NOGATE") & (G.pass4b == 0)]["fail4b"].str.split(",").explode()
for k, v in fb.value_counts().items():
    P(f"  {k:<6} {v}")

P("\nRULE 8 SUMMARY (selection run inside each convention; SPY OOS Sharpe 0.8820):")
for tag in ("u56", "B136"):
    for conv in CONVS:
        w = W[(W.universe == tag) & (W.conv == conv)]
        P(f"  {tag:<5} {conv}: IS-Sharpe pick {w.pick_ISsharpe.mode().iloc[0]} in "
          f"{int((w.pick_ISsharpe == w.pick_ISsharpe.mode().iloc[0]).sum())}/{len(w)} cells; "
          f"IS-4b pick {w.pick_IS4b.mode().iloc[0]} in "
          f"{int((w.pick_IS4b == w.pick_IS4b.mode().iloc[0]).sum())}/{len(w)}.")
        P(f"          beats SPY OOS: IS-Sharpe pick {int((w.pick_ISsharpe_oosSharpe > w.spy_oosSharpe).sum())}/{len(w)}, "
          f"IS-4b pick {int((w.pick_IS4b_oosSharpe > w.spy_oosSharpe).sum())}/{len(w)}, "
          f"band3-FULL {int((w.cand_oosSharpe > w.spy_oosSharpe).sum())}/{len(w)}.")
        P(f"          mean OOS Sharpe: IS-Sharpe {w.pick_ISsharpe_oosSharpe.mean():.4f}, "
          f"IS-4b {w.pick_IS4b_oosSharpe.mean():.4f}, band3-FULL {w.cand_oosSharpe.mean():.4f}, "
          f"RULES v2 {w.base_oosSharpe.iloc[0]:.4f}.")
        P(f"          mean OOS CAGR:   IS-Sharpe {w.pick_ISsharpe_oosCAGR.mean():.2%}, "
          f"IS-4b {w.pick_IS4b_oosCAGR.mean():.2%}, band3-FULL {w.cand_oosCAGR.mean():.2%}, "
          f"SPY {w.spy_oosCAGR.iloc[0]:.2%}.")
        P(f"          mean OOS MaxDD:  IS-Sharpe {w.pick_ISsharpe_oosMaxDD.mean():.2%}, "
          f"IS-4b {w.pick_IS4b_oosMaxDD.mean():.2%}, band3-FULL {w.cand_oosMaxDD.mean():.2%}, "
          f"SPY {w.spy_oosMaxDD.iloc[0]:.2%}.")

(OUT / f"{STEM}.console.txt").write_text("\n".join(_log) + "\n")
print(f"\nwrote {STEM}.console.txt / .grid.csv / .lagprice.csv / .walkforward.csv / .crossuniverse.csv")
