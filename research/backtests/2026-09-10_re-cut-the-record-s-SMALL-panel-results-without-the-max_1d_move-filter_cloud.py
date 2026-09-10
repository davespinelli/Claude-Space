#!/usr/bin/env python3
"""Idea 627 — re-cut the record's SMALL-panel results without the max_1d_move filter.

Idea 623 PART B found that `data/small_meta.csv`'s `max_1d_move` is a FULL-SAMPLE max of
|daily return| and that the record's SMALL panel is defined by dropping the 44 names with
max_1d_move >= 1.0 -- a statistic dated at the END of the sample, applied from day one, in
298 of 560 committed rule-8 files.  This script prices that screen.

TWO TUNED PARAMETERS, and no more (PROTOCOL 4):
  FILTER form   in {TERMINAL, OFF, CAUSAL}
  BOOK          in a pre-registered 7-book slice of the record's SMALL-panel headline books

  TERMINAL = the record's convention: drop the 44 names with max_1d_move >= 1.0 from day one
             (a terminal-dated screen, the object under test).
  OFF      = keep all 483 names, always.
  CAUSAL   = at every date t a name is eligible iff its EXPANDING max |1d return| observed
             up to and including t is < 1.0.  Same threshold, same statistic, honest dating:
             a name is held right up to its 100% day and dropped from the next rebalance on.

Everything else is PROTOCOL-fixed: weekly cadence, weights decided at close t and applied at
t+1 (engine convention), 10 bps per unit turnover, gross 0.75, no shorting, no leverage.
Rule 8 walk-forward is run on every filter form: the BOOK is chosen on 2010-2016 IS Sharpe
alone and 2017-2026 is read exactly once.

SURVIVORSHIP CAVEAT (stated, not fixed): data/prices_small.csv is the CURRENT constituent
list of a sub-$2B screen, so the whole panel is a survivor set before any filter is applied.
Removing max_1d_move does not make the panel clean -- it removes ONE undeclared terminal-dated
screen from a panel that still has a large declared one.  No level claim from this file should
be read as an achievable return.

Run:  python3 research/backtests/2026-09-10_re-cut-...-filter_cloud.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, band_state, score  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, rebalance_mask, metrics  # noqa

pd.set_option("display.width", 220)
FREQ, COST, GROSS, NTOP = "W", 10.0, 0.75, 20
IS_END, OOS_START = "2016-12-31", "2017-01-01"
OUT = Path(__file__).with_suffix("")


# ------------------------------------------------------------------ fast engine + its gate
def fast_backtest(prices, weights, freq=FREQ):
    """(gross returns at 0 bps, turnover); costs via r(c) = r(0) - turnover*c/1e4.
    Gate G1 checks this against a live engine.backtest run."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy(); m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]; W0 = wt[s0]
    h = W0 * (Cp / Cp[s0]); V = h.sum(axis=1) + (1.0 - W0.sum(axis=1)); held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]; W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p]); Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1)); heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T); turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1), index=idx), pd.Series(turn, index=idx)


def net(gross_r, turn, cost=COST):
    return gross_r - turn * cost / 1e4


# ------------------------------------------------------------------ panel + the three filters
PX_ALL = load_universe(small=True)                      # 483 small caps + an SPY benchmark column
SPY = PX_ALL["SPY"]
PANEL = PX_ALL.drop(columns=["SPY"])
META = pd.read_csv(ROOT / "data" / "small_meta.csv")
TERM_BAD = sorted(set(META.loc[META.max_1d_move >= 1.0, "ticker"]) & set(PANEL.columns))

_absret = PANEL.pct_change().abs()
_expmax = _absret.expanding().max()                     # max |1d ret| observed up to and incl. t


def elig_mask(filter_form):
    """Boolean DataFrame: is name j tradeable on day t under this filter form?"""
    priced = PANEL.notna()
    if filter_form == "OFF":
        return priced
    if filter_form == "TERMINAL":
        keep = pd.Series(True, index=PANEL.columns); keep[TERM_BAD] = False
        return priced & keep
    if filter_form == "CAUSAL":
        return priced & (_expmax.fillna(0.0) < 1.0)
    raise ValueError(filter_form)


FILTERS = ["TERMINAL", "OFF", "CAUSAL"]
ELIG = {f: elig_mask(f) for f in FILTERS}


# ------------------------------------------------------------------ the 7-book slice
# Pre-registered before any result was read: these are the SMALL-panel books the record's
# headline rows are built from (top-20 equal weight is the 2026-09-04 KEEP 4b family).
def _topn(sig, elig, n=NTOP, gross=GROSS):
    s = sig.where(elig)
    rank = s.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    return sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * gross


def book_weights(book, elig):
    px = PANEL
    if book == "CAND20":                 # scan.py composite, WITH the vol scaler
        s, above, vol20 = score(px, vol_scale=True)
        return _topn(s.where(above), elig)
    if book == "CAND20_NOVOL":           # the 2026-09-04 KEEP 4b family: no vol scaler
        s, above, vol20 = score(px, vol_scale=False)
        return _topn(s.where(above), elig)
    if book == "MOM20":                  # 12-1 momentum
        return _topn(px.shift(21) / px.shift(252) - 1, elig)
    if book == "R6_20":                  # 6-month return
        return _topn(px / px.shift(126) - 1, elig)
    if book == "LOWVOL20":               # lowest realised 20d vol
        v = px.pct_change().rolling(20).std()
        return _topn(-v, elig)
    if book == "EWALL":                  # equal weight every eligible name
        e = elig.astype(float)
        return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS
    if book == "MABAND":                 # RULES v2's band clause, run on the panel
        e = elig.astype(float)
        ew = e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * GROSS
        return ew.where(band_state(px, 0.03), 0.0)
    raise ValueError(book)


BOOKS = ["CAND20", "CAND20_NOVOL", "MOM20", "R6_20", "LOWVOL20", "EWALL", "MABAND"]

START = PANEL.index[260]                                # same warm-up skip as baseline.compare


def legs(r):
    r = r.loc[START:]
    h = len(r) // 2
    full, h1, h2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    oos = metrics(r.loc[OOS_START:]); ins = metrics(r.loc[:IS_END])
    return dict(CAGR=full["CAGR"], Sharpe=full["Sharpe"], MaxDD=full["MaxDD"],
                H1=h1["Sharpe"], H2=h2["Sharpe"], IS=ins["Sharpe"],
                OOS_CAGR=oos["CAGR"], OOS=oos["Sharpe"], OOS_DD=oos["MaxDD"])


# ------------------------------------------------------------------ comparands
BASE = net(*fast_backtest(PX_ALL, rules_v2_weights(PX_ALL)))          # RULES v2, live book
BASE_V1 = net(*fast_backtest(PX_ALL, rules_v1_weights(PX_ALL)))
SPY_R = SPY.pct_change().fillna(0.0)
L_BASE, L_V1, L_SPY = legs(BASE), legs(BASE_V1), legs(SPY_R)


def legs_4b(L, Ls=L_SPY):
    """Which 4b bars this arm fails (SET semantics, per idea 529: every failing leg, not the
    first).  Reported so that 'the verdict did not move' can be read against a margin."""
    f = []
    if not L["H1"] > Ls["H1"]: f.append("H1")
    if not L["H2"] > Ls["H2"]: f.append("H2")
    if not L["OOS"] > Ls["OOS"]: f.append("OOS")
    if not L["MaxDD"] >= 0.60 * Ls["MaxDD"]: f.append("DD")
    if not L["CAGR"] >= 0.70 * Ls["CAGR"]: f.append("CAGR")
    return f


def verdict(L, Lb=L_BASE, Ls=L_SPY):
    """PROTOCOL 4a / 4b, both priced on every arm."""
    a = (L["H1"] > Lb["H1"]) and (L["H2"] > Lb["H2"]) and (L["MaxDD"] >= Lb["MaxDD"])
    b = not legs_4b(L, Ls)
    return ("KEEP-4a" if a else "") + ("+" if a and b else "") + ("KEEP-4b" if b else "") or "KILL"


# ------------------------------------------------------------------ G1: fast == engine
def gate_g1():
    w = book_weights("CAND20_NOVOL", ELIG["TERMINAL"])
    fr, ft = fast_backtest(PX_ALL.drop(columns=["SPY"]), w)
    eng = backtest(PANEL, w, cost_bps=0.0, freq=FREQ)
    dr = float((fr.loc[START:] - eng["returns"].loc[START:]).abs().max())
    dt_ = float((ft.loc[START:] - eng["turnover"].loc[START:]).abs().max())
    print(f"G1 fast_backtest vs engine.backtest on CAND20_NOVOL/TERMINAL: "
          f"max|dret| {dr:.3e}  max|dturnover| {dt_:.3e}")
    assert dr < 1e-10 and dt_ < 1e-10, "G1 FAILED"
    return dr, dt_


# ------------------------------------------------------------------ run
def main():
    print(__doc__.split("Run:")[0])
    gate_g1()

    print(f"\nPanel: {PANEL.shape[1]} names, {PANEL.index[0].date()} -> {PANEL.index[-1].date()}; "
          f"evaluation from {START.date()}.  TERMINAL drops {len(TERM_BAD)} names.")
    nel = pd.DataFrame({f: ELIG[f].sum(axis=1) for f in FILTERS})
    print("Mean eligible names/day: " + ", ".join(f"{f} {nel[f].mean():.1f}" for f in FILTERS))
    first_hit = (_expmax >= 1.0).idxmax().where((_expmax >= 1.0).any())
    hits = first_hit.dropna()
    print(f"CAUSAL: {len(hits)} names ever cross 1.0; median first-crossing date "
          f"{pd.Timestamp(hits.sort_values().iloc[len(hits)//2]).date()}; "
          f"{(hits <= pd.Timestamp(IS_END)).sum()} cross inside the IS window.")

    rows, curves = [], {}
    for book in BOOKS:
        for f in FILTERS:
            r = net(*fast_backtest(PX_ALL.drop(columns=["SPY"]), book_weights(book, ELIG[f])))
            curves[(book, f)] = r
            L = legs(r)
            L.update(book=book, filt=f, verdict=verdict(L),
                     fail4b="/".join(legs_4b(L)) or "-",
                     ddmargin=L["MaxDD"] - 0.60 * L_SPY["MaxDD"])
            rows.append(L)
    G = pd.DataFrame(rows).set_index(["book", "filt"])
    cols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS", "OOS_CAGR", "OOS", "OOS_DD",
            "fail4b", "ddmargin", "verdict"]
    print("\n=== ALL 21 GRID POINTS (full sample, 10 bps, weekly, t+1, gross 0.75) ===")
    print(G[cols].to_string(float_format=lambda x: f"{x:.3f}"))
    print("\ncomparands:")
    print(pd.DataFrame({"RULES v2 (live)": L_BASE, "RULES v1": L_V1, "SPY": L_SPY}).T
          .to_string(float_format=lambda x: f"{x:.3f}"))

    # ---- how many published verdicts move?
    print("\n=== DOES THE FILTER MOVE THE VERDICT? (TERMINAL is the record's convention) ===")
    mv = []
    for book in BOOKS:
        t = G.loc[(book, "TERMINAL")]
        for f in ["OFF", "CAUSAL"]:
            o = G.loc[(book, f)]
            mv.append(dict(book=book, alt=f, v_term=t["verdict"], v_alt=o["verdict"],
                           moved=t["verdict"] != o["verdict"],
                           f4b_term=t["fail4b"], f4b_alt=o["fail4b"],
                           legs_moved=t["fail4b"] != o["fail4b"],
                           dSharpe=o["Sharpe"] - t["Sharpe"], dCAGR=o["CAGR"] - t["CAGR"],
                           dMaxDD=o["MaxDD"] - t["MaxDD"], dOOS=o["OOS"] - t["OOS"]))
    MV = pd.DataFrame(mv)
    print(MV.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    for f in ["OFF", "CAUSAL"]:
        sub = MV[MV.alt == f]
        print(f"  {f}: verdict moves in {int(sub.moved.sum())} of {len(sub)} books, "
              f"the 4b FAIL-SET moves in {int(sub.legs_moved.sum())} of {len(sub)}; "
              f"median dSharpe {sub.dSharpe.median():+.4f}, median dCAGR {sub.dCAGR.median():+.4%}, "
              f"median dMaxDD {sub.dMaxDD.median():+.4%}, median dOOS Sharpe {sub.dOOS.median():+.4f}")

    # ---- rule 8: choose the book on IS Sharpe alone, read OOS once, under each filter
    print("\n=== RULE 8 WALK-FORWARD: book chosen on 2010-2016 IS Sharpe, 2017-2026 read once ===")
    wf = []
    for f in FILTERS:
        sub = G.xs(f, level="filt")
        pick = sub["IS"].idxmax()
        L = sub.loc[pick]
        wf.append(dict(filt=f, pick=pick, IS_Sharpe=L["IS"], OOS_CAGR=L["OOS_CAGR"],
                       OOS_Sharpe=L["OOS"], OOS_MaxDD=L["OOS_DD"],
                       oracle=sub["OOS"].idxmax(), oracle_OOS=sub["OOS"].max()))
    WF = pd.DataFrame(wf)
    print(WF.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print(f"  OOS comparands: SPY CAGR {L_SPY['OOS_CAGR']:.2%} Sharpe {L_SPY['OOS']:.3f} "
          f"MaxDD {L_SPY['OOS_DD']:.2%} | RULES v2 CAGR {L_BASE['OOS_CAGR']:.2%} "
          f"Sharpe {L_BASE['OOS']:.3f} MaxDD {L_BASE['OOS_DD']:.2%}")
    npick = WF["pick"].nunique()
    print(f"  The rule-8 PICK is {'THE SAME' if npick == 1 else 'DIFFERENT'} under the three "
          f"filter forms ({npick} distinct picks); OOS Sharpe spread across forms "
          f"{WF.OOS_Sharpe.max() - WF.OOS_Sharpe.min():+.4f}.")

    # ---- what the 44 terminal-dropped names actually did
    drop_r = PANEL[TERM_BAD].pct_change()
    keepset = [c for c in PANEL.columns if c not in TERM_BAD]
    print(f"\nThe 44 terminal-dropped names: mean daily ret {drop_r.stack().mean():+.6f} vs "
          f"{PANEL[keepset].pct_change().stack().mean():+.6f} for the 439 kept; "
          f"mean daily vol {drop_r.stack().std():.4f} vs {PANEL[keepset].pct_change().stack().std():.4f}.")

    G.to_csv(OUT.with_name(OUT.name + ".grid.csv"))
    MV.to_csv(OUT.with_name(OUT.name + ".moves.csv"), index=False)
    WF.to_csv(OUT.with_name(OUT.name + ".walkforward.csv"), index=False)
    print(f"\nwrote {OUT.name}.grid.csv / .moves.csv / .walkforward.csv")


if __name__ == "__main__":
    main()
