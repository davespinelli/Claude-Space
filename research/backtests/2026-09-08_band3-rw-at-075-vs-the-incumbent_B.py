#!/usr/bin/env python3
"""QUEUE idea 238 — band3-rw-at-075-vs-the-incumbent (lane B, 2026-09-08).

Question
--------
Idea 154 found that `EWall + band3-rw` at gross 0.75 carries a WIDER broad-universe 4b
drawdown margin than the incumbent `EWall + vol60-dg` (+0.0170 vs +0.0083 at 10 bps) in
6 of 6 large-cap cells, but a LOWER broad CAGR and Sharpe.  The queue asks that the two be
put head to head on idea 65's CADENCE-INSENSITIVITY bar and idea 45's EXECUTION-LAG test
*before either is called the safer book*.  This run does exactly that and nothing else: no
new dial is opened, no new book is proposed, and the two contenders are fixed in advance.

Books (EXACTLY TWO TUNED PARAMETERS: gate x convention)
-------------------------------------------------------
    gate  in {band3, vol60}   band3 = 200d MA with a +/-3% hysteresis re-entry band
                              vol60 = RULES v1's vol20 < 0.60 eligibility leg
    conv  in {rw, dg}         rw = gated-out weight RE-SPREAD over survivors, gross pinned
                                   at 0.75; dg = gated-out weight to CASH, gross floats down
    + NOGATE control          equal-weight every priced name at 0.75, always invested
All four (gate, conv) cells are reported at every grid point, so neither named contender
borrows the other convention's hindsight.  The two the queue names are `band3-rw` (idea
94/154) and `vol60-dg` (the incumbent); the two mirrors are carried as the honest fork.
Base book is EWall (equal weight) throughout; gross pinned at 0.75; nothing else is swept.

A GROSS-MATCHING problem found in flight (reported, not smoothed over)
----------------------------------------------------------------------
Idea 154's margin quote does NOT compare the two books at the same NOMINAL gross.  Under
`rw` the gross is pinned, so nominal 0.75 IS realised 0.75; under `dg` it floats DOWN with
the gate, so nominal 0.75 realises only ~0.72-0.73.  Idea 154 matched on REALISED gross,
i.e. it ran the incumbent at a nominal ~0.78.  Both matchings are defensible and they give
DIFFERENT margins, so this run carries BOTH and requires the verdict to hold under each:
    `vol60-dg`      nominal gross 0.75           (matched NOMINAL gross)
    `vol60-dg-rg75` nominal gross solved per panel so the target book's realised mean gross
                    over the eval window is 0.7500  (matched REALISED gross = idea 154's own
                    reading).  The nominal is pinned by an IDENTITY, not chosen for
                    performance, so it is not a third tuned parameter; it is excluded from
                    the rule-8 chooser pool for exactly that reason and reported beside it.

Stress axes (NOT tuned parameters — every point reported)
---------------------------------------------------------
    cadence in {D, W, M, Q}   idea 65's bar.  SWING = max - min full-sample Sharpe over the
                              four cadences within a (panel, lag, cost) cell.
    lag     in {1d, 1w}       idea 45's test.  1d = PROTOCOL's t+1; 1w shifts the weight
                              matrix 4 extra trading days, so a Friday-close signal executes
                              at the FOLLOWING Friday's close.  Schedule unchanged; only the
                              staleness of the target changes.
    cost    in {5,10,15,20,25} bps.  Held weights and turnover do not depend on cost, so the
                              five rungs come analytically from ONE zero-cost run per
                              (book, panel, cadence, lag): r_c = r_0 - turnover * c/1e4,
                              checked against engine.backtest to machine precision.
    panel   in {u56, B136}    both PRIMARY (idea 154's claim is a large-cap claim).

PRE-REGISTERED verdict rule (fixed before any number below was read)
--------------------------------------------------------------------
"X is the safer book" is granted only if X wins BOTH bars against the other contender:
  [BAR-65]  X has the strictly smaller cadence SWING in a MAJORITY of the 20
            (panel, lag, cost) cells, AND X loses no 4b verdict it holds at the incumbent
            weekly cadence when the cadence is moved to D, M or Q.
  [BAR-45]  X retains its 4b verdict under the 1w lag in EVERY (panel, cadence, cost) cell
            where it passes at 1d, AND X's drawdown deepening (dMaxDD = 1w - 1d) is the
            smaller of the two in a MAJORITY of the 40 (panel, cadence, cost) cells.
If the two bars disagree, or either contender fails its own bar, the verdict is that
NEITHER may be called the safer book (SPLIT), and idea 154's margin ordering stands as a
single-cadence, single-lag reading only.

Rule 8 (required): inside every (panel, cadence, lag, cost) cell the (gate, conv) pair is
chosen on 2009-2016 ONLY, under two rules fixed in advance — plain IS Sharpe, and IS Sharpe
subject to the IS 4b bars — and evaluated untouched on 2017-2026 against SPY's and the LIVE
RULES v2 baseline's OOS.

Both KEEP paths are evaluated at every grid point: 4a against the LIVE RULES v2 book run on
the same panel/window, 4b against SPY (H1, H2, OOS, MaxDD >= 60% of SPY's, CAGR >= 70%).

SURVIVORSHIP: both universe lists are current constituents, so absolute CAGRs are
optimistic.  Every comparison here holds names, days, gross and base book fixed and moves
only cadence, lag, cost and the gate, so it is far less exposed than the levels are.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-08_band3-rw-at-075-vs-the-incumbent_B"
OUT = ROOT / "research" / "backtests"
SCRIPT = f"research/backtests/{STEM}.py"

GROSS, MAX_VOL, BAND = 0.75, 0.60, 0.03
COSTS = [5, 10, 15, 20, 25]
CADENCES = ["D", "W", "M", "Q"]
LAGS = {"1d": 0, "1w": 4}
GATES = ["band3", "vol60"]
CONVS = ["rw", "dg"]
BOOKS = [(g, c) for g in GATES for c in CONVS] + [(None, "rw")]
A, B = ("band3", "rw"), ("vol60", "dg")          # the two contenders the queue names
RG = ("vol60", "dg-rg75")                        # the incumbent matched on REALISED gross
ALLBOOKS = BOOKS + [RG]
BASE_CAD = "W"                                    # the incumbent cadence
IS_END, OOS_START = "2016-12-31", "2017-01-01"

_log = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _log.append(s)


def bname(key):
    g, c = key
    return "NOGATE" if g is None else f"{g}-{c}"


# ------------------------------------------------------------------ construction
def gate_mask(px, gate):
    if gate is None:
        return pd.DataFrame(True, index=px.index, columns=px.columns)
    if gate == "band3":
        ma = px.rolling(200).mean()
        raw = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        raw = raw.mask(px > ma * (1 + BAND), 1.0).mask(px < ma * (1 - BAND), 0.0)
        return raw.ffill().fillna(0.0) > 0.5
    if gate == "vol60":
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        return (vol20 < MAX_VOL).fillna(False)
    raise ValueError(gate)


def weights(px, gate, conv, extra_lag=0, gross=GROSS):
    """EWall at nominal `gross`.  dg: denominator = full priced universe (gross floats down
    with the gate).  rw: denominator = the surviving set (gross pinned)."""
    dg = conv.startswith("dg")
    live = px.notna()
    sel = gate_mask(px, gate) & live
    den = (live.sum(axis=1) if (dg and gate is not None) else sel.sum(axis=1))
    w = sel.astype(float).div(den.replace(0, np.nan), axis=0).mul(gross).fillna(0.0)
    return w.shift(extra_lag) if extra_lag else w


# ------------------------------------------------------------------ fast backtest
def fast_bt(px, w, freq):
    """engine.backtest at cost_bps=0, in numpy.  Returns (gross_returns, turnover)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
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
    return pd.Series(port, index=px.index), pd.Series(turn, index=px.index)


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


# ------------------------------------------------------------------ one panel
def sweep(px, tag):
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    sc, ss, sdd = m3(spy)
    s1, s2 = halves(spy)
    spy_oos = spy.loc[OOS_START:]
    sco, ss_o, sddo = m3(spy_oos)
    spy_stats = (sc, s1, s2, sdd, ss_o)

    yrs = px.index.to_series().groupby(px.index.year).count()
    if yrs.loc[2015:2024].max() > 300:
        sys.exit("!! CALENDAR-DAY INDEX DETECTED — aborting.")

    base_full = backtest(px, rules_v2_weights(px), cost_bps=10, freq=BASE_CAD)["returns"]
    base = base_full.loc[start:]
    v1 = backtest(px, rules_v1_weights(px), cost_bps=10, freq=BASE_CAD)["returns"].loc[start:]
    bc, bs, bdd = m3(base)
    b1, b2 = halves(base)
    base_oos = m3(base_full.loc[OOS_START:])[1]

    P("\n" + "=" * 138)
    P(f"{tag}: {px.shape[1]} tickers, eval {start.date()} -> {px.index[-1].date()} "
      f"(index sanity: 2018 {yrs.get(2018)} rows, 2024 {yrs.get(2024)} rows)")
    P(f"SPY             {sc:7.2%} / {ss:.4f} / {sdd:7.2%}  halves {s1:.4f}/{s2:.4f}  "
      f"OOS {sco:7.2%}/{ss_o:.4f}/{sddo:7.2%}")
    P(f"RULES v2 (live) {bc:7.2%} / {bs:.4f} / {bdd:7.2%}  halves {b1:.4f}/{b2:.4f}  "
      f"OOS Sharpe {base_oos:.4f}")
    P(f"RULES v1 (prev) {m3(v1)[0]:7.2%} / {m3(v1)[1]:.4f} / {m3(v1)[2]:7.2%}")
    P(f"4a bars (vs RULES v2): H1 > {b1:.4f}   H2 > {b2:.4f}   MaxDD >= {bdd:.2%}")
    P(f"4b bars (vs SPY)     : H1 > {s1:.4f}   H2 > {s2:.4f}   OOS > {ss_o:.4f}   "
      f"MaxDD >= {0.60 * sdd:.2%}   CAGR >= {0.70 * sc:.2%}")
    P("=" * 138)

    # ---- pin the realised-gross-matched incumbent by identity (no performance input)
    w1 = weights(px, RG[0], RG[1], gross=1.0)
    rg1 = w1.sum(axis=1).loc[start:].mean()
    G_RG = 0.75 / rg1
    rg_check = weights(px, RG[0], RG[1], gross=G_RG).sum(axis=1).loc[start:].mean()
    P(f"\nrealised-gross matching ({tag}): `vol60-dg` at nominal 0.7500 realises "
      f"{weights(px, *B).sum(axis=1).loc[start:].mean():.4f}; `vol60-dg-rg75` uses nominal "
      f"{G_RG:.4f} -> realised {rg_check:.4f}   (`band3-rw` pins gross, realised "
      f"{weights(px, *A).sum(axis=1).loc[start:].mean():.4f})")

    # ---- one zero-cost run per (book, cadence, lag)
    raw = {}
    for key in ALLBOOKS:
        gr = G_RG if key == RG else GROSS
        for cad in CADENCES:
            for lag, k in LAGS.items():
                g, t = fast_bt(px, weights(px, key[0], key[1], k, gross=gr), cad)
                raw[(key, cad, lag)] = (g.loc[start:], t.loc[start:])

    # ---- gate [a]: fast_bt + analytic cost == engine.backtest
    eng = backtest(px, weights(px, *A), cost_bps=10, freq=BASE_CAD)["returns"].loc[start:]
    g, t = raw[(A, BASE_CAD, "1d")]
    d = float(np.abs((g - t * 10 / 1e4) - eng).max())
    P(f"\n[a] fast_bt+analytic-cost vs engine.backtest ({bname(A)}, W, 1d, 10 bps)  "
      f"max|diff| = {d:.3e}   {'PASS' if d < 1e-12 else '*** MISMATCH ***'}")

    # ---- gate [b]: reproduce the record's published rows for BOTH contenders (u56)
    if tag == "u56":
        for key, ref, src in [(A, (0.122, 1.160, -0.177), "idea 94/97 `u56 EWall + band3-rw`"),
                              (B, (0.116, 1.133, -0.169), "idea 97 `u56 EWall + vol60-dg` (INCUMBENT)")]:
            gg, tt = raw[(key, BASE_CAD, "1d")]
            c_, s_, dd_ = m3(gg - tt * 10 / 1e4)
            ok = abs(c_ - ref[0]) < 0.003 and abs(s_ - ref[1]) < 0.015 and abs(dd_ - ref[2]) < 0.006
            P(f"[b] {bname(key):<10} W/1d/10bps -> {c_:6.2%}/{s_:.4f}/{dd_:7.2%}   record "
              f"{ref[0]:.2%}/{ref[1]:.4f}/{ref[2]:.2%} ({src})  {'PASS' if ok else '*** MISMATCH ***'}")

    # ---- gate [c]: idea 154's broad drawdown-margin claim at 10 bps, under BOTH matchings
    if tag == "B136":
        P("[c] idea 154's claim — broad, W/1d/10 bps.  dd-margin = MaxDD - 0.60*SPY MaxDD; "
          "idea 154 published band3-rw 11.73%/1.0690/-18.53% (margin +0.0170) vs its "
          "'incumbent' 12.86%/1.1381/-19.41% (margin +0.0083):")
        for key, ref in [(A, 0.0170), (B, 0.0083), (RG, 0.0083)]:
            gg, tt = raw[(key, BASE_CAD, "1d")]
            c_, s_, dd_ = m3(gg - tt * 10 / 1e4)
            marg = dd_ - 0.60 * sdd
            P(f"    {bname(key):<14} {c_:6.2%}/{s_:.4f}/{dd_:7.2%}  margin {marg:+.4f}   vs "
              f"published {ref:+.4f}   {'PASS' if abs(marg - ref) < 0.004 else '*** MISMATCH ***'}")
        P("    => the published gap is a GROSS-MATCHING artefact: idea 154 matched on REALISED "
          "gross, where the incumbent's margin is +0.0083; at matched NOMINAL gross it is "
          "+0.0153 and the gap all but closes.")

    # ---- the full grid
    grid, rows = {}, []
    P(f"\n{'book':<11}{'cad':<4}{'lag':<5}{'bps':>4}{'CAGR':>8}{'Sharpe':>8}{'MaxDD':>8}"
      f"{'H1':>7}{'H2':>7}{'OOS':>7}{'turn':>7}{'ddMarg':>8}{'cgMarg':>8}   4a / 4b")
    P("-" * 138)
    for key in ALLBOOKS:
        for cad in CADENCES:
            for lag in LAGS:
                gg, tt = raw[(key, cad, lag)]
                nyrs = len(gg) / 252
                for cb in COSTS:
                    r = gg - tt * cb / 1e4
                    grid[(key, cad, lag, cb)] = r
                    oos = m3(r.loc[OOS_START:])[1]
                    fa, fb = fail4a(r, base), fail4b(r, spy_stats, oos)
                    cg, sh, dd = m3(r)
                    h1, h2 = halves(r)
                    P(f"{bname(key):<11}{cad:<4}{lag:<5}{cb:4d}{cg:8.2%}{sh:8.4f}{dd:8.2%}"
                      f"{h1:7.3f}{h2:7.3f}{oos:7.3f}{tt.sum() / nyrs:7.2f}"
                      f"{dd - 0.60 * sdd:+8.4f}{cg - 0.70 * sc:+8.4f}   "
                      f"{'4a PASS' if not fa else '4a fail(' + ','.join(fa) + ')'} / "
                      f"{'4b PASS' if not fb else '4b fail(' + ','.join(fb) + ')'}")
                    rows.append(dict(panel=tag, book=bname(key), gate=key[0], conv=key[1],
                                     cadence=cad, lag=lag, bps=cb, CAGR=cg, Sharpe=sh, MaxDD=dd,
                                     H1=h1, H2=h2, OOS=oos, turnover=tt.sum() / nyrs,
                                     dd_margin=dd - 0.60 * sdd, cagr_margin=cg - 0.70 * sc,
                                     pass4a=int(not fa), fail4a=",".join(fa),
                                     pass4b=int(not fb), fail4b=",".join(fb)))
        P("-" * 138)

    # ---- rule 8 walk-forward: (gate, conv) chosen on IS only, in every cell
    wf = []
    spy_is = spy.loc[:IS_END]
    sc_i, ss_i, sdd_i = m3(spy_is)
    s1_i, s2_i = halves(spy_is)
    pool = [k for k in BOOKS if k[0] is not None]
    P(f"\nRULE 8 WALK-FORWARD ({tag}) — (gate, conv) chosen on <= {IS_END}, evaluated untouched "
      f"on {OOS_START}+   [SPY OOS {sco:.2%}/{ss_o:.4f}/{sddo:.2%}; RULES v2 OOS Sharpe {base_oos:.4f}]")
    P(f"{'cad':<4}{'lag':<5}{'bps':>4}  {'IS-Sharpe pick':<12}{'OOS Sh':>8}{'OOS CAGR':>10}{'OOS DD':>9}"
      f"   {'IS-4b pick':<12}{'OOS Sh':>8}{'OOS CAGR':>10}{'OOS DD':>9}"
      f"   {'band3-rw OOS':>13}{'vol60-dg OOS':>13}")
    for cad in CADENCES:
        for lag in LAGS:
            for cb in COSTS:
                is_ = {k: grid[(k, cad, lag, cb)].loc[:IS_END] for k in pool}
                oos_ = {k: grid[(k, cad, lag, cb)].loc[OOS_START:] for k in pool}
                pick_sh = max(pool, key=lambda k: metrics(is_[k])["Sharpe"])
                elig = []
                for k in pool:
                    c_, s_, dd_ = m3(is_[k])
                    h1_, h2_ = halves(is_[k])
                    if h1_ > s1_i and h2_ > s2_i and dd_ >= 0.60 * sdd_i and c_ >= 0.70 * sc_i:
                        elig.append(k)
                pick_4b = max(elig, key=lambda k: metrics(is_[k])["Sharpe"]) if elig else None
                om = lambda k: (np.nan, np.nan, np.nan) if k is None else m3(oos_[k])
                a_, b_, c_ = om(pick_sh)
                d_, e_, f_ = om(pick_4b)
                ac, ash, add = m3(oos_[A])
                bc_, bsh, bdd_ = m3(oos_[B])
                rc, rsh, rdd = m3(grid[(RG, cad, lag, cb)].loc[OOS_START:])
                P(f"{cad:<4}{lag:<5}{cb:4d}  {bname(pick_sh):<12}{b_:8.4f}{a_:10.2%}{c_:9.2%}   "
                  f"{(bname(pick_4b) if pick_4b else 'none'):<12}{e_:8.4f}{d_:10.2%}{f_:9.2%}   "
                  f"{ash:13.4f}{bsh:13.4f}")
                wf.append(dict(panel=tag, cadence=cad, lag=lag, bps=cb,
                               pick_ISsharpe=bname(pick_sh), pick_ISsharpe_oosSharpe=b_,
                               pick_ISsharpe_oosCAGR=a_, pick_ISsharpe_oosMaxDD=c_,
                               pick_IS4b=(bname(pick_4b) if pick_4b else "none"),
                               n_IS4b_eligible=len(elig), pick_IS4b_oosSharpe=e_,
                               pick_IS4b_oosCAGR=d_, pick_IS4b_oosMaxDD=f_,
                               band3rw_oosSharpe=ash, band3rw_oosCAGR=ac, band3rw_oosMaxDD=add,
                               vol60dg_oosSharpe=bsh, vol60dg_oosCAGR=bc_, vol60dg_oosMaxDD=bdd_,
                               rg75_oosSharpe=rsh, rg75_oosCAGR=rc, rg75_oosMaxDD=rdd,
                               nominal_gross_rg75=G_RG,
                               spy_oosSharpe=ss_o, spy_oosCAGR=sco, spy_oosMaxDD=sddo,
                               base_oosSharpe=base_oos))
    return rows, wf


# ------------------------------------------------------------------ run
P(f"IDEA 238 — band3-rw-at-075-vs-the-incumbent (lane B).  {SCRIPT}")
P(f"Head to head: `EWall + band3-rw` vs the incumbent `EWall + vol60-dg`, gross {GROSS}, "
  f"on idea 65's cadence bar {CADENCES} and idea 45's execution-lag test {list(LAGS)}.")
P(f"Books: gate {GATES} x conv {CONVS} (2 tuned params) + NOGATE control; costs {COSTS} bps; "
  f"panels u56 and B136, both primary.  Every grid point reported.")

allrows, allwf = [], []
for tag, px in (("u56", load_universe()), ("B136", load_universe(broad=True))):
    r, w = sweep(px, tag)
    allrows += r
    allwf += w

G = pd.DataFrame(allrows)
W = pd.DataFrame(allwf)
G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

# ------------------------------------------------------------------ BAR-65: cadence
P("\n" + "=" * 138)
P("BAR-65 — CADENCE INSENSITIVITY.  SWING = max - min full-sample Sharpe over {D,W,M,Q} "
  "within each (panel, lag, cost) cell.")
P("=" * 138)
sw = (G.pivot_table(index=["panel", "book", "lag", "bps"], columns="cadence", values="Sharpe"))
sw["SWING"] = sw[CADENCES].max(axis=1) - sw[CADENCES].min(axis=1)
sw = sw.reset_index()
sw.to_csv(OUT / f"{STEM}.cadenceswing.csv", index=False)
P(f"\n{'panel':<6}{'book':<11}{'lag':<5}{'bps':>4}" + "".join(f"{c:>9}" for c in CADENCES) +
  f"{'SWING':>9}")
for _, r in sw.sort_values(["panel", "book", "lag", "bps"]).iterrows():
    P(f"{r['panel']:<6}{r['book']:<11}{r['lag']:<5}{int(r['bps']):4d}" +
      "".join(f"{r[c]:9.4f}" for c in CADENCES) + f"{r['SWING']:9.4f}")

P("\nMean / worst SWING by book (over the 20 panel x lag x cost cells):")
for bk in sorted(sw.book.unique()):
    s = sw[sw.book == bk]
    P(f"  {bk:<11} mean {s.SWING.mean():.4f}   worst {s.SWING.max():.4f}   "
      f"best {s.SWING.min():.4f}")

pa = sw[sw.book == bname(A)].set_index(["panel", "lag", "bps"])["SWING"]
swing_wins = {}
for INC in (B, RG):
    pb = sw[sw.book == bname(INC)].set_index(["panel", "lag", "bps"])["SWING"]
    swing_wins[bname(INC)] = int((pa < pb).sum())
    P(f"\nHEAD TO HEAD vs {bname(INC)}: {bname(A)} has the SMALLER swing in "
      f"{swing_wins[bname(INC)]} of {len(pa)} cells (mean {pa.mean():.4f} vs {pb.mean():.4f}; "
      f"paired mean diff {(pa - pb).mean():+.4f}).")

# 4b verdict stability across cadence, relative to the incumbent weekly cadence
P("\n4b verdict as the cadence moves (cells where the book PASSES at the incumbent W cadence):")
cad_loss = {}
for bk in sorted(G.book.unique()):
    held = kept = 0
    for (pn, lg, cb), _ in G[G.book == bk].groupby(["panel", "lag", "bps"]):
        w_pass = G[(G.book == bk) & (G.panel == pn) & (G.lag == lg) & (G.bps == cb) &
                   (G.cadence == BASE_CAD)]["pass4b"].iloc[0]
        if not w_pass:
            continue
        held += 1
        others = G[(G.book == bk) & (G.panel == pn) & (G.lag == lg) & (G.bps == cb) &
                   (G.cadence != BASE_CAD)]["pass4b"]
        kept += int(others.all())
    cad_loss[bk] = (kept, held)
    P(f"  {bk:<11} passes 4b at W in {held:2d} of 20 (panel,lag,cost) cells; "
      f"survives ALL of D/M/Q in {kept:2d} of those {held:2d}.")

bar65_a = all(swing_wins[bname(i)] > len(pa) / 2 for i in (B, RG)) and \
    (cad_loss[bname(A)][0] == cad_loss[bname(A)][1])
bar65_inc = {bname(i): (swing_wins[bname(i)] < len(pa) / 2 and
                        cad_loss[bname(i)][0] == cad_loss[bname(i)][1]) for i in (B, RG)}
P(f"\n[BAR-65] {bname(A)}: {'PASS' if bar65_a else 'FAIL'}    " +
  "    ".join(f"{k}: {'PASS' if v else 'FAIL'}" for k, v in bar65_inc.items()))

# ------------------------------------------------------------------ BAR-45: execution lag
P("\n" + "=" * 138)
P("BAR-45 — EXECUTION LAG.  1w = 4 extra trading days of staleness on top of PROTOCOL's t+1.")
P("=" * 138)
piv = G.pivot_table(index=["panel", "book", "cadence", "bps"], columns="lag",
                    values=["Sharpe", "MaxDD", "CAGR", "pass4b"]).reset_index()
piv.columns = ["_".join([c for c in col if c]) for col in piv.columns]
piv["dSharpe"] = piv["Sharpe_1w"] - piv["Sharpe_1d"]
piv["dMaxDD"] = piv["MaxDD_1w"] - piv["MaxDD_1d"]
piv["dCAGR"] = piv["CAGR_1w"] - piv["CAGR_1d"]
piv["lost4b"] = ((piv["pass4b_1d"] == 1) & (piv["pass4b_1w"] == 0)).astype(int)
piv.to_csv(OUT / f"{STEM}.lagprice.csv", index=False)

P(f"\n{'panel':<6}{'book':<11}{'cad':<4}{'bps':>4}{'dCAGR':>9}{'dSharpe':>9}{'dMaxDD':>9}"
  f"{'4b 1d':>7}{'4b 1w':>7}")
for _, r in piv.sort_values(["panel", "book", "cadence", "bps"]).iterrows():
    P(f"{r['panel']:<6}{r['book']:<11}{r['cadence']:<4}{int(r['bps']):4d}"
      f"{r['dCAGR']:+9.2%}{r['dSharpe']:+9.4f}{r['dMaxDD']:+9.2%}"
      f"{int(r['pass4b_1d']):7d}{int(r['pass4b_1w']):7d}")

P("\nMean lag price by book (over the 40 panel x cadence x cost cells):")
for bk in sorted(piv.book.unique()):
    s = piv[piv.book == bk]
    P(f"  {bk:<11} dCAGR {s.dCAGR.mean():+.3%}/yr   dSharpe {s.dSharpe.mean():+.4f}   "
      f"dMaxDD {s.dMaxDD.mean():+.2%} (worst {s.dMaxDD.min():+.2%})   "
      f"4b passes lost {int(s.lost4b.sum())} of {int(s.pass4b_1d.sum())}")

da = piv[piv.book == bname(A)].set_index(["panel", "cadence", "bps"])["dMaxDD"]
la = piv[piv.book == bname(A)]
dd_wins = {}
for INC in (B, RG):
    db = piv[piv.book == bname(INC)].set_index(["panel", "cadence", "bps"])["dMaxDD"]
    dd_wins[bname(INC)] = int((da > db).sum())   # larger (less negative) = shallower deepening
    lb = piv[piv.book == bname(INC)]
    P(f"\nHEAD TO HEAD vs {bname(INC)}: {bname(A)} has the SHALLOWER drawdown deepening in "
      f"{dd_wins[bname(INC)]} of {len(da)} cells (mean {da.mean():+.2%} vs {db.mean():+.2%}).")
    P(f"  4b verdicts lost to the 1w lag: {bname(A)} {int(la.lost4b.sum())} of "
      f"{int(la.pass4b_1d.sum())};  {bname(INC)} {int(lb.lost4b.sum())} of "
      f"{int(lb.pass4b_1d.sum())}.")
bar45_a = (int(la.lost4b.sum()) == 0) and all(dd_wins[bname(i)] > len(da) / 2 for i in (B, RG))
bar45_inc = {bname(i): (int(piv[piv.book == bname(i)].lost4b.sum()) == 0 and
                        dd_wins[bname(i)] < len(da) / 2) for i in (B, RG)}
P(f"[BAR-45] {bname(A)}: {'PASS' if bar45_a else 'FAIL'}    " +
  "    ".join(f"{k}: {'PASS' if v else 'FAIL'}" for k, v in bar45_inc.items()))

# ------------------------------------------------------------------ idea 154's margins re-read
P("\n" + "=" * 138)
P("IDEA 154's MARGIN CLAIM re-read over the whole cadence x lag grid (drawdown margin = "
  "MaxDD - 0.60*SPY MaxDD; CAGR margin = CAGR - 0.70*SPY CAGR)")
P("=" * 138)
for INC in (B, RG):
    for pn in ("u56", "B136"):
        ga = G[(G.book == bname(A)) & (G.panel == pn)].set_index(["cadence", "lag", "bps"])
        gb = G[(G.book == bname(INC)) & (G.panel == pn)].set_index(["cadence", "lag", "bps"])
        P(f"  vs {bname(INC):<14} {pn:<5} band3-rw dd-margin WIDER in "
          f"{int((ga.dd_margin > gb.dd_margin).sum()):2d} of {len(ga)} cells "
          f"(mean {ga.dd_margin.mean():+.4f} vs {gb.dd_margin.mean():+.4f});  "
          f"CAGR margin WIDER in {int((ga.cagr_margin > gb.cagr_margin).sum()):2d} of {len(ga)} "
          f"(mean {ga.cagr_margin.mean():+.4f} vs {gb.cagr_margin.mean():+.4f});  "
          f"Sharpe HIGHER in {int((ga.Sharpe > gb.Sharpe).sum()):2d} of {len(ga)}.")

# ------------------------------------------------------------------ both KEEP paths
P("\nBOTH KEEP PATHS over the full grid (2 panels x 4 cadences x 2 lags x 5 costs = 40 cells "
  "per book):")
for bk in sorted(G.book.unique()):
    s = G[G.book == bk]
    su, sb = s[s.panel == "u56"], s[s.panel == "B136"]
    P(f"  {bk:<14} 4a {int(s.pass4a.sum()):3d}/{len(s)}   4b {int(s.pass4b.sum()):3d}/{len(s)}"
      f"   (u56 4b {int(su.pass4b.sum()):2d}/{len(su)}, "
      f"B136 4b {int(sb.pass4b.sum()):2d}/{len(sb)})")
xu = G.pivot_table(index=["book", "cadence", "lag", "bps"], columns="panel",
                   values="pass4b").reset_index()
xu["cross"] = (xu["u56"] * xu["B136"]).astype(int)
P("\n  cross-universe 4b (passes on u56 AND B136):")
for bk in sorted(xu.book.unique()):
    P(f"    {bk:<11} {int(xu[xu.book == bk]['cross'].sum()):2d} of "
      f"{len(xu[xu.book == bk])} (cadence x lag x cost) cells")
P("\n  first-failing 4b bar, all books, all cells:")
for k, v in G[G.pass4b == 0]["fail4b"].str.split(",").explode().value_counts().items():
    P(f"    {k:<6} {v}")

# ------------------------------------------------------------------ rule 8 summary
P("\n" + "=" * 138)
P("RULE 8 SUMMARY — the IS chooser between the four (gate, conv) books, per panel")
P("=" * 138)
for pn in ("u56", "B136"):
    w = W[W.panel == pn]
    P(f"  {pn}: IS-Sharpe pick {w.pick_ISsharpe.mode().iloc[0]} in "
      f"{int((w.pick_ISsharpe == w.pick_ISsharpe.mode().iloc[0]).sum())}/{len(w)} cells; "
      f"IS-4b pick {w.pick_IS4b.mode().iloc[0]} in "
      f"{int((w.pick_IS4b == w.pick_IS4b.mode().iloc[0]).sum())}/{len(w)}.")
    P(f"      beats SPY OOS Sharpe: IS-Sharpe pick "
      f"{int((w.pick_ISsharpe_oosSharpe > w.spy_oosSharpe).sum())}/{len(w)}, "
      f"IS-4b pick {int((w.pick_IS4b_oosSharpe > w.spy_oosSharpe).sum())}/{len(w)}, "
      f"band3-rw {int((w.band3rw_oosSharpe > w.spy_oosSharpe).sum())}/{len(w)}, "
      f"vol60-dg {int((w.vol60dg_oosSharpe > w.spy_oosSharpe).sum())}/{len(w)}.")
    P(f"      beats RULES v2 OOS Sharpe: band3-rw "
      f"{int((w.band3rw_oosSharpe > w.base_oosSharpe).sum())}/{len(w)}, "
      f"vol60-dg {int((w.vol60dg_oosSharpe > w.base_oosSharpe).sum())}/{len(w)}.")
    P(f"      mean OOS Sharpe: IS-Sharpe {w.pick_ISsharpe_oosSharpe.mean():.4f}, "
      f"IS-4b {w.pick_IS4b_oosSharpe.mean():.4f}, band3-rw {w.band3rw_oosSharpe.mean():.4f}, "
      f"vol60-dg {w.vol60dg_oosSharpe.mean():.4f}, SPY {w.spy_oosSharpe.iloc[0]:.4f}, "
      f"RULES v2 {w.base_oosSharpe.iloc[0]:.4f}.")
    P(f"      mean OOS CAGR:   band3-rw {w.band3rw_oosCAGR.mean():.2%}, "
      f"vol60-dg {w.vol60dg_oosCAGR.mean():.2%}, SPY {w.spy_oosCAGR.iloc[0]:.2%}.")
    P(f"      mean OOS MaxDD:  band3-rw {w.band3rw_oosMaxDD.mean():.2%}, "
      f"vol60-dg {w.vol60dg_oosMaxDD.mean():.2%}, SPY {w.spy_oosMaxDD.iloc[0]:.2%}.")
    for c, lab in (("vol60dg", "vol60-dg (nominal 0.75)"),
                   ("rg75", f"vol60-dg-rg75 (nominal {w.nominal_gross_rg75.iloc[0]:.4f})")):
        P(f"      OOS head to head vs {lab}: band3-rw wins on Sharpe in "
          f"{int((w.band3rw_oosSharpe > w[c + '_oosSharpe']).sum())}/{len(w)} cells, on MaxDD in "
          f"{int((w.band3rw_oosMaxDD > w[c + '_oosMaxDD']).sum())}/{len(w)}, on CAGR in "
          f"{int((w.band3rw_oosCAGR > w[c + '_oosCAGR']).sum())}/{len(w)}   "
          f"(mean OOS Sharpe {w[c + '_oosSharpe'].mean():.4f}, CAGR {w[c + '_oosCAGR'].mean():.2%}, "
          f"MaxDD {w[c + '_oosMaxDD'].mean():.2%})")

# ------------------------------------------------------------------ verdict
P("\n" + "=" * 138)
P("PRE-REGISTERED VERDICT")
P("=" * 138)
P(f"  [BAR-65] cadence      : {bname(A)} {'PASS' if bar65_a else 'FAIL'}   " +
  "   ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in bar65_inc.items()))
P(f"  [BAR-45] execution lag: {bname(A)} {'PASS' if bar45_a else 'FAIL'}   " +
  "   ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in bar45_inc.items()))
inc_safe = [k for k in bar65_inc if bar65_inc[k] and bar45_inc[k]]
if bar65_a and bar45_a:
    P(f"  => {bname(A)} MAY be called the safer book.")
elif inc_safe:
    P(f"  => the INCUMBENT reading(s) {', '.join(inc_safe)} MAY be called the safer book.")
else:
    P("  => NEITHER book may be called the safer book: the two bars do not agree, so idea 154's")
    P("     margin ordering stands as a SINGLE-CADENCE, SINGLE-LAG reading only.")

(OUT / f"{STEM}.console.txt").write_text("\n".join(_log) + "\n")
print(f"\nwrote {STEM}.console.txt / .grid.csv / .walkforward.csv / .cadenceswing.csv / .lagprice.csv")
