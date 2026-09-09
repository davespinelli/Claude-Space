#!/usr/bin/env python3
"""Idea 312 (lane B, 2026-09-09) - is-the-panel-ordering-an-ETF-SHARE-effect.

QUESTION
--------
Idea 51 measured the 200d-MA gate's SELECTION premium as `dSharpe(MA-RS) - dSharpe(EWall)`
at matched (gross, cadence) and found it monotone across three panels:

    U56 -0.0045  >  B136 -0.0465  >  SMALL439 -0.1023      (mean over 6 (g, cadence) points)

and the same ordering in all four filter arms.  The record has been reading that as a
"universe boundary" (large-cap vs small-cap).  But the three panels also differ in ASSET
CLASS: U56 is 36/56 = 64.3% ETFs, B136 is 36/136 = 26.5%, SMALL439 is 0%.  The ordering in
cap is the ordering in ETF share.  The queue asks: hold ETF share FIXED by building
k-matched sub-panels out of B136 at 0% / 25% / 50% (and beyond) ETF and re-measure the same
premium.  If the premium tracks s, the "universe boundary" is an ASSET-CLASS boundary; if it
is flat in s, ETF share is not the carrier and the cap reading survives this test.

DESIGN
------
Panels: k = 36 names drawn from B136 = ETF36 (universe.json broad + sectors + bonds_fx_commod
less crypto) + STK100 (the other 100 names).  n_etf = round(s*36), n_stk = 36 - n_etf, six
seeds per rung, drawn with idea 291's committed crc32 scheme `MIX|{s:.3f}|{sd}` so the panels
are the SAME objects as that run's where the rungs coincide.  k is 36 at every rung, so panel
WIDTH is never confounded with composition.

Arms (idea 51 verbatim):
    EWall  gross g spread equally over every priced tradable name          (CONTROL)
    MA-RS  gross g spread equally over names with px > 200d MA (RESPREAD)  (TREATMENT)
premium = Sharpe(MA-RS) - Sharpe(EWall) at the SAME (panel, g, cadence).  RESPREAD holds
gross fixed, so the premium is pure selection, no exposure dial.

ASSET-CLASS CONTRAST (reported, not tuned): the ETF half is drawn from three pools -
ALL36 (every ETF), EQ24 (broad + sectors, equity only) and NONEQ12 (bonds/FX/commodities).
If the ETF effect is really a bonds-and-gold effect, only the NONEQ ladder carries a slope.

PRE-REGISTERED HYPOTHESES (written before any MIX number was read)
------------------------------------------------------------------
GAP = published U56 - SMALL439 premium gap = +0.0978 Sharpe.
H_ETF  : premium is monotone non-decreasing in s over the 5 ALL36 rungs AND
         premium(s=1) - premium(s=0) >= 0.5 * GAP.  -> the panel ordering is ETF share.
H_FLAT : |premium(s=1) - premium(s=0)| < 0.25 * GAP.  -> ETF share is NOT the carrier.
H_PRED : OLS premium ~ a + b*s on the 5 ALL36 rungs, evaluated at the real panels' own
         shares (U56 0.643, B136 0.265, SMALL439 0.000), reproduces their published
         ordering AND every |residual| <= 0.03.
H_CLASS: the EQ24 ladder's slope has the same sign as ALL36's and >= 50% its magnitude.
         Failing it while NONEQ12 carries the slope makes this an asset-class effect in
         the narrow sense (duration/commodity), not "ETF" as a wrapper.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two): ETF share s and cadence {W, M}.  Gross
g in {0.50, 0.75, 1.00} is a REPORTED axis (idea 51's own by-product: on unlevered
gross-scalar books Sharpe is near-invariant in g; the span is reported here too), seed is
replication, and the ETF pool flavour is a reported contrast.  Every grid point is written
to .grid.csv and the ladders to .ladder.csv.

GATES (run before any new number is read)
    G1 reproduction: idea 51's committed `.grid.csv`, all 36 (panel x {EWall, MA-RS} x g x
       cadence) rows, rebuilt from source - CAGR, Sharpe, MaxDD, H1, H2, OOS and both
       d-columns - to 1e-9.
    G2 identity: the vectorised runner against engine.backtest on one book per panel.

RULE 8 WALK-FORWARD (required)
    IS = start..2016-12-31, OOS = 2017-01-01..end, read once.
    WF-A on the ANSWER: refit the premium ~ s slope on IS returns only and on OOS returns
       only; report sign hold and magnitude.
    WF-B on a BOOK: choose (s, cadence) by IS Sharpe of the seed-pooled MA-RS book, read
       OOS CAGR/Sharpe/MaxDD once against RULES v2 (live baseline, per panel) and SPY.

KEEP PATHS: 4a (vs the live RULES v2 book on the same panel) and 4b (vs SPY: Sharpe in both
    halves and OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's) evaluated for EVERY book.
    Stated up front: a MIX panel is a seeded random draw of 36 names, NOT a rule anyone can
    trade, so a 4b pass here is a diagnostic, not a capital candidate.

SURVIVORSHIP: universe_broad.json is CURRENT constituents, so the STOCK end of every ladder
    carries a survivorship premium the ETF end structurally cannot.  That bias pushes the
    stock end's LEVEL up; its effect on the MA-gate PREMIUM (an arm-minus-arm difference on
    the same panel) largely cancels, but it is restated beside the headline.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py; modifies nothing but its
own outputs: .grid.csv .ladder.csv .predict.csv .chars.csv .walkforward.csv .keeppaths.csv
.console.txt
"""
from __future__ import annotations
import json, sys, time, zlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, rules_v1_weights  # noqa
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics, rebalance_mask  # noqa

STAMP = Path(__file__).name[:-3]
OUT = Path(__file__).resolve().parent
COST = 10.0
GROSS = [0.50, 0.75, 1.00]
CADENCE = ["W", "M"]
MA_WIN = 200
IS_END, OOS_START = "2016-12-31", "2017-01-01"
K_MIX = 36
SEEDS = [0, 1, 2, 3, 4, 5]
SHARES_ALL = [0.000, 0.250, 0.500, 0.750, 1.000]
SHARES_EQ = [0.125, 0.250, 0.500, 0.667]
SHARES_NONEQ = [0.125, 0.250, 0.333]
GAP = 0.0978                       # published U56 - SMALL439 premium gap (idea 51)
PARENT = "2026-09-06_trend-filter-by-market-cap_B.grid.csv"
PARENT_END = "2026-09-04"          # idea 51's last bar; data/prices.csv has since grown 4 bars
G1_TOL = 1e-9
G2_TOL = 1e-12
PRED_TOL = 0.03

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


# ------------------------------------------------------------------ vectorised runner
def fast_backtest(prices, weights, cost_bps=COST, freq="W"):
    """Vectorised equivalent of engine.backtest (asserted in G2)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    mask[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
    reb = np.flatnonzero(mask)
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return {"returns": pd.Series(port, index=idx), "turnover": pd.Series(turn, index=idx)}


# ------------------------------------------------------------------------- books
def _priced(px, tradable):
    e = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    cols = [c for c in px.columns if c in tradable]
    e[cols] = px[cols].notna().astype(float)
    return e


def _ew(mask, g):
    n = mask.sum(axis=1).replace(0, np.nan)
    return g * mask.div(n, axis=0).fillna(0.0)


def above_ma(px, win=MA_WIN):
    return px > px.rolling(win).mean()


def make_books(px, tradable, g):
    """idea 51's two arms at one gross."""
    e = _priced(px, tradable) > 0
    ma = above_ma(px) & e
    return {"EWall": _ew(e, g), "MA-RS": _ew(ma, g)}


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def rowify(r, tn=None):
    m = metrics(r)
    h1, h2 = halves(r)
    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
    d = dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
             IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"],
             OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"])
    if tn is not None:
        d["turnover"] = float(tn.sum() / m["Years"])
    return d


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy):
    a1, a2 = halves(r)
    s1, s2 = halves(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not a1 > s1: f.append("H1")
    if not a2 > s2: f.append("H2")
    if not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]: f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]: f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------------- panels
def real_panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    # Truncate to idea 51's last bar so the reproduction gate and the published premia are
    # read on idea 51's OWN sample.  data/prices.csv has grown 4 bars since that run
    # (2026-09-04 -> 2026-09-08); prices_broad.csv and prices_small.csv.gz have not.
    return {
        "U56": (px56.dropna(how="all").ffill().loc[:PARENT_END], set(px56.columns)),
        "B136": (px136.dropna(how="all").ffill().loc[:PARENT_END], set(px136.columns)),
        f"SMALL{len(s_stk)}": (pxs[s_stk + ["SPY"]].dropna(how="all").ffill().loc[:PARENT_END],
                               set(s_stk)),
    }


def etf_pools(px136):
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    eq = [t for t in U["broad"] + U["sectors"] if t not in crypto and t in px136.columns]
    noneq = [t for t in U["bonds_fx_commod"] if t not in crypto and t in px136.columns]
    all36 = sorted(set(eq) | set(noneq))
    stk = sorted([t for t in px136.columns if t not in set(all36) and t != "SPY"])
    return dict(ALL36=sorted(all36), EQ24=sorted(eq), NONEQ12=sorted(noneq)), stk


def mix_panels(px136, pools, stk):
    """k-matched draws; crc32 seeding identical to idea 291 for the ALL36 flavour."""
    stk_pool = np.array(stk)
    panels, seen = {}, {}
    plan = [("ALL36", SHARES_ALL), ("EQ24", SHARES_EQ), ("NONEQ12", SHARES_NONEQ)]
    for flavour, shares in plan:
        etf_pool = np.array(pools[flavour])
        for s in shares:
            n_etf = int(round(s * K_MIX))
            n_stk = K_MIX - n_etf
            assert n_etf <= len(etf_pool), (flavour, s, n_etf, len(etf_pool))
            for sd in SEEDS:
                seed = zlib.crc32(f"MIX|{s:.3f}|{sd}".encode()) % (2 ** 32)
                rng = np.random.default_rng(seed)
                pick = []
                if n_etf:
                    pick += rng.choice(etf_pool, size=n_etf, replace=False).tolist()
                if n_stk:
                    pick += rng.choice(stk_pool, size=n_stk, replace=False).tolist()
                pick = sorted(pick)
                fs = frozenset(pick)
                if fs in seen:                      # identical composition -> one panel
                    continue
                key = f"{flavour}~s{s:.3f}~{sd}"
                seen[fs] = key
                cols = list(dict.fromkeys(pick + (["SPY"] if "SPY" in px136.columns else [])))
                panels[key] = dict(px=px136[cols].dropna(how="all").ffill(), tradable=set(pick),
                                   flavour=flavour, s=s, seed=sd, k=len(pick), n_etf=n_etf)
    return panels


def panel_chars(px, tradable, spy_r):
    """Reported covariates of composition: constituent vol, pairwise corr, MA breadth, beta."""
    cols = [c for c in px.columns if c in tradable]
    r = px[cols].pct_change()
    vol = float((r.std() * np.sqrt(252)).mean())
    C = r.corr().to_numpy()
    n = C.shape[0]
    rho = float((np.nansum(C) - n) / (n * (n - 1))) if n > 1 else np.nan
    on = above_ma(px[cols]) & px[cols].notna()
    breadth = float(on.sum(axis=1).div(px[cols].notna().sum(axis=1).replace(0, np.nan)).mean())
    ew = r.mean(axis=1).fillna(0.0)
    sp = spy_r.reindex(ew.index).fillna(0.0)
    beta = float(np.cov(ew.values, sp.values)[0, 1] / np.var(sp.values)) if np.var(sp.values) > 0 else np.nan
    return dict(cvol=vol, rho=rho, breadth=breadth, beta=beta)


def ols(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    ss = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float((resid ** 2).sum()) / ss if ss > 0 else np.nan
    return float(coef[0]), float(coef[1]), r2


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 112)
    P("IDEA 312  is-the-panel-ordering-an-ETF-SHARE-effect   (lane B, 2026-09-09)")
    P("=" * 112)
    P("Treatment = idea 51's MA-gate SELECTION premium, dSharpe(MA-RS) - dSharpe(EWall) at")
    P("matched (gross, cadence).  Composition is the axis; panel WIDTH is pinned at k = 36.")
    P("10 bps, t+1 fills, no leverage, no shorting.  GAP (published U56 - SMALL439) = %.4f" % GAP)
    P("")

    # ---------------------------------------------------------------- G1 reproduction
    P("=" * 112)
    P("G1  REPRODUCTION GATE - idea 51's committed grid.csv, 36 rows x 12 columns")
    P("=" * 112)
    panels = real_panels()
    SMALLK = [k for k in panels if k.startswith("SMALL")][0]
    ref, real_rows = {}, []
    for nm, (px, tr) in panels.items():
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        v2 = backtest(px, rules_v2_weights(px), cost_bps=COST, freq="W")["returns"].loc[st:]
        v1 = backtest(px, rules_v1_weights(px), cost_bps=COST, freq="W")["returns"].loc[st:]
        ref[nm] = dict(start=st, spy=spy, v2=v2, v1=v1)
        for g in GROSS:
            books = make_books(px, tr, g)
            for freq in CADENCE:
                res = {k: fast_backtest(px, w, COST, freq) for k, w in books.items()}
                rets = {k: v["returns"].loc[st:] for k, v in res.items()}
                mc = metrics(rets["EWall"])
                for k in books:
                    r = rets[k]
                    row = dict(panel=nm, kind="REAL", flavour="-", etf_share=np.nan, seed=-1,
                               arm=k, gross=g, cadence=freq)
                    row.update(rowify(r, res[k]["turnover"].loc[st:]))
                    row["dCAGR_vs_EWall"] = row["CAGR"] - mc["CAGR"]
                    row["dSharpe_vs_EWall"] = row["Sharpe"] - mc["Sharpe"]
                    row["keep4a"] = keep_4a(r, ref[nm]["v2"])
                    row["fail4b"] = fail_4b(r, spy)
                    row["keep4b"] = row["fail4b"] == "-"
                    real_rows.append(row)
        P(f"  {nm:9s} {px.shape[1]:4d} cols, {len(tr):4d} tradable, sample from {st.date()}  "
          f"({time.time()-t0:.0f}s)")
    REAL = pd.DataFrame(real_rows)

    par = pd.read_csv(OUT / PARENT)
    par = par[par.arm.isin(["EWall", "MA-RS"])].copy()
    cmpcols = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "IS_CAGR", "OOS_CAGR",
               "OOS_Sharpe", "OOS_MaxDD", "turnover", "dCAGR_vs_EWall", "dSharpe_vs_EWall"]
    keys = ["panel", "arm", "gross", "cadence"]
    m = REAL.merge(par, on=keys, suffixes=("", "_p"))
    assert len(m) == 36, len(m)
    diffs = {c: float(np.abs(m[c] - m[c + "_p"]).max()) for c in cmpcols}
    g1 = max(diffs.values())
    P(f"  rows matched: {len(m)}/36   max abs diff over {len(cmpcols)} columns: {g1:.3e}")
    perp = m.assign(d=np.abs(m[cmpcols].values - m[[c + '_p' for c in cmpcols]].values).max(1)) \
            .groupby("panel").d.max()
    P("  per panel: " + "  ".join(f"{k} {v:.2e}" for k, v in perp.items()))
    P("  NOTE: data/prices.csv (the U56 cache) was REVISED between idea 51's run and this one:")
    P("        against commit e02949d's copy, every shared bar moved by <= 5.09e-05 RELATIVE")
    P("        (AVGO 5.1e-5, NVDA 4.1e-5, AAPL 3.5e-5 - an adjusted-close back-revision) and")
    P("        one bar was appended (2026-09-08, truncated away above).  prices_broad.csv and")
    P("        prices_small.csv.gz are byte-identical, so B136 and SMALL439 gate at 1e-15 and")
    P("        U56 carries a residual of that revision's size.  The MIX ladder is drawn from")
    P("        B136 only, so nothing downstream touches the revised cache except SPY.")
    for pnl, tol in ((SMALLK, G1_TOL), ("B136", G1_TOL), ("U56", 1e-4)):
        assert float(perp[pnl]) < tol, f"G1 FAILED on {pnl} at {perp[pnl]:.3e} (bar {tol:.0e})"
    P("  worst columns: " + ", ".join(f"{k} {v:.2e}" for k, v in
                                      sorted(diffs.items(), key=lambda kv: -kv[1])[:4]))
    P("  G1 PASS (B136 / SMALL439 < 1e-9; U56 within the cache revision).  4a/4b flags: "
      f"4a {int((m.keep4a == m.keep4a_p).sum())}/36, 4b {int((m.keep4b == m.keep4b_p).sum())}/36")
    pub = REAL[REAL.arm == "MA-RS"].groupby("panel").dSharpe_vs_EWall.mean()
    P("  published premium re-read:  " + "  ".join(f"{k} {v:+.4f}" for k, v in pub.items()))
    gap_reread = float(pub["U56"] - pub[SMALLK])
    P(f"  U56 - {SMALLK} gap re-read: {gap_reread:+.4f}  (pre-registered GAP {GAP:.4f})")

    # ---------------------------------------------------------------- G2 identity
    P("")
    P("=" * 112)
    P("G2  IDENTITY GATE - fast_backtest vs engine.backtest")
    P("=" * 112)
    worst = 0.0
    for nm, (px, tr) in panels.items():
        w = make_books(px, tr, 0.75)["MA-RS"]
        a = fast_backtest(px, w, COST, "W")["returns"]
        b = backtest(px, w, cost_bps=COST, freq="W")["returns"]
        d = float((a - b).abs().max())
        worst = max(worst, d)
        P(f"  {nm:9s} max |dreturn| {d:.3e}")
    assert worst < G2_TOL, f"G2 FAILED at {worst:.3e}"
    P(f"  G2 PASS ({worst:.3e} < {G2_TOL:.0e})")

    # ---------------------------------------------------------------- MIX panels
    P("")
    P("=" * 112)
    P("THE LADDER - k-matched MIX sub-panels of B136 (k = 36 at every rung)")
    P("=" * 112)
    px136, tr136 = panels["B136"]
    pools, stk = etf_pools(px136)
    P(f"  pools: ALL36 {len(pools['ALL36'])}, EQ24 {len(pools['EQ24'])}, "
      f"NONEQ12 {len(pools['NONEQ12'])}, STK {len(stk)}")
    P(f"  EQ24  = {' '.join(pools['EQ24'])}")
    P(f"  NONEQ = {' '.join(pools['NONEQ12'])}")
    mix = mix_panels(px136, pools, stk)
    P(f"  panels built: {len(mix)}  (identical compositions collapse to one panel)")
    st136 = ref["B136"]["start"]
    spy136 = ref["B136"]["spy"]
    P(f"  common sample: {st136.date()} -> {px136.index[-1].date()} "
      f"(B136 warm-up skip, index[260])")

    chars, rows = [], []
    for key, d in mix.items():
        px, tr = d["px"], d["tradable"]
        c = panel_chars(px.loc[st136:], tr, spy136)
        c.update(panel=key, flavour=d["flavour"], etf_share=d["s"], seed=d["seed"], k=d["k"],
                 n_etf=d["n_etf"])
        chars.append(c)
        v2 = fast_backtest(px, rules_v2_weights(px[[c2 for c2 in px.columns if c2 in tr]])
                           .reindex(columns=px.columns).fillna(0.0), COST, "W")["returns"].loc[st136:]
        for g in GROSS:
            books = make_books(px, tr, g)
            for freq in CADENCE:
                res = {k: fast_backtest(px, w, COST, freq) for k, w in books.items()}
                rets = {k: v["returns"].loc[st136:] for k, v in res.items()}
                mc = metrics(rets["EWall"])
                for k in books:
                    r = rets[k]
                    row = dict(panel=key, kind="MIX", flavour=d["flavour"], etf_share=d["s"],
                               seed=d["seed"], arm=k, gross=g, cadence=freq)
                    row.update(rowify(r, res[k]["turnover"].loc[st136:]))
                    row["dCAGR_vs_EWall"] = row["CAGR"] - mc["CAGR"]
                    row["dSharpe_vs_EWall"] = row["Sharpe"] - mc["Sharpe"]
                    row["keep4a"] = keep_4a(r, v2)
                    row["fail4b"] = fail_4b(r, spy136)
                    row["keep4b"] = row["fail4b"] == "-"
                    rows.append(row)
    MIX = pd.DataFrame(rows)
    GRID = pd.concat([REAL, MIX], ignore_index=True)
    GRID.to_csv(OUT / f"{STAMP}.grid.csv", index=False)
    CH = pd.DataFrame(chars)
    CH.to_csv(OUT / f"{STAMP}.chars.csv", index=False)
    P(f"  books run: {len(GRID)} ({len(REAL)} real + {len(MIX)} mix)  ({time.time()-t0:.0f}s)")

    # ---------------------------------------------------------------- the ladder
    prem = MIX[MIX.arm == "MA-RS"].copy()
    lad = prem.groupby(["flavour", "etf_share", "gross", "cadence"]).dSharpe_vs_EWall.agg(
        ["mean", "std", "min", "max", "count"]).reset_index()
    lad = lad.rename(columns={"mean": "premium", "std": "sd_seed"})
    dcag = prem.groupby(["flavour", "etf_share", "gross", "cadence"]).dCAGR_vs_EWall.mean()
    lad["dCAGR"] = dcag.values
    lad.to_csv(OUT / f"{STAMP}.ladder.csv", index=False)

    P("")
    P("ALL GRID POINTS - premium = Sharpe(MA-RS) - Sharpe(EWall), mean over 6 seeds")
    for fl in ["ALL36", "EQ24", "NONEQ12"]:
        sub = lad[lad.flavour == fl]
        if sub.empty:
            continue
        pv = sub.pivot_table(index="etf_share", columns=["gross", "cadence"], values="premium")
        P(f"\n  [{fl}]  premium by (gross, cadence)")
        P("  " + fmt(pv).replace("\n", "\n  "))
        sv = sub.pivot_table(index="etf_share", columns=["gross", "cadence"], values="sd_seed")
        P(f"  [{fl}]  seed sd")
        P("  " + fmt(sv).replace("\n", "\n  "))

    P("")
    P("HEADLINE LADDER - premium averaged over the 6 (gross, cadence) points, per rung")
    head = lad.groupby(["flavour", "etf_share"]).agg(
        premium=("premium", "mean"), sd_seed=("sd_seed", "mean"),
        dCAGR=("dCAGR", "mean")).reset_index()
    P("  " + fmt(head.set_index(["flavour", "etf_share"])).replace("\n", "\n  "))

    a36 = head[head.flavour == "ALL36"].sort_values("etf_share")
    p0 = float(a36.premium.iloc[0]); p1 = float(a36.premium.iloc[-1])
    spread = p1 - p0
    mono = bool(np.all(np.diff(a36.premium.values) >= 0))
    P("")
    P(f"  ALL36:  premium(s=0) {p0:+.4f} -> premium(s=1) {p1:+.4f},  spread {spread:+.4f} "
      f"= {spread / GAP:+.2f} x GAP;  monotone non-decreasing: {mono}")
    h_etf = bool(mono and spread >= 0.5 * GAP)
    h_flat = bool(abs(spread) < 0.25 * GAP)
    P(f"  H_ETF  (monotone AND spread >= 0.5*GAP = {0.5*GAP:+.4f}): {h_etf}")
    P(f"  H_FLAT (|spread| < 0.25*GAP = {0.25*GAP:.4f}):            {h_flat}")

    # cadence split - the published ordering is mostly a cadence-W fact
    P("")
    P("  by cadence (the published ordering is far wider at W than M):")
    cad = lad[lad.flavour == "ALL36"].pivot_table(index="etf_share", columns="cadence",
                                                  values="premium")
    P("  " + fmt(cad).replace("\n", "\n  "))
    for c in CADENCE:
        v = cad[c].values
        P(f"    cadence {c}: spread {v[-1] - v[0]:+.4f} = {(v[-1]-v[0])/GAP:+.2f} x GAP, "
          f"monotone {bool(np.all(np.diff(v) >= 0))}")
    P("  gross span (Sharpe near-invariance check, ALL36): "
      f"{float(lad[lad.flavour=='ALL36'].groupby(['etf_share','cadence']).premium.agg(lambda x: x.max()-x.min()).max()):.4f} "
      "max premium range across the 3 gross rungs")

    # ------------------------------------------------------- POST-HOC: the noise floor
    P("")
    P("NOISE FLOOR (POST-HOC, not pre-registered - forced by the seed sd above)")
    P("  Per (flavour, rung, seed): premium averaged over the 6 (gross, cadence) points.")
    P("  If two 36-name draws at the SAME ETF share can differ by more than the published")
    P("  three-panel GAP, composition luck alone reproduces the published ordering.")
    seedprem = (MIX[MIX.arm == "MA-RS"]
                .groupby(["flavour", "etf_share", "seed"]).dSharpe_vs_EWall.mean())
    nf = []
    for (fl, s), grp in seedprem.groupby(level=[0, 1]):
        v = grp.values
        if len(v) < 2:
            continue
        pairs = [abs(v[i] - v[j]) for i in range(len(v)) for j in range(i + 1, len(v))]
        nf.append(dict(flavour=fl, etf_share=s, n_seed=len(v), lo=v.min(), hi=v.max(),
                       rng=v.max() - v.min(), sd=v.std(ddof=1),
                       pairs=len(pairs), pairs_ge_GAP=int(sum(p >= GAP for p in pairs)),
                       share_ge_GAP=float(np.mean([p >= GAP for p in pairs]))))
    NF = pd.DataFrame(nf)
    P("  " + fmt(NF.set_index(["flavour", "etf_share"])).replace("\n", "\n  "))
    P(f"  ACROSS ALL RUNGS: {int(NF.pairs_ge_GAP.sum())} of {int(NF.pairs.sum())} same-s seed "
      f"pairs ({NF.pairs_ge_GAP.sum() / NF.pairs.sum():.1%}) differ by more than the published "
      f"GAP of {GAP:.4f}")
    P(f"  mean within-rung seed sd {float(NF.sd.mean()):.4f} vs GAP {GAP:.4f} "
      f"(ratio {float(NF.sd.mean()) / GAP:.2f}); se of a 6-seed rung mean "
      f"{float(NF.sd.mean()) / np.sqrt(6):.4f}")
    NF.to_csv(OUT / f"{STAMP}.noisefloor.csv", index=False)

    # ---------------------------------------------------------------- H_CLASS
    P("")
    P("H_CLASS - is the slope an ETF-WRAPPER fact or a bonds/commodity fact?")
    slopes = {}
    for fl in ["ALL36", "EQ24", "NONEQ12"]:
        sub = head[head.flavour == fl].sort_values("etf_share")
        xs = sub.etf_share.values
        if fl != "ALL36":                      # splice the shared s = 0 rung (n_etf = 0)
            xs = np.concatenate([[0.0], xs])
            ys = np.concatenate([[p0], sub.premium.values])
        else:
            ys = sub.premium.values
        a, b, r2 = ols(xs, ys)
        slopes[fl] = dict(intercept=a, slope=b, r2=r2, n=len(xs),
                          lo=float(ys[0]), hi=float(ys[-1]), s_hi=float(xs[-1]))
        P(f"  {fl:8s} n={len(xs)}  premium = {a:+.4f} {b:+.4f}*s   R2 {r2:5.3f}   "
          f"range over its own support [0, {xs[-1]:.3f}]: {ys[0]:+.4f} -> {ys[-1]:+.4f}")
    h_class = bool(np.sign(slopes["EQ24"]["slope"]) == np.sign(slopes["ALL36"]["slope"])
                   and abs(slopes["EQ24"]["slope"]) >= 0.5 * abs(slopes["ALL36"]["slope"]))
    P(f"  H_CLASS (EQ24 slope same sign and >= 50% of ALL36's): {h_class}")

    # ---------------------------------------------------------------- H_PRED
    P("")
    P("H_PRED - does the MIX ladder PREDICT the three real panels' published premia?")
    a, b, r2 = slopes["ALL36"]["intercept"], slopes["ALL36"]["slope"], slopes["ALL36"]["r2"]
    real_share = {"U56": 36 / 56, "B136": 36 / 136, SMALLK: 0.0}
    pr = []
    for nm, s in real_share.items():
        pred = a + b * s
        act = float(pub[nm])
        pr.append(dict(panel=nm, etf_share=s, predicted=pred, actual=act, resid=act - pred))
    PR = pd.DataFrame(pr).sort_values("etf_share", ascending=False)
    PR.to_csv(OUT / f"{STAMP}.predict.csv", index=False)
    P("  " + fmt(PR.set_index("panel")).replace("\n", "\n  "))
    ord_ok = bool(PR.predicted.is_monotonic_decreasing and PR.actual.is_monotonic_decreasing)
    h_pred = bool(ord_ok and float(PR.resid.abs().max()) <= PRED_TOL)
    P(f"  ordering reproduced: {ord_ok};  max |residual| {float(PR.resid.abs().max()):.4f} "
      f"(bar {PRED_TOL});  H_PRED {h_pred}")
    P(f"  share of the published GAP the ladder explains: "
      f"{(b * (real_share['U56'] - real_share[SMALLK])) / gap_reread:+.2%}")

    # ---------------------------------------------------------------- covariates
    P("")
    P("WHAT ELSE MOVES WITH s (reported covariates, not instruments)")
    cc = CH.groupby(["flavour", "etf_share"])[["cvol", "rho", "breadth", "beta"]].mean()
    P("  " + fmt(cc).replace("\n", "\n  "))
    j = head.merge(CH.groupby(["flavour", "etf_share"])[["cvol", "rho", "breadth", "beta"]]
                   .mean().reset_index(), on=["flavour", "etf_share"])
    P("  univariate fits of premium on each covariate (all rungs, all flavours, n=%d):" % len(j))
    for c in ["etf_share", "cvol", "rho", "breadth", "beta"]:
        a_, b_, r2_ = ols(j[c].values, j.premium.values)
        P(f"    premium ~ {c:9s}  slope {b_:+.4f}  R2 {r2_:5.3f}")
    # the real panels' own covariates, for context
    P("  real panels for context:")
    for nm, (px, tr) in panels.items():
        c = panel_chars(px.loc[ref[nm]['start']:], tr, ref[nm]["spy"])
        P(f"    {nm:9s} etf_share {real_share[nm]:.3f}  cvol {c['cvol']:.3f}  rho {c['rho']:.3f}  "
          f"breadth {c['breadth']:.3f}  beta {c['beta']:.3f}")

    # ---------------------------------------------------------------- rule 8
    P("")
    P("=" * 112)
    P("RULE 8 WALK-FORWARD   IS <= %s, OOS >= %s (read once)" % (IS_END, OOS_START))
    P("=" * 112)
    wf = []
    # WF-A: the ANSWER refit on each window
    P("WF-A  the premium ~ s slope, refit inside each window (ALL36)")
    for win in ["FULL", "IS", "OOS"]:
        col = {"FULL": "Sharpe", "IS": "IS_Sharpe", "OOS": "OOS_Sharpe"}[win]
        sub = MIX[MIX.flavour == "ALL36"]
        piv = sub.pivot_table(index=["etf_share", "seed", "gross", "cadence"], columns="arm",
                              values=col)
        piv["prem"] = piv["MA-RS"] - piv["EWall"]
        lad_w = piv.groupby("etf_share").prem.mean()
        a_, b_, r2_ = ols(lad_w.index.values, lad_w.values)
        P(f"  {win:5s}  " + "  ".join(f"s={s:.2f} {v:+.4f}" for s, v in lad_w.items()) +
          f"   slope {b_:+.4f}  R2 {r2_:5.3f}")
        wf.append(dict(test="WF-A", window=win, slope=b_, r2=r2_,
                       lo=float(lad_w.iloc[0]), hi=float(lad_w.iloc[-1])))
    sgn = {r["window"]: np.sign(r["slope"]) for r in wf}
    P(f"  sign holds IS -> OOS: {bool(sgn['IS'] == sgn['OOS'])};  "
      f"|slope| OOS / IS = {abs(wf[2]['slope']) / abs(wf[1]['slope']):.2f}")

    # WF-B: a BOOK chosen on IS, read OOS
    P("")
    P("WF-B  book pick: (s, cadence) chosen by IS Sharpe of the seed-POOLED MA-RS book at")
    P("      g = 0.75, then read OOS once against RULES v2 (B136, live) and SPY.")
    pooled = {}
    for fl in ["ALL36"]:
        for s in SHARES_ALL:
            for freq in CADENCE:
                keys_ = [k for k, d in mix.items() if d["flavour"] == fl and abs(d["s"] - s) < 1e-9]
                rs = []
                for k in keys_:
                    px, tr = mix[k]["px"], mix[k]["tradable"]
                    w = make_books(px, tr, 0.75)["MA-RS"]
                    rs.append(fast_backtest(px, w, COST, freq)["returns"].loc[st136:])
                pooled[(s, freq)] = pd.concat(rs, axis=1).mean(axis=1)
    is_s = {k: metrics(v.loc[:IS_END])["Sharpe"] for k, v in pooled.items()}
    pick = max(is_s, key=is_s.get)
    P("  IS Sharpe by (s, cadence): " + "  ".join(f"{k[0]:.2f}/{k[1]} {v:.4f}"
                                                  for k, v in sorted(is_s.items())))
    P(f"  -> pick s = {pick[0]:.3f}, cadence {pick[1]}")
    v2b = ref["B136"]["v2"]
    v1b = ref["B136"]["v1"]
    for lbl, r in [(f"WF-B pick MA-RS s={pick[0]:.3f}/{pick[1]}", pooled[pick]),
                   ("WF-B same pick, EWall control", None),
                   ("RULES v2 (live, B136)", v2b), ("RULES v1 (B136)", v1b),
                   ("SPY", spy136)]:
        if r is None:
            rs = []
            for k, d in mix.items():
                if d["flavour"] == "ALL36" and abs(d["s"] - pick[0]) < 1e-9:
                    w = make_books(d["px"], d["tradable"], 0.75)["EWall"]
                    rs.append(fast_backtest(d["px"], w, COST, pick[1])["returns"].loc[st136:])
            r = pd.concat(rs, axis=1).mean(axis=1)
        m, mo = metrics(r), metrics(r.loc[OOS_START:])
        h1, h2 = halves(r)
        P(f"  {lbl:34s} CAGR {m['CAGR']:7.2%} Sharpe {m['Sharpe']:6.3f} MaxDD {m['MaxDD']:7.2%} "
          f"H1/H2 {h1:5.3f}/{h2:5.3f} | OOS CAGR {mo['CAGR']:7.2%} Sharpe {mo['Sharpe']:6.3f} "
          f"MaxDD {mo['MaxDD']:7.2%}")
        wf.append(dict(test="WF-B", window="book", book=lbl, CAGR=m["CAGR"], Sharpe=m["Sharpe"],
                       MaxDD=m["MaxDD"], H1=h1, H2=h2, OOS_CAGR=mo["CAGR"],
                       OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
    pd.DataFrame(wf).to_csv(OUT / f"{STAMP}.walkforward.csv", index=False)

    # ---------------------------------------------------------------- keep paths
    P("")
    P("=" * 112)
    P("BOTH KEEP PATHS - every book (PROTOCOL rule 4)")
    P("=" * 112)
    kp = GRID.groupby(["kind", "arm"]).agg(n=("Sharpe", "size"), pass4a=("keep4a", "sum"),
                                           pass4b=("keep4b", "sum")).reset_index()
    P("  " + fmt(kp.set_index(["kind", "arm"]), 0).replace("\n", "\n  "))
    P(f"  TOTAL 4a: {int(GRID.keep4a.sum())} / {len(GRID)};  "
      f"4b: {int(GRID.keep4b.sum())} / {len(GRID)}")
    bind = GRID[~GRID.keep4b].fail4b.str.split(",").explode().value_counts()
    P("  4b binding legs: " + "  ".join(f"{k} {v}" for k, v in bind.items()))
    GRID[["panel", "kind", "flavour", "etf_share", "seed", "arm", "gross", "cadence", "CAGR",
          "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "keep4a", "keep4b",
          "fail4b"]].to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    if GRID.keep4b.any():
        P("  4b passers:")
        P("  " + fmt(GRID[GRID.keep4b][["panel", "arm", "gross", "cadence", "CAGR", "Sharpe",
                                        "MaxDD", "OOS_Sharpe"]]).replace("\n", "\n  "))

    # ---------------------------------------------------------------- verdict
    P("")
    P("=" * 112)
    P("VERDICT")
    P("=" * 112)
    P(f"  H_ETF   {h_etf}    H_FLAT  {h_flat}    H_PRED  {h_pred}    H_CLASS {h_class}")
    P(f"  ALL36 ladder spread {spread:+.4f} vs published panel GAP {gap_reread:+.4f} "
      f"({spread / gap_reread:+.1%} of it)")
    P(f"  runtime {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
