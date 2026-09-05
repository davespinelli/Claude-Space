#!/usr/bin/env python3
"""QUEUE idea 109 (filed as a second "104") — CAGR-floor-constrained-rule-8-selector
(cloud, 2026-09-05).

Question (as worded in QUEUE.md)
--------------------------------
"idea 100 (both runs) found rule 8's IS-Sharpe selector picks f=0.50 on the S4 sleeve while only
f=0.25 passes 4b, because the selector optimises Sharpe and 4b's binding bar is the CAGR floor.
Idea 101 fixes this one arm by fixing gross; the general question is the selector.  Pre-register
'maximise IS Sharpe subject to IS CAGR >= 70% of SPY's IS CAGR' and re-run it across every
overlay grid already on the leaderboard (crypto, band, breadth gate, stop, sleeve): does the
constrained selector pick better arms out of sample, or is it just a third dial?"

PRE-REGISTERED SELECTORS (declared before any number is computed)
----------------------------------------------------------------
  S_sharpe   argmax IS Sharpe                                   <- PROTOCOL rule 8 as written
  S_floor    argmax IS Sharpe s.t. IS CAGR >= 0.70 * SPY IS CAGR <- the queue's proposal
  S_cagr     argmax IS CAGR                                     <- control: is S_floor just a
                                                                   CAGR tilt in disguise?
  S_null     the no-overlay point (overlay parameter = 0)        <- control: does ANY selection
                                                                   beat not selecting?
IS = 2009..2016-12-31.  OOS = 2017-01-01..end, never touched by any selector.
Tie-break in every selector: the SMALLEST overlay parameter, so no selector gets a free pass
from an arbitrary argmax order.
Infeasibility rule (pre-registered): if no grid point meets S_floor's constraint, S_floor takes
the point with the highest IS CAGR.  Cells where this fires are counted and reported separately.

TUNED (2, per PROTOCOL rule 4): the selector (4 levels) x the overlay parameter (4-5 levels per
grid).  Everything else -- universe, base book, cost, which overlay -- is a reported control and
is never selected on.  ALL grid points are written to .grid.csv and printed.

OVERLAY GRIDS (all five the queue names, plus the gross lever, which is the leaderboard's sixth)
------------------------------------------------------------------------------------------------
  sleeve   f in {0,.25,.50,.75,1.00} of the S4 sleeve (idea 100/101), gross-renormalised to 1.00
  band     200d gate with a hysteresis band of {0,2,3,5,8}% (idea 57)
  breadth  cut book gross by {0,.25,.50,.75,1.00} when % of names above their 200d MA < 30%
           (ideas 40/41; B pre-set at 30%, not tuned)
  stop     per-name trailing stop at {none,25,20,15,10}% off the 126d high (idea 9)
  crypto   BTC/ETH carve-out at {0,2,5,10}% of gross (idea 5) -- u56 ONLY, see caveat
  gross    static gross lever g in {0.50,0.75,1.00,1.25} (ideas 66/84)
Each grid is run on 2 base books (top20, ewall) x 2 universes (u56, broad) x 2 cost rungs
(10, 25 bps), weekly cadence.

CRYPTO CAVEAT: BTC-USD starts 2014-09-17 and ETH-USD later, so the crypto grid's IS window
(2009-2016) contains barely two years of crypto.  That is a property of the grid the leaderboard
actually ran, not a choice made here; it is reported and the crypto rows are excluded from the
headline pooled statistic as well as included, both shown.

Both KEEP paths evaluated for every pick: 4a (Sharpe > RULES v1 in both halves, MaxDD no worse)
and 4b (Sharpe > SPY in both halves and OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's).

SURVIVORSHIP: both equity panels are current constituents of their lists; equity levels are
biased up.  The bias is identical across selectors, which is what this run compares.

COST NOTE: engine.backtest applies costs as `gross - turnover * bps/1e4` with the holdings path
independent of bps, so each weight matrix is run ONCE at 0 bps and both rungs derived exactly.
Asserted at start-up.

KNOWN DATA CAVEAT (queue idea 38): data/prices*.csv are calendar-day indexed after 2014-09-17.
It hits every grid point and every selector identically.

Deterministic, standalone:
    python research/backtests/2026-09-05_cagr-floor-constrained-selector_cloud.py
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
FLOOR_FRAC = 0.70                 # the queue's constraint: IS CAGR >= 70% of SPY's IS CAGR
BOOK_GROSS = 0.75
S4 = ["TLT", "GLD", "DBC", "UUP"]
CRYPTO = ["BTC-USD", "ETH-USD"]
BREADTH_B = 0.30                  # pre-set, not tuned
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
OUT = Path(__file__).with_suffix("")


# ---------------------------------------------------------------- gates and books
def _band_above(px, w):
    """200d gate with hysteresis: enter above MA*(1+w), exit below MA*(1-w). w=0 -> plain 200d."""
    ma = px.rolling(200).mean()
    up = (px > ma * (1 + w))
    dn = (px < ma * (1 - w))
    st = pd.DataFrame(np.where(up, 1.0, np.where(dn, 0.0, np.nan)),
                      index=px.index, columns=px.columns)
    return st.ffill().fillna(0.0) > 0.5


def _elig(px, band=0.0, stop=None):
    """Eligibility mask: band-gated 200d trend AND vol20 < 0.60, optionally minus stopped names."""
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
    else:                                          # ewall
        w = (m & s.notna()).astype(float)
    k = w.sum(axis=1)
    return w.div(k.where(k > 0), axis=0).fillna(0.0) * gross


# ---------------------------------------------------------------- sleeve (idea 18 variant B)
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


# ---------------------------------------------------------------- the six overlay grids
def overlay(px, kind, grid, p, crypto_px=None):
    """Return the weight matrix for base book `kind` with overlay `grid` at parameter `p`."""
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
    "gross":   [0.75, 0.50, 1.00, 1.25],          # first entry = the incumbent = "no overlay"
}
NULL_P = {"sleeve": 0.00, "band": 0.00, "breadth": 0.00, "stop": None,
          "crypto": 0.00, "gross": 0.75}


def pkey(grid, p):
    """Ordering key used for the pre-registered smallest-parameter tie-break."""
    if grid == "stop":
        return 0.0 if p is None else 1.0 - p          # None (no stop) is smallest, then 25,20,15,10
    if grid == "gross":
        return abs(p - 0.75)                           # incumbent is smallest
    return float(p)


# ---------------------------------------------------------------- metrics
def net(gr, to, bps):
    return gr - to * bps / 1e4


def stats(r):
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


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
    """4b evaluated on the OOS window ALONE -- the honest test of a selector's pick."""
    return bool(r["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and r["OOS_MaxDD"] >= 0.60 * spy["OOS_MaxDD"]
                and r["OOS_CAGR"] >= 0.70 * spy["OOS_CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


# ---------------------------------------------------------------- selectors
def select(sub, how, floor):
    """sub: DataFrame of grid points for one cell.  Returns the chosen row (a Series)."""
    s = sub.sort_values("pkey")
    if how == "S_null":
        return s[s["is_null"]].iloc[0]
    if how == "S_cagr":
        return s.loc[[s["IS_CAGR"].idxmax()]].iloc[0]
    if how == "S_sharpe":
        return s.loc[[s["IS_Sharpe"].idxmax()]].iloc[0]
    if how == "S_floor":
        ok = s[s["IS_CAGR"] >= floor]
        if len(ok) == 0:
            r = s.loc[[s["IS_CAGR"].idxmax()]].iloc[0].copy()
            r["infeasible"] = True
            return r
        r = ok.loc[[ok["IS_Sharpe"].idxmax()]].iloc[0].copy()
        r["infeasible"] = False
        return r
    raise ValueError(how)


SELECTORS = ["S_sharpe", "S_floor", "S_cagr", "S_null"]


# ---------------------------------------------------------------- main
def main():
    u56 = load_universe(exclude=set())          # keeps BTC/ETH so the crypto grid can run
    broad = load_universe(broad=True)
    universes = {"u56": u56, "broad": broad}
    print(f"[data] u56 {u56.shape[1]} cols (incl. {[t for t in CRYPTO if t in u56.columns]}), "
          f"broad {broad.shape[1]} cols")
    print(f"[pre-registered] selectors {SELECTORS} · floor = {FLOOR_FRAC:.0%} of SPY IS CAGR · "
          f"IS <= {IS_END} · OOS >= {SPLIT} · tie-break = smallest overlay parameter\n")

    # cost-linearity assertion
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
        spy = full_row(px["SPY"].pct_change().fillna(0).loc[start:])
        bt = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        bgr, bto = bt["returns"].loc[start:], bt["turnover"].loc[start:]
        refs[tag] = (spy, bgr, bto)
        print("=" * 122)
        print(f"### UNIVERSE {tag}: {px.shape[1]} tickers | eval {start.date()} -> {px.index[-1].date()}")
        print(fmt(pd.DataFrame({"RULES v1 (10bps)": full_row(net(bgr, bto, 10)), "SPY": spy}).T))
        print(f"IS CAGR floor for S_floor = {FLOOR_FRAC:.0%} x SPY IS CAGR "
              f"{spy['IS_CAGR']:.2%} = {FLOOR_FRAC * spy['IS_CAGR']:.2%}")

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
                        row = full_row(net(gr, to, bps))
                        base = full_row(net(bgr, bto, bps))
                        row.update(universe=tag, grid=grid, book=kind,
                                   param=("none" if p is None else p), cost_bps=bps,
                                   Gross=gross, Turn_yr=turn,
                                   pkey=pkey(grid, p), is_null=(p == NULL_P[grid]))
                        row["4a"] = keep_4a(row, base)
                        row["4b"] = keep_4b(row, spy)
                        row["4b_oos"] = keep_4b_oos(row, spy)
                        records.append(row)

    G = pd.DataFrame(records)
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    print(f"\n[grid] {len(G)} points -> {OUT.name}.grid.csv")

    # ------------------------------------------------------------ (1) every grid, printed
    print("\n" + "=" * 122)
    print("### (1) EVERY GRID POINT (10 bps shown; 25 bps in .grid.csv)\n")
    for (tag, grid, kind), sub in G[G.cost_bps == 10].groupby(["universe", "grid", "book"], sort=False):
        print(f"--- {tag} | grid={grid} | book={kind}")
        print(fmt(sub.set_index("param")[["Gross", "Turn_yr", "CAGR", "Sharpe", "MaxDD",
                                          "IS_CAGR", "IS_Sharpe", "OOS_CAGR", "OOS_Sharpe",
                                          "OOS_MaxDD", "4a", "4b", "4b_oos"]]))
        print()

    # ------------------------------------------------------------ (2) the selector census
    print("=" * 122)
    print("### (2) THE SELECTOR CENSUS — each selector's pick per cell, and its OOS outcome\n")
    picks = []
    for (tag, grid, kind, bps), sub in G.groupby(["universe", "grid", "book", "cost_bps"], sort=False):
        spy, _, _ = refs[tag]
        floor = FLOOR_FRAC * spy["IS_CAGR"]
        best_oos = sub["OOS_Sharpe"].max()
        for how in SELECTORS:
            r = select(sub, how, floor)
            picks.append(dict(universe=tag, grid=grid, book=kind, cost_bps=bps, selector=how,
                              param=r["param"], IS_Sharpe=r["IS_Sharpe"], IS_CAGR=r["IS_CAGR"],
                              OOS_CAGR=r["OOS_CAGR"], OOS_Sharpe=r["OOS_Sharpe"],
                              OOS_MaxDD=r["OOS_MaxDD"], CAGR=r["CAGR"], Sharpe=r["Sharpe"],
                              MaxDD=r["MaxDD"],
                              regret=r["OOS_Sharpe"] - best_oos,
                              full_4a=bool(r["4a"]), full_4b=bool(r["4b"]),
                              oos_4b=bool(r["4b_oos"]),
                              infeasible=bool(r.get("infeasible", False)),
                              spy_OOS_Sharpe=spy["OOS_Sharpe"], spy_OOS_CAGR=spy["OOS_CAGR"]))
    P = pd.DataFrame(picks)
    P.to_csv(OUT.with_suffix(".picks.csv"), index=False)
    print(fmt(P.set_index(["universe", "grid", "book", "cost_bps", "selector"])[
        ["param", "IS_Sharpe", "IS_CAGR", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
         "regret", "full_4b", "oos_4b", "infeasible"]]))

    # ------------------------------------------------------------ (3) does the constraint bind?
    print("\n" + "=" * 122)
    print("### (3) DOES THE CONSTRAINT EVER BIND?  If S_floor == S_sharpe everywhere it is not a dial.\n")
    piv = P.pivot_table(index=["universe", "grid", "book", "cost_bps"], columns="selector",
                        values="param", aggfunc="first")
    same = (piv["S_floor"].astype(str) == piv["S_sharpe"].astype(str))
    print(piv.assign(floor_eq_sharpe=same).to_string())
    ncell = len(piv)
    print(f"\nS_floor picks the SAME point as S_sharpe in {int(same.sum())}/{ncell} cells "
          f"({same.mean():.0%}); it differs in {int((~same).sum())}.")
    inf = P[(P.selector == 'S_floor') & P.infeasible]
    print(f"S_floor's constraint was INFEASIBLE (no grid point clears the floor) in "
          f"{len(inf)}/{ncell} cells: "
          f"{sorted(set(zip(inf.universe, inf.grid, inf.book))) if len(inf) else 'none'}")

    # ------------------------------------------------------------ (4) the headline comparison
    print("\n" + "=" * 122)
    print("### (4) OUT-OF-SAMPLE OUTCOME BY SELECTOR (2017-2026, never touched by any selector)\n")
    for label, sel in (("ALL grids", P), ("excl. crypto (short IS window)", P[P.grid != "crypto"])):
        agg = sel.groupby("selector").agg(
            n=("param", "size"), OOS_Sharpe=("OOS_Sharpe", "mean"), OOS_CAGR=("OOS_CAGR", "mean"),
            OOS_MaxDD=("OOS_MaxDD", "mean"), regret=("regret", "mean"),
            full_4b=("full_4b", "sum"), oos_4b=("oos_4b", "sum"),
            beats_SPY_OOS=("OOS_Sharpe", lambda s: int((s.values > sel.loc[s.index, "spy_OOS_Sharpe"].values).sum())),
            OOS_CAGR_floor_met=("OOS_CAGR", lambda s: int((s.values >= FLOOR_FRAC * sel.loc[s.index, "spy_OOS_CAGR"].values).sum())),
        ).reindex(SELECTORS)
        print(f"--- {label}")
        print(fmt(agg))
        print()

    # paired, cell by cell
    print("Paired comparison S_floor - S_sharpe, cell by cell (same cell, same grid):")
    key = ["universe", "grid", "book", "cost_bps"]
    a = P[P.selector == "S_floor"].set_index(key)
    b = P[P.selector == "S_sharpe"].set_index(key)
    D = pd.DataFrame({"dOOS_Sharpe": a["OOS_Sharpe"] - b["OOS_Sharpe"],
                      "dOOS_CAGR": a["OOS_CAGR"] - b["OOS_CAGR"],
                      "dOOS_MaxDD": a["OOS_MaxDD"] - b["OOS_MaxDD"],
                      "d4b": a["full_4b"].astype(int) - b["full_4b"].astype(int),
                      "d4b_oos": a["oos_4b"].astype(int) - b["oos_4b"].astype(int),
                      "differs": (a["param"].astype(str) != b["param"].astype(str))})
    D.to_csv(OUT.with_suffix(".paired.csv"))
    print(fmt(D))
    d = D[D["differs"]]
    print(f"\nAcross ALL {len(D)} cells: mean dOOS_Sharpe {D.dOOS_Sharpe.mean():+.4f}, "
          f"dOOS_CAGR {D.dOOS_CAGR.mean():+.4%}, dOOS_MaxDD {D.dOOS_MaxDD.mean():+.4%}; "
          f"S_floor better OOS Sharpe in {int((D.dOOS_Sharpe > 0).sum())}, worse in "
          f"{int((D.dOOS_Sharpe < 0).sum())}, tied in {int((D.dOOS_Sharpe == 0).sum())}")
    if len(d):
        print(f"Restricted to the {len(d)} cells where the two selectors DIFFER: "
              f"mean dOOS_Sharpe {d.dOOS_Sharpe.mean():+.4f}, dOOS_CAGR {d.dOOS_CAGR.mean():+.4%}, "
              f"dOOS_MaxDD {d.dOOS_MaxDD.mean():+.4%}; better in {int((d.dOOS_Sharpe > 0).sum())}, "
              f"worse in {int((d.dOOS_Sharpe < 0).sum())}")
        print(f"4b pass count moved by {int(d.d4b.sum()):+d} (full sample) and "
              f"{int(d.d4b_oos.sum()):+d} (OOS-only) across those cells")
        print("\nThe differing cells in full:")
        print(fmt(d))

    # per-grid breakdown — where, if anywhere, the constraint earns its keep
    print("\nPer-grid mean dOOS (S_floor - S_sharpe):")
    print(fmt(D.groupby(level="grid")[["dOOS_Sharpe", "dOOS_CAGR", "dOOS_MaxDD"]].mean()
              .join(D.groupby(level="grid")["differs"].sum().rename("n_differ"))))

    # ------------------------------------------------------------ (5) the queue's own example
    print("\n" + "=" * 122)
    print("### (5) THE MOTIVATING CASE — the sleeve grid, where idea 100 saw the mismatch\n")
    s = P[(P.grid == "sleeve")]
    print(fmt(s.set_index(["universe", "book", "cost_bps", "selector"])[
        ["param", "IS_Sharpe", "IS_CAGR", "CAGR", "Sharpe", "MaxDD",
         "OOS_CAGR", "OOS_Sharpe", "full_4b", "oos_4b"]]))

    # ------------------------------------------------------------ (6) is it just a third dial?
    print("\n" + "=" * 122)
    print("### (6) IS IT JUST A THIRD DIAL?\n")
    print("A selector is a dial if it (a) changes the pick often and (b) does not improve OOS.")
    print(f"  (a) S_floor differs from rule 8 in {int((~same).sum())}/{ncell} cells")
    print(f"  (b) mean OOS Sharpe: " + ", ".join(
        f"{k} {P[P.selector == k].OOS_Sharpe.mean():.3f}" for k in SELECTORS))
    print(f"      mean OOS CAGR  : " + ", ".join(
        f"{k} {P[P.selector == k].OOS_CAGR.mean():.2%}" for k in SELECTORS))
    print(f"      OOS-only 4b passes: " + ", ".join(
        f"{k} {int(P[P.selector == k].oos_4b.sum())}/{ncell}" for k in SELECTORS))
    print(f"      full-sample 4b passes: " + ", ".join(
        f"{k} {int(P[P.selector == k].full_4b.sum())}/{ncell}" for k in SELECTORS))
    print(f"      mean regret vs the best OOS point in each grid: " + ", ".join(
        f"{k} {P[P.selector == k].regret.mean():+.3f}" for k in SELECTORS))
    print("\nDone.")


if __name__ == "__main__":
    main()
