#!/usr/bin/env python3
"""Idea 671 (cloud lane, 2026-09-15) — is the ROUND channel's LEFT TAIL a BOOK-WIDTH fact?

QUESTION (QUEUE idea 671, verbatim)
    idea 668 found ROUND's median cost is +0.0000 on all five dials (664's free-channel result
    replicates) yet it carries the run's single worst flip, -0.4617 OOS Sharpe, when reading to
    0 decimals moves U56's n from 50 to 3.  Sweep the rounding ladder over dials whose rungs
    differ in BOOK WIDTH (n, coverage, sector cap) against dials that do not (band, gross,
    cadence) and report whether the fat left tail is a width phenomenon.
    Max 2 params (dial class, decimals).

THE CHANNEL, restated exactly as 668 implemented it.  A rule-8 chooser reads each rung's
    IN-SAMPLE Sharpe and takes the argmax, ties broken to the SMALLEST rung index.  The ROUND
    channel rounds that read to `dp` decimals BEFORE the argmax, so coarse rounding manufactures
    TIES and the tie-break -- not the evidence -- decides the book.  dp=10 is the honest control.

WHAT IS NEW AGAINST 668.  668 measured the channel on five dials at one gross and reported the
    pooled median and the single worst flip.  This run does the thing the queue asks: it splits
    the dials by whether their rungs change BOOK WIDTH, replicates each dial over three
    committed context settings and three panels so the tail has a population instead of one
    observation, and -- because "width" is an assumption, not a fact -- it MEASURES the width
    spread of every dial and reports the a-priori classification against the measurement.

TUNED PARAMETERS: exactly TWO, the two the queue names.  ALL grid points reported.
    (1) DIAL CLASS in {WIDTH, NONWIDTH} -- the queue's own partition, declared before any number:
            WIDTH     N        top-n ranked book, n in {3,5,10,15,20,30,40,50}
                      COVERAGE top-q fraction of that day's eligible names,
                               q in {0.05,0.10,0.20,0.30,0.50,0.70,0.85,1.00}
                      VOLBREADTH  hold EVERY band-eligible name with vol20 < cap,
                               cap in {0.20,0.25,0.30,0.40,0.50,0.60,0.80,9.99}
            NONWIDTH  BAND     200d band half-width, {0.00..0.20}   (the queue calls this
                               non-width; this run MEASURES it and reports otherwise -- see H_MEASURE)
                      GROSS    {0.20..1.00} -- identical holdings, different exposure
                      CADENCE  {D,W,M,Q}    -- identical book, different rebalance dates
        The queue's third width dial, SECTOR CAP, is run as SLEEVECAP on U56 ONLY and reported
        separately: `research/universe.json`'s four sleeves (broad / sectors / bonds_fx_commod /
        megacap) are the only group map in the repo; `universe_broad.json` is a flat list and the
        small panel has none.  Nothing is fabricated to fill the gap.
    (2) DECIMALS dp in {10 (CONTROL), 3, 2, 1, 0} -- 668's own ladder, all five reported.

CORPUS (not tuned): 3 panels (U56 / B136 / SMALL) x 6 dials x 3 committed context rungs = 54
    sites, plus 3 U56-only SLEEVECAP sites.  Every rung of every site at every dp is published.

PRE-REGISTERED HYPOTHESES (declared before any OOS number was read)
    H_MEDIAN0   668's free-channel result replicates: the MEDIAN dOOS Sharpe of the ROUND channel
                is +0.0000 in BOTH classes.
    H_WIDTH     the LEFT TAIL is a width phenomenon: min dOOS Sharpe and P(d <= -0.10) are
                materially worse for WIDTH dials than for NONWIDTH dials.
    H_TIE       the channel only ever bites through TIES: every cell with d != 0 has >= 2 rungs
                tied at the rounded maximum.
    H_MEASURE   the a-priori classification is WRONG about BAND -- its measured width spread is
                large, because the band gate admits and expels names.
    H_SCALE     |d| tracks the WIDTH JUMP between the control pick and the rounded pick, not the
                dial's IS-Sharpe spread.

GATES (printed before any new number; all must pass or the run stops)
    G1  fast_backtest == engine.backtest @10 bps (max |d| < 1e-12)
    G2  band_book(0.03,0.75) == baseline.rules_v2_weights (EXACT 0)
    G3  668's HEADLINE ROUND OBSERVATION reproduced: on U56's N dial at gross 0.75, dp=0 moves
        the pick from n=50 to n=3 and costs about -0.4617 OOS Sharpe.  668 itself reported this
        channel is VINTAGE-SENSITIVE (data/prices.csv gains trading days), so the gate is tried
        on today's tape and on truncations and the reproducing vintage is NAMED.
    G4  CONTROL IDENTITY: at dp=10 the rounded argmax equals the unrounded argmax at every site.
    G5  determinism: one dial rebuilt twice, max |d| == 0.

PROTOCOL: 10 bps per unit turnover (25 bps also reported), weights decided at close t applied at
    t+1, no shorting, no leverage.  BOTH KEEP paths evaluated on every pick, full sample and read
    inside OOS.  Rule 8 IS the design: the chooser (and its rounding) sees 2009/2010-2016 only;
    the OOS window 2017-2026 is read once per (site, dp).

SURVIVORSHIP, up front: U56 / B136 / SMALL are CURRENT-constituent lists (SMALL = the sub-$2B
    screen after dropping the 52 tickers with max_1d_move >= 1.0 per data/small_meta.csv), so
    every CAGR and drawdown LEVEL is optimistic.  What this run measures is a DIFFERENCE between
    two readings of the SAME books, which is survivorship-neutral by construction.  Nothing here
    is a capital claim and nothing is promoted.

Outputs (committed under research/backtests/):
    .console.txt      full log
    .rungs.csv        every rung of every site: IS Sharpe, mean held names, FULL/OOS metrics
    .cells.csv        every (site, dp): pick, tie count, index jump, width jump, d vs control
    .walkforward.csv  the rule-8 table: per (site, dp) the pick's OOS CAGR/Sharpe/MaxDD against
                      RULES v2 and SPY on the same window, with 4a/4b at 10 and 25 bps
    .tails.csv        the left-tail summary by dial class and by dial

Run: python research/backtests/2026-09-15_is-the-ROUND-channel-s-LEFT-TAIL-a-BOOK-WIDTH-fact_cloud.py
Deterministic; no network (reads the committed price caches only).
"""
import json
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
SLUG = "is-the-ROUND-channel-s-LEFT-TAIL-a-BOOK-WIDTH-fact"
STEM = f"{DATE}_{SLUG}_cloud"
OUT = Path(__file__).resolve().parent

FREQ0 = "W"
COST_HEAD = 10.0
WARM = 260
BAND0, GROSS0, N0 = 0.03, 0.75, 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"

DPS = [10, 3, 2, 1, 0]          # 10 == CONTROL
DP_CTRL = 10

BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20]
NS = [3, 5, 10, 15, 20, 30, 40, 50]
QS = [0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 0.85, 1.00]
VOLCAPS = [0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 9.99]
GROSSES = [0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00]
CADENCES = ["D", "W", "M", "Q"]
SLEEVECAPS = [1, 2, 3, 4, 6, 8, 12, 999]

CTX_GROSS = [0.50, 0.75, 1.00]          # the record's three committed gross rungs
CTX_BAND = [0.02, 0.03, 0.05]           # context for the GROSS dial (its own rung IS gross)

CLASS = {"N": "WIDTH", "COVERAGE": "WIDTH", "VOLBREADTH": "WIDTH",
         "BAND": "NONWIDTH", "GROSS": "NONWIDTH", "CADENCE": "NONWIDTH",
         "SLEEVECAP": "WIDTH"}

# idea 668's committed headline ROUND observation (CHANGELOG 2026-09-10, idea 668)
IDEA668 = dict(panel="U56", dial="N", gross=0.75, dp=0, ctrl_pick=50, round_pick=3,
               dOOS=-0.4617)

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==================================================================================
# 1.  ENGINE (vectorised equivalent of engine.backtest; asserted against it in G1)
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


def sel_to_w(sel, gross):
    k = sel.sum(axis=1).replace(0, np.nan)
    return (sel.mul(gross / k, axis=0)).fillna(0.0)


def sel_topn(rank, n):
    return (rank <= n).astype(float)


def sel_topq(rank, elig_count, q):
    n_t = np.maximum(1.0, np.round(q * elig_count))
    return (rank.le(n_t, axis=0)).astype(float)


def sel_volbreadth(px, band, cap, vol20):
    return (band_state(px, band) & px.notna() & (vol20 < cap)).astype(float)


def sel_sleevecap(rank, sleeve_of, cols, cap):
    """At most `cap` names per sleeve among the ranked eligible names, then top-N0 overall."""
    if cap >= 999:
        return sel_topn(rank, N0)
    out = pd.DataFrame(0.0, index=rank.index, columns=rank.columns)
    for sl in sorted(set(sleeve_of.values())):
        c = [t for t in cols if sleeve_of.get(t) == sl]
        if not c:
            continue
        sub = rank[c].rank(axis=1, method="first")      # rank within sleeve, order preserved
        out[c] = (sub <= cap).astype(float)
    keep = rank.where(out > 0)
    inner = keep.rank(axis=1, method="first")
    return (inner <= N0).astype(float)


def build_site(px, dial, ctx, cache):
    """Return (rung labels, {rung: parts}, {rung: mean held names})."""
    start = px.index[WARM]
    sc, above, vol20 = cache["score"]

    def clip(parts):
        return tuple(s.loc[start:] for s in parts)

    labels, books = [], {}
    if dial == "BAND":
        labels = [f"{b:.2f}" for b in BANDS]
        for b, L in zip(BANDS, labels):
            books[L] = clip(fast_parts(px, band_book(px, b, ctx)))
    elif dial == "GROSS":
        labels = [f"{g:.2f}" for g in GROSSES]
        for g, L in zip(GROSSES, labels):
            books[L] = clip(fast_parts(px, band_book(px, ctx, g)))
    elif dial == "CADENCE":
        labels = list(CADENCES)
        w = band_book(px, BAND0, ctx)
        for c in CADENCES:
            books[c] = clip(fast_parts(px, w, c))
    elif dial == "N":
        labels = [str(n) for n in NS]
        for n, L in zip(NS, labels):
            books[L] = clip(fast_parts(px, sel_to_w(sel_topn(cache["rank"], n), ctx)))
    elif dial == "COVERAGE":
        labels = [f"{q:.2f}" for q in QS]
        for q, L in zip(QS, labels):
            books[L] = clip(fast_parts(px, sel_to_w(
                sel_topq(cache["rank"], cache["elig_count"], q), ctx)))
    elif dial == "VOLBREADTH":
        labels = [f"{v:.2f}" for v in VOLCAPS]
        for v, L in zip(VOLCAPS, labels):
            books[L] = clip(fast_parts(px, sel_to_w(sel_volbreadth(px, BAND0, v, vol20), ctx)))
    elif dial == "SLEEVECAP":
        labels = [str(c) for c in SLEEVECAPS]
        for c, L in zip(SLEEVECAPS, labels):
            books[L] = clip(fast_parts(px, sel_to_w(
                sel_sleevecap(cache["rank"], cache["sleeve"], cache["cols"], c), ctx)))
    width = {L: float(books[L][2].mean()) for L in labels}
    return labels, books, width


# ==================================================================================
# 3.  THE ROUNDED CHOOSER
# ==================================================================================
def pick_at(labels, is_sharpe, dp):
    """argmax of the IS Sharpe read to dp decimals; ties -> SMALLEST rung index."""
    vals = [round(is_sharpe[L], dp) for L in labels]
    best = max(v for v in vals if np.isfinite(v))
    ties = [i for i, v in enumerate(vals) if np.isfinite(v) and v == best]
    return ties[0], len(ties)


def keeppaths(r, base, spy, leg):
    if leg == "OOS":
        r, base, spy = r.loc[OOS_START:], base.loc[OOS_START:], spy.loc[OOS_START:]
    m, mb, ms = M(r), M(base), M(spy)
    oos_s, oos_b = M0(r.loc[OOS_START:]), M0(spy.loc[OOS_START:])
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > oos_b)
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
           and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return bool(p4a), bool(p4b), m, mb, ms


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    rx = pd.Series(x[ok]).rank().values
    ry = pd.Series(y[ok]).rank().values
    return float(np.corrcoef(rx, ry)[0, 1])


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(x[ok], y[ok])[0, 1])


# ==================================================================================
# 4.  GATES
# ==================================================================================
def gates(PX, caches):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    px = PX["U56"]
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

    g5 = float(np.abs(at_cost(fast_parts(px, w), COST_HEAD).values - fast.values).max())
    P(f"  G5 determinism (same book rebuilt twice)               : {g5:.3e}  "
      f"{'PASS' if g5 == 0.0 else 'FAIL'}")
    ok &= (g5 == 0.0)

    P("  G3 idea 668's HEADLINE ROUND observation (U56 / N dial / gross 0.75 / dp=0):")
    P(f"     committed: pick {IDEA668['ctrl_pick']} -> {IDEA668['round_pick']}, "
      f"dOOS Sharpe {IDEA668['dOOS']:+.4f}.  VINTAGE-PINNED (668 reported this channel itself).")
    best = None
    for end in (None, "2026-09-11", "2026-09-09", "2026-09-04"):
        q = px if end is None else px.loc[:end]
        if len(q) < WARM + 500:
            continue
        st = q.index[WARM]
        sc, above, vol20 = score(q, vol_scale=True)
        rk = sc.where(above).rank(axis=1, ascending=False)   # 668's N dial: max_vol=9.99
        bk = {str(n): at_cost(fast_parts(q, sel_to_w(sel_topn(rk, n), GROSS0)),
                              COST_HEAD).loc[st:] for n in NS}
        iss = {L: M0(bk[L].loc[:IS_END]) for L in bk}
        labs = [str(n) for n in NS]
        i_c, _ = pick_at(labs, iss, DP_CTRL)
        i_0, nt = pick_at(labs, iss, 0)
        d = M0(bk[labs[i_0]].loc[OOS_START:]) - M0(bk[labs[i_c]].loc[OOS_START:])
        row = (end or "TODAY", labs[i_c], labs[i_0], d, nt)
        if best is None or abs(d - IDEA668["dOOS"]) < abs(best[3] - IDEA668["dOOS"]):
            best = row
        P(f"     vintage {row[0]:10s} pick {row[1]:>2s} -> {row[2]:>2s} "
          f"(ties at dp=0: {nt})   dOOS {d:+.4f}")
    hit = (best[1] == str(IDEA668["ctrl_pick"]) and best[2] == str(IDEA668["round_pick"])
           and abs(best[3] - IDEA668["dOOS"]) < 5e-3)
    P(f"     best vintage {best[0]}  -> {'PASS' if hit else 'FAIL'}  "
      f"(residual {abs(best[3]-IDEA668['dOOS']):.3e})")
    ok &= hit
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


def make_cache(pn, px):
    sc, above, vol20 = score(px, vol_scale=True)
    # ELIGIBILITY for the ranked families is idea 668's own: above the 200d MA, vol cap OFF
    # (668's N dial calls ranked_book(..., max_vol=9.99)).  The vol cap is a DIAL here, not a
    # constant, so folding it into eligibility would double-count it.
    elig = sc.where(above)
    rank = elig.rank(axis=1, ascending=False)
    c = dict(score=(sc, above, vol20), rank=rank,
             elig_count=elig.notna().sum(axis=1).astype(float))
    if pn == "U56":
        U = json.loads((ROOT / "research" / "universe.json").read_text())
        c["sleeve"] = {t: g for g, ts in U.items() for t in ts}
        c["cols"] = [t for t in px.columns if t in c["sleeve"]]
    return c


def main():
    t0 = time.time()
    P("=" * 100)
    P(f"IDEA 671  {SLUG}   (cloud)  {pd.Timestamp.today().date()}")
    P("=" * 100)
    PX = panels()
    caches = {pn: make_cache(pn, px) for pn, px in PX.items()}
    for k, v in PX.items():
        P(f"  panel {k:6s} {v.shape[1]-1:4d} names + SPY   "
          f"{v.index[0].date()} .. {v.index[-1].date()}  ({len(v)} rows)")
    P("  SURVIVORSHIP: current-constituent lists; LEVELS optimistic.  This run measures a")
    P("  DIFFERENCE between two READINGS of the same books, which is survivorship-neutral.")
    P()
    if not gates(PX, caches):
        sys.exit(1)

    DIALS = [("BAND", CTX_GROSS), ("GROSS", CTX_BAND), ("CADENCE", CTX_GROSS),
             ("N", CTX_GROSS), ("COVERAGE", CTX_GROSS), ("VOLBREADTH", CTX_GROSS)]

    rung_rows, cell_rows, wf_rows = [], [], []
    ctrl_ok = True

    for pn, px in PX.items():
        start = px.index[WARM]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base = at_cost(fast_parts(px, rules_v2_weights(px, BAND0, GROSS0)), COST_HEAD).loc[start:]
        dials = list(DIALS) + ([("SLEEVECAP", CTX_GROSS)] if pn == "U56" else [])
        P("-" * 100)
        P(f"panel {pn}")
        for dial, ctxs in dials:
            for ctx in ctxs:
                labels, books, width = build_site(px, dial, ctx, caches[pn])
                iss = {L: M0(at_cost(books[L], COST_HEAD).loc[:IS_END]) for L in labels}
                site = f"{pn}|{dial}|ctx{ctx}"
                for L in labels:
                    r = at_cost(books[L], COST_HEAD)
                    mf, mo = M(r), M(r.loc[OOS_START:])
                    rung_rows.append(dict(panel=pn, dial=dial, dial_class=CLASS[dial], ctx=ctx,
                                          rung=L, mean_names=width[L], IS_Sharpe=iss[L],
                                          FULL_CAGR=mf["CAGR"], FULL_Sharpe=mf["Sharpe"],
                                          FULL_MaxDD=mf["MaxDD"], OOS_CAGR=mo["CAGR"],
                                          OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
                wvals = np.array([width[L] for L in labels], float)
                wspread = float(wvals.max() - wvals.min())
                wrel = float((wvals.max() - wvals.min()) / max(wvals.mean(), 1e-9))
                isspread = float(max(iss.values()) - min(iss.values()))
                i_ctrl, _ = pick_at(labels, iss, DP_CTRL)
                i_raw = int(np.nanargmax([iss[L] for L in labels]))
                ctrl_ok &= (i_ctrl == i_raw)
                oos_ctrl = M0(at_cost(books[labels[i_ctrl]], COST_HEAD).loc[OOS_START:])
                line = []
                for dp in DPS:
                    i_d, nties = pick_at(labels, iss, dp)
                    L = labels[i_d]
                    r = at_cost(books[L], COST_HEAD)
                    r25 = at_cost(books[L], 25.0)
                    a_f, b_f, mf, mbf, msf = keeppaths(r, base, spy, "FULL")
                    a_o, b_o, mo, mbo, mso = keeppaths(r, base, spy, "OOS")
                    _, b_f25, _, _, _ = keeppaths(r25, base, spy, "FULL")
                    _, b_o25, _, _, _ = keeppaths(r25, base, spy, "OOS")
                    d_sh = mo["Sharpe"] - oos_ctrl
                    cell_rows.append(dict(
                        panel=pn, dial=dial, dial_class=CLASS[dial], ctx=ctx, dp=dp,
                        site=site, pick=L, ctrl_pick=labels[i_ctrl], n_ties=nties,
                        idx_jump=abs(i_d - i_ctrl), width=width[L],
                        width_ctrl=width[labels[i_ctrl]],
                        width_jump=abs(width[L] - width[labels[i_ctrl]]),
                        width_spread=wspread, width_rel_spread=wrel, IS_spread=isspread,
                        dOOS_Sharpe=d_sh,
                        dOOS_CAGR=mo["CAGR"] - M(at_cost(books[labels[i_ctrl]],
                                                         COST_HEAD).loc[OOS_START:])["CAGR"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        pass4a_OOS=a_o, pass4b_OOS=b_o, pass4b_FULL=b_f,
                        pass4b_OOS_25bps=b_o25, pass4b_FULL_25bps=b_f25))
                    wf_rows.append(dict(
                        panel=pn, dial=dial, dial_class=CLASS[dial], ctx=ctx, dp=dp, pick=L,
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        BASE_OOS_CAGR=mbo["CAGR"], BASE_OOS_Sharpe=mbo["Sharpe"],
                        BASE_OOS_MaxDD=mbo["MaxDD"], SPY_OOS_CAGR=mso["CAGR"],
                        SPY_OOS_Sharpe=mso["Sharpe"], SPY_OOS_MaxDD=mso["MaxDD"],
                        pass4a_OOS=a_o, pass4b_OOS=b_o))
                    line.append(f"dp{dp}={L}{'' if nties == 1 else f'(t{nties})'}"
                                f"{'' if abs(d_sh) < 5e-5 else f'[{d_sh:+.3f}]'}")
                P(f"  {dial:11s} ctx {ctx:<5} width {wvals.min():6.1f}..{wvals.max():6.1f} "
                  f"(rel {wrel:4.2f})  | " + " ".join(line))

    RU, CE, WF = pd.DataFrame(rung_rows), pd.DataFrame(cell_rows), pd.DataFrame(wf_rows)
    P()
    P(f"  G4 CONTROL IDENTITY (dp=10 argmax == unrounded argmax at every site): "
      f"{'PASS' if ctrl_ok else 'FAIL'}")
    if not ctrl_ok:
        sys.exit(1)

    NC = CE[CE.dp != DP_CTRL].copy()          # the channel: control excluded
    MAIN = NC[NC.dial != "SLEEVECAP"]

    P()
    P("=" * 100)
    P("(B) RESULTS -- the ROUND channel, 4 non-control decimal levels x 54 sites = "
      f"{len(MAIN)} cells (+{len(NC)-len(MAIN)} U56-only SLEEVECAP cells, reported apart)")
    P("=" * 100)

    P()
    P("  B1  MEASURED BOOK WIDTH per dial (mean names held; the queue's classification is an")
    P("      ASSUMPTION and this is the measurement)")
    wtab = (CE.groupby(["dial", "dial_class"])
              .agg(width_min=("width_ctrl", "min"), width_max=("width", "max"),
                   rel_spread=("width_rel_spread", "mean")).reset_index())
    P(wtab.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    band_rel = float(CE[CE.dial == "BAND"].width_rel_spread.mean())
    P(f"  H_MEASURE (BAND's measured width spread is large despite its NONWIDTH label): "
      f"{'CONFIRMED' if band_rel > 0.25 else 'FALSIFIED'}  (BAND mean relative width spread "
      f"{band_rel:.3f})")

    P()
    P("  B2  THE CHANNEL BY CLASS (dOOS Sharpe against the dp=10 control)")

    def tail(g):
        d = g.dOOS_Sharpe.values
        return pd.Series(dict(
            cells=len(d), median=float(np.median(d)), mean=float(np.mean(d)),
            min=float(np.min(d)), p05=float(np.percentile(d, 5)),
            frac_moved=float(np.mean(np.abs(d) > 5e-5)),
            frac_le_010=float(np.mean(d <= -0.10)), frac_le_025=float(np.mean(d <= -0.25)),
            mean_neg=float(np.mean(d[d < 0])) if (d < 0).any() else 0.0))

    bycls = MAIN.groupby("dial_class").apply(tail, include_groups=False)
    P(bycls.to_string(float_format=lambda x: f"{x:.4f}"))
    P()
    P("  by dial:")
    P(NC.groupby(["dial_class", "dial"]).apply(tail, include_groups=False)
      .to_string(float_format=lambda x: f"{x:.4f}"))
    P()
    P("  by decimals (both classes pooled, MAIN dials):")
    P(MAIN.groupby("dp").apply(tail, include_groups=False)
      .to_string(float_format=lambda x: f"{x:.4f}"))

    medW = bycls.loc["WIDTH", "median"]
    medN = bycls.loc["NONWIDTH", "median"]
    P()
    P(f"  H_MEDIAN0 (668's free-channel median replicates in BOTH classes): "
      f"{'CONFIRMED' if abs(medW) < 5e-5 and abs(medN) < 5e-5 else 'FALSIFIED'}  "
      f"(WIDTH median {medW:+.4f}, NONWIDTH median {medN:+.4f})")
    hw = (bycls.loc["WIDTH", "min"] < bycls.loc["NONWIDTH", "min"] - 0.05
          and bycls.loc["WIDTH", "frac_le_010"] > bycls.loc["NONWIDTH", "frac_le_010"])
    P(f"  H_WIDTH (the left tail is a WIDTH phenomenon): "
      f"{'CONFIRMED' if hw else 'FALSIFIED'}  "
      f"(min {bycls.loc['WIDTH','min']:+.4f} vs {bycls.loc['NONWIDTH','min']:+.4f}; "
      f"P(d<=-0.10) {bycls.loc['WIDTH','frac_le_010']:.3f} vs "
      f"{bycls.loc['NONWIDTH','frac_le_010']:.3f})")

    moved = MAIN[np.abs(MAIN.dOOS_Sharpe) > 5e-5]
    P()
    P(f"  H_TIE (every moved cell is decided by a TIE): "
      f"{'CONFIRMED' if (moved.n_ties >= 2).all() else 'FALSIFIED'}  "
      f"({int((moved.n_ties >= 2).sum())} of {len(moved)} moved cells have >= 2 tied rungs; "
      f"min ties among moved {int(moved.n_ties.min()) if len(moved) else 0})")

    P()
    P("  B3  WHAT PREDICTS THE DAMAGE?  (statistic NAMED, per the record's open idea 564)")
    for nm, xcol in (("width_jump", "width_jump"), ("idx_jump", "idx_jump"),
                     ("width_rel_spread", "width_rel_spread"), ("IS_spread", "IS_spread"),
                     ("n_ties", "n_ties")):
        y = MAIN.dOOS_Sharpe.values
        x = MAIN[xcol].values
        P(f"     {nm:18s} vs dOOS Sharpe   Spearman {spearman(x, y):+.4f}   "
          f"Pearson {pearson(x, y):+.4f}   (n={len(y)})")
    P(f"  H_SCALE (|d| tracks the WIDTH JUMP more than the IS-Sharpe spread): ")
    sw = abs(spearman(MAIN.width_jump.values, -np.abs(MAIN.dOOS_Sharpe.values)))
    si = abs(spearman(MAIN.IS_spread.values, -np.abs(MAIN.dOOS_Sharpe.values)))
    P(f"     |Spearman(width_jump, -|d|)| {sw:.4f} vs |Spearman(IS_spread, -|d|)| {si:.4f}"
      f"  -> {'CONFIRMED' if sw > si else 'FALSIFIED'}")

    P()
    P("  B4  THE WORST CELLS IN THE RUN (dOOS Sharpe, all dials)")
    worst = NC.nsmallest(12, "dOOS_Sharpe")
    P(worst[["panel", "dial", "dial_class", "ctx", "dp", "ctrl_pick", "pick", "n_ties",
             "width_ctrl", "width", "dOOS_Sharpe", "dOOS_CAGR"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P()
    P("  B5  RULE 8 / KEEP PATHS.  Every cell is a rule-8 pick: the (rounded) chooser sees IS")
    P("      only and the OOS window is read once.  Verdicts at 10 bps unless stated.")
    P(f"     4a passes OOS : {int(CE.pass4a_OOS.sum())} of {len(CE)}")
    P(f"     4b passes OOS : {int(CE.pass4b_OOS.sum())} of {len(CE)}  "
      f"(at 25 bps: {int(CE.pass4b_OOS_25bps.sum())})")
    P(f"     4b passes FULL: {int(CE.pass4b_FULL.sum())} of {len(CE)}  "
      f"(at 25 bps: {int(CE.pass4b_FULL_25bps.sum())})")
    agg = CE.groupby("dp").agg(OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
                               OOS_MaxDD=("OOS_MaxDD", "mean"), n4b=("pass4b_OOS", "sum"),
                               n4a=("pass4a_OOS", "sum"))
    P(agg.to_string(float_format=lambda x: f"{x:.4f}"))
    P("     comparands on the same OOS window:")
    for pn in PX:
        w = WF[WF.panel == pn].iloc[0]
        P(f"       {pn:6s} SPY {w.SPY_OOS_CAGR:7.2%} / {w.SPY_OOS_Sharpe:6.4f} / "
          f"{w.SPY_OOS_MaxDD:7.2%}   RULES v2 {w.BASE_OOS_CAGR:7.2%} / "
          f"{w.BASE_OOS_Sharpe:6.4f} / {w.BASE_OOS_MaxDD:7.2%}")
    P("     4b-passing cells whose verdict is CREATED OR DESTROYED by the rounding:")
    flips = []
    for site, g in CE.groupby("site"):
        c = g[g.dp == DP_CTRL].iloc[0]
        for _, r in g[g.dp != DP_CTRL].iterrows():
            if bool(r.pass4b_OOS) != bool(c.pass4b_OOS):
                flips.append(dict(site=site, dp=r.dp, ctrl_pick=c.pick, pick=r.pick,
                                  ctrl_4b=bool(c.pass4b_OOS), dp_4b=bool(r.pass4b_OOS),
                                  dOOS_Sharpe=r.dOOS_Sharpe))
    FL = pd.DataFrame(flips)
    if len(FL):
        P(FL.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    else:
        P("       none -- the rounding never changes a 4b verdict in this corpus")
    P(f"     4b-verdict flips caused by rounding: {len(FL)} of {len(MAIN)+len(NC)-len(MAIN)}"
      f" non-control cells")

    P()
    P("  B6  SLEEVECAP (the queue's 'sector cap', U56 ONLY -- universe_broad.json is a flat")
    P("      list and the small panel has no group map, so nothing is fabricated for them)")
    SC = NC[NC.dial == "SLEEVECAP"]
    if len(SC):
        P(SC[["ctx", "dp", "ctrl_pick", "pick", "n_ties", "width_ctrl", "width",
              "dOOS_Sharpe"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    P()
    P("=" * 100)
    P("(C) OUTPUTS")
    P("=" * 100)
    dump(RU, "rungs")
    dump(CE, "cells")
    dump(WF, "walkforward")
    tails = pd.concat([
        NC.groupby(["dial_class", "dial"]).apply(tail, include_groups=False).reset_index(),
        MAIN.groupby("dial_class").apply(tail, include_groups=False)
            .reset_index().assign(dial="ALL"),
    ], ignore_index=True)
    dump(tails, "tails")
    P(f"  elapsed {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")


if __name__ == "__main__":
    main()
