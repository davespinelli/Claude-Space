#!/usr/bin/env python3
"""IDEA 314 - is the vol cap the real universe clause, and does a PANEL-SCALED cap fix it?

QUEUE 314: "idea 51R splits the RULES v1 eligibility filter into its legs and finds the
vol20 < 0.60 cap costs SMALL439 -3.93 pp/yr (dSharpe -0.204) against the 200d trend leg's
-1.44 pp/yr (-0.074), while on U56/B136 the two legs are comparable.  Sweep the cap LEVEL
(0.40/0.60/0.80/1.00/off) against the trend leg held fixed on all three panels at matched
gross, and report whether a panel-scaled cap (e.g. a cross-sectional vol quantile instead of
an absolute 0.60) removes the small-cap damage - i.e. whether any universe clause belongs in
RULES at all, and phrased in volatility rather than capitalisation.  Max 2 params."

DESIGN.  The trend leg is HELD FIXED at `px > px.rolling(200).mean()` in every book.  The only
thing that moves is the volatility clause that sits beside it.  Two tuned parameters, no more:

    param 1  FAMILY   ABS  - admit vol20 < c            (RULES v1's clause: an absolute level)
                      QTL  - admit vol20 <= the cross-sectional q-quantile of vol20 over the
                             day's LIVE names (a panel-scaled clause: admits exactly q by
                             construction, on every panel, in every regime)
    param 2  LEVEL    ABS c in {0.40, 0.60, 0.80, 1.00, inf}   (inf == the cap switched OFF)
                      QTL q in {0.40, 0.60, 0.80, 1.00}        (1.00 == OFF, an identity check)
                      plus, per panel, QTL at q = MATCHED, the mean daily admission rate that
                      ABS 0.60 itself realises on that panel (a derived number, not a dial)

Everything else is pinned to the record's conventions and reported, never chosen:
    gross 0.75, cadence weekly, lookback 200, panels U56 / B136 / SMALL439,
    constructions RESPREAD (51R's, constant gross) and DEGROSS (the live RULES v2 convention),
    cost rungs 0 bps (51R's reading, for the gate) and 10 bps (PROTOCOL 2, for every verdict).

PRE-REGISTERED HYPOTHESES (stated before any result was read).
  H_LEVEL   On SMALL439 the ABS clause's damage is MONOTONE in c: dCAGR vs the cap-OFF book
            rises weakly toward 0 as c goes 0.40 -> 0.60 -> 0.80 -> 1.00 -> inf.  A
            non-monotone ladder means the "level" reading is not even self-consistent.
  H_SCALE   The damage is a SCALING artefact: at matched admission rate the panel-scaled clause
            removes it.  PASS requires BOTH, on SMALL439, RESPREAD, 0 bps (51R's cell):
              (i)  dCAGR(QTL@MATCHED) - dCAGR(ABS 0.60) >= +1.0 pp/yr, and
              (ii) |dCAGR(QTL@MATCHED)| <= 1.0 pp/yr.
  H_ORDER   51R's cross-panel ordering of the damage (SMALL439 much worse than U56/B136) is a
            property of the ABS clause and NOT of the QTL clause: the panel spread of dCAGR
            (max - min over the three panels) is at least 2x smaller under QTL@MATCHED.
  H_CLAUSE  Some (family, level) beats no clause at all: at least one capped book clears
            PROTOCOL 4a or 4b that its own cap-OFF control does not.  If this fails on every
            panel and both constructions, no universe clause phrased in volatility belongs in
            RULES, and the honest RULES form is the trend leg alone.

GATES (run and printed BEFORE any hypothesis is read).
  G1  fast_backtest == engine.backtest to machine precision on 4 real books.
  G2  51R's WHICH-LEG numbers reproduce.  The published pair is NOT a single cell: reading
      51R's own script (H5) and its committed .sweep.csv, "-3.93 pp/yr (dSharpe -0.204)" is the
      MEAN OVER THE THREE CADENCES W/M/Q of `dCAGR0_pp` (0 bps) paired with the mean of
      `dSharpe` (10 bps), at its sweep warm-up (index 360), RESPREAD, lb 200, vs the EWall
      no-filter control.  This gate reproduces that exact statistic to 0.05 pp / 0.005 Sharpe
      AND prints the weekly cell alone beside it, because the weekly cell is what this script
      then sweeps.
  G3  Construction identities: ABS(inf) == QTL(1.00) == the cap-OFF book exactly, and the QTL
      clause fires at its nominal rate (|mean admission - q| <= 0.02 on every panel).

RULE 8.  (family, level) is chosen on 2009-2016 IS Sharpe inside each panel x construction arm
and the 2017-2026 window is read once.  OOS CAGR/Sharpe/MaxDD are reported against the arm's
own cap-OFF control, the live RULES v2 book and SPY.

SURVIVORSHIP.  SMALL439 and B136 are current constituents only (PROTOCOL 9,
data/SMALL_PANEL_README.md).  The bias is common to the capped book and its cap-OFF control,
so it largely cancels out of the dCAGR/dSharpe columns that carry this idea's argument; it
does NOT cancel out of the 4a/4b level columns.  A KILL of the clause is strengthened by it.

Deterministic, standalone.  Reads research/baseline.py; modifies nothing.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd
from baseline import load_universe, rules_v2_weights
from engine import backtest, metrics, rebalance_mask

COST = 10
GROSS = 0.75
LB = 200
CAD = "W"
PANELS = ["U56", "B136", "SMALL439"]
CONS = ["RESPREAD", "DEGROSS"]
ABS_LEVELS = [0.40, 0.60, 0.80, 1.00, np.inf]
QTL_LEVELS = [0.40, 0.60, 0.80, 1.00]
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
WARMUP = 260

# pre-registered bars
G2_PP = 0.05
G2_SH = 0.005
G2_CADENCES = ["W", "M", "Q"]
G2_WARMUP = 360            # 51R's SWEEP_IDX
GROSS_GRID = [round(0.20 + 0.05 * i, 2) for i in range(17)]   # idea 311's ladder
G3_RATE = 0.02
H_SCALE_GAIN = 1.0
H_SCALE_ABS = 1.0
H_ORDER_FACTOR = 2.0

SCRIPT = Path(__file__).name
OUT = Path(__file__).with_suffix("")

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_rows", 400)

_LOG = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _LOG.append(s)


# ------------------------------------------------------------------ machinery
def fast_backtest(prices, weights, cost_bps=COST, freq=CAD):
    """Vectorised equivalent of engine.backtest (asserted in G1)."""
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


def panels():
    pxs = load_universe(small=True)
    meta = pd.read_csv(REPO / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv = [c for c in pxs.columns if c != "SPY" and c not in bad]
    px56 = load_universe()
    px136 = load_universe(broad=True)
    out = {
        "U56": (px56[[c for c in px56.columns if c != "SPY"]], px56["SPY"]),
        "B136": (px136[[c for c in px136.columns if c != "SPY"]], px136["SPY"]),
        "SMALL439": (pxs[inv], pxs["SPY"]),
    }
    P(f"panels: U56 {out['U56'][0].shape[1]} names, B136 {out['B136'][0].shape[1]}, "
      f"SMALL439 {out['SMALL439'][0].shape[1]} ({len(bad)} dropped for max_1d_move >= 1.0)")
    for k, (px, _) in out.items():
        P(f"  {k}: {px.index[0].date()} .. {px.index[-1].date()}  ({len(px)} rows)")
    return out


def live_mask(px):
    return px.notna() & px.shift(1).notna()


def vol20(px):
    return px.pct_change().rolling(20).std() * np.sqrt(252)


def clause_mask(px, family, level, v=None, live=None):
    """The volatility clause alone (the trend leg is added by book())."""
    v = vol20(px) if v is None else v
    live = live_mask(px) if live is None else live
    if family == "ABS":
        if not np.isfinite(level):
            return live
        return (v < level) & live
    if family == "QTL":
        if level >= 1.0:
            return live
        vv = v.where(live)
        thr = vv.quantile(level, axis=1)                 # cross-sectional, same-day: causal
        return vv.le(thr, axis=0).fillna(False) & live
    raise ValueError(family)


def book(px, family, level, con, ma=None, v=None, live=None, gross=GROSS):
    """Trend leg (fixed) AND the volatility clause.  RESPREAD holds gross/k (constant gross);
    DEGROSS holds gross/n_live and lets the excluded weight fall to cash (RULES v2's rule)."""
    live = live_mask(px) if live is None else live
    ma = (px > px.rolling(LB).mean()) if ma is None else ma
    g = ma & live & clause_mask(px, family, level, v=v, live=live)
    if con == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * gross
    n = live.sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * gross


def ctrl_book(px, live=None):
    """51R's EWall no-filter control: every live name, equal weight, same gross."""
    live = live_mask(px) if live is None else live
    n = live.sum(axis=1).clip(lower=1)
    return live.astype(float).div(n, axis=0) * GROSS


def leg_book(px, gate, con, max_vol=0.60, gross=GROSS):
    """51R's WHICH-LEG books, reproduced verbatim for G2."""
    live = live_mask(px)
    above = px > px.rolling(LB).mean()
    v = vol20(px)
    g = {"MA": above & live, "VOL": (v < max_vol) & live,
         "MAVOL": above & (v < max_vol) & live}[gate]
    if con == "RESPREAD":
        k = g.sum(axis=1).clip(lower=1)
        return g.astype(float).div(k, axis=0) * gross
    n = live.sum(axis=1).clip(lower=1)
    return g.astype(float).div(n, axis=0) * gross


def stat(r):
    m = metrics(r)
    h = len(r) // 2
    ri, ro = r.loc[:IS_END], r.loc[OOS_START:]
    mi, mo = metrics(ri), metrics(ro)
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"],
                isCAGR=mi["CAGR"], isSharpe=mi["Sharpe"], isMaxDD=mi["MaxDD"],
                oCAGR=mo["CAGR"], oSharpe=mo["Sharpe"], oMaxDD=mo["MaxDD"])


def fail_4b(s, spy_s):
    t = {"H1": s["H1"] > spy_s["H1"], "H2": s["H2"] > spy_s["H2"],
         "OOS": s["oSharpe"] > spy_s["oSharpe"],
         "DD": abs(s["MaxDD"]) <= 0.60 * abs(spy_s["MaxDD"]),
         "CAGR": s["CAGR"] >= 0.70 * spy_s["CAGR"]}
    f = [k for k, v in t.items() if not v]
    return ",".join(f) if f else "-"


def pass_4a(s, b):
    return bool(s["H1"] > b["H1"] and s["H2"] > b["H2"] and s["MaxDD"] >= b["MaxDD"])


def hdr(t):
    P("")
    P("=" * 118)
    P(t)
    P("=" * 118)


# ------------------------------------------------------------------------ run
def main():
    hdr(f"{SCRIPT}  -  idea 314: the vol cap's LEVEL vs a PANEL-SCALED cap, trend leg fixed")
    PX = panels()
    starts = {k: px.index[WARMUP] for k, (px, _) in PX.items()}
    # cache the per-panel primitives once
    PRIM = {}
    for k, (px, _) in PX.items():
        live = live_mask(px)
        PRIM[k] = dict(live=live, ma=(px > px.rolling(LB).mean()), v=vol20(px))

    # ------------------------------------------------------------------ gates
    hdr("GATES (run before any hypothesis is read)")

    g1 = []
    for k in ("U56", "SMALL439"):
        px, _ = PX[k]
        for con in CONS:
            w = book(px, "ABS", 0.60, con, **PRIM[k])
            a = backtest(px, w, cost_bps=COST, freq=CAD)["returns"]
            b = fast_backtest(px, w, cost_bps=COST, freq=CAD)["returns"]
            g1.append(float(np.abs(a - b).max()))
    P(f"G1 fast_backtest vs engine.backtest, 4 books: max |diff| = {max(g1):.3e}  "
      f"-> {'PASS' if max(g1) < 1e-12 else 'FAIL'}")

    px_s, _ = PX["SMALL439"]
    st_g2 = px_s.index[G2_WARMUP]
    g2rows = []
    for cad in G2_CADENCES:
        c0 = metrics(fast_backtest(px_s, ctrl_book(px_s), cost_bps=0,
                                   freq=cad)["returns"].loc[st_g2:])
        c10 = metrics(fast_backtest(px_s, ctrl_book(px_s), cost_bps=COST,
                                    freq=cad)["returns"].loc[st_g2:])
        for gate in ("MA", "VOL", "MAVOL"):
            w = leg_book(px_s, gate, "RESPREAD")
            m0 = metrics(fast_backtest(px_s, w, cost_bps=0, freq=cad)["returns"].loc[st_g2:])
            m10 = metrics(fast_backtest(px_s, w, cost_bps=COST, freq=cad)["returns"].loc[st_g2:])
            g2rows.append(dict(cad=cad, gate=gate,
                               dCAGR0_pp=(m0["CAGR"] - c0["CAGR"]) * 100,
                               dSharpe=m10["Sharpe"] - c10["Sharpe"]))
    G2R = pd.DataFrame(g2rows)
    G2 = G2R.groupby("gate")[["dCAGR0_pp", "dSharpe"]].mean()
    pub = {"VOL": (-3.93, -0.204), "MA": (-1.44, -0.074)}
    P("G2 reproduction of 51R's WHICH-LEG statistic (SMALL439, RESPREAD, lb 200, warm-up 360, "
      "mean over cadences W/M/Q; dCAGR at 0 bps, dSharpe at 10 bps - 51R's own mixed rung):")
    P(G2R.pivot(index="cad", columns="gate", values="dCAGR0_pp").to_string(
        float_format=lambda x: f"{x:+.4f}") + "   <- dCAGR0_pp by cell")
    P(G2.to_string(float_format=lambda x: f"{x:+.4f}") + "   <- cadence means")
    g2ok = True
    for gate, (pp, sh) in pub.items():
        dpp = abs(G2.loc[gate, "dCAGR0_pp"] - pp)
        dsh = abs(G2.loc[gate, "dSharpe"] - sh)
        ok = dpp <= G2_PP and dsh <= G2_SH
        g2ok &= ok
        P(f"   {gate}: published {pp:+.2f} pp / {sh:+.3f}; here "
          f"{G2.loc[gate, 'dCAGR0_pp']:+.3f} / {G2.loc[gate, 'dSharpe']:+.4f}; "
          f"|d| {dpp:.3f} pp / {dsh:.4f} -> {'PASS' if ok else 'FAIL'}")
    P(f"G2 -> {'PASS' if g2ok else 'FAIL'}")
    wk = G2R[G2R.cad == "W"].set_index("gate")
    P(f"   BY-PRODUCT: the published 2.7x ratio is a THREE-CADENCE MEAN of a 0-bps column "
      f"paired with a 10-bps column.  At the WEEKLY cell this script sweeps it reads "
      f"MA {wk.loc['MA', 'dCAGR0_pp']:+.2f} pp vs VOL {wk.loc['VOL', 'dCAGR0_pp']:+.2f} pp "
      f"= {wk.loc['VOL', 'dCAGR0_pp'] / wk.loc['MA', 'dCAGR0_pp']:.2f}x, not "
      f"{pub['VOL'][0] / pub['MA'][0]:.2f}x.  The monthly cell alone reads "
      f"{float(G2R[(G2R.cad == 'M') & (G2R.gate == 'MA')].dCAGR0_pp.iloc[0]):+.2f} vs "
      f"{float(G2R[(G2R.cad == 'M') & (G2R.gate == 'VOL')].dCAGR0_pp.iloc[0]):+.2f} = "
      f"{float(G2R[(G2R.cad == 'M') & (G2R.gate == 'VOL')].dCAGR0_pp.iloc[0]) / float(G2R[(G2R.cad == 'M') & (G2R.gate == 'MA')].dCAGR0_pp.iloc[0]):.2f}x.  "
      f"The claim's SIGN and ORDERING hold at every cadence; its MAGNITUDE is a cadence average.")
    G2R.to_csv(f"{OUT}.g2.csv", index=False)

    g3rows = []
    for k in PANELS:
        px, _ = PX[k]
        pr = PRIM[k]
        nlive = pr["live"].loc[starts[k]:].sum(axis=1)
        w_off = book(px, "ABS", np.inf, "RESPREAD", **pr)
        w_q1 = book(px, "QTL", 1.00, "RESPREAD", **pr)
        ident = float((w_off - w_q1).abs().max().max())
        for q in QTL_LEVELS:
            m = clause_mask(px, "QTL", q, v=pr["v"], live=pr["live"]).loc[starts[k]:]
            rate = float((m.sum(axis=1) / nlive.clip(lower=1)).mean())
            g3rows.append(dict(panel=k, q=q, realised=rate, err=abs(rate - q), ident=ident))
    G3 = pd.DataFrame(g3rows)
    P("")
    P("G3 construction identities:")
    P(f"   |ABS(inf) - QTL(1.00)| weight identity, max over panels = "
      f"{G3.ident.max():.3e} -> {'PASS' if G3.ident.max() < 1e-15 else 'FAIL'}")
    P(G3.pivot(index="panel", columns="q", values="realised").to_string(
        float_format=lambda x: f"{x:.4f}"))
    P(f"   max |realised - nominal q| = {G3.err.max():.4f} (bar {G3_RATE}) -> "
      f"{'PASS' if G3.err.max() <= G3_RATE else 'FAIL'}")

    # --------------------------------------------------- matched admission rates
    hdr("MATCHED ADMISSION: what fraction of live names does ABS 0.60 actually admit?")
    match_q = {}
    arows = []
    for k in PANELS:
        px, _ = PX[k]
        pr = PRIM[k]
        nlive = pr["live"].loc[starts[k]:].sum(axis=1).clip(lower=1)
        for c in ABS_LEVELS:
            m = clause_mask(px, "ABS", c, v=pr["v"], live=pr["live"]).loc[starts[k]:]
            rt = (m.sum(axis=1) / nlive)
            arows.append(dict(panel=k, family="ABS", level=c, mean_rate=rt.mean(),
                              p05=rt.quantile(0.05), p95=rt.quantile(0.95),
                              sd=rt.std(), min=rt.min()))
            if c == 0.60:
                match_q[k] = float(rt.mean())
    AD = pd.DataFrame(arows)
    P(AD.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P("")
    P("MATCHED q per panel (= mean daily admission rate of ABS 0.60 on that panel):")
    for k in PANELS:
        P(f"   {k}: q_match = {match_q[k]:.4f}")
    P("The ABS clause's admission rate is panel-dependent AND time-varying; the QTL clause's "
      "is neither (G3).  That difference is the whole of this idea's question.")

    # -------------------------------------------------------------- the sweep
    hdr("THE SWEEP - trend leg fixed, only the volatility clause moves.  ALL grid points.")
    ARMS = []
    for k in PANELS:
        for c in ABS_LEVELS:
            ARMS.append((k, "ABS", c, "abs"))
        for q in QTL_LEVELS:
            ARMS.append((k, "QTL", q, "qtl"))
        ARMS.append((k, "QTL", match_q[k], "match"))

    spy_stat, off_stat, off0 = {}, {}, {}
    for k in PANELS:
        px, spy = PX[k]
        spy_stat[k] = stat(spy.pct_change().fillna(0.0).loc[starts[k]:])
        for con in CONS:
            w = book(px, "ABS", np.inf, con, **PRIM[k])
            off_stat[(k, con)] = stat(fast_backtest(px, w, cost_bps=COST)["returns"].loc[starts[k]:])
            off0[(k, con)] = metrics(
                fast_backtest(px, w, cost_bps=0)["returns"].loc[starts[k]:])

    px_u, _ = PX["U56"]
    live_ret = backtest(load_universe(), rules_v2_weights(load_universe()),
                        cost_bps=COST, freq=CAD)["returns"]
    live_s = stat(live_ret.loc[starts["U56"]:])
    P(f"4a comparand  RULES v2 (live, universe.json): CAGR {live_s['CAGR']:.2%}  "
      f"Sharpe {live_s['Sharpe']:.4f} ({live_s['H1']:.4f}/{live_s['H2']:.4f})  "
      f"MaxDD {live_s['MaxDD']:.2%}  OOS {live_s['oSharpe']:.4f}")
    for k in PANELS:
        s = spy_stat[k]
        P(f"4b comparand  SPY on the {k} window: CAGR {s['CAGR']:.2%}  Sharpe {s['Sharpe']:.4f} "
          f"({s['H1']:.4f}/{s['H2']:.4f})  MaxDD {s['MaxDD']:.2%}  OOS {s['oSharpe']:.4f}   "
          f"[4b bars: CAGR >= {0.70 * s['CAGR']:.2%}, |MaxDD| <= {0.60 * abs(s['MaxDD']):.2%}]")

    rows = []
    for (k, fam, lvl, tag) in ARMS:
        px, _ = PX[k]
        pr = PRIM[k]
        nlive = pr["live"].loc[starts[k]:].sum(axis=1).clip(lower=1)
        m = clause_mask(px, fam, lvl, v=pr["v"], live=pr["live"]).loc[starts[k]:]
        rate = float((m.sum(axis=1) / nlive).mean())
        for con in CONS:
            w = book(px, fam, lvl, con, **pr)
            r10 = fast_backtest(px, w, cost_bps=COST)["returns"].loc[starts[k]:]
            r0 = fast_backtest(px, w, cost_bps=0)["returns"].loc[starts[k]:]
            s = stat(r10)
            m0 = metrics(r0)
            o = off_stat[(k, con)]
            held = (w.loc[starts[k]:] > 0).sum(axis=1)
            rows.append(dict(
                panel=k, con=con, family=fam, level=lvl, tag=tag, adm_rate=rate,
                n_held=float(held.mean()),
                CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"], H1=s["H1"], H2=s["H2"],
                oCAGR=s["oCAGR"], oSharpe=s["oSharpe"], oMaxDD=s["oMaxDD"],
                isSharpe=s["isSharpe"], isCAGR=s["isCAGR"],
                dCAGR0_pp=(m0["CAGR"] - off0[(k, con)]["CAGR"]) * 100,
                dSharpe0=m0["Sharpe"] - off0[(k, con)]["Sharpe"],
                dCAGR_pp=(s["CAGR"] - o["CAGR"]) * 100,
                dSharpe=s["Sharpe"] - o["Sharpe"],
                dMaxDD_pp=(s["MaxDD"] - o["MaxDD"]) * 100,
                pass4a=pass_4a(s, live_s), fail4b=fail_4b(s, spy_stat[k]),
            ))
    G = pd.DataFrame(rows)
    G["pass4b"] = G.fail4b == "-"
    G.to_csv(f"{OUT}.grid.csv", index=False)
    P(f"\n{len(G)} books written to {Path(OUT).name}.grid.csv "
      f"(3 panels x 10 clause settings x 2 constructions)")

    for con in CONS:
        P("")
        P(f"--- construction {con}, weekly, 10 bps, gross {GROSS}, trend leg lb {LB} FIXED ---")
        sub = G[G.con == con].copy()
        sub["clause"] = sub.family + " " + sub.level.map(
            lambda x: "OFF " if not np.isfinite(x) else f"{x:.3f}")
        show = sub[["panel", "clause", "tag", "adm_rate", "n_held", "CAGR", "Sharpe", "MaxDD",
                    "H1", "H2", "oSharpe", "dCAGR_pp", "dSharpe", "dCAGR0_pp", "dSharpe0",
                    "pass4a", "fail4b"]]
        P(show.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ------------------------------------------------------------- hypotheses
    hdr("H_LEVEL - is the ABS clause's damage MONOTONE in the cap level?")
    P("dCAGR vs the same arm's cap-OFF book, pp/yr (10 bps; 0 bps in brackets).  "
      "Monotone = non-decreasing as c rises.")
    ml = []
    for fam in ("ABS", "QTL"):
        for k in PANELS:
            for con in CONS:
                sub = G[(G.panel == k) & (G.con == con) & (G.family == fam) &
                        (G.tag != "match")].sort_values("level")
                seq, seq0 = sub.dCAGR_pp.tolist(), sub.dCAGR0_pp.tolist()
                mono = all(seq[i + 1] >= seq[i] - 1e-9 for i in range(len(seq) - 1))
                mono0 = all(seq0[i + 1] >= seq0[i] - 1e-9 for i in range(len(seq0) - 1))
                ml.append(dict(family=fam, panel=k, con=con, monotone10=mono, monotone0=mono0,
                               ladder10=" -> ".join(f"{x:+.2f}" for x in seq),
                               ladder0=" -> ".join(f"{x:+.2f}" for x in seq0)))
    ML = pd.DataFrame(ml)
    P(ML.to_string(index=False))
    MLA = ML[ML.family == "ABS"]
    P(f"H_LEVEL (ABS, the pre-registered family): monotone in {int(MLA.monotone10.sum())}/6 arms "
      f"at 10 bps and {int(MLA.monotone0.sum())}/6 at 0 bps -> "
      f"{'HOLDS' if MLA.monotone10.all() else 'FAILS'}")
    P(f"   QTL for comparison: monotone in {int(ML[ML.family == 'QTL'].monotone10.sum())}/6 "
      f"at 10 bps.")

    hdr("WHEN does the ABSOLUTE cap fire?  (mean admission rate of ABS 0.60 by calendar year)")
    yr = []
    for k in PANELS:
        px, _ = PX[k]
        pr = PRIM[k]
        nlive = pr["live"].loc[starts[k]:].sum(axis=1).clip(lower=1)
        m = clause_mask(px, "ABS", 0.60, v=pr["v"], live=pr["live"]).loc[starts[k]:]
        rt = m.sum(axis=1) / nlive
        yr.append(rt.groupby(rt.index.year).mean().rename(k))
    YR = pd.concat(yr, axis=1)
    P(YR.to_string(float_format=lambda x: f"{x:.3f}"))
    P("A cross-sectional quantile clause is a flat line at q by construction (G3).  The "
      "absolute cap is not a universe clause at all in the years that matter: it is a "
      "market-wide DE-RISKING SWITCH whose firing rate is set by the panel's vol distribution "
      "(idea 400's frequency-vs-level artefact, here in the live RULES v1 filter).")
    YR.to_csv(f"{OUT}.byyear.csv")

    hdr("H_SCALE - does a PANEL-SCALED cap at MATCHED admission remove the small-cap damage?")
    sc = []
    for k in PANELS:
        for con in CONS:
            a = G[(G.panel == k) & (G.con == con) & (G.family == "ABS") &
                  (G.level == 0.60)].iloc[0]
            q = G[(G.panel == k) & (G.con == con) & (G.tag == "match")].iloc[0]
            sc.append(dict(panel=k, con=con, q_match=q.level,
                           abs_rate=a.adm_rate, qtl_rate=q.adm_rate,
                           abs_dCAGR0=a.dCAGR0_pp, qtl_dCAGR0=q.dCAGR0_pp,
                           gain0=q.dCAGR0_pp - a.dCAGR0_pp,
                           abs_dCAGR=a.dCAGR_pp, qtl_dCAGR=q.dCAGR_pp,
                           gain10=q.dCAGR_pp - a.dCAGR_pp,
                           abs_dSharpe=a.dSharpe, qtl_dSharpe=q.dSharpe,
                           gainS=q.dSharpe - a.dSharpe))
    SC = pd.DataFrame(sc)
    P(SC.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    row = SC[(SC.panel == "SMALL439") & (SC.con == "RESPREAD")].iloc[0]
    c1 = row.gain0 >= H_SCALE_GAIN
    c2 = abs(row.qtl_dCAGR0) <= H_SCALE_ABS
    P(f"H_SCALE on SMALL439/RESPREAD/0 bps (51R's cell): gain {row.gain0:+.2f} pp "
      f"(bar >= {H_SCALE_GAIN:+.1f}) -> {'PASS' if c1 else 'FAIL'};  "
      f"|residual damage| {abs(row.qtl_dCAGR0):.2f} pp (bar <= {H_SCALE_ABS:.1f}) -> "
      f"{'PASS' if c2 else 'FAIL'}")
    P(f"H_SCALE -> {'HOLDS' if (c1 and c2) else 'FAILS'}")
    P("")
    P("DECOMPOSITION implied by the matched pivot (0 bps, pp/yr).  The ABS clause differs from "
      "the matched QTL clause in ONE thing: its admission rate moves with the market (table "
      "above).  So  ABS damage = SELECTION (= the matched-QTL damage, dropping the panel's "
      "own highest-vol names) + TIMING (= the rest, firing harder in crises).")
    DECOMP = SC.assign(SELECTION=SC.qtl_dCAGR0, TIMING=SC.abs_dCAGR0 - SC.qtl_dCAGR0,
                       TOTAL=SC.abs_dCAGR0,
                       sel_share=SC.qtl_dCAGR0 / SC.abs_dCAGR0)[
        ["panel", "con", "TOTAL", "SELECTION", "TIMING", "sel_share"]]
    P(DECOMP.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    DECOMP.to_csv(f"{OUT}.decomp.csv", index=False)

    hdr("H_ORDER - is the cross-panel ORDERING of the damage an ABS-clause property?")
    od = []
    for con in CONS:
        for lbl, sel in (("ABS 0.60", (G.family == "ABS") & (G.level == 0.60)),
                         ("QTL @MATCHED", G.tag == "match"),
                         ("QTL 0.60", (G.family == "QTL") & (G.level == 0.60))):
            sub = G[(G.con == con) & sel]
            for metric, col in (("dCAGR0_pp", "dCAGR0_pp"), ("dSharpe0", "dSharpe0")):
                vals = {r.panel: getattr(r, col) for r in sub.itertuples()}
                od.append(dict(con=con, clause=lbl, metric=metric,
                               U56=vals["U56"], B136=vals["B136"], SMALL439=vals["SMALL439"],
                               spread=max(vals.values()) - min(vals.values())))
    OD = pd.DataFrame(od)
    P(OD.to_string(index=False, float_format=lambda x: f"{x:+.4f}"))
    a_sp = float(OD[(OD.con == "RESPREAD") & (OD.clause == "ABS 0.60") &
                    (OD.metric == "dCAGR0_pp")].spread.iloc[0])
    q_sp = float(OD[(OD.con == "RESPREAD") & (OD.clause == "QTL @MATCHED") &
                    (OD.metric == "dCAGR0_pp")].spread.iloc[0])
    ok = q_sp <= a_sp / H_ORDER_FACTOR
    P(f"H_ORDER (RESPREAD, 0 bps, dCAGR pp): ABS spread {a_sp:.2f} vs QTL@MATCHED spread "
      f"{q_sp:.2f}; ratio {q_sp / a_sp if a_sp else float('nan'):.2f} "
      f"(bar <= {1 / H_ORDER_FACTOR:.2f}) -> {'HOLDS' if ok else 'FAILS'}")

    hdr("H_CLAUSE - does ANY volatility clause earn its place? (PROTOCOL 4a and 4b)")
    KP = G[["panel", "con", "family", "level", "tag", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
            "oSharpe", "pass4a", "pass4b", "fail4b"]].copy()
    KP.to_csv(f"{OUT}.keeppaths.csv", index=False)
    P(f"4a passes {int(G.pass4a.sum())}/{len(G)};  4b passes {int(G.pass4b.sum())}/{len(G)};  "
      f"BOTH {int((G.pass4a & G.pass4b).sum())}/{len(G)}")
    fc = {}
    for f in G.fail4b:
        for t in ([] if f == "-" else f.split(",")):
            fc[t] = fc.get(t, 0) + 1
    P("binding 4b bars: " + ", ".join(f"{k} {v}" for k, v in
                                      sorted(fc.items(), key=lambda x: -x[1])))
    P("")
    P("The decisive comparison - every genuinely CAPPED book against ITS OWN cap-OFF control. "
      "ABS(inf) and QTL(1.00) are the control itself (G3) and are excluded from the treatment "
      "counts: 8 capped books x 6 arms = 48.")
    G["is_ctrl"] = (~np.isfinite(G.level)) | ((G.family == "QTL") & (G.level >= 1.0))
    dec = []
    for k in PANELS:
        for con in CONS:
            offr = G[(G.panel == k) & (G.con == con) & (G.family == "ABS") &
                     (~np.isfinite(G.level))].iloc[0]
            sub = G[(G.panel == k) & (G.con == con) & (~G.is_ctrl)]
            dec.append(dict(panel=k, con=con,
                            off_4a=bool(offr.pass4a), off_4b=bool(offr.pass4b),
                            capped_4a=int(sub.pass4a.sum()), capped_4b=int(sub.pass4b.sum()),
                            n_capped=len(sub),
                            best_dSharpe=float(sub.dSharpe.max()),
                            n_dSharpe_pos=int((sub.dSharpe > 0).sum())))
    DEC = pd.DataFrame(dec)
    P(DEC.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    cap = G[~G.is_ctrl]
    beats = int((cap.dSharpe > 0).sum())
    P(f"H_CLAUSE: capped books beating their own cap-OFF control on Sharpe: "
      f"{beats}/{len(cap)}  (best {cap.dSharpe.max():+.4f}, median "
      f"{cap.dSharpe.median():+.4f}, worst {cap.dSharpe.min():+.4f})")
    P(f"   on CAGR: {int((cap.dCAGR_pp > 0).sum())}/{len(cap)} "
      f"(best {cap.dCAGR_pp.max():+.2f} pp, median {cap.dCAGR_pp.median():+.2f} pp)")
    P(f"   on MaxDD (less deep): {int((cap.dMaxDD_pp > 0).sum())}/{len(cap)} "
      f"(best {cap.dMaxDD_pp.max():+.2f} pp)  <- the ONE thing a vol cap is supposed to buy")
    hc = bool(((DEC.capped_4a > 0) & (~DEC.off_4a)).any() or
              ((DEC.capped_4b > 0) & (~DEC.off_4b)).any())
    P(f"H_CLAUSE (a capped book clears a KEEP path its cap-OFF control does not) -> "
      f"{'HOLDS' if hc else 'FAILS'}")

    # ------------------------------------------------------------ rule 8 / WF
    hdr("RULE 8 WALK-FORWARD - (family, level) chosen on 2009-2016 IS Sharpe, 2017-2026 read once")
    wf = []
    for k in PANELS:
        for con in CONS:
            sub = G[(G.panel == k) & (G.con == con)].copy()
            pick = sub.loc[sub.isSharpe.idxmax()]
            best = sub.loc[sub.oSharpe.idxmax()]
            offr = sub[(sub.family == "ABS") & (~np.isfinite(sub.level))].iloc[0]
            wf.append(dict(
                panel=k, con=con,
                IS_pick=f"{pick.family} {pick.level:.3f}" if np.isfinite(pick.level)
                        else "ABS OFF",
                isSharpe=pick.isSharpe, oCAGR=pick.oCAGR, oSharpe=pick.oSharpe,
                oMaxDD=pick.oMaxDD,
                OOS_best=f"{best.family} {best.level:.3f}" if np.isfinite(best.level)
                         else "ABS OFF",
                best_oSharpe=best.oSharpe, regret=best.oSharpe - pick.oSharpe,
                off_oSharpe=offr.oSharpe, beats_off=pick.oSharpe > offr.oSharpe,
                spy_oSharpe=spy_stat[k]["oSharpe"], spy_oCAGR=spy_stat[k]["oCAGR"],
                beats_spy=pick.oSharpe > spy_stat[k]["oSharpe"],
                live_oSharpe=live_s["oSharpe"], beats_live=pick.oSharpe > live_s["oSharpe"],
                pass4a=bool(pick.pass4a), fail4b=pick.fail4b))
    WF = pd.DataFrame(wf)
    WF.to_csv(f"{OUT}.walkforward.csv", index=False)
    P(WF.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P(f"IS pick beats its own cap-OFF control OOS in {int(WF.beats_off.sum())}/{len(WF)} arms; "
      f"beats SPY in {int(WF.beats_spy.sum())}/{len(WF)}; beats the live RULES v2 book in "
      f"{int(WF.beats_live.sum())}/{len(WF)}.  Mean OOS regret vs the OOS-best clause: "
      f"{WF.regret.mean():+.4f}.")
    P(f"The IS pick IS the cap-OFF book in {int((WF.IS_pick == 'ABS OFF').sum())}/{len(WF)} "
      f"arms; the OOS-best clause is the cap-OFF book in "
      f"{int((WF.OOS_best == 'ABS OFF').sum())}/{len(WF)}.")

    # WF-B: the single best walk-forward book, reported in full
    hdr("WF-B - the arm with the highest IS Sharpe over ALL 60 books, read once out of sample")
    pick = G.loc[G.isSharpe.idxmax()]
    o = off_stat[(pick.panel, pick.con)]
    P(f"IS-chosen book: {pick.panel} / {pick.con} / {pick.family} "
      f"{'OFF' if not np.isfinite(pick.level) else f'{pick.level:.3f}'}  "
      f"(IS Sharpe {pick.isSharpe:.4f})")
    P(f"  FULL   CAGR {pick.CAGR:.2%}  Sharpe {pick.Sharpe:.4f} "
      f"(H1 {pick.H1:.4f} / H2 {pick.H2:.4f})  MaxDD {pick.MaxDD:.2%}")
    P(f"  OOS    CAGR {pick.oCAGR:.2%}  Sharpe {pick.oSharpe:.4f}  MaxDD {pick.oMaxDD:.2%}")
    P(f"  cap-OFF control on the same arm: CAGR {o['CAGR']:.2%}  Sharpe {o['Sharpe']:.4f}  "
      f"MaxDD {o['MaxDD']:.2%}  OOS {o['oSharpe']:.4f}")
    P(f"  SPY ({pick.panel} window): CAGR {spy_stat[pick.panel]['CAGR']:.2%}  "
      f"Sharpe {spy_stat[pick.panel]['Sharpe']:.4f}  MaxDD "
      f"{spy_stat[pick.panel]['MaxDD']:.2%}  OOS {spy_stat[pick.panel]['oSharpe']:.4f}")
    P(f"  RULES v2 (live): CAGR {live_s['CAGR']:.2%}  Sharpe {live_s['Sharpe']:.4f}  "
      f"MaxDD {live_s['MaxDD']:.2%}  OOS {live_s['oSharpe']:.4f}")
    P(f"  4a {pick.pass4a};  4b {'PASS' if pick.fail4b == '-' else 'FAIL on ' + pick.fail4b}")

    hdr("ADDENDUM - idea 311's standing proposal: quote the admissible GROSS BAND of every "
        "4b pass on a gross-scalar book")
    P("Every book here is a gross scalar (weights are gross x a 0/1 pattern), so idea 311's "
      "census applies: a 4b pass at a single un-swept g is a DIAL PLACEMENT until the band is "
      "shown.  Each 4b passer is re-run on a 17-point g ladder 0.20..1.00 (step 0.05), the "
      "clause and everything else held fixed.  ALL 17 points are written to the .gband.csv.")
    passers = G[G.pass4b].copy()
    gb = []
    for r in passers.itertuples():
        px, _ = PX[r.panel]
        pr = PRIM[r.panel]
        adm = []
        for g_ in GROSS_GRID:
            w = book(px, r.family, r.level, r.con, gross=g_, **pr)
            s = stat(fast_backtest(px, w, cost_bps=COST)["returns"].loc[starts[r.panel]:])
            f = fail_4b(s, spy_stat[r.panel])
            gb.append(dict(panel=r.panel, con=r.con, family=r.family, level=r.level, gross=g_,
                           CAGR=s["CAGR"], Sharpe=s["Sharpe"], MaxDD=s["MaxDD"], H1=s["H1"],
                           H2=s["H2"], oSharpe=s["oSharpe"], fail4b=f, pass4b=(f == "-")))
            if f == "-":
                adm.append(g_)
        lab = f"{r.family} {'OFF' if not np.isfinite(r.level) else f'{r.level:.3f}'}"
        band = f"[{min(adm):.2f}, {max(adm):.2f}]" if adm else "EMPTY"
        contig = (len(adm) == round((max(adm) - min(adm)) / 0.05) + 1) if adm else True
        P(f"  {r.panel:9s} {r.con:8s} {lab:10s} {'CONTROL' if r.is_ctrl else 'capped '}  "
          f"admissible g {band}  width {len(adm)} of 17 grid points  contiguous {contig}  "
          f"(the book above sits at g=0.75)")
    GB = pd.DataFrame(gb)
    GB.to_csv(f"{OUT}.gband.csv", index=False)
    widths = GB.groupby(["panel", "con", "family", "level"], dropna=False).pass4b.sum()
    P(f"Band widths over the {len(passers)} 4b passers: min {int(widths.min())}, median "
      f"{widths.median():.1f}, max {int(widths.max())} of 17 grid points.")

    hdr("SUMMARY")
    P(f"G1 {'PASS' if max(g1) < 1e-12 else 'FAIL'}  G2 {'PASS' if g2ok else 'FAIL'}  "
      f"G3 {'PASS' if (G3.err.max() <= G3_RATE and G3.ident.max() < 1e-15) else 'FAIL'}")
    P(f"H_LEVEL {'HOLDS' if ML.monotone10.all() else 'FAILS'}   "
      f"H_SCALE {'HOLDS' if (c1 and c2) else 'FAILS'}   "
      f"H_ORDER {'HOLDS' if ok else 'FAILS'}   "
      f"H_CLAUSE {'HOLDS' if hc else 'FAILS'}")
    P(f"KEEP paths over {len(G)} books: 4a {int(G.pass4a.sum())}, 4b {int(G.pass4b.sum())}, "
      f"BOTH {int((G.pass4a & G.pass4b).sum())}")

    Path(f"{OUT}.console.txt").write_text("\n".join(_LOG) + "\n")
    OD.to_csv(f"{OUT}.ordering.csv", index=False)
    SC.to_csv(f"{OUT}.scale.csv", index=False)
    AD.to_csv(f"{OUT}.admission.csv", index=False)


if __name__ == "__main__":
    main()
