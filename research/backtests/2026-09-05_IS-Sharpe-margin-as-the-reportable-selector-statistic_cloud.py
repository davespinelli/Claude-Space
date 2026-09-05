#!/usr/bin/env python3
"""QUEUE idea 114 — IS-Sharpe-margin-as-the-reportable-selector-statistic (cloud, 2026-09-05).

Question (as worded in QUEUE.md)
--------------------------------
"idea 112 found rule 8's pick moves in 20.5% of 352 cell-year deletions and that those swaps are
OOS-negative (-0.014 mean Sharpe), i.e. the IS surface is flat and noisy rather than wrong.
Measure the IS Sharpe MARGIN at the pick (best minus runner-up) in all 44 cells and test whether
margin predicts LOYO pick stability and OOS regret; if it does, PROTOCOL rule 8 should quote the
margin next to every walk-forward."

WHY IT MATTERS
--------------
Rule 8 reports a single picked parameter and its OOS numbers.  It never reports how much better
that pick was than the runner-up on the in-sample window it was chosen on.  If the margin is
informative, it is a free confidence interval on every walk-forward the project has published,
computable from numbers each run already has.  If it is not, rule 8's output stays a point estimate
with no attached confidence and the proposal must be withdrawn — which is the result this run is
equally willing to report.

THE HARNESS (identical construction to ideas 99/109/112 so every number is comparable)
---------------------------------------------------------------------------------------
  6 overlay grids  sleeve (S4 fraction), band (200d hysteresis), breadth (gross cut), stop
                   (trailing), crypto (u56 only), gross (static lever)
  x 2 base books   top20 (ranked, gross 0.75), ewall (equal-weight all eligible, gross 0.75)
  x 2 universes    u56 (research/universe.json + BTC/ETH), broad (universe_broad.json)
  x 2 cost rungs   10 and 25 bps, weekly rebalance, next-day execution (engine)
  = 44 CELLS (u56 6 grids x 2 books + broad 5 grids x 2 books = 22, x 2 cost rungs).

STATISTICS, DECLARED BEFORE ANY NUMBER IS COMPUTED
---------------------------------------------------
Windows.  IS = [eval start .. 2016-12-31].  OOS = [2017-01-01 .. end], NEVER used for any pick.
          IS_ex_y = IS with calendar year y deleted, y in 2009..2016 (2009 partial).

M  MARGIN (the proposed statistic).  For a cell, order the grid's points by IS Sharpe.
       M      = IS_Sharpe(best) - IS_Sharpe(runner-up)          [raw, in Sharpe units]
       M_norm = M / stdev(IS Sharpe over all points in the cell) [scale-free variant]
   Both are reported everywhere; M is the PRIMARY, because a statistic PROTOCOL quotes should be
   in the units of the thing it qualifies.

S  LOYO PICK STABILITY (idea 112's S1, per cell rather than pooled).
       S = (# of the 8 IS_ex_y windows whose argmax differs from the full-IS argmax) / 8.
   Hypothesis H1: larger margin -> lower S.  Pre-registered direction: Spearman(M,S) < 0.

R  OOS REGRET.  R = max_p OOS_Sharpe(p) - OOS_Sharpe(pick).  R >= 0 by construction; it is what
   rule 8 gave up by picking on IS instead of knowing the future.
   Hypothesis H2: larger margin -> lower regret.  Pre-registered direction: Spearman(M,R) < 0.

C  LOYO SWAP COST (secondary).  Mean over the 8 dropped years of
       OOS_Sharpe(pick_ex_y) - OOS_Sharpe(pick_full),  = 0 for years that do not swap.
   Idea 112's pooled value is -0.014.  A margin that predicts S should also predict |C|.

PRE-REGISTERED DECISION RULE (fixed before the first number is computed)
-------------------------------------------------------------------------
The 44 cells are NOT independent: each (universe, grid, book) appears at both cost rungs and the
two rungs share the same gross series.  So the PRIMARY test is the 22 cells at 10 bps; the 44-cell
pooled version and the 22 cells at 25 bps are reported as supporting evidence.

    ADOPT (recommend PROTOCOL rule 8 quote the margin) iff, on the 22 primary cells,
        Spearman(M, S) <= -0.30 with permutation p < 0.05   AND
        Spearman(M, R) <= -0.30 with permutation p < 0.05   AND
        both signs replicate (rho < 0) on the 25 bps rung.
    PARTIAL  iff exactly one of the two hypotheses clears its bar and replicates.
    WITHDRAW otherwise — the margin is not a usable confidence statistic and rule 8 keeps
        reporting a bare point estimate.

Permutation p: 10,000 label shuffles of M against the statistic, seed 114, one-sided in the
hypothesised direction.  Deterministic.

USE TEST (reported whatever the verdict).  Split the primary cells at the MEDIAN margin and
compare mean S, mean R and mean |C| in the high- and low-margin halves.  A statistic PROTOCOL
quotes has to separate cells in a way a reader can act on, not merely correlate.

TUNED (2, per PROTOCOL rule 4): the overlay parameter (4-5 levels per grid) x the dropped year
(8 levels + the no-drop control).  ALL grid points are reported, in the console and in .grid.csv.
The margin, stability and regret statistics have no free parameters; the -0.30 / p<0.05 bars are
pre-registered above and are not moved.

WALK-FORWARD (PROTOCOL rule 8, mandatory).  Every cell's full-IS pick is carried into the untouched
2017-2026 window: OOS CAGR / Sharpe / MaxDD against RULES v1 and SPY, plus full-sample
CAGR/Sharpe/MaxDD/halves and BOTH KEEP paths (4a beat-the-book, 4b capital-worthy).  Each row now
also carries its margin, so the walk-forward table is exactly what the proposal asks PROTOCOL to
print.  The standing KEEP-4b candidate's cell (sleeve / u56 / top20 / 10 bps) is printed in full.

CAVEATS
-------
SURVIVORSHIP: both equity panels are current constituents of their lists; levels are biased up.
  The bias is identical across every window and every cell, which is all this run compares.
CRYPTO: BTC-USD starts 2014-09-17, so the crypto grid's IS window is short; crypto cells are
  reported inside and outside every pooled statistic.
DATA (queue idea 38): data/prices*.csv are calendar-day indexed after 2014-09-17; weekend rows are
  zero-return.  It hits every grid point and every window identically.
SHARPE ON A SPLICED SERIES: deleting a year's rows leaves mean/std well defined (idea 89's
  convention); MaxDD is never taken on a spliced series.
44 cells is a small sample for a correlation; the permutation test prices exactly that, and a
  rho that clears -0.30 on 22 points still has a wide interval.  Stated, not hidden.

Deterministic, standalone (no network; reads the committed price caches):
    python research/backtests/2026-09-05_IS-Sharpe-margin-as-the-reportable-selector-statistic_cloud.py
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
PRIMARY_BPS = 10
IS_END = "2016-12-31"
SPLIT = "2017-01-01"
BOOK_GROSS = 0.75
S4 = ["TLT", "GLD", "DBC", "UUP"]
CRYPTO = ["BTC-USD", "ETH-USD"]
BREADTH_B = 0.30
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
IS_YEARS = list(range(2009, 2017))
RHO_BAR = -0.30
P_BAR = 0.05
NPERM = 10000
SEED = 114
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- gates and books (idea 112 verbatim)
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


def _rank(a):
    a = np.asarray(a, float)
    order = a.argsort(kind="mergesort")
    r = np.empty(len(a), float)
    r[order] = np.arange(1, len(a) + 1, dtype=float)
    # average ties
    s = pd.Series(a)
    return s.rank(method="average").to_numpy()


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 4:
        return np.nan, np.nan, int(m.sum())
    rx, ry = _rank(x[m]), _rank(y[m])
    if rx.std() == 0 or ry.std() == 0:
        return np.nan, np.nan, int(m.sum())
    return float(np.corrcoef(rx, ry)[0, 1]), None, int(m.sum())


def perm_p(x, y, rho, seed=SEED, n=NPERM, side="less"):
    """One-sided permutation p for Spearman rho in the pre-registered direction."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 4 or not np.isfinite(rho):
        return np.nan
    rx, ry = _rank(x), _rank(y)
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n):
        pr = rng.permutation(ry)
        r = np.corrcoef(rx, pr)[0, 1]
        if (r <= rho) if side == "less" else (r >= rho):
            hits += 1
    return (hits + 1) / (n + 1)


# ---------------------------------------------------------------- main
def main():
    u56 = load_universe(exclude=set())
    broad = load_universe(broad=True)
    universes = {"u56": u56, "broad": broad}
    print(f"[data] u56 {u56.shape[1]} cols, broad {broad.shape[1]} cols")
    print("[pre-registered] M = IS Sharpe(best) - IS Sharpe(runner-up) at the rule-8 pick")
    print("[pre-registered] H1 Spearman(M, LOYO pick-change rate) < 0;  H2 Spearman(M, OOS regret) < 0")
    print(f"[pre-registered] ADOPT iff BOTH rho <= {RHO_BAR} with permutation p < {P_BAR} on the")
    print(f"                 {PRIMARY_BPS} bps cells AND both signs replicate at 25 bps; else PARTIAL/WITHDRAW.")
    print(f"[pre-registered] IS = ..{IS_END}, OOS = {SPLIT}.. (never used for any pick)\n")

    # cost linearity (every point is run once at 0 bps and both rungs derived exactly)
    st0 = u56.index[260]
    w0 = book(u56, "top20")
    r0 = backtest(u56, w0, cost_bps=0.0, freq=FREQ)
    err = float((net(r0["returns"].loc[st0:], r0["turnover"].loc[st0:], 10)
                 - backtest(u56, w0, cost_bps=10, freq=FREQ)["returns"].loc[st0:]).abs().max())
    print(f"[check] cost linearity max |derived - direct| at 10 bps = {err:.2e}")
    assert err < 1e-12

    records, refs = [], {}
    for tag, px in universes.items():
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy = full_row(spy_r)
        bt = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        bgr, bto = bt["returns"].loc[start:], bt["turnover"].loc[start:]
        refs[tag] = (spy, bgr, bto)
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
                        row = full_row(r)
                        base = full_row(net(bgr, bto, bps))
                        row.update(universe=tag, grid=grid, book=kind,
                                   param=("none" if p is None else p), cost_bps=bps,
                                   Gross=gross, Turn_yr=turn, pkey=pkey(grid, p),
                                   is_null=(p == NULL_P[grid]))
                        isr = r.loc[:IS_END]
                        row["IS_Sharpe_full"] = sharpe(isr)
                        for y in IS_YEARS:
                            row[f"IS_Sharpe_ex{y}"] = sharpe(isr[isr.index.year != y])
                        row["4a"] = keep_4a(row, base)
                        row["4b"] = keep_4b(row, spy)
                        row["4b_oos"] = keep_4b_oos(row, spy)
                        records.append(row)

    G = pd.DataFrame(records)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print(f"\n[grid] {len(G)} points -> {OUT.name}.grid.csv")

    CELL = ["universe", "grid", "book", "cost_bps"]
    print(f"[cells] {G.groupby(CELL, sort=False).ngroups} cells (expected 44)")

    # ============================================================ (1) every grid point
    print("\n" + "=" * 124)
    print("### (1) EVERY GRID POINT — IS Sharpe (what rule 8 maximises) and its OOS consequence")
    print("###     10 bps shown; 25 bps in .grid.csv\n")
    for (tag, grid, kind), sub in G[G.cost_bps == PRIMARY_BPS].groupby(["universe", "grid", "book"], sort=False):
        print(f"--- {tag} | grid={grid} | book={kind}")
        cols = ["Gross", "Turn_yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                "IS_Sharpe_full", "OOS_Sharpe", "OOS_CAGR", "OOS_MaxDD", "4a", "4b"]
        print(fmt(sub.set_index("param")[cols]))
        print()

    # ============================================================ (2) M, S, R, C per cell
    def pick_on(sub, col):
        s = sub[[col, "pkey", "param"]].dropna(subset=[col])
        if s.empty:
            return None
        best = s[col].max()
        tied = s[np.isclose(s[col], best)]
        return tied.sort_values("pkey").iloc[0]["param"]

    look = G.set_index(CELL + ["param"])
    rows = []
    for keys, sub in G.groupby(CELL, sort=False):
        d = dict(zip(CELL, keys))
        vals = sub["IS_Sharpe_full"].dropna().sort_values(ascending=False)
        p_full = pick_on(sub, "IS_Sharpe_full")
        margin = float(vals.iloc[0] - vals.iloc[1]) if len(vals) > 1 else np.nan
        sd = float(sub["IS_Sharpe_full"].std())
        rec = dict(d, n_points=len(sub), pick=p_full,
                   IS_best=float(vals.iloc[0]) if len(vals) else np.nan,
                   IS_runnerup=float(vals.iloc[1]) if len(vals) > 1 else np.nan,
                   M=margin, IS_sd=sd, M_norm=(margin / sd if sd and sd > 0 else np.nan))
        # S: LOYO pick stability
        chg, swap_d = 0, []
        for y in IS_YEARS:
            py = pick_on(sub, f"IS_Sharpe_ex{y}")
            if str(py) != str(p_full):
                chg += 1
                swap_d.append(look.loc[keys + (py,)]["OOS_Sharpe"]
                              - look.loc[keys + (p_full,)]["OOS_Sharpe"])
            else:
                swap_d.append(0.0)
            rec[f"pick_ex{y}"] = py
        rec["n_changed"] = chg
        rec["S"] = chg / len(IS_YEARS)
        rec["C"] = float(np.mean(swap_d))
        rec["absC"] = abs(rec["C"])
        # R: OOS regret
        pr = look.loc[keys + (p_full,)]
        rec["OOS_Sharpe_pick"] = float(pr["OOS_Sharpe"])
        rec["OOS_Sharpe_best"] = float(sub["OOS_Sharpe"].max())
        rec["R"] = rec["OOS_Sharpe_best"] - rec["OOS_Sharpe_pick"]
        rec["pick_is_OOS_best"] = bool(np.isclose(rec["R"], 0.0))
        rows.append(rec)
    K = pd.DataFrame(rows)
    K.to_csv(OUT.with_suffix(".cells.csv"), index=False)

    print("=" * 124)
    print("### (2) PER-CELL: MARGIN M, LOYO STABILITY S, OOS REGRET R, SWAP COST C — ALL 44 CELLS\n")
    show = ["pick", "IS_best", "IS_runnerup", "M", "M_norm", "n_changed", "S",
            "OOS_Sharpe_pick", "OOS_Sharpe_best", "R", "C"]
    print(fmt(K.sort_values(["cost_bps", "universe", "grid", "book"]).set_index(CELL)[show]))
    print(f"\n  pooled: mean M {K.M.mean():.3f} (median {K.M.median():.3f}, max {K.M.max():.3f}), "
          f"mean S {K.S.mean():.3f}, mean R {K.R.mean():.3f}, mean C {K.C.mean():+.4f}")
    print(f"  rule 8's pick was also the OOS-best point in {int(K.pick_is_OOS_best.sum())}/{len(K)} cells")
    print(f"  idea 112 cross-check — pooled LOYO change rate {K.n_changed.sum()}/{len(K)*8} = "
          f"{K.n_changed.sum()/(len(K)*8):.3f} (idea 112 reported 20.5% of 352)")

    # ============================================================ (3) the two hypotheses
    print("\n" + "=" * 124)
    print("### (3) DOES THE MARGIN PREDICT ANYTHING? (pre-registered one-sided permutation tests)\n")
    tests = []
    for lbl, sub in [(f"PRIMARY  {PRIMARY_BPS} bps (22 cells)", K[K.cost_bps == PRIMARY_BPS]),
                     ("support  25 bps (22 cells)", K[K.cost_bps == 25]),
                     ("support  pooled (44 cells)", K),
                     (f"support  {PRIMARY_BPS} bps ex-crypto", K[(K.cost_bps == PRIMARY_BPS) & (K.grid != "crypto")])]:
        for xn, x in [("M", sub.M), ("M_norm", sub.M_norm)]:
            for yn, y in [("S (LOYO change rate)", sub.S), ("R (OOS regret)", sub.R),
                          ("|C| (swap cost)", sub.absC)]:
                rho, _, n = spearman(x, y)
                tests.append(dict(sample=lbl, x=xn, y=yn, n=n, rho=rho,
                                  p_one_sided=perm_p(x, y, rho) if np.isfinite(rho) else np.nan))
    T = pd.DataFrame(tests)
    T.to_csv(OUT.with_suffix(".tests.csv"), index=False)
    print(fmt(T.set_index(["sample", "x", "y"])))

    prim = K[K.cost_bps == PRIMARY_BPS]
    sec = K[K.cost_bps == 25]
    rho_S, _, _ = spearman(prim.M, prim.S)
    rho_R, _, _ = spearman(prim.M, prim.R)
    p_S = perm_p(prim.M, prim.S, rho_S)
    p_R = perm_p(prim.M, prim.R, rho_R)
    rho_S25, _, _ = spearman(sec.M, sec.S)
    rho_R25, _, _ = spearman(sec.M, sec.R)
    h1 = bool(np.isfinite(rho_S) and rho_S <= RHO_BAR and p_S < P_BAR and rho_S25 < 0)
    h2 = bool(np.isfinite(rho_R) and rho_R <= RHO_BAR and p_R < P_BAR and rho_R25 < 0)
    verdict = "ADOPT" if (h1 and h2) else ("PARTIAL" if (h1 or h2) else "WITHDRAW")
    print(f"\n  H1 Spearman(M,S) = {rho_S:+.3f} (p {p_S:.4f}), 25bps replication {rho_S25:+.3f} -> {'PASS' if h1 else 'FAIL'}")
    print(f"  H2 Spearman(M,R) = {rho_R:+.3f} (p {p_R:.4f}), 25bps replication {rho_R25:+.3f} -> {'PASS' if h2 else 'FAIL'}")
    print(f"  PRE-REGISTERED VERDICT: {verdict}")

    # ============================================================ (4) use test
    print("\n" + "=" * 124)
    print("### (4) USE TEST — split the primary cells at the median margin\n")
    med_M = float(prim.M.median())
    hi, lo = prim[prim.M >= med_M], prim[prim.M < med_M]
    UT = pd.DataFrame([
        dict(half="high margin", n=len(hi), mean_M=hi.M.mean(), mean_S=hi.S.mean(),
             mean_R=hi.R.mean(), mean_absC=hi.absC.mean(),
             frac_pick_OOS_best=hi.pick_is_OOS_best.mean()),
        dict(half="low margin", n=len(lo), mean_M=lo.M.mean(), mean_S=lo.S.mean(),
             mean_R=lo.R.mean(), mean_absC=lo.absC.mean(),
             frac_pick_OOS_best=lo.pick_is_OOS_best.mean()),
    ]).set_index("half")
    print(fmt(UT))
    print(f"\n  median margin = {med_M:.3f} Sharpe. Separation high-minus-low: "
          f"S {hi.S.mean()-lo.S.mean():+.3f}, R {hi.R.mean()-lo.R.mean():+.3f}, "
          f"|C| {hi.absC.mean()-lo.absC.mean():+.4f}")

    print("\n--- MARGIN BY GRID (is the margin a property of the cell or of the instrument?)")
    print(fmt(prim.groupby("grid").agg(n=("M", "size"), mean_M=("M", "mean"),
                                       mean_S=("S", "mean"), mean_R=("R", "mean"))))

    # ============================================================ (5) walk-forward (rule 8)
    print("\n" + "=" * 124)
    print("### (5) PROTOCOL RULE 8 WALK-FORWARD — every cell's full-IS pick on the UNTOUCHED")
    print("###     2017-2026 window, vs RULES v1 and SPY, WITH THE MARGIN ALONGSIDE\n")
    wf = []
    for _, rec in K.iterrows():
        keys = tuple(rec[c] for c in CELL)
        spy, bgr, bto = refs[rec["universe"]]
        base = full_row(net(bgr, bto, rec["cost_bps"]))
        r = look.loc[keys + (rec["pick"],)]
        wf.append(dict(zip(CELL, keys), pick=rec["pick"], M=rec["M"], S=rec["S"], R=rec["R"],
                       CAGR=r["CAGR"], Sharpe=r["Sharpe"], MaxDD=r["MaxDD"], H1=r["H1"], H2=r["H2"],
                       OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"], OOS_MaxDD=r["OOS_MaxDD"],
                       base_Sharpe=base["Sharpe"], base_OOS_Sharpe=base["OOS_Sharpe"],
                       SPY_Sharpe=spy["Sharpe"], SPY_OOS_Sharpe=spy["OOS_Sharpe"],
                       SPY_OOS_CAGR=spy["OOS_CAGR"], SPY_OOS_MaxDD=spy["OOS_MaxDD"],
                       keep_4a=bool(r["4a"]), keep_4b=bool(r["4b"]), keep_4b_oos=bool(r["4b_oos"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)
    print(fmt(WF.set_index(CELL)[["pick", "M", "S", "R", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                                  "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
                                  "keep_4a", "keep_4b", "keep_4b_oos"]]))
    print("\n--- KEEP-PATH COUNTS ACROSS THE 44 CELLS, BY COST RUNG")
    print(fmt(WF.groupby("cost_bps").agg(n=("keep_4a", "size"), pass_4a=("keep_4a", "sum"),
                                         pass_4b=("keep_4b", "sum"), pass_4b_oos=("keep_4b_oos", "sum"),
                                         mean_OOS_Sharpe=("OOS_Sharpe", "mean"))))
    print("\n--- DOES THE MARGIN SEPARATE THE CELLS THAT PASS 4b?")
    print(fmt(WF[WF.cost_bps == PRIMARY_BPS].groupby("keep_4b").agg(
        n=("M", "size"), mean_M=("M", "mean"), mean_S=("S", "mean"), mean_R=("R", "mean"),
        mean_OOS_Sharpe=("OOS_Sharpe", "mean"))))

    print("\n--- HEADLINE CELL: sleeve / u56 / top20 / 10 bps (the standing KEEP-4b candidate's cell)")
    h = WF[(WF.universe == "u56") & (WF.grid == "sleeve") & (WF.book == "top20") & (WF.cost_bps == PRIMARY_BPS)]
    print(fmt(h.set_index("pick").drop(columns=CELL)))
    hs = G[(G.universe == "u56") & (G.grid == "sleeve") & (G.book == "top20") & (G.cost_bps == PRIMARY_BPS)]
    print("\n  its IS Sharpe by grid point (the surface rule 8 maximises):")
    print(fmt(hs.set_index("param")[["IS_Sharpe_full", "OOS_Sharpe", "CAGR", "Sharpe", "MaxDD"]]))

    # ============================================================ (6) verdict
    print("\n" + "=" * 124)
    print("### (6) VERDICT\n")
    print(f"  margin distribution : mean {K.M.mean():.3f}, median {K.M.median():.3f}, "
          f"IQR {K.M.quantile(0.25):.3f}-{K.M.quantile(0.75):.3f}, max {K.M.max():.3f} Sharpe")
    print(f"  H1 margin -> stability : rho {rho_S:+.3f} p {p_S:.4f} (bar {RHO_BAR}, p<{P_BAR}) -> {'PASS' if h1 else 'FAIL'}")
    print(f"  H2 margin -> regret    : rho {rho_R:+.3f} p {p_R:.4f} (bar {RHO_BAR}, p<{P_BAR}) -> {'PASS' if h2 else 'FAIL'}")
    print(f"  use test               : high-margin half mean R {hi.R.mean():.3f} vs low {lo.R.mean():.3f}, "
          f"mean S {hi.S.mean():.3f} vs {lo.S.mean():.3f}")
    print(f"  PRE-REGISTERED VERDICT : {verdict}")
    print(f"\n[outputs] {OUT.name}.grid.csv .cells.csv .tests.csv .walkforward.csv")


if __name__ == "__main__":
    main()
