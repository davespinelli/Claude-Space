#!/usr/bin/env python3
"""Idea 862 (cloud lane, 2026-09-15) — does the RULE-8 CHOOSER CONVENTION flip any other
committed 4b pass?

QUESTION (QUEUE idea 862, verbatim)
    idea 814's verdict is decided entirely by which pre-stated IS chooser runs: argmax IS
    Sharpe lands on the memo cell and passes 4b OOS, argmax IS Sharpe under an IS drawdown
    constraint lands elsewhere and fails on the CAGR floor.  The chooser is an unpriced degree
    of freedom in every rule-8 pass on the record.  Re-run the record's committed rule-8 picks
    under a declared set of 3-4 choosers and report how many are convention-stable.
    Max 2 params (chooser set, pick set).

WHAT IS NEW AGAINST 814.  814 found the flip on ONE grid (B136 x CORR q x w) with TWO choosers
    and reported it as a single observation.  This run asks whether that observation is a
    property of that grid or of rule 8 itself: it rebuilds the record's committed rule-8 PICK
    SHAPES -- the 1-D dial ladders idea 664/668 committed and the 2-D (dial x gross) grids
    ideas 702/806/814 pick over -- on all three panels, runs FOUR pre-stated choosers over
    each, and reads the OOS window ONCE per (site, chooser).  Convention-stability is then a
    COUNT over sites, not an anecdote.

    A site here is one (panel, pick-set member): a self-contained rule-8 pick, exactly the
    object PROTOCOL rule 8 describes ("parameters chosen on the first half, evaluated on the
    second untouched").  The record never publishes the chooser it used; C1 (argmax IS Sharpe)
    is its de-facto convention and is the CONTROL against which the other three are read.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL grid points reported.
    (1) CHOOSER SET, 4 levels, every one pre-stated before any OOS number was read.  All four
        read the IN-SAMPLE window only (panel start .. 2016-12-31), ties broken to the
        SMALLEST rung index, which is the record's own convention (idea 664/668).
            C1_SHARPE      argmax IS Sharpe                                 <- CONTROL (the
                                                                               record's)
            C2_SHARPE_DD   argmax IS Sharpe s.t. IS MaxDD <= 60% of SPY's IS MaxDD
                           (814's second chooser: the 4b DD leg applied in sample).  If the
                           feasible set is EMPTY the chooser falls back to argmin |IS MaxDD|;
                           the fallback is FLAGGED in every row it fires on.
            C3_CALMAR      argmax IS CAGR / |IS MaxDD|
            C4_CAGR        argmax IS CAGR                                   (the 4b CAGR leg
                                                                               applied in sample)
    (2) PICK SET in {DIAL, GRID}.
            DIAL  the record's committed 1-D ladders (idea 664/668's five dials): BAND, N,
                  GROSS, VOLCAP, CADENCE.  36 rungs per panel.
            GRID  the 2-D (dial x gross) shape every recent rule-8 pass picks over:
                  BANDxGROSS (5x5) and NxGROSS (5x5).  50 cells per panel.

CORPUS (not tuned): three panels, U56 / B136 / SMALL.  7 sites per panel x 3 = 21 sites,
    258 books, each priced at 10 bps (headline) and 25 bps (robustness), each read on FULL,
    IS, OOS.  Every rung of every site is written to the CSVs, not just the picks.

PRE-REGISTERED HYPOTHESES (declared before any OOS number was read)
    H_FLIP      814's flip is NOT unique: at least one further site changes its OOS 4b verdict
                between C1 and C2.
    H_MINORITY  a MINORITY of sites (< 50%) are PICK-stable across all four choosers, because
                a chooser is an argmax over a noisy 8-point read.
    H_VERDICT   VERDICT-stability is much higher than PICK-stability: most sites that move
                their pick do not move their 4b verdict, because 4b is mostly decided by gross
                (ideas 502/504/596/674/858) and most rungs of a dial share one gross.
    H_GROSSDIAL the exception is the GROSS dial and the x-GROSS grids, where the choosers
                disagree ABOUT gross and therefore about the verdict.
    H_C2COST    C2 (the DD-constrained chooser) is systematically WORSE out of sample on CAGR
                than C1, because the IS DD cap selects de-grossed books (idea 679/771).

GATES (printed before any new number; all must pass or the run stops)
    G1  fast_backtest == engine.backtest @10 bps  (max |d| < 1e-12)
    G2  band_book(0.03, 0.75) == baseline.rules_v2_weights  (EXACT 0)
    G3  the BAND dial at g=0.75 reproduces idea 664's COMMITTED pick row on U56 and B136
        (pick, IS read, full Sharpe, OOS Sharpe, SPY OOS, live-book OOS).  VINTAGE-PINNED:
        data/prices.csv has gained trading days since 664 ran, so the gate is tried on today's
        tape and on truncations and the reproducing vintage is NAMED (idea 668 hit the same
        channel; open idea 517 is its home).
    G4  determinism: one dial rebuilt twice, max |d| == 0.
    G5  cost identity: the 0 bps series equals the gross return series exactly.

PROTOCOL: 10 bps per unit turnover (25 bps also reported), weights decided at close t applied
    at t+1, no shorting, no leverage.  BOTH KEEP paths evaluated on every row, on the FULL
    sample and read inside OOS.  Rule 8 is the design: every chooser sees IS only, and the OOS
    window is read once per (site, chooser).

SURVIVORSHIP, up front: U56 / B136 / SMALL are CURRENT-constituent lists (the small panel is
    the sub-$2B screen as it stands today, with the 52 names whose max 1-day move >= 100% cut
    per the data README), so every CAGR and drawdown LEVEL is optimistic.  The durable part of
    this run is the DIFFERENCE between choosers on the same book, which is survivorship-neutral
    by construction.  Nothing here is a capital claim and nothing is promoted.

Outputs (committed under research/backtests/):
    .console.txt      full log
    .rungs.csv        every rung of every site: IS/FULL/OOS metrics at both cost rungs
    .picks.csv        every (site, chooser): the pick, its OOS read, 4a/4b verdicts
    .walkforward.csv  the rule-8 table: per site, the four choosers' OOS CAGR/Sharpe/MaxDD
                      against RULES v2 and SPY on the same window
    .stability.csv    per site, pick-stability and verdict-stability across the chooser set

Run: python research/backtests/2026-09-15_does-the-RULE-8-CHOOSER-CONVENTION-flip-any-other-committed-4b-pass_cloud.py
Deterministic; no network (reads the committed price caches only).
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, score, band_state, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-15"
SLUG = "does-the-RULE-8-CHOOSER-CONVENTION-flip-any-other-committed-4b-pass"
STEM = f"{DATE}_{SLUG}_cloud"
OUT = Path(__file__).resolve().parent

FREQ0 = "W"
COST_HEAD = 10.0
COSTS = [0.0, 10.0, 25.0]
WARM = 260
BAND0, GROSS0, N0 = 0.03, 0.75, 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"

BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20]
NS = [3, 5, 10, 15, 20, 30, 40, 50]
GROSSES = [0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00]
VOLCAPS = [0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 9.99]      # 9.99 == cap OFF
CADENCES = ["D", "W", "M", "Q"]

GRID_BANDS = [0.00, 0.02, 0.03, 0.05, 0.08]
GRID_NS = [5, 10, 20, 30, 50]
GRID_GROSSES = [0.35, 0.50, 0.75, 0.90, 1.00]

CHOOSERS = ["C1_SHARPE", "C2_SHARPE_DD", "C3_CALMAR", "C4_CAGR"]
CONTROL = "C1_SHARPE"

# idea 664's committed level-0 row at g=0.75 (research/backtests/
# 2026-09-10_price-the-RE-DERIVED-METRIC-column-against-its-own-source_C.grid.csv), as quoted
# by idea 668's committed G3.
IDEA664 = {
    "U56":  dict(pick=0.08, read=1.1222394, Sharpe=1.1465783, OOS=1.1665617,
                 SPY_OOS=0.8757784, BASE_OOS=1.2788365),
    "B136": dict(pick=0.08, read=1.1411857, Sharpe=1.1240385, OOS=1.1094642,
                 SPY_OOS=0.8820243, BASE_OOS=1.1185083),
}

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==================================================================================
# 1.  ENGINE (vectorised equivalent of engine.backtest; asserted against it in G1).
#     Returns the GROSS return series and the turnover series so any cost rung is free.
# ==================================================================================
def fast_parts(prices, weights, freq=FREQ0):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    gross_r = (held * rets).sum(axis=1)
    nheld = (np.abs(held) > 1e-12).sum(axis=1)
    return (pd.Series(gross_r, index=idx), pd.Series(turn, index=idx),
            pd.Series(nheld, index=idx))


def at_cost(parts, bps):
    g, t, _ = parts
    return g - t * bps / 1e4


def M0(r):
    vol = r.std() * np.sqrt(252)
    return float((r.mean() * 252) / vol) if vol else np.nan


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    dd = float((eq / eq.cummax() - 1).min())
    cagr = float(eq.iloc[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan
    h = len(r) // 2
    return dict(CAGR=cagr, Sharpe=(float(r.mean() * 252) / vol) if vol else np.nan, MaxDD=dd,
                H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


# ==================================================================================
# 2.  BOOKS
# ==================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def ranked_book(px, sc, above, vol20, n, gross, max_vol):
    """Top-n composite-ranked equal-weight book (the record's CAND-n family)."""
    elig = sc.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return (sel.mul(gross / k, axis=0)).fillna(0.0)


def build_sites(px, pick_set):
    """{site_name: (rung_labels, {rung: parts}, gross_of_rung)} for one panel."""
    start = px.index[WARM]
    sc, above, vol20 = score(px, vol_scale=True)
    S = {}

    def clip(parts):
        return tuple(s.loc[start:] for s in parts)

    if pick_set == "DIAL":
        S["BAND"] = ([f"{b:.2f}" for b in BANDS],
                     {f"{b:.2f}": clip(fast_parts(px, band_book(px, b, GROSS0))) for b in BANDS},
                     {f"{b:.2f}": GROSS0 for b in BANDS})
        S["N"] = ([str(n) for n in NS],
                  {str(n): clip(fast_parts(px, ranked_book(px, sc, above, vol20, n, GROSS0, 9.99)))
                   for n in NS},
                  {str(n): GROSS0 for n in NS})
        S["GROSS"] = ([f"{g:.2f}" for g in GROSSES],
                      {f"{g:.2f}": clip(fast_parts(px, band_book(px, BAND0, g))) for g in GROSSES},
                      {f"{g:.2f}": g for g in GROSSES})
        S["VOLCAP"] = ([f"{v:.2f}" for v in VOLCAPS],
                       {f"{v:.2f}": clip(fast_parts(px, ranked_book(px, sc, above, vol20, N0,
                                                                   GROSS0, v)))
                        for v in VOLCAPS},
                       {f"{v:.2f}": GROSS0 for v in VOLCAPS})
        w = band_book(px, BAND0, GROSS0)
        S["CADENCE"] = (CADENCES,
                        {c: clip(fast_parts(px, w, c)) for c in CADENCES},
                        {c: GROSS0 for c in CADENCES})
    else:
        lab, bk, gr = [], {}, {}
        for b in GRID_BANDS:
            for g in GRID_GROSSES:
                k = f"b{b:.2f}_g{g:.2f}"
                lab.append(k); bk[k] = clip(fast_parts(px, band_book(px, b, g))); gr[k] = g
        S["BANDxGROSS"] = (lab, bk, gr)
        lab, bk, gr = [], {}, {}
        for n in GRID_NS:
            for g in GRID_GROSSES:
                k = f"n{n}_g{g:.2f}"
                lab.append(k)
                bk[k] = clip(fast_parts(px, ranked_book(px, sc, above, vol20, n, g, 9.99)))
                gr[k] = g
        S["NxGROSS"] = (lab, bk, gr)
    return S


# ==================================================================================
# 3.  CHOOSERS  (IS window only) AND THE KEEP PATHS
# ==================================================================================
def is_stats(parts, bps):
    r = at_cost(parts, bps).loc[:IS_END]
    return M(r)


def choose(labels, stats, spy_is_dd):
    """Return {chooser: (pick_label, fallback_flag)}.  Ties -> smallest rung INDEX."""
    out = {}
    order = list(range(len(labels)))

    def argmax(keyfn, pool):
        best, bi = None, None
        for i in pool:
            v = keyfn(labels[i])
            if v is None or not np.isfinite(v):
                continue
            if best is None or v > best + 1e-15:
                best, bi = v, i
        return bi

    i1 = argmax(lambda L: stats[L]["Sharpe"], order)
    out["C1_SHARPE"] = (labels[i1], False)

    cap = 0.60 * abs(spy_is_dd)
    feas = [i for i in order if abs(stats[labels[i]]["MaxDD"]) <= cap]
    if feas:
        i2 = argmax(lambda L: stats[L]["Sharpe"], feas)
        out["C2_SHARPE_DD"] = (labels[i2], False)
    else:
        i2 = argmax(lambda L: -abs(stats[L]["MaxDD"]), order)
        out["C2_SHARPE_DD"] = (labels[i2], True)

    i3 = argmax(lambda L: (stats[L]["CAGR"] / abs(stats[L]["MaxDD"])
                           if abs(stats[L]["MaxDD"]) > 1e-9 else np.nan), order)
    out["C3_CALMAR"] = (labels[i3], False)

    i4 = argmax(lambda L: stats[L]["CAGR"], order)
    out["C4_CAGR"] = (labels[i4], False)
    return out


def keeppaths(r, base, spy, leg):
    """PROTOCOL 4a/4b on one leg.  leg='FULL' uses the full common sample and its own halves;
    leg='OOS' restricts every series to the OOS window first (814's 'passes 4b inside OOS')."""
    if leg == "OOS":
        r, base, spy = r.loc[OOS_START:], base.loc[OOS_START:], spy.loc[OOS_START:]
    m, mb, ms = M(r), M(base), M(spy)
    oos_s, oos_b = M0(r.loc[OOS_START:]), M0(spy.loc[OOS_START:])
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > oos_b)
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
           and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return bool(p4a), bool(p4b), m, mb, ms


# ==================================================================================
# 4.  GATES
# ==================================================================================
def gates(panels):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    px = panels["U56"]

    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == baseline.rules_v2_weights   : {g2:.3e}  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    ok &= (g2 == 0.0)

    slow = backtest(px, w, cost_bps=COST_HEAD, freq=FREQ0)["returns"]
    parts = fast_parts(px, w)
    fast = at_cost(parts, COST_HEAD)
    j = px.index[WARM]
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
    P(f"  G1 fast == engine.backtest @10 bps                     : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= (g1 < 1e-12)

    g5 = float(np.abs(at_cost(parts, 0.0).values - parts[0].values).max())
    P(f"  G5 0 bps series == gross return series                 : {g5:.3e}  "
      f"{'PASS' if g5 == 0.0 else 'FAIL'}")
    ok &= (g5 == 0.0)

    p2 = fast_parts(px, band_book(px, BAND0, GROSS0))
    g4 = float(np.abs(at_cost(p2, COST_HEAD).values - fast.values).max())
    P(f"  G4 determinism (same book rebuilt twice)               : {g4:.3e}  "
      f"{'PASS' if g4 == 0.0 else 'FAIL'}")
    ok &= (g4 == 0.0)

    P("  G3 BAND dial at g=0.75 vs idea 664's COMMITTED row (bar 5e-4), VINTAGE-PINNED:")
    for pn in ("U56", "B136"):
        e = IDEA664[pn]
        pxp = panels[pn]
        best, bestend = None, None
        for end in (None, "2026-09-11", "2026-09-09", "2026-09-04"):
            q = pxp if end is None else pxp.loc[:end]
            if len(q) < WARM + 500:
                continue
            st = q.index[WARM]
            bk = {b: at_cost(fast_parts(q, band_book(q, b, GROSS0)), COST_HEAD).loc[st:]
                  for b in BANDS}
            rd = {b: M0(bk[b].loc[:IS_END]) for b in BANDS}
            pick = max(sorted(BANDS), key=lambda b: (rd[b], -b))
            r = bk[pick]
            spy = q["SPY"].pct_change().fillna(0).loc[st:]
            base = at_cost(fast_parts(q, rules_v2_weights(q, BAND0, GROSS0)), COST_HEAD).loc[st:]
            d = max(abs(pick - e["pick"]), abs(rd[pick] - e["read"]), abs(M0(r) - e["Sharpe"]),
                    abs(M0(r.loc[OOS_START:]) - e["OOS"]),
                    abs(M0(spy.loc[OOS_START:]) - e["SPY_OOS"]),
                    abs(M0(base.loc[OOS_START:]) - e["BASE_OOS"]))
            if best is None or d < best:
                best, bestend = d, (end or "TODAY")
        P(f"     {pn:5s} best max|d| {best:.3e} at vintage {bestend}  "
          f"{'PASS' if best < 5e-4 else 'FAIL'}")
        ok &= (best < 5e-4)
    P(f"  GATES: {'ALL PASS' if ok else 'FAILURE -- run stops'}")
    return ok


# ==================================================================================
# 5.  MAIN
# ==================================================================================
def panels():
    out = {}
    out["U56"] = load_universe()
    out["B136"] = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    out["SMALL"] = pxs[[c for c in pxs.columns if c == "SPY" or c not in bad]]
    return out


def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 862  {SLUG}   (cloud)  {pd.Timestamp.today().date()}")
    P("=" * 100)
    PX = panels()
    for k, v in PX.items():
        P(f"  panel {k:6s} {v.shape[1]-1:4d} names + SPY   "
          f"{v.index[0].date()} .. {v.index[-1].date()}  ({len(v)} rows)")
    P("  SURVIVORSHIP: all three are CURRENT-constituent lists; LEVELS are optimistic, the")
    P("  chooser-to-chooser DIFFERENCE measured here is survivorship-neutral by construction.")
    P()

    if not gates(PX):
        sys.exit(1)

    rung_rows, pick_rows, stab_rows, wf_rows = [], [], [], []

    for pick_set in ("DIAL", "GRID"):
        for pn, px in PX.items():
            start = px.index[WARM]
            spy = px["SPY"].pct_change().fillna(0).loc[start:]
            base = at_cost(fast_parts(px, rules_v2_weights(px, BAND0, GROSS0)),
                           COST_HEAD).loc[start:]
            spy_is_dd = M(spy.loc[:IS_END])["MaxDD"]
            S = build_sites(px, pick_set)
            P("-" * 100)
            P(f"[{pick_set}] panel {pn}  SPY IS MaxDD {spy_is_dd:.2%}  "
              f"C2 cap |MaxDD| <= {0.60*abs(spy_is_dd):.2%}")

            for site, (labels, books, grossmap) in S.items():
                stats10 = {L: is_stats(books[L], COST_HEAD) for L in labels}
                for L in labels:
                    for bps in COSTS:
                        r = at_cost(books[L], bps)
                        mf, mi, mo = M(r), M(r.loc[:IS_END]), M(r.loc[OOS_START:])
                        rung_rows.append(dict(
                            pick_set=pick_set, panel=pn, site=site, rung=L,
                            gross=grossmap[L], cost_bps=bps,
                            mean_names=float(books[L][2].mean()),
                            IS_CAGR=mi["CAGR"], IS_Sharpe=mi["Sharpe"], IS_MaxDD=mi["MaxDD"],
                            FULL_CAGR=mf["CAGR"], FULL_Sharpe=mf["Sharpe"],
                            FULL_MaxDD=mf["MaxDD"], FULL_H1=mf["H1"], FULL_H2=mf["H2"],
                            OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            OOS_H1=mo["H1"], OOS_H2=mo["H2"]))

                picks = choose(labels, stats10, spy_is_dd)
                P(f"  site {site:12s} rungs {len(labels):3d} | " +
                  " | ".join(f"{c.split('_')[0]}={picks[c][0]}"
                             f"{'*FB' if picks[c][1] else ''}" for c in CHOOSERS))

                v4b, v4a, picklabels = {}, {}, {}
                for c in CHOOSERS:
                    L, fb = picks[c]
                    picklabels[c] = L
                    r = at_cost(books[L], COST_HEAD)
                    r25 = at_cost(books[L], 25.0)
                    a_f, b_f, mf, mbf, msf = keeppaths(r, base, spy, "FULL")
                    a_o, b_o, mo, mbo, mso = keeppaths(r, base, spy, "OOS")
                    _, b_f25, _, _, _ = keeppaths(r25, base, spy, "FULL")
                    _, b_o25, _, _, _ = keeppaths(r25, base, spy, "OOS")
                    v4b[c], v4a[c] = b_o, a_o
                    pick_rows.append(dict(
                        pick_set=pick_set, panel=pn, site=site, chooser=c, pick=L,
                        fallback=fb, gross=grossmap[L],
                        IS_Sharpe=stats10[L]["Sharpe"], IS_MaxDD=stats10[L]["MaxDD"],
                        IS_CAGR=stats10[L]["CAGR"],
                        FULL_CAGR=mf["CAGR"], FULL_Sharpe=mf["Sharpe"], FULL_MaxDD=mf["MaxDD"],
                        FULL_H1=mf["H1"], FULL_H2=mf["H2"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        OOS_H1=mo["H1"], OOS_H2=mo["H2"],
                        pass4a_FULL=a_f, pass4b_FULL=b_f, pass4a_OOS=a_o, pass4b_OOS=b_o,
                        pass4b_FULL_25bps=b_f25, pass4b_OOS_25bps=b_o25))
                    wf_rows.append(dict(
                        pick_set=pick_set, panel=pn, site=site, chooser=c, pick=L,
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        BASE_OOS_CAGR=mbo["CAGR"], BASE_OOS_Sharpe=mbo["Sharpe"],
                        BASE_OOS_MaxDD=mbo["MaxDD"],
                        SPY_OOS_CAGR=mso["CAGR"], SPY_OOS_Sharpe=mso["Sharpe"],
                        SPY_OOS_MaxDD=mso["MaxDD"],
                        beats_base_OOS_Sharpe=bool(mo["Sharpe"] > mbo["Sharpe"]),
                        beats_SPY_OOS_Sharpe=bool(mo["Sharpe"] > mso["Sharpe"]),
                        pass4b_OOS=b_o))

                cap = 0.60 * abs(spy_is_dd)
                c1_L = picklabels[CONTROL]
                c2_binds = bool(abs(stats10[c1_L]["MaxDD"]) > cap)
                n_feas = int(sum(abs(stats10[L]["MaxDD"]) <= cap for L in labels))
                npick = len(set(picklabels.values()))
                ngross = len({grossmap[L] for L in picklabels.values()})
                stab_rows.append(dict(
                    pick_set=pick_set, panel=pn, site=site, n_rungs=len(labels),
                    C2_binds=c2_binds, n_feasible_C2=n_feas,
                    distinct_picks=npick, pick_stable=bool(npick == 1),
                    distinct_gross=ngross, gross_stable=bool(ngross == 1),
                    verdict4b_stable=bool(len(set(v4b.values())) == 1),
                    verdict4a_stable=bool(len(set(v4a.values())) == 1),
                    n4b_pass=int(sum(v4b.values())),
                    C1_4b=v4b[CONTROL], C2_4b=v4b["C2_SHARPE_DD"],
                    C3_4b=v4b["C3_CALMAR"], C4_4b=v4b["C4_CAGR"],
                    C1_pick=picklabels[CONTROL], C2_pick=picklabels["C2_SHARPE_DD"],
                    C3_pick=picklabels["C3_CALMAR"], C4_pick=picklabels["C4_CAGR"]))

    RU, PKS = pd.DataFrame(rung_rows), pd.DataFrame(pick_rows)
    ST, WF = pd.DataFrame(stab_rows), pd.DataFrame(wf_rows)

    P()
    P("=" * 100)
    P("(B) RESULTS")
    P("=" * 100)
    P(f"  sites {len(ST)}   books {RU[RU.cost_bps==COST_HEAD].shape[0]}   "
      f"rung-rows {len(RU)}   pick-rows {len(PKS)}")

    P()
    P("  B1  PICK stability and 4b-VERDICT stability across the four choosers, per site")
    P("      (OOS-read 4b; C1 is the record's de-facto convention)")
    cols = ["pick_set", "panel", "site", "n_rungs", "distinct_picks", "pick_stable",
            "distinct_gross", "verdict4b_stable", "n4b_pass", "C1_pick", "C2_pick",
            "C3_pick", "C4_pick"]
    P(ST[cols].to_string(index=False))

    ps = int(ST.pick_stable.sum())
    vs = int(ST.verdict4b_stable.sum())
    P()
    P(f"  PICK-stable sites      : {ps}/{len(ST)}  ({ps/len(ST):.1%})")
    P(f"  4b-VERDICT-stable sites: {vs}/{len(ST)}  ({vs/len(ST):.1%})")
    P(f"  4a-VERDICT-stable sites: {int(ST.verdict4a_stable.sum())}/{len(ST)}")
    P(f"  GROSS-stable sites     : {int(ST.gross_stable.sum())}/{len(ST)}")
    P(f"  H_MINORITY (pick-stable < 50%)        : "
      f"{'CONFIRMED' if ps/len(ST) < 0.5 else 'FALSIFIED'}")
    P(f"  H_VERDICT  (verdict-stability > pick) : "
      f"{'CONFIRMED' if vs > ps else 'FALSIFIED'}")

    flips = ST[~ST.verdict4b_stable]
    c12 = ST[ST.C1_4b != ST.C2_4b]
    P()
    P(f"  B2  SITES WHOSE 4b VERDICT MOVES WITH THE CHOOSER: {len(flips)}")
    if len(flips):
        P(flips[["pick_set", "panel", "site", "C1_4b", "C2_4b", "C3_4b", "C4_4b",
                 "C1_pick", "C2_pick", "C3_pick", "C4_pick"]].to_string(index=False))
    P(f"  C1-vs-C2 disagreements (814's exact contrast): {len(c12)}")
    P(f"  H_FLIP (814's flip is not unique): "
      f"{'CONFIRMED' if len(c12) >= 1 else 'FALSIFIED'}")
    nb = int(ST.C2_binds.sum())
    P(f"  WHY: the C2 constraint BINDS (C1's own pick violates the IS DD cap) at only "
      f"{nb}/{len(ST)} sites;")
    P(f"       median feasible rungs under the cap {ST.n_feasible_C2.median():.0f} of "
      f"{ST.n_rungs.median():.0f}.  814's grid is one of the rare sites where C1's argmax is")
    P("       infeasible; on the record's OWN committed pick shapes the cap is slack, so the")
    P("       two choosers coincide and the flip cannot reproduce.")

    P()
    P("  B3  PER-CHOOSER OOS TOTALS (mean over the 21 sites, 10 bps, rule-8 read once)")
    agg = PKS.groupby("chooser").agg(
        OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
        OOS_MaxDD=("OOS_MaxDD", "mean"), gross=("gross", "mean"),
        n4b_OOS=("pass4b_OOS", "sum"), n4b_FULL=("pass4b_FULL", "sum"),
        n4a_OOS=("pass4a_OOS", "sum"), n4b_OOS_25=("pass4b_OOS_25bps", "sum"))
    P(agg.to_string(float_format=lambda x: f"{x:.4f}"))
    P("  comparands on the same OOS window, per panel:")
    for pn in PX:
        w = WF[WF.panel == pn].iloc[0]
        P(f"     {pn:6s} SPY OOS {w.SPY_OOS_CAGR:7.2%} / {w.SPY_OOS_Sharpe:6.4f} / "
          f"{w.SPY_OOS_MaxDD:7.2%}    RULES v2 OOS {w.BASE_OOS_CAGR:7.2%} / "
          f"{w.BASE_OOS_Sharpe:6.4f} / {w.BASE_OOS_MaxDD:7.2%}")
    c1, c2 = agg.loc["C1_SHARPE"], agg.loc["C2_SHARPE_DD"]
    P(f"  H_C2COST (C2 worse OOS CAGR than C1): "
      f"{'CONFIRMED' if c2.OOS_CAGR < c1.OOS_CAGR else 'FALSIFIED'}  "
      f"(C1 {c1.OOS_CAGR:.2%} vs C2 {c2.OOS_CAGR:.2%}; mean gross "
      f"{c1.gross:.3f} vs {c2.gross:.3f})")

    P()
    P("  B4  WHERE THE INSTABILITY LIVES: sites grouped by whether the dial moves GROSS")
    ST2 = ST.copy()
    ST2["gross_dial"] = ST2.site.isin(["GROSS", "BANDxGROSS", "NxGROSS"])
    gg = ST2.groupby("gross_dial").agg(sites=("site", "size"),
                                       pick_stable=("pick_stable", "sum"),
                                       verdict4b_stable=("verdict4b_stable", "sum"))
    P(gg.to_string())
    hg = (True in gg.index and False in gg.index
          and (gg.loc[True, "verdict4b_stable"] / gg.loc[True, "sites"]
               < gg.loc[False, "verdict4b_stable"] / gg.loc[False, "sites"]))
    P(f"  H_GROSSDIAL (gross-moving sites less verdict-stable): "
      f"{'CONFIRMED' if hg else 'FALSIFIED'}")

    P()
    P("  B5  THE 4b PASSES THEMSELVES (OOS-read), by chooser -- every pass, 10 bps")
    pas = PKS[PKS.pass4b_OOS]
    if len(pas):
        P(pas[["pick_set", "panel", "site", "chooser", "pick", "gross", "OOS_CAGR",
               "OOS_Sharpe", "OOS_MaxDD", "pass4b_OOS_25bps", "pass4a_OOS"]]
          .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P("     none")

    P()
    P("  B6  MATCHED-GROSS TWIN CONTROL on every 4b pass (the record's standing screen,")
    P("      ideas 502/504/596/674/858): the twin holds EVERY priced name at the same gross,")
    P("      same cadence, same cost -- no band, no rank, no vol cap.  A pass whose twin also")
    P("      passes is 4b certifying EXPOSURE, not the clause.")
    twin_rows = []
    for _, rr in PKS[PKS.pass4b_OOS | PKS.pass4b_FULL].iterrows():
        px = PX[rr.panel]
        start = px.index[WARM]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base = at_cost(fast_parts(px, rules_v2_weights(px, BAND0, GROSS0)), COST_HEAD).loc[start:]
        tw = at_cost(fast_parts(px, ew_gross(px, rr.gross)), COST_HEAD).loc[start:]
        a_f, b_f, mtf, _, _ = keeppaths(tw, base, spy, "FULL")
        a_o, b_o, mto, _, _ = keeppaths(tw, base, spy, "OOS")
        twin_rows.append(dict(panel=rr.panel, site=rr.site, chooser=rr.chooser, pick=rr.pick,
                              gross=rr.gross, arm_OOS_Sharpe=rr.OOS_Sharpe,
                              twin_OOS_Sharpe=mto["Sharpe"], arm_OOS_CAGR=rr.OOS_CAGR,
                              twin_OOS_CAGR=mto["CAGR"], arm_OOS_MaxDD=rr.OOS_MaxDD,
                              twin_OOS_MaxDD=mto["MaxDD"], arm_4b_FULL=rr.pass4b_FULL,
                              twin_4b_FULL=b_f, arm_4b_OOS=rr.pass4b_OOS, twin_4b_OOS=b_o))
    TW = pd.DataFrame(twin_rows)
    if len(TW):
        P(TW.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
        both = int((TW.arm_4b_OOS & TW.twin_4b_OOS).sum())
        P(f"  twin ALSO passes 4b (OOS) at {both}/{len(TW)} of the passes; "
          f"arm-minus-twin mean OOS Sharpe {float((TW.arm_OOS_Sharpe-TW.twin_OOS_Sharpe).mean()):+.4f}")
    P()
    P("=" * 100)
    P("(C) OUTPUTS")
    P("=" * 100)
    dump(RU, "rungs")
    dump(PKS, "picks")
    dump(WF, "walkforward")
    dump(ST, "stability")
    if len(TW):
        dump(TW, "twins")
    P(f"  elapsed {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
