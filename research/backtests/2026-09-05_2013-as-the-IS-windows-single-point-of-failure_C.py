#!/usr/bin/env python3
"""QUEUE idea 112 — 2013-as-the-IS-window's-single-point-of-failure (lane C, 2026-09-05).

Question (as worded in QUEUE.md)
--------------------------------
"idea 99 found 2013 (SPY +32%, MaxDD -5.6%) is the worst year for overlays in the whole sample
(pooled d -0.36 u56, -0.42 broad, roughly 3x the next-worst) and sits inside the IS window at
every one of the six pre-registered split dates.  Run idea 89's leave-one-year-out harness on the
IS WINDOW ITSELF: does deleting 2013 change rule 8's pick in any of the 44 overlay cells, and does
the G statistic survive?"

WHY IT MATTERS
--------------
PROTOCOL rule 8 fixes ONE in-sample window (2009-2016) and picks parameters by argmax IS Sharpe.
If a single calendar year inside that window is doing the selecting, rule 8 is not a walk-forward
procedure, it is a bet on 2013.  This run measures that dependence directly.

THE HARNESS (identical construction to ideas 99/109 so every number is comparable)
----------------------------------------------------------------------------------
  6 overlay grids  sleeve (S4 fraction), band (200d hysteresis), breadth (gross cut), stop
                   (trailing), crypto (u56 only), gross (static lever)
  x 2 base books   top20 (ranked, gross 0.75), ewall (equal-weight all eligible, gross 0.75)
  x 2 universes    u56 (research/universe.json + BTC/ETH), broad (universe_broad.json)
  x 2 cost rungs   10 and 25 bps, weekly rebalance, next-day execution (engine)
  = 44 CELLS (u56 6 grids x 2 books + broad 5 grids x 2 books = 22, x 2 cost rungs).

STATISTICS, DECLARED BEFORE ANY NUMBER IS COMPUTED
---------------------------------------------------
Windows.  IS_full = [eval start .. 2016-12-31].  OOS = [2017-01-01 .. end], NEVER touched.
          IS_ex_y = IS_full with every row in calendar year y deleted, y in 2009..2016.
          (2009 is a partial year — the eval starts ~2009-01 — and is flagged as such.)

S1 PICK STABILITY.  pick(W) = argmax over the grid of Sharpe on W, tie-break smallest |parameter|
   (pkey), exactly as rule 8 is applied elsewhere in this project.  For each cell and each dropped
   year y: does pick(IS_ex_y) differ from pick(IS_full)?  Reported as a count over the 44 cells,
   PER YEAR.  The queue's hypothesis is that 2013 is special; the null is that pick instability is
   spread evenly over the eight IS years.  Pre-registered decision rule:
       2013 IS a single point of failure iff it changes strictly more cells than every other
       IS year AND that count is at least 2x the median year's count.
   Otherwise the finding is "rule 8's pick is (un)stable to any one year", which is the honest
   headline either way.

S2 COST OF THE SWAP.  Where the pick changes, the OOS consequence: OOS Sharpe, OOS CAGR and OOS
   MaxDD of pick(IS_ex_y) minus pick(IS_full), and the change in the count of 4b passes.  A pick
   change that is OOS-neutral is a curiosity; one that is OOS-signed is a defect in rule 8.

S3 DOES G SURVIVE.  Idea 99's statistic, recomputed with the reduced IS window:
       d(W,p) = Sharpe_W(p) - Sharpe_W(no-overlay point);  G(p) = d(IS,p) - d(OOS,p).
   Full-IS reference values from idea 99: pooled mean G = -0.058, negative in 82% of 164 points;
   per grid sleeve -0.169, crypto -0.078, breadth -0.057, band -0.036, stop -0.004, gross 0.000.
   Pre-registered survival test for a dropped year y:
       G SURVIVES ex-y iff pooled mean G(IS_ex_y) is still negative AND frac(G<0) > 0.50 AND
       |mean G(IS_ex_y)| >= 0.5 x |mean G(IS_full)|.
   If G survives deleting 2013, idea 99's gap is not a 2013 artefact.  If it collapses, PROTOCOL
   rule 8's window has a named single point of failure and the memo says so.

S4 PREMISE CHECK.  Idea 99's per-year pooled d is re-derived here on this run's own grid points,
   to confirm 2013 really is the worst year for overlays before anything is built on it.

TUNED (2, per PROTOCOL rule 4): the overlay parameter (4-5 levels per grid) x the dropped year
(8 levels + the no-drop control).  Nothing is selected on the dropped year — ALL nine variants of
every cell are reported, in the console and in the CSVs.

WALK-FORWARD (PROTOCOL rule 8, mandatory).  For every cell, the point rule 8 picks on IS_full and
the point it picks on IS_ex_2013 are both carried into the untouched 2017-2026 window and reported
with OOS CAGR / Sharpe / MaxDD against RULES v1 and SPY, plus full-sample CAGR/Sharpe/MaxDD/halves
and BOTH KEEP paths (4a beat-the-book, 4b capital-worthy).  The headline sleeve cell
(u56 / top20 / 10 bps — the standing KEEP-4b candidate's cell) is printed in full.

CAVEATS
-------
SURVIVORSHIP: both equity panels are current constituents of their lists; levels are biased up.
  The bias is identical across every window and every dropped year, which is all this run compares.
CRYPTO: BTC-USD starts 2014-09-17, ETH-USD later, so the crypto grid's IS window is short and its
  2009-2013 LOYO drops are near-no-ops.  Crypto rows are shown both in and out of every pooled stat.
DATA (queue idea 38): data/prices*.csv are calendar-day indexed after 2014-09-17; weekend rows are
  zero-return.  It hits every grid point, every window and every dropped year identically.
SHARPE ON A SPLICED SERIES: deleting a year's rows leaves mean/std well defined (this is idea 89's
  convention); MaxDD is NOT meaningful on a spliced series and is therefore never taken on one.

Deterministic, standalone (no network; reads the committed price caches):
    python research/backtests/2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C.py
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics

FREQ = "W"
COSTS = (10, 25)
IS_END = "2016-12-31"
SPLIT = "2017-01-01"
BOOK_GROSS = 0.75
S4 = ["TLT", "GLD", "DBC", "UUP"]
CRYPTO = ["BTC-USD", "ETH-USD"]
BREADTH_B = 0.30
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
IS_YEARS = list(range(2009, 2017))          # every calendar year inside the IS window
FOCUS_YEAR = 2013                           # the queue's named suspect
OUT = Path(__file__).with_suffix("")

APRIORI = {"sleeve": "defensive", "band": "defensive", "breadth": "defensive",
           "stop": "defensive", "crypto": "offensive", "gross": "mixed"}

# idea 99's published full-IS reference numbers, quoted so the deltas below are checkable
IDEA99_G = {"ALL": -0.058, "sleeve": -0.169, "crypto": -0.078, "breadth": -0.057,
            "band": -0.036, "stop": -0.004, "gross": 0.000}


# ---------------------------------------------------------------- gates and books (idea 99 verbatim)
def _band_above(px, w):
    ma = px.rolling(200).mean()
    up = (px > ma * (1 + w))
    dn = (px < ma * (1 - w))
    st = pd.DataFrame(np.where(up, 1.0, np.where(dn, 0.0, np.nan)),
                      index=px.index, columns=px.columns)
    return st.ffill().fillna(0.0) > 0.5


def _elig(px, band=0.0, stop=None):
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    m = _band_above(px, band) & (vol20 < 0.60)
    if stop is not None:
        dd = px / px.rolling(126).max() - 1.0
        m = m & (dd > -stop)
    return m


def book(px, kind, band=0.0, stop=None, gross=BOOK_GROSS, n=20):
    s, _, _ = score(px, vol_scale=False)
    m = _elig(px, band, stop)
    if kind == "top20":
        rank = s.where(m).rank(axis=1, ascending=False)
        w = (rank <= n).astype(float)
    else:
        w = (m & s.notna()).astype(float)
    k = w.sum(axis=1)
    return w.div(k.where(k > 0), axis=0).fillna(0.0) * gross


def sleeve_weights(px, assets):
    sub = px[assets]
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = (1.0 / vol.replace(0.0, np.nan))
    rp = inv.div(inv.sum(axis=1), axis=0)
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    vote = sum((x > 0).astype(float).where(x.notna()) for x in sig) / len(sig)
    w = (vote * rp).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w
    return out


def _regross(w, g=1.00):
    tot = w.sum(axis=1)
    return w.mul((g / tot.where(tot > 1e-12)).fillna(0.0), axis=0)


def overlay(px, kind, grid, p):
    if grid == "sleeve":
        E = book(px, kind)
        return _regross((1 - p) * E + p * sleeve_weights(px, S4), 1.00)
    if grid == "band":
        return book(px, kind, band=p)
    if grid == "breadth":
        E = book(px, kind)
        above = _band_above(px, 0.0).drop(columns=["SPY"], errors="ignore")
        br = above.mean(axis=1)
        mult = pd.Series(np.where(br < BREADTH_B, 1.0 - p, 1.0), index=px.index)
        return E.mul(mult, axis=0)
    if grid == "stop":
        return book(px, kind, stop=None if p is None else p)
    if grid == "gross":
        return book(px, kind, gross=p)
    if grid == "crypto":
        E = book(px, kind, gross=BOOK_GROSS * (1 - p))
        if p == 0.0:
            return E
        c = [t for t in CRYPTO if t in px.columns]
        avail = px[c].notna().astype(float)
        k = avail.sum(axis=1)
        cw = avail.div(k.where(k > 0), axis=0).fillna(0.0) * (BOOK_GROSS * p)
        out = E.copy()
        out[c] = out[c].values + cw.values
        return out
    raise ValueError(grid)


GRIDS = {
    "sleeve":  [0.00, 0.25, 0.50, 0.75, 1.00],
    "band":    [0.00, 0.02, 0.03, 0.05, 0.08],
    "breadth": [0.00, 0.25, 0.50, 0.75, 1.00],
    "stop":    [None, 0.25, 0.20, 0.15, 0.10],
    "crypto":  [0.00, 0.02, 0.05, 0.10],
    "gross":   [0.75, 0.50, 1.00, 1.25],
}
NULL_P = {"sleeve": 0.00, "band": 0.00, "breadth": 0.00, "stop": None,
          "crypto": 0.00, "gross": 0.75}


def pkey(grid, p):
    if grid == "stop":
        return 0.0 if p is None else 1.0 - p
    if grid == "gross":
        return abs(p - 0.75)
    return float(p)


# ---------------------------------------------------------------- metrics
def net(gr, to, bps):
    return gr - to * bps / 1e4


def stats(r):
    if len(r) < 60:
        return np.nan, np.nan, np.nan
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def sharpe(r):
    """Sharpe on a (possibly spliced) return series. NaN if too short to mean anything."""
    if len(r) < 60:
        return np.nan
    v = r.std()
    return float(r.mean() * 252 / (v * np.sqrt(252))) if v > 0 else np.nan


def full_row(r):
    h = len(r) // 2
    c, s, d = stats(r)
    _, h1, _ = stats(r.iloc[:h])
    _, h2, _ = stats(r.iloc[h:])
    ic, is_, idd = stats(r.loc[:IS_END])
    oc, os_, od = stats(r.loc[SPLIT:])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2,
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def keep_4a(r, base):
    return bool(r["H1"] > base["H1"] and r["H2"] > base["H2"] and r["MaxDD"] >= base["MaxDD"])


def keep_4b(r, spy):
    return bool(r["H1"] > spy["H1"] and r["H2"] > spy["H2"] and r["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and r["MaxDD"] >= 0.60 * spy["MaxDD"] and r["CAGR"] >= 0.70 * spy["CAGR"])


def keep_4b_oos(r, spy):
    return bool(r["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and r["OOS_MaxDD"] >= 0.60 * spy["OOS_MaxDD"]
                and r["OOS_CAGR"] >= 0.70 * spy["OOS_CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


def ols(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return np.nan, np.nan, np.nan
    x, y = x[m], y[m]
    b = np.polyfit(x, y, 1)
    return float(b[0]), float(b[1]), float(np.corrcoef(x, y)[0, 1])


# ---------------------------------------------------------------- main
def main():
    u56 = load_universe(exclude=set())
    broad = load_universe(broad=True)
    universes = {"u56": u56, "broad": broad}
    print(f"[data] u56 {u56.shape[1]} cols, broad {broad.shape[1]} cols")
    print("[pre-registered] S1 pick stability · S2 OOS cost of the swap · S3 G survival · S4 premise")
    print(f"[pre-registered] IS = ..{IS_END}, OOS = {SPLIT}.. (never touched); dropped years {IS_YEARS}")
    print("[pre-registered] 2013 is a single point of failure iff it changes strictly more cells")
    print("                 than every other IS year AND >= 2x the median year's count.")
    print("[pre-registered] G survives ex-y iff mean G < 0 AND frac(G<0) > 0.50 AND")
    print("                 |mean G(ex-y)| >= 0.5 x |mean G(full)|.\n")

    # cost linearity (lets every point be run once at 0 bps and both rungs derived exactly)
    st0 = u56.index[260]
    w0 = book(u56, "top20")
    r0 = backtest(u56, w0, cost_bps=0.0, freq=FREQ)
    err = float((net(r0["returns"].loc[st0:], r0["turnover"].loc[st0:], 10)
                 - backtest(u56, w0, cost_bps=10, freq=FREQ)["returns"].loc[st0:]).abs().max())
    print(f"[check] cost linearity max |derived - direct| at 10 bps = {err:.2e}")
    assert err < 1e-12

    series = {}          # (universe, grid, book, cost_bps, param) -> net return series
    records, refs = [], {}
    for tag, px in universes.items():
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy = full_row(spy_r)
        bt = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        bgr, bto = bt["returns"].loc[start:], bt["turnover"].loc[start:]
        refs[tag] = (spy, bgr, bto, spy_r)
        print("=" * 124)
        print(f"### UNIVERSE {tag}: {px.shape[1]} tickers | eval {start.date()} -> {px.index[-1].date()}")
        print(fmt(pd.DataFrame({"RULES v1 (10bps)": full_row(net(bgr, bto, 10)), "SPY": spy}).T))

        for grid, params in GRIDS.items():
            if grid == "crypto" and not all(t in px.columns for t in CRYPTO):
                print(f"  [skip] grid={grid} on {tag}: crypto tickers absent from this panel")
                continue
            for kind in ("top20", "ewall"):
                for p in params:
                    w = overlay(px, kind, grid, p)
                    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
                    gr, to = res["returns"].loc[start:], res["turnover"].loc[start:]
                    gross = float(w.loc[start:].sum(axis=1).mean())
                    turn = float(to.sum() / (len(gr) / 252))
                    for bps in COSTS:
                        r = net(gr, to, bps)
                        key = (tag, grid, kind, bps, "none" if p is None else p)
                        series[key] = r
                        row = full_row(r)
                        base = full_row(net(bgr, bto, bps))
                        row.update(universe=tag, grid=grid, book=kind,
                                   param=("none" if p is None else p), cost_bps=bps,
                                   Gross=gross, Turn_yr=turn, pkey=pkey(grid, p),
                                   is_null=(p == NULL_P[grid]), apriori=APRIORI[grid])
                        # IS Sharpe with each single IS year deleted (the LOYO harness)
                        isr = r.loc[:IS_END]
                        row["IS_Sharpe_full"] = sharpe(isr)
                        for y in IS_YEARS:
                            row[f"IS_Sharpe_ex{y}"] = sharpe(isr[isr.index.year != y])
                        # per-calendar-year Sharpe over the whole sample (for S4)
                        for y in range(2010, 2027):
                            row[f"SH_y_{y}"] = sharpe(r.loc[f"{y}-01-01":f"{y}-12-31"])
                        row["4a"] = keep_4a(row, base)
                        row["4b"] = keep_4b(row, spy)
                        row["4b_oos"] = keep_4b_oos(row, spy)
                        records.append(row)

    G = pd.DataFrame(records)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print(f"\n[grid] {len(G)} points -> {OUT.name}.grid.csv")

    CELL = ["universe", "grid", "book", "cost_bps"]
    cells = list(G.groupby(CELL, sort=False).groups.keys())
    print(f"[cells] {len(cells)} cells (expected 44)")

    # ============================================================ (1) every grid point
    print("\n" + "=" * 124)
    print("### (1) EVERY GRID POINT — full-IS Sharpe and IS-ex-2013 Sharpe (10 bps; 25 bps in .grid.csv)\n")
    for (tag, grid, kind), sub in G[G.cost_bps == 10].groupby(["universe", "grid", "book"], sort=False):
        print(f"--- {tag} | grid={grid} | book={kind}")
        cols = ["Gross", "Turn_yr", "CAGR", "Sharpe", "MaxDD", "IS_Sharpe_full",
                f"IS_Sharpe_ex{FOCUS_YEAR}", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "4a", "4b"]
        print(fmt(sub.set_index("param")[cols]))
        print()

    # ============================================================ (2) S1 pick stability
    print("=" * 124)
    print("### (2) S1 — RULE 8's PICK, FULL IS vs EACH LEAVE-ONE-YEAR-OUT IS WINDOW\n")

    def pick_on(sub, col):
        s = sub[[col, "pkey", "param"]].dropna(subset=[col])
        if s.empty:
            return None
        best = s[col].max()
        tied = s[np.isclose(s[col], best)]
        return tied.sort_values("pkey").iloc[0]["param"]

    picks = []
    for keys, sub in G.groupby(CELL, sort=False):
        d = dict(zip(CELL, keys))
        p_full = pick_on(sub, "IS_Sharpe_full")
        rec = dict(d, pick_full=p_full)
        for y in IS_YEARS:
            rec[f"pick_ex{y}"] = pick_on(sub, f"IS_Sharpe_ex{y}")
        picks.append(rec)
    P = pd.DataFrame(picks)
    P.to_csv(OUT.with_suffix(".picks.csv"), index=False)
    print(fmt(P.set_index(CELL)))

    print("\n--- CELLS WHOSE PICK CHANGES, BY DROPPED YEAR (out of 44)")
    counts = {}
    for y in IS_YEARS:
        chg = (P[f"pick_ex{y}"].astype(str) != P["pick_full"].astype(str))
        counts[y] = int(chg.sum())
    CT = pd.Series(counts, name="cells_changed").to_frame()
    CT["frac"] = CT["cells_changed"] / len(P)
    print(CT.to_string(float_format=lambda x: f"{x:.3f}"))
    med = float(np.median(list(counts.values())))
    c13 = counts[FOCUS_YEAR]
    strictly_most = all(c13 > counts[y] for y in IS_YEARS if y != FOCUS_YEAR)
    twice_median = c13 >= 2 * med if med > 0 else c13 > 0
    verdict_s1 = "SUPPORTED" if (strictly_most and twice_median) else "NOT SUPPORTED"
    print(f"\n  2013 changes {c13}/44 cells; median year {med:.1f}; "
          f"max other year {max(counts[y] for y in IS_YEARS if y != FOCUS_YEAR)}")
    print(f"  PRE-REGISTERED S1 (2013 as a single point of failure): {verdict_s1}")

    print("\n--- WHICH CELLS 2013 MOVES")
    mv = P[P[f"pick_ex{FOCUS_YEAR}"].astype(str) != P["pick_full"].astype(str)]
    print(fmt(mv.set_index(CELL)[["pick_full", f"pick_ex{FOCUS_YEAR}"]]) if len(mv) else "  (none)")

    # ============================================================ (3) S2 OOS cost of the swap
    print("\n" + "=" * 124)
    print("### (3) S2 — OOS CONSEQUENCE OF EVERY PICK CHANGE (2017-2026, untouched)\n")
    look = G.set_index(CELL + ["param"])
    swaps = []
    for _, rec in P.iterrows():
        keys = tuple(rec[c] for c in CELL)
        spy = refs[rec["universe"]][0]
        for y in IS_YEARS:
            a, b = rec["pick_full"], rec[f"pick_ex{y}"]
            if str(a) == str(b):
                continue
            ra, rb = look.loc[keys + (a,)], look.loc[keys + (b,)]
            swaps.append(dict(zip(CELL, keys), dropped=y, pick_full=a, pick_ex=b,
                              dOOS_Sharpe=rb["OOS_Sharpe"] - ra["OOS_Sharpe"],
                              dOOS_CAGR=rb["OOS_CAGR"] - ra["OOS_CAGR"],
                              dOOS_MaxDD=rb["OOS_MaxDD"] - ra["OOS_MaxDD"],
                              d4b=int(rb["4b"]) - int(ra["4b"]),
                              d4b_oos=int(rb["4b_oos"]) - int(ra["4b_oos"])))
    S = pd.DataFrame(swaps)
    S.to_csv(OUT.with_suffix(".swaps.csv"), index=False)
    if len(S):
        print(fmt(S.set_index(CELL + ["dropped"])))
        print("\n--- POOLED OOS EFFECT OF THE SWAP, BY DROPPED YEAR")
        agg = S.groupby("dropped").agg(n=("dOOS_Sharpe", "size"),
                                       mean_dOOS_Sharpe=("dOOS_Sharpe", "mean"),
                                       worse_count=("dOOS_Sharpe", lambda s: int((s < 0).sum())),
                                       mean_dOOS_CAGR=("dOOS_CAGR", "mean"),
                                       mean_dOOS_MaxDD=("dOOS_MaxDD", "mean"),
                                       net_d4b=("d4b", "sum"), net_d4b_oos=("d4b_oos", "sum"))
        print(fmt(agg))
        print(f"\n  ALL swaps pooled: n={len(S)} mean dOOS Sharpe {S.dOOS_Sharpe.mean():+.3f}, "
              f"worse in {(S.dOOS_Sharpe < 0).sum()}/{len(S)}, net 4b {int(S.d4b.sum()):+d}, "
              f"net 4b_oos {int(S.d4b_oos.sum()):+d}")
    else:
        print("  no pick changed under any single-year deletion — rule 8's pick is fully LOYO-stable")

    # ============================================================ (4) S3 G survival
    print("\n" + "=" * 124)
    print("### (4) S3 — DOES THE GAP G = d(IS) - d(OOS) SURVIVE DELETING A YEAR OF THE IS WINDOW?\n")
    deltas = []
    for keys, sub in G.groupby(CELL, sort=False):
        nullrow = sub[sub.is_null].iloc[0]
        for _, r in sub[~sub.is_null].iterrows():
            rec = dict(zip(CELL, keys), param=r["param"], apriori=r["apriori"],
                       dGross=r["Gross"] - nullrow["Gross"],
                       d_OOS=r["OOS_Sharpe"] - nullrow["OOS_Sharpe"])
            rec["d_IS_full"] = r["IS_Sharpe_full"] - nullrow["IS_Sharpe_full"]
            rec["G_full"] = rec["d_IS_full"] - rec["d_OOS"]
            for y in IS_YEARS:
                rec[f"d_IS_ex{y}"] = r[f"IS_Sharpe_ex{y}"] - nullrow[f"IS_Sharpe_ex{y}"]
                rec[f"G_ex{y}"] = rec[f"d_IS_ex{y}"] - rec["d_OOS"]
            rec["measured"] = "defensive" if rec["dGross"] < -1e-6 else (
                "offensive" if rec["dGross"] > 1e-6 else "neutral-gross")
            deltas.append(rec)
    D = pd.DataFrame(deltas)
    D.to_csv(OUT.with_suffix(".deltas.csv"), index=False)
    print(f"[deltas] {len(D)} non-null grid points (idea 99 reported 164)")

    def gsum(col, sub):
        return dict(n=len(sub), mean_G=sub[col].mean(), median_G=sub[col].median(),
                    frac_neg=float((sub[col] < 0).mean()))

    rows = []
    for label, col in [("full IS (idea 99 control)", "G_full")] + [(f"ex-{y}", f"G_ex{y}") for y in IS_YEARS]:
        a = gsum(col, D)
        b = gsum(col, D[D.grid != "crypto"])
        rows.append(dict(window=label, n=a["n"], mean_G=a["mean_G"], median_G=a["median_G"],
                         frac_neg=a["frac_neg"], mean_G_excrypto=b["mean_G"],
                         frac_neg_excrypto=b["frac_neg"]))
    GS = pd.DataFrame(rows).set_index("window")
    print("\n--- POOLED G BY IS WINDOW")
    print(fmt(GS))

    gfull = float(D["G_full"].mean())
    surv = {}
    for y in IS_YEARS:
        m, f = float(D[f"G_ex{y}"].mean()), float((D[f"G_ex{y}"] < 0).mean())
        surv[y] = bool(m < 0 and f > 0.50 and abs(m) >= 0.5 * abs(gfull))
    print("\n--- PRE-REGISTERED G-SURVIVAL TEST, BY DROPPED YEAR")
    print(pd.Series(surv, name="G_survives").to_frame().to_string())
    print(f"  G(full IS) mean {gfull:+.3f} (idea 99: {IDEA99_G['ALL']:+.3f}); "
          f"ex-{FOCUS_YEAR} mean {D[f'G_ex{FOCUS_YEAR}'].mean():+.3f} -> "
          f"SURVIVES: {surv[FOCUS_YEAR]}")

    print("\n--- G BY GRID, FULL IS vs EX-2013 (idea 99's per-grid values quoted)")
    per = D.groupby("grid").agg(n=("G_full", "size"), G_full=("G_full", "mean"),
                                G_ex2013=(f"G_ex{FOCUS_YEAR}", "mean"))
    per["idea99"] = [IDEA99_G.get(g, np.nan) for g in per.index]
    per["shift_ex2013"] = per["G_ex2013"] - per["G_full"]
    print(fmt(per))

    print("\n--- G BY MEASURED LABEL, FULL IS vs EX-2013")
    perm = D.groupby("measured").agg(n=("G_full", "size"), G_full=("G_full", "mean"),
                                     G_ex2013=(f"G_ex{FOCUS_YEAR}", "mean"),
                                     frac_neg_full=("G_full", lambda s: (s < 0).mean()),
                                     frac_neg_ex=(f"G_ex{FOCUS_YEAR}", lambda s: (s < 0).mean()))
    print(fmt(perm))

    print("\n--- LEVERAGE: how far each dropped year moves pooled mean G")
    lev = pd.DataFrame({"mean_G": [D[f"G_ex{y}"].mean() for y in IS_YEARS],
                        "shift_vs_full": [D[f"G_ex{y}"].mean() - gfull for y in IS_YEARS]},
                       index=IS_YEARS).sort_values("shift_vs_full")
    print(fmt(lev))

    # ============================================================ (5) S4 premise check
    print("\n" + "=" * 124)
    print("### (5) S4 — PREMISE: is 2013 really the worst calendar year for overlays?\n")
    peryear = []
    for keys, sub in G.groupby(CELL, sort=False):
        nullrow = sub[sub.is_null].iloc[0]
        for _, r in sub[~sub.is_null].iterrows():
            for y in range(2010, 2027):
                peryear.append(dict(universe=keys[0], grid=keys[1], year=y,
                                    d=r[f"SH_y_{y}"] - nullrow[f"SH_y_{y}"]))
    PY = pd.DataFrame(peryear)
    tab = PY.pivot_table(index="year", columns="universe", values="d", aggfunc="mean")
    tab["all"] = PY.groupby("year")["d"].mean()
    tab["n"] = PY.groupby("year")["d"].size()
    print(fmt(tab))
    worst = tab["all"].idxmin()
    print(f"\n  worst year for overlays (pooled mean d): {worst} ({tab['all'].min():+.3f}); "
          f"2013 = {tab['all'].get(2013, float('nan')):+.3f}, rank "
          f"{int(tab['all'].rank().get(2013, -1))} of {len(tab)} (1 = worst)")
    PY.to_csv(OUT.with_suffix(".peryear.csv"), index=False)

    print("\n--- IS-window years ranked by pooled mean d (the years rule 8 actually sees)")
    isy = tab.loc[[y for y in IS_YEARS if y in tab.index], "all"].sort_values()
    print(isy.to_string(float_format=lambda x: f"{x:+.3f}"))

    # ============================================================ (6) walk-forward (rule 8)
    print("\n" + "=" * 124)
    print("### (6) PROTOCOL RULE 8 WALK-FORWARD — the pick from full IS and from IS-ex-2013,")
    print("###     both evaluated on the UNTOUCHED 2017-2026 window, vs RULES v1 and SPY\n")
    wf = []
    for _, rec in P.iterrows():
        keys = tuple(rec[c] for c in CELL)
        tag = rec["universe"]
        spy, bgr, bto, _ = refs[tag]
        base = full_row(net(bgr, bto, rec["cost_bps"]))
        for lbl, p in [("full", rec["pick_full"]), (f"ex{FOCUS_YEAR}", rec[f"pick_ex{FOCUS_YEAR}"])]:
            r = look.loc[keys + (p,)]
            wf.append(dict(zip(CELL, keys), IS_window=lbl, pick=p,
                           CAGR=r["CAGR"], Sharpe=r["Sharpe"], MaxDD=r["MaxDD"],
                           H1=r["H1"], H2=r["H2"],
                           OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"], OOS_MaxDD=r["OOS_MaxDD"],
                           SPY_Sharpe=spy["Sharpe"], SPY_OOS_Sharpe=spy["OOS_Sharpe"],
                           SPY_OOS_CAGR=spy["OOS_CAGR"], SPY_OOS_MaxDD=spy["OOS_MaxDD"],
                           base_Sharpe=base["Sharpe"], base_OOS_Sharpe=base["OOS_Sharpe"],
                           keep_4a=bool(r["4a"]), keep_4b=bool(r["4b"]), keep_4b_oos=bool(r["4b_oos"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    print(fmt(WF.set_index(CELL + ["IS_window"])[
        ["pick", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "keep_4a", "keep_4b", "keep_4b_oos"]]))

    print("\n--- KEEP-PATH COUNTS ACROSS THE 44 CELLS, BY IS WINDOW")
    kc = WF.groupby("IS_window").agg(n=("keep_4a", "size"), pass_4a=("keep_4a", "sum"),
                                     pass_4b=("keep_4b", "sum"), pass_4b_oos=("keep_4b_oos", "sum"),
                                     mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
                                     mean_OOS_CAGR=("OOS_CAGR", "mean"),
                                     mean_OOS_MaxDD=("OOS_MaxDD", "mean"))
    print(fmt(kc))

    print("\n--- HEADLINE CELL: sleeve / u56 / top20 / 10 bps (the standing KEEP-4b candidate's cell)")
    h = WF[(WF.universe == "u56") & (WF.grid == "sleeve") & (WF.book == "top20") & (WF.cost_bps == 10)]
    print(fmt(h.set_index("IS_window").drop(columns=CELL)))
    hs = G[(G.universe == "u56") & (G.grid == "sleeve") & (G.book == "top20") & (G.cost_bps == 10)]
    print("\n  its IS Sharpe by window (the number rule 8 maximises):")
    print(fmt(hs.set_index("param")[["IS_Sharpe_full"] + [f"IS_Sharpe_ex{y}" for y in IS_YEARS]]))

    # ============================================================ (7) verdict
    print("\n" + "=" * 124)
    print("### (7) VERDICT\n")
    print(f"  S1 pick stability   : 2013 moves {c13}/44 cells; median year {med:.1f}; "
          f"pre-registered claim {verdict_s1}")
    if len(S):
        s13 = S[S.dropped == FOCUS_YEAR]
        print(f"  S2 OOS cost of 2013 : n={len(s13)} swaps, mean dOOS Sharpe "
              f"{s13.dOOS_Sharpe.mean():+.3f}, net 4b {int(s13.d4b.sum()):+d}"
              if len(s13) else "  S2 OOS cost of 2013 : no swaps to price")
    print(f"  S3 G survival       : mean G full {gfull:+.3f} -> ex-2013 "
          f"{D[f'G_ex{FOCUS_YEAR}'].mean():+.3f}, survives = {surv[FOCUS_YEAR]}; "
          f"survives for {sum(surv.values())}/{len(surv)} dropped years")
    print(f"  S4 premise          : worst overlay year = {worst}; 2013 rank "
          f"{int(tab['all'].rank().get(2013, -1))} of {len(tab)}")
    print(f"\n[outputs] {OUT.name}.grid.csv .picks.csv .swaps.csv .deltas.csv .peryear.csv .walkforward.csv")


if __name__ == "__main__":
    main()
