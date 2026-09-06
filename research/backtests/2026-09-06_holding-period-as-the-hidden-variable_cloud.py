#!/usr/bin/env python3
"""Idea 76 - "holding-period-as-the-hidden-variable" (cloud, 2026-09-06).

The claim under test
--------------------
Idea 9 found a per-name trailing stop's firing rate is governed by mean holding-episode
length and held-name vol20 (v1 16d/0.144 -> 3.3% hit rate; top20 39d/0.228 -> 22.4%;
ew-band3 170d/0.189 -> 70.3%), not by the stop level.  Idea 76 proposes the general form:

    "measure episode length and held-name vol for every book the project has run and test
     whether they predict each book's cost sensitivity (idea 68's -0.068..-0.099
     Sharpe/10bps) and its response to cadence (idea 3).  If they do, holding period is
     the design variable and turnover is only its shadow."

Two things are pre-registered here BEFORE any number was read, because the second one
decides whether the question is answerable at all:

  P1 (the identity).  In `engine.backtest` cost enters as `- turnover_t * bps/1e4`, and
     the weights (hence the turnover path) do not depend on the cost rung.  So
         dCAGR/d(bps)   = -(annual turnover)/1e4      exactly, and
         dSharpe/10bps ~= -(annual turnover) * 0.0010 / sigma_ann.
     Cost sensitivity is therefore an ARITHMETIC IDENTITY in turnover and book vol, not an
     empirical property that holding period could independently explain.  This run
     MEASURES the identity's residual rather than assuming it: if |measured - predicted|
     is at the 3rd decimal, idea 76's first half is answered by construction.
  P2 (the shadow).  Turnover and episode length are mechanically reciprocal:
     turnover ~ 2 * gross / L for a book that fully replaces its names every L days.  If
     R^2 between annual turnover and gross/L is near 1 across the corpus, then "holding
     period is the design variable and turnover is its shadow" is a RE-PARAMETERISATION,
     not a discovery, and neither variable can be shown to dominate.
  The one place L can earn independence is CADENCE (idea 3), which does NOT enter through
  turnover arithmetic: a book whose names sit for months should be indifferent to being
  re-decided daily/weekly/monthly.  That is the run's live question.

Corpus (a pre-registered book list spanning the project's construction families)
-------------------------------------------------------------------------------
    NOGATE    equal-weight every tradable name, no gate            (longest episodes)
    EWALL     equal-weight every ELIGIBLE name (200d & vol20<0.60) (idea 72/10's book)
    BAND3     EWALL with a 3% re-entry band on the 200d gate       (idea 57)
    ABS       equal-weight names with positive 12-1 momentum       (idea 4's abs gate)
    V1        RULES v1 as live: vol-scaled composite, n=5, w=0.15  (the incumbent)
    V1C20     vol-scaled composite, top-20, gross/n                (the "V1C-shaped" book)
    CAND5/10/20/30/40/60  composite WITHOUT the vol scaler, top-n, constant gross
    MOM20     top-20 by 12-1 momentum alone, constant gross
  = 13 books x 4 panels (U56, ETF36, B136, SMALL) = 52 book-cells.

Axes reported in full (NOT tuned - every point is published)
    cost in {0, 10, 20, 30} bps   cadence in {D, W, M}
  = 52 x 4 x 3 = 624 backtests, all in `.grid.csv`.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. panel (4)   2. book (13).
  Cost and cadence are REPORTED AXES, not selected over, except inside the rule-8 chooser
  test where the selection is explicit and its OOS cost is the reported quantity.
  PROTOCOL's own rung (10 bps) and cadence (W) are the primary cell everywhere.

Measurements per book-cell (on the W/10bps primary book, so one number per cell)
    L          mean holding-episode length in trading days: a maximal run of consecutive
               days with weight > 1e-12 in one name, counted over every name.  Episodes
               open at the first day and censored at the last are INCLUDED (they are real
               holdings); the censored share is reported so the bias is visible.
    L_med      median episode length (L is right-skewed).
    heldvol    weight-weighted mean vol20 of the held names, averaged over days.
    turn       annualised turnover (sum of per-rebalance |dw| / years).
    gross      mean invested weight.

Walk-forward (PROTOCOL rule 8) -- rules and directions fixed before any OOS read
    IS = 2009-2016, OOS = 2017-2026 read once.  Choosers pick ONE book per panel on IS
    only, then the OOS return of that pick is read:
    LONGEST    the book with the longest IS mean episode length   (idea 76's variable)
    LOWTURN    the book with the lowest IS annual turnover        (its shadow)
    LOWVOL     the book with the lowest IS held-name vol20
    ISSHARPE   the book with the best IS Sharpe                   (the incumbent selector)
    NOTHING    U56 / CAND20, the project's standing candidate     (do-nothing control)
    RANDOM     mean OOS over the 13 books                         (a coin flip)
    Reported per panel and pooled (equal weight over the 4 panels).

Verdicts: both KEEP paths on every one of the 624 points.
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1 (same panel).
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

SURVIVORSHIP: every panel is CURRENT constituents, one-directional, hardest on B136 and
SMALL.  The small panel additionally drops the 44 tickers with max_1d_move >= 1.0 in
data/small_meta.csv.  Holding-period statistics are especially exposed: a delisted name's
episode ends at delisting in reality and never appears here at all, so measured L is
biased UP on the survivorship-selected panels.  Restated in the memo.

Deterministic, standalone.  Reads baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import json
import numpy as np
import pandas as pd
from baseline import load_universe, score
from engine import backtest, metrics

COSTS = [0, 10, 20, 30]
CADENCES = ["D", "W", "M"]
PRIMARY_COST, PRIMARY_FREQ = 10, "W"
MAX_VOL = 0.60
GROSS = 0.75
W_FIXED = 0.15
BAND = 0.03
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
BOOKS = ["NOGATE", "EWALL", "BAND3", "ABS", "V1", "V1C20",
         "CAND5", "CAND10", "CAND20", "CAND30", "CAND40", "CAND60", "MOM20"]
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 60)
pd.set_option("display.max_rows", 900)


# ---------------------------------------------------------------- panels
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)

    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    pxs = pxs[[c for c in pxs.columns if c == "SPY" or c not in bad]]
    dropped = len(bad & set(meta["ticker"]))

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    return {
        "U56":   sub(px56, list(px56.columns)),
        "ETF36": sub(px56, etf36),
        "B136":  sub(px136, list(px136.columns)),
        "SMALL": sub(pxs, [c for c in pxs.columns if c != "SPY"],
                     tradable=[c for c in pxs.columns if c != "SPY"]),
    }, dropped


# ---------------------------------------------------------------- books
def _tradable_mask(px, tradable):
    m = pd.DataFrame(True, index=px.index, columns=px.columns)
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def _ew(mask):
    cnt = mask.sum(axis=1).replace(0, np.nan)
    return mask.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)


def _topn(px, elig, n, vol_scale):
    s = score(px, vol_scale=vol_scale)[0]
    rank = s.where(elig).rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    held = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(held, axis=0).mul(GROSS).fillna(0.0)


def make_weights(px, tradable, book):
    _, above, vol20 = score(px)
    tr = _tradable_mask(px, tradable)
    elig = above & (vol20 < MAX_VOL) & tr

    if book == "NOGATE":
        return _ew(tr & px.notna())
    if book == "EWALL":
        return _ew(elig)
    if book == "BAND3":
        ma = px.rolling(200).mean()
        up, dn = px > ma * (1 + BAND), px < ma * (1 - BAND)
        st = pd.DataFrame(np.nan, index=px.index, columns=px.columns)
        st = st.where(~up, 1.0).where(~dn, 0.0).ffill().fillna(0.0).astype(bool)
        return _ew(st & (vol20 < MAX_VOL) & tr)
    if book == "ABS":
        mom = px.shift(21) / px.shift(252) - 1
        return _ew((mom > 0) & (vol20 < MAX_VOL) & tr)
    if book == "V1":
        s = score(px, vol_scale=True)[0]
        rank = s.where(elig).rank(axis=1, ascending=False)
        return (rank <= 5).astype(float) * W_FIXED
    if book == "V1C20":
        return _topn(px, elig, 20, True)
    if book == "MOM20":
        mom = px.shift(21) / px.shift(252) - 1
        rank = mom.where(elig).rank(axis=1, ascending=False)
        sel = (rank <= 20).astype(float)
        held = sel.sum(axis=1).replace(0, np.nan)
        return sel.div(held, axis=0).mul(GROSS).fillna(0.0)
    if book.startswith("CAND"):
        return _topn(px, elig, int(book[4:]), False)
    raise ValueError(book)


# ---------------------------------------------------------------- holding-period measurement
def episode_stats(held, vol20):
    """Mean/median holding-episode length in trading days over every name, plus the
    weight-weighted mean vol20 of the held book and the right-censored episode share."""
    H = (held.values > 1e-12)
    lens, censored = [], 0
    for j in range(H.shape[1]):
        col = H[:, j]
        if not col.any():
            continue
        d = np.diff(np.concatenate(([0], col.view(np.int8), [0])))
        starts = np.flatnonzero(d == 1)
        ends = np.flatnonzero(d == -1)
        L = ends - starts
        lens.append(L)
        censored += int(ends[-1] == len(col)) if len(ends) else 0
    if not lens:
        return dict(L=np.nan, L_med=np.nan, n_episodes=0, censored_share=np.nan, heldvol=np.nan)
    L = np.concatenate(lens)
    w = held.clip(lower=0)
    tot = w.sum(axis=1).replace(0, np.nan)
    hv = (w * vol20.reindex_like(w)).sum(axis=1).div(tot)
    return dict(L=float(L.mean()), L_med=float(np.median(L)), n_episodes=int(L.size),
                censored_share=float(censored / L.size), heldvol=float(hv.mean()))


# ---------------------------------------------------------------- metric helpers
def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def verdict_4a(r, base):
    h1, h2 = half_sharpes(r); b1, b2 = half_sharpes(base)
    return bool(h1 > b1 and h2 > b2 and metrics(r)["MaxDD"] >= metrics(base)["MaxDD"])


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r); s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3: return np.nan, int(ok.sum())
    xr = pd.Series(x[ok]).rank().values; yr = pd.Series(y[ok]).rank().values
    if xr.std() == 0 or yr.std() == 0: return np.nan, int(ok.sum())
    return float(np.corrcoef(xr, yr)[0, 1]), int(ok.sum())


def ols(y, X):
    """y ~ [1, X]; returns (coefs, R2). X is (n,k)."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    ok = np.isfinite(y) & np.isfinite(X).all(axis=1)
    y, X = y[ok], X[ok]
    if len(y) < X.shape[1] + 2: return None, np.nan
    A = np.column_stack([np.ones(len(y)), X])
    b, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ b
    ss = ((y - y.mean()) ** 2).sum()
    return b, float(1 - (resid ** 2).sum() / ss) if ss else np.nan


def fmt(df, p=3):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ---------------------------------------------------------------- main
def main():
    panels, dropped = build_panels()

    print("=" * 200)
    print(f"Idea 76 holding-period-as-the-hidden-variable (cloud) | {SCRIPT} | "
          f"primary cell = {PRIMARY_COST} bps, {PRIMARY_FREQ}, next-day execution")
    print("=" * 200)
    px56 = panels["U56"][0]
    yrs = px56.index.to_series().groupby(px56.index.year).count()
    print(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        print("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)
    print(f"small panel hygiene: dropped {dropped} tickers with max_1d_move >= 1.0; "
          f"{len(panels['SMALL'][1])} tradable remain")
    for k, (p, tr) in panels.items():
        print(f"  {k:<6} {len(tr):>3} tradable   {p.index[0].date()} -> {p.index[-1].date()}")

    start = max(p.index[260] for p, _ in panels.values())
    end = min(p.index[-1] for p, _ in panels.values())
    years = (end - start).days / 365.25
    print(f"\nCommon evaluation window: {start.date()} -> {end.date()} ({years:.2f} yrs)")
    spy = px56["SPY"].pct_change().fillna(0).loc[start:end]
    spy_is, spy_oos = spy.loc[:IS_END], spy.loc[OOS_START:]

    # ---- run everything
    W = {}
    for pk, (p, tr) in panels.items():
        for bk in BOOKS:
            W[(pk, bk)] = make_weights(p, tr, bk)
        print(f"  weights built: {pk}")

    rows, ret_cache, ep = [], {}, {}
    for pk, (p, tr) in panels.items():
        _, _, vol20 = score(p)
        for bk in BOOKS:
            w = W[(pk, bk)]
            for fq in CADENCES:
                res0 = backtest(p, w, cost_bps=0, freq=fq)
                held = res0["weights"]
                to_ann = res0["turnover"].loc[start:end].sum() / years
                if fq == PRIMARY_FREQ:
                    ep[(pk, bk)] = episode_stats(held.loc[start:end], vol20)
                    ep[(pk, bk)]["turn"] = to_ann
                    ep[(pk, bk)]["gross"] = held.loc[start:end].sum(axis=1).mean()
                for cb in COSTS:
                    r = (res0["returns"] - res0["turnover"] * cb / 1e4).loc[start:end]
                    ret_cache[(pk, bk, fq, cb)] = r
                    m = metrics(r); mo = metrics(r.loc[OOS_START:]); mi = metrics(r.loc[:IS_END])
                    h1, h2 = half_sharpes(r)
                    rows.append(dict(panel=pk, book=bk, freq=fq, cost=cb,
                                     CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=h1, H2=h2, IS_Sharpe=mi["Sharpe"],
                                     OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                     turn=to_ann, gross=held.loc[start:end].sum(axis=1).mean()))
        print(f"  ran {pk}")

    grid = pd.DataFrame(rows)
    grid["pass4a"] = False
    for pk in panels:
        base = ret_cache[(pk, "V1", PRIMARY_FREQ, PRIMARY_COST)]
        m = grid.panel == pk
        grid.loc[m, "pass4a"] = [verdict_4a(ret_cache[(r.panel, r.book, r.freq, r.cost)], base)
                                 for r in grid[m].itertuples()]
    grid["fail4b"] = [fail_4b(ret_cache[(r.panel, r.book, r.freq, r.cost)], spy,
                              ret_cache[(r.panel, r.book, r.freq, r.cost)].loc[OOS_START:], spy_oos)
                      for r in grid.itertuples()]
    grid["pass4b"] = grid["fail4b"] == "-"
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    print("\n--- harness sanity (must match published rows) ---")
    r = ret_cache[("U56", "V1", "W", 10)]
    m = metrics(r); h1, h2 = half_sharpes(r)
    print(f"  U56/V1     {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}"
          f"   [live v1 on this window]")
    r = ret_cache[("U56", "CAND20", "W", 10)]
    m = metrics(r); h1, h2 = half_sharpes(r)
    print(f"  U56/CAND20 {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}"
          f"   [idea 2 KEEP, NORM gross]")

    # ---------------- (1) the holding-period table
    eptab = pd.DataFrame([dict(panel=pk, book=bk, **v) for (pk, bk), v in ep.items()])
    eptab["turn_pred_from_L"] = 2 * eptab["gross"] / (eptab["L"] / 252)
    eptab.to_csv(OUT / f"{STEM}.episodes.csv", index=False)
    print("\n" + "=" * 200)
    print("(1) HOLDING PERIOD, HELD-NAME VOL AND TURNOVER for every book-cell "
          f"(primary cell {PRIMARY_FREQ}/{PRIMARY_COST}bps)")
    print("=" * 200)
    print(fmt(eptab[["panel", "book", "L", "L_med", "n_episodes", "censored_share",
                     "heldvol", "turn", "gross", "turn_pred_from_L"]], 3))
    print("\nidea 9's published anchors, for reference: v1 16d/0.144, top20 39d/0.228, ew-band3 170d/0.189")
    a = eptab[eptab.panel == "U56"].set_index("book")
    for b, want in [("V1", "16d / 0.144"), ("CAND20", "39d / 0.228"), ("BAND3", "170d / 0.189")]:
        if b in a.index:
            print(f"  U56/{b:<7} L {a.loc[b,'L']:6.1f}d  heldvol {a.loc[b,'heldvol']:.3f}   [idea 9: {want}]")

    # ---------------- (2) P2: is turnover the shadow of L, or the same variable?
    print("\n" + "=" * 200)
    print("(2) P2 - are annual turnover and holding-period length the SAME dial?")
    print("=" * 200)
    e = eptab.dropna(subset=["L", "turn"])
    rho, n = spearman(e["L"], e["turn"])
    print(f"  Spearman(L, annual turnover)          = {rho:+.3f} (N={n})")
    rho2, _ = spearman(1 / e["L"], e["turn"])
    print(f"  Spearman(1/L, annual turnover)        = {rho2:+.3f}")
    _, r2 = ols(e["turn"], np.column_stack([2 * e["gross"] / (e["L"] / 252)]))
    print(f"  OLS turnover ~ 2*gross/L (yrs)        R2 = {r2:.4f}   "
          f"[mean |turn - 2*gross/L| = {np.abs(e['turn'] - e['turn_pred_from_L']).mean():.3f}x/yr]")
    rho3, _ = spearman(e["heldvol"], e["turn"])
    print(f"  Spearman(held-name vol20, turnover)   = {rho3:+.3f}")

    # ---------------- (3) P1: cost sensitivity is an identity
    print("\n" + "=" * 200)
    print("(3) P1 - cost sensitivity: measured vs the arithmetic prediction -turnover*0.0010/sigma")
    print("=" * 200)
    cs = []
    for pk in panels:
        for bk in BOOKS:
            s = {cb: metrics(ret_cache[(pk, bk, PRIMARY_FREQ, cb)])["Sharpe"] for cb in COSTS}
            c = {cb: metrics(ret_cache[(pk, bk, PRIMARY_FREQ, cb)])["CAGR"] for cb in COSTS}
            sig = metrics(ret_cache[(pk, bk, PRIMARY_FREQ, PRIMARY_COST)])["Vol"]
            t = ep[(pk, bk)]["turn"]
            slope = (s[30] - s[0]) / 3.0                     # Sharpe per 10 bps
            cs.append(dict(panel=pk, book=bk, L=ep[(pk, bk)]["L"], heldvol=ep[(pk, bk)]["heldvol"],
                           turn=t, vol=sig,
                           dSharpe_per_10bps=slope, pred_dSharpe=-t * 0.0010 / sig,
                           resid=slope + t * 0.0010 / sig,
                           dCAGR_per_10bps_pp=(c[30] - c[0]) / 3.0 * 100,
                           pred_dCAGR_pp=-t * 0.0010 * 100,
                           S0=s[0], S10=s[10], S20=s[20], S30=s[30]))
    cs = pd.DataFrame(cs)
    cs.to_csv(OUT / f"{STEM}.costsens.csv", index=False)
    print(fmt(cs, 4))
    print(f"\n  measured dSharpe/10bps range: {cs['dSharpe_per_10bps'].min():.4f} .. "
          f"{cs['dSharpe_per_10bps'].max():.4f}   [idea 68 published -0.068 .. -0.099]")
    print(f"  |measured - predicted| Sharpe: mean {cs['resid'].abs().mean():.5f}  "
          f"max {cs['resid'].abs().max():.5f}")
    print(f"  |measured - predicted| CAGR pp: mean "
          f"{(cs['dCAGR_per_10bps_pp'] - cs['pred_dCAGR_pp']).abs().mean():.5f}  max "
          f"{(cs['dCAGR_per_10bps_pp'] - cs['pred_dCAGR_pp']).abs().max():.5f}")
    for lab, x in [("L", cs["L"]), ("1/L", 1 / cs["L"]), ("heldvol", cs["heldvol"]),
                   ("turnover", cs["turn"]), ("turnover/vol", cs["turn"] / cs["vol"])]:
        rho, n = spearman(x, cs["dSharpe_per_10bps"])
        print(f"  Spearman({lab:<12}, dSharpe/10bps) = {rho:+.3f} (N={n})")
    _, r2a = ols(cs["dSharpe_per_10bps"], np.column_stack([cs["turn"] / cs["vol"]]))
    _, r2b = ols(cs["dSharpe_per_10bps"], np.column_stack([1 / cs["L"], cs["heldvol"]]))
    _, r2c = ols(cs["dSharpe_per_10bps"], np.column_stack([cs["turn"] / cs["vol"], 1 / cs["L"], cs["heldvol"]]))
    print(f"  R2  dSharpe ~ turnover/vol                : {r2a:.4f}")
    print(f"  R2  dSharpe ~ 1/L + heldvol               : {r2b:.4f}")
    print(f"  R2  dSharpe ~ turnover/vol + 1/L + heldvol: {r2c:.4f}   "
          f"(incremental over turnover/vol: {r2c - r2a:+.4f})")

    # ---------------- (4) the live question: cadence response
    print("\n" + "=" * 200)
    print("(4) CADENCE (idea 3) - the one channel that is NOT turnover arithmetic")
    print("=" * 200)
    cad = []
    for pk in panels:
        for bk in BOOKS:
            s = {fq: metrics(ret_cache[(pk, bk, fq, PRIMARY_COST)])["Sharpe"] for fq in CADENCES}
            d = {fq: metrics(ret_cache[(pk, bk, fq, PRIMARY_COST)])["MaxDD"] for fq in CADENCES}
            cad.append(dict(panel=pk, book=bk, L=ep[(pk, bk)]["L"], heldvol=ep[(pk, bk)]["heldvol"],
                            turn=ep[(pk, bk)]["turn"],
                            S_D=s["D"], S_W=s["W"], S_M=s["M"],
                            range_S=max(s.values()) - min(s.values()),
                            dS_M_minus_W=s["M"] - s["W"], dS_D_minus_W=s["D"] - s["W"],
                            dDD_M_minus_W_pp=(d["M"] - d["W"]) * 100))
    cad = pd.DataFrame(cad)
    cad.to_csv(OUT / f"{STEM}.cadence.csv", index=False)
    print(fmt(cad, 3))
    for lab, x in [("L", cad["L"]), ("1/L", 1 / cad["L"]), ("heldvol", cad["heldvol"]),
                   ("turnover", cad["turn"])]:
        rho, n = spearman(x, cad["range_S"])
        rho2, _ = spearman(x, cad["dS_M_minus_W"].abs())
        print(f"  Spearman({lab:<8}, cadence Sharpe RANGE) = {rho:+.3f} (N={n})   "
              f"vs |Sharpe(M)-Sharpe(W)| = {rho2:+.3f}")
    _, rA = ols(cad["range_S"], np.column_stack([1 / cad["L"]]))
    _, rB = ols(cad["range_S"], np.column_stack([cad["turn"]]))
    _, rC = ols(cad["range_S"], np.column_stack([1 / cad["L"], cad["turn"]]))
    print(f"  R2  cadence range ~ 1/L        : {rA:.4f}")
    print(f"  R2  cadence range ~ turnover   : {rB:.4f}")
    print(f"  R2  cadence range ~ both       : {rC:.4f}  (1/L incremental over turnover: {rC - rB:+.4f})")
    print(f"  mean cadence Sharpe range by L quartile:")
    q = cad.assign(Lq=pd.qcut(cad["L"], 4, labels=["Q1 short", "Q2", "Q3", "Q4 long"]))
    print(q.groupby("Lq", observed=True)[["L", "turn", "range_S", "dS_M_minus_W"]].mean().to_string(
        float_format=lambda x: f"{x:.3f}"))

    # ---------------- (5) rule 8
    print("\n" + "=" * 200)
    print(f"(5) RULE 8 WALK-FORWARD - IS <= {IS_END}, OOS >= {OOS_START} read once")
    print("=" * 200)
    is_stats = {}
    for pk in panels:
        _, _, v20 = score(panels[pk][0])
        for bk in BOOKS:
            r = ret_cache[(pk, bk, PRIMARY_FREQ, PRIMARY_COST)]
            heldW = backtest(panels[pk][0], W[(pk, bk)], cost_bps=0, freq=PRIMARY_FREQ)["weights"]
            e_is = episode_stats(heldW.loc[start:IS_END], v20)
            is_stats[(pk, bk)] = dict(IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                      IS_L=e_is["L"], IS_heldvol=e_is["heldvol"],
                                      IS_turn=grid[(grid.panel == pk) & (grid.book == bk) &
                                                   (grid.freq == PRIMARY_FREQ) &
                                                   (grid.cost == PRIMARY_COST)]["turn"].iloc[0])
        print(f"  IS stats done: {pk}")

    wf = []
    for rule in ("LONGEST", "LOWTURN", "LOWVOL", "ISSHARPE", "NOTHING", "RANDOM"):
        for pk in panels:
            cand = {bk: is_stats[(pk, bk)] for bk in BOOKS}
            if rule == "LONGEST":
                pick = max(cand, key=lambda b: cand[b]["IS_L"])
            elif rule == "LOWTURN":
                pick = min(cand, key=lambda b: cand[b]["IS_turn"])
            elif rule == "LOWVOL":
                pick = min(cand, key=lambda b: cand[b]["IS_heldvol"])
            elif rule == "ISSHARPE":
                pick = max(cand, key=lambda b: cand[b]["IS_Sharpe"])
            elif rule == "NOTHING":
                pick = "CAND20"
            else:
                pick = None
            if rule == "RANDOM":
                oo = [metrics(ret_cache[(pk, b, PRIMARY_FREQ, PRIMARY_COST)].loc[OOS_START:]) for b in BOOKS]
                wf.append(dict(rule=rule, panel=pk, pick="(mean of 13)",
                               OOS_CAGR=np.mean([m["CAGR"] for m in oo]),
                               OOS_Sharpe=np.mean([m["Sharpe"] for m in oo]),
                               OOS_MaxDD=np.mean([m["MaxDD"] for m in oo])))
            else:
                p = "U56" if rule == "NOTHING" else pk
                mo = metrics(ret_cache[(p, pick, PRIMARY_FREQ, PRIMARY_COST)].loc[OOS_START:])
                wf.append(dict(rule=rule, panel=pk, pick=(f"U56/{pick}" if rule == "NOTHING" else pick),
                               OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    wf = pd.DataFrame(wf)
    wf.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    print(fmt(wf, 3))
    print("\npooled OOS (equal weight over the 4 panels):")
    print(fmt(wf.groupby("rule")[["OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD"]].mean().sort_values(
        "OOS_Sharpe", ascending=False), 3))
    print(f"\nSPY OOS: {metrics(spy_oos)['CAGR']:.1%} / {metrics(spy_oos)['Sharpe']:.3f} / "
          f"{metrics(spy_oos)['MaxDD']:.1%}")
    v1o = ret_cache[("U56", "V1", PRIMARY_FREQ, PRIMARY_COST)].loc[OOS_START:]
    print(f"RULES v1 OOS: {metrics(v1o)['CAGR']:.1%} / {metrics(v1o)['Sharpe']:.3f} / "
          f"{metrics(v1o)['MaxDD']:.1%}")

    # ---------------- (6) KEEP paths
    print("\n" + "=" * 200)
    print("(6) KEEP PATHS over all 624 points")
    print("=" * 200)
    ms = metrics(spy); sh1, sh2 = half_sharpes(spy)
    print(f"SPY: CAGR {ms['CAGR']:.1%}  Sharpe {ms['Sharpe']:.3f}  MaxDD {ms['MaxDD']:.1%}  "
          f"halves {sh1:.3f}/{sh2:.3f}  |  4b bars MaxDD <= {0.60*abs(ms['MaxDD']):.1%}, "
          f"CAGR >= {0.70*ms['CAGR']:.1%}")
    print(f"4a passes: {int(grid['pass4a'].sum())} of {len(grid)}   "
          f"4b passes: {int(grid['pass4b'].sum())} of {len(grid)}")
    print(grid.groupby(["freq", "cost"])[["pass4a", "pass4b"]].sum().to_string())
    prim = grid[(grid.freq == PRIMARY_FREQ) & (grid.cost == PRIMARY_COST)]
    print(f"\nprimary cell ({PRIMARY_FREQ}/{PRIMARY_COST}bps): 4a {int(prim.pass4a.sum())}/{len(prim)}  "
          f"4b {int(prim.pass4b.sum())}/{len(prim)}")
    cols = ["panel", "book", "freq", "cost", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "OOS_Sharpe", "OOS_MaxDD", "turn", "gross", "pass4a", "pass4b", "fail4b"]
    if prim["pass4b"].any():
        print("\n4b-passing points in the primary cell:")
        print(fmt(prim[prim.pass4b][cols].merge(
            eptab[["panel", "book", "L", "heldvol"]], on=["panel", "book"], how="left"), 3))
    print("\nfull primary-cell table:")
    print(fmt(prim[cols], 3))

    print("\n" + "=" * 200)
    print("Artefacts:", ", ".join(sorted(p.name for p in OUT.glob(f"{STEM}.*"))))
    print("=" * 200)


if __name__ == "__main__":
    main()
