#!/usr/bin/env python3
"""idea 2524 (lane cloud, run 70, 2026-09-23) — DOES THE CAPPED CANDIDATE'S EWBH FAILURE REVERSE
ON THE SMALL-CAP PANEL?

THE GAP.  Idea 2516 replaced rule 4b's SPY comparand with EWBH(panel) — equal-weight buy-and-hold
of the book's OWN investable set, identical names, tape, days and survivorship draw — and every
one of the 21 committed capped-family 4b passes died: 21 of 48 under SPY, 0 of 48 under EWBH.
The cause it named was the SURVIVORSHIP PREMIUM: EWBH of the 20 current megacaps returns 32.27%
a year against SPY's 15.23%, so 4b was crediting the rule with +17 pp of panel luck.

BUT THAT KILL WAS PRICED ON U56 AND B136 ONLY — the two panels whose current-constituent premium
is LARGEST.  The record has never scored the band book against EWBH on the SMALL-CAP panel, whose
equal-weight buy-and-hold should carry a far deeper drawdown and a far weaker Sharpe, and where a
200d trend gate therefore has the most room to earn its keep.  This run closes that axis:

  * a PASS here would be the record's first 4b that is not a megacap-survivorship artefact;
  * a FAILURE closes the panel axis for good — the EWBH kill would then be panel-independent.

DIAL 1 -- per-name cap in {0.005, 0.010, 0.020 (idea 2322's CAP2), INF (the uncapped CAND)}.
DIAL 2 -- gross g in {0.75 (live), 1.00}.
EXACTLY TWO TUNED PARAMETERS.  Everything else is a PUBLISHED AXIS, never selected on: panels
{SMALL, U56, B136}; the COMMON WINDOW (every panel re-scored on SMALL's own 2010-2026 dates, so
the three are read on the same tape); cost rungs {0, 10, 25, 50} bps; cadence {W, M}; t+1
execution; band 0.03; MA 200d; SHY sweep at phi = 1.00.

COMPARANDS, ALL SCORED ON ALL FIVE 4b LEGS, NONE SELECTED ON.
  SPY   -- PROTOCOL rule 4b as written.
  EWBH  -- idea 2516's comparand: equal-weight buy-and-hold of the panel from the first scored
           day, never rebalanced, gross 1.00, zero turnover after inception.
  EWRB  -- equal-weight of every PRICED name, rebalanced on the book's own cadence and charged
           the book's own rung.  On a panel whose members list at different dates this is the
           FAIRER of the two, because EWBH can only ever hold the names already priced on day
           one; 2516 called it "the mildest fair substitute" and it is the tradable twin.

TWO BARS AT EVERY COMPARAND (as in 2532/2535):
  4b-PROTO  -- rule 4b verbatim: Sharpe > X in BOTH halves AND out of sample, MaxDD >= 0.60 x
               X's, CAGR >= 0.70 x X's.
  4b-STRICT -- beats it outright: Sharpe > X in both halves AND OOS, MaxDD no worse, CAGR no
               lower.  Free of any SPY-calibrated constant.

GATES.  G0 >= 10y per panel.  G1 the candidate runner IS `engine.backtest` on the same
risk-weight frame.  G2 the eligible set IS `baseline.band_state` & priced.  G3 the committed U56
CAP2 / g0.75 / W / 10 bps headline is reproduced.  G4 no leverage anywhere.  G5 the
`max_1d_move >= 1.0` names are dropped from the SMALL panel BEFORE anything is computed, and the
count is published.  G6 exactly two tuned parameters.  G7 SPY and EWBH are bit-identical across
every arm within a (panel, window).  G8 EWBH trades exactly once (inception).  G9 the sweep
instrument is priced on every scored row of every panel.  G10 the EWBH/EWRB sleeves exclude SPY
and SHY; their name counts are published.

SURVIVORSHIP CAVEAT (rule 9 and `data/SMALL_PANEL_README.md`) — THIS RUN IS ABOUT IT, SO IT IS
STATED TWICE.  `universe.json` (U56), `universe_broad.json` (B136) and the sub-$2B screen behind
`data/prices_small.csv` are ALL CURRENT-CONSTITUENT lists.  The small panel is the worst of the
three: it holds only companies still listed, still public and still under $2B TODAY, so every
name survived 2010-2026 by construction and the acquired, delisted and bankrupted small caps of
that window are simply absent.  Its returns are biased UPWARD and its drawdowns biased SHALLOW.
The EWBH and EWRB comparands carry the IDENTICAL contamination on the IDENTICAL tape and days, so
the candidate-vs-EWBH contrast is differenced clean; the SPY columns are NOT and are kept for
protocol continuity only.  NOTHING in this run licenses a small-cap book for real capital.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_small-panel-ewbh-reversal_cloud.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "small-panel-ewbh-reversal", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, WARMUP = 0.03, 200, 260
CAPS = [0.005, 0.010, 0.020, np.inf]             # DIAL 1
GROSSES = [0.75, 1.00]                           # DIAL 2
RUNGS = [0.0, 10.0, 25.0, 50.0]                  # published
CADENCES = ["W", "M"]                            # published
SWEEP, BENCH = "SHY", "SPY"
COMPARANDS = ["SPY", "EWBH", "EWRB"]
HEAD_CAP, HEAD_G, HEAD_RUNG, HEAD_CAD = 0.020, 0.75, 10.0, "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
TOL = 1e-12

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUB   {name}: {value}")


def cname(c):
    return "INF" if not np.isfinite(c) else f"{c:.3f}"


def eligible(px):
    return band_state(px, BAND) & px.notna()


def load_small():
    """The sub-$2B panel with the `max_1d_move >= 1.0` names dropped FIRST (G5), SHY joined from
    data/prices.csv as the sweep instrument (the small cache carries no bond ETF)."""
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    keep = [c for c in px.columns if c == BENCH or c not in bad]
    dropped = len(px.columns) - len(keep)
    px = px[keep]
    shy = pd.read_csv(ROOT / "data" / "prices.csv", index_col=0, parse_dates=True)[SWEEP]
    px = pd.concat([px, shy.reindex(px.index, method="ffill").rename(SWEEP)], axis=1)
    return px, dropped, len(bad)


# ---------------------------------------------------------------- the candidate
def run_cand(prices, el, gross, cap, freq, sweep=True):
    """The committed book (runner verbatim from ideas 2532/2535): hold every in-band, priced name
    at min(gross/N_in, cap) of NAV, rebalanced on `freq`, decided at t-1 and applied at t,
    drifting in between, residual swept into SHY.  `engine.backtest` semantics (G1)."""
    cols = list(prices.columns)
    si = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[SWEEP].notna().values.astype(float)
    el_dec = el.reindex(prices.index).fillna(False).shift(1, fill_value=False).values
    nin = el.sum(axis=1).replace(0, np.nan)
    per_dec = (gross / nin).clip(upper=cap).fillna(0.0).shift(1, fill_value=0.0).values
    s_key = pd.Series(prices.index.to_period(freq), index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    cur = np.zeros(m); risk = np.zeros(m)
    turn = np.zeros(n); r0 = np.zeros(n); gr = np.zeros(n); rg = np.zeros(n)
    nheld = np.zeros(n); mx = np.zeros(n); capbind = np.zeros(n); lev = 0; pre_max = 0.0
    for i in range(n):
        if mask[i] or i == 0:
            new_r = np.where(el_dec[i], per_dec[i], 0.0)
            tot_r = new_r.sum()
            pre_max = max(pre_max, float(tot_r))
            if tot_r > 1.0:
                new_r = new_r / tot_r; lev += 1
            new = new_r.copy()
            new[si] += max(0.0, 1.0 - new.sum()) * s_ok[i] if sweep else 0.0
            turn[i] = float(np.abs(new - cur).sum())
            cur = new; risk = new_r
        gr[i] = cur.sum(); rg[i] = float(risk.sum()); nheld[i] = float((risk > TOL).sum())
        mx[i] = float(risk.max())
        capbind[i] = float(per_dec[i] < (gross / max(nin.values[i], 1e-9)) - 1e-15) \
            if np.isfinite(cap) else 0.0
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        if tot > 0:
            cur = g / tot; risk = risk * (1 + rv[i]) / tot
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), risk_gross=pd.Series(rg, index=idx),
                names=pd.Series(nheld, index=idx), maxw=pd.Series(mx, index=idx),
                capbind=pd.Series(capbind, index=idx), lev=lev, pre_max=pre_max)


# ---------------------------------------------------------------- the comparands
def ewbh_frame(px, t0):
    """Equal-weight BUY-AND-HOLD from day t0, never rebalanced.  Sleeve EXCLUDES SPY and SHY
    (G10) and can only hold names already priced at t0 — which is exactly why EWRB is also run."""
    names = [c for c in px.columns if c not in (BENCH, SWEEP) and pd.notna(px[c].loc[t0])]
    rel = px[names].div(px[names].loc[t0], axis=1).ffill()
    w = rel.div(rel.sum(axis=1), axis=0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[names] = w.fillna(0.0)
    ret = rel.sum(axis=1).pct_change().fillna(0.0)     # zero-turnover buy-and-hold, by identity
    return out, names, ret


def ewrb_frame(px):
    """Equal weight over EVERY priced name (SPY and SHY excluded), gross 1.00.  Traded on the
    book's cadence by engine.backtest and charged the book's rung."""
    names = [c for c in px.columns if c not in (BENCH, SWEEP)]
    pr = px[names].notna().astype(float)
    sl = pr.div(pr.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[names] = sl.values
    return out, names


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    return float((1 + r).cumprod().iloc[-1] ** (252 / len(r)) - 1)


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def calmar(r):
    d = maxdd(r)
    return float(cagr(r) / abs(d)) if d < 0 else np.nan


def avol(r):
    return float(r.std() * np.sqrt(252))


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def score(r, x, oos):
    h1, h2 = halves(r); x1, x2 = halves(x)
    ro, xo = r.loc[oos:], x.loc[oos:]
    so, sxo = sharpe(ro), sharpe(xo)
    dd, xdd = maxdd(r), maxdd(x)
    cg, xcg = cagr(r), cagr(x)
    P = dict(L_H1=h1 > x1, L_H2=h2 > x2, L_OOS=so > sxo,
             L_DD=dd >= DD_CAP * xdd, L_CAGR=cg >= CAGR_FLOOR * xcg)
    S = dict(S_H1=h1 > x1, S_H2=h2 > x2, S_OOS=so > sxo, S_DD=dd >= xdd, S_CAGR=cg >= xcg)
    return dict(**{k: bool(v) for k, v in P.items()}, **{k: bool(v) for k, v in S.items()},
                pass4b=bool(all(P.values())), pass4b_strict=bool(all(S.values())),
                x_CAGR=xcg, x_Sharpe=sharpe(x), x_MaxDD=xdd, x_Vol=avol(x),
                x_H1=x1, x_H2=x2, x_OOS_Sharpe=sxo, x_OOS_CAGR=cagr(xo),
                x_OOS_MaxDD=maxdd(xo))


def main():
    t0 = time.time()
    say("=== idea 2524 — DOES THE CAPPED CANDIDATE'S EWBH FAILURE REVERSE ON THE SMALL-CAP")
    say("    PANEL?  (lane cloud, run 70) ===")
    say(f"    {DATE}  band {BAND}  MA {MA_LEN}d  cadence {CADENCES}  t+1  rungs {RUNGS} bps"
        f"  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 per-name cap {[cname(c) for c in CAPS]} (0.020 = CAP2, INF = CAND)"
        f"    DIAL 2 gross {GROSSES}")
    say(f"    COMPARANDS, ALL SCORED, NONE SELECTED ON: {COMPARANDS}")
    say("    2516 killed every capped-family 4b pass by swapping SPY for EWBH(panel), on U56 and")
    say("    B136 ONLY — the two panels with the LARGEST current-constituent premium.  A pass on")
    say("    SMALL would be the record's first 4b that is not a megacap-survivorship artefact; a")
    say("    failure closes the panel axis.")
    say("    SURVIVORSHIP (rule 9 + data/SMALL_PANEL_README.md): ALL THREE panels are CURRENT-")
    say("    CONSTITUENT lists and SMALL is the worst — only companies still listed, still public")
    say("    and still under $2B TODAY, so every name survived 2010-2026 by construction.  EWBH")
    say("    and EWRB carry the IDENTICAL contamination on the IDENTICAL tape, so the")
    say("    candidate-vs-EWBH contrast is differenced clean; the SPY columns are NOT.")
    gate("G6 exactly two tuned parameters", "per-name cap, gross", "2", True)

    px_s, dropped, n_bad = load_small()
    gate("G5 the max_1d_move >= 1.0 names are dropped from SMALL BEFORE anything is computed",
         f"{n_bad} such tickers in data/small_meta.csv, {dropped} dropped from the loaded panel,"
         f" {len(px_s.columns)} columns left (incl. SPY benchmark + SHY sweep)", "> 0 dropped",
         dropped > 0)

    panels = {"SMALL": px_s, "U56": load_universe(), "B136": load_universe(broad=True)}
    s_start, s_end = px_s.index[0], px_s.index[-1]
    # the COMMON WINDOW: every panel re-scored on SMALL's own dates, so the three are read on the
    # same tape.  Published axis, never selected on.
    arms = [("OWN", nm, px) for nm, px in panels.items()] + \
           [("COMMON", nm, px.loc[s_start:s_end]) for nm, px in panels.items() if nm != "SMALL"]
    for win, nm, px in arms:
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm}/{win})",
             f"{yrs:.1f}y scored, {len(px.columns)} columns, {len(px)} rows", ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    bs_u = band_state(px_u, BAND) & px_u.notna()
    d2 = int((eligible(px_u) != bs_u).sum().sum())
    bs_s = band_state(px_s, BAND) & px_s.notna()
    d2s = int((eligible(px_s) != bs_s).sum().sum())
    gate("G2 the eligible set IS baseline.band_state & priced, unmodified",
         f"{d2} differing cells on U56, {d2s} on SMALL; mean names IN"
         f" {bs_u.sum(axis=1).mean():.2f} (U56) / {bs_s.sum(axis=1).mean():.2f} (SMALL)",
         "0", d2 == 0 and d2s == 0)

    el_u = eligible(px_u)
    nin_u = el_u.sum(axis=1).replace(0, np.nan)
    d1 = 0.0
    for _cap in (HEAD_CAP, np.inf):
        w = el_u.astype(float).mul((HEAD_G / nin_u).clip(upper=_cap), axis=0).fillna(0.0)
        r_eng = backtest(px_u, w, cost_bps=HEAD_RUNG, freq=HEAD_CAD)["returns"]
        lv = run_cand(px_u, el_u, HEAD_G, _cap, HEAD_CAD, sweep=False)
        d1 = max(d1, float((r_eng - (lv["r0"] - lv["turn"] * HEAD_RUNG / 1e4)).abs().max()))
    gate("G1 the candidate runner IS engine.backtest on the same risk-weight frame (cap 0.020 and"
         " INF, g 0.75, W, 10 bps, sweep off)", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for _, _, px in arms)
    gate("G9 sweep instrument priced on every scored row of every panel",
         f"SHY non-null on all {len(arms)} arms: {shy_ok}", "True", shy_ok)

    # ------------------------------------------------------------ the grid
    rows, facts, lev_tot, pre_maxes = [], [], 0, []
    for win, pname, px in arms:
        el = eligible(px)
        start = px.index[WARMUP]
        ew_w, ew_names, ew_ret_full = ewbh_frame(px, start)
        rb_w, rb_names = ewrb_frame(px)
        spy_t = px[BENCH].pct_change().fillna(0.0).loc[start:]
        base_t = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEAD_RUNG, freq="W")["returns"].loc[start:]
        ew_t = ew_ret_full.loc[start:]
        rets_all = px.pct_change().fillna(0.0)
        drift_id = float((ew_t - (ew_w.shift(1) * rets_all).sum(axis=1).loc[start:]).abs().max())
        gate(f"G8 EWBH is pure drift — zero turnover after inception ({pname}/{win})",
             f"max|d| vs the held-weight identity {drift_id:.3e}", "< 1e-12", drift_id < 1e-12)
        publish(f"G10 sleeves ({pname}/{win})",
                f"EWBH {len(ew_names)} names priced on day one of {len(rb_names)} in the panel"
                f" ({100 * len(ew_names) / len(rb_names):.1f}%), SPY and SHY excluded;"
                f" EWBH {cagr(ew_t):.2%} / {sharpe(ew_t):.4f} / {maxdd(ew_t):.2%}"
                f" / vol {avol(ew_t):.2%}")
        rb_cache = {}
        for cad in CADENCES:
            bb = backtest(px, rb_w, cost_bps=0.0, freq=cad)
            rb_cache[cad] = (bb["returns"].loc[start:], bb["turnover"].loc[start:])
            publish(f"G10b EWRB ({pname}/{win}/{cad})",
                    f"{len(rb_names)} names, turnover {rb_cache[cad][1].sum() / (len(ew_t) / 252):.2f}"
                    f"x/yr, pre-cost {cagr(rb_cache[cad][0]):.2%} / {sharpe(rb_cache[cad][0]):.4f}"
                    f" / {maxdd(rb_cache[cad][0]):.2%}")
            for cap in CAPS:
                for gross in GROSSES:
                    bk = run_cand(px, el, gross, cap, cad)
                    lev_tot += bk["lev"]; pre_maxes.append(bk["pre_max"])
                    r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                    yrs = len(tn) / 252
                    facts.append(dict(window=win, panel=pname, cadence=cad, cap=cname(cap),
                                      gross=gross, turnover_yr=float(tn.sum() / yrs),
                                      mean_risk_gross=float(bk["risk_gross"].loc[start:].mean()),
                                      cap_bind_share=float(bk["capbind"].loc[start:].mean()),
                                      mean_names=float(bk["names"].loc[start:].mean()),
                                      mean_panel_names=float(px.drop(columns=[BENCH, SWEEP])
                                                             .notna().sum(axis=1).loc[start:].mean()),
                                      max_gross=float(bk["gross"].loc[start:].max()),
                                      max_name_w=float(bk["maxw"].loc[start:].max()),
                                      cand_vol=avol(r0)))
                    for rung in RUNGS:
                        r = r0 - tn * rung / 1e4
                        r_is = r.loc[:IS_END]
                        b1, b2 = halves(base_t)
                        h1, h2 = halves(r)
                        pass4a = bool(h1 > b1 and h2 > b2 and maxdd(r) >= maxdd(base_t))
                        comp = {"SPY": spy_t, "EWBH": ew_t,
                                "EWRB": rb_cache[cad][0] - rb_cache[cad][1] * rung / 1e4}
                        for cn, x in comp.items():
                            rows.append(dict(window=win, panel=pname, cadence=cad, cap=cname(cap),
                                             gross=gross, cost_bps=rung, comparand=cn,
                                             CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                                             Vol=avol(r), H1=h1, H2=h2, Calmar=calmar(r),
                                             turnover_yr=float(tn.sum() / yrs),
                                             IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is),
                                             OOS_CAGR=cagr(r.loc[OOS_START:]),
                                             OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                                             OOS_MaxDD=maxdd(r.loc[OOS_START:]),
                                             pass4a=pass4a,
                                             base_Sharpe=sharpe(base_t), base_MaxDD=maxdd(base_t),
                                             base_CAGR=cagr(base_t), base_H1=b1, base_H2=b2,
                                             base_OOS_Sharpe=sharpe(base_t.loc[OOS_START:]),
                                             base_OOS_CAGR=cagr(base_t.loc[OOS_START:]),
                                             base_OOS_MaxDD=maxdd(base_t.loc[OOS_START:]),
                                             **score(r, x, OOS_START)))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.rows.csv", index=False)
    fdf = pd.DataFrame(facts); fdf.to_csv(f"{OUT}.books.csv", index=False)

    gate("G4 no leverage EVER",
         f"max PRE-clamp target gross {max(pre_maxes):.15f}; {lev_tot} float-level rescales;"
         f" max REALISED book gross {fdf.max_gross.max():.12f}", "<= 1 + 1e-9",
         max(pre_maxes) <= 1.0 + 1e-9 and float(fdf.max_gross.max()) <= 1.0 + 1e-9)
    uniq = df[df.comparand.isin(["SPY", "EWBH"])].groupby(
        ["window", "panel", "comparand"]).x_Sharpe.nunique()
    gate("G7 SPY and EWBH are bit-identical across every arm within a (panel, window)",
         f"max distinct values {int(uniq.max())} over {len(uniq)} groups", "all 1",
         int(uniq.max()) == 1)
    hd = df[(df.window == "OWN") & (df.panel == "U56") & (df.cadence == "W")
            & (df.cap == cname(HEAD_CAP)) & (df.gross == HEAD_G)
            & (df.cost_bps == HEAD_RUNG) & (df.comparand == "SPY")].iloc[0]
    publish("G3 committed U56 CAP2 W 10bps g0.75 headline reproduced here",
            f"{hd.CAGR:.2%} / {hd.Sharpe:.4f} / {hd.MaxDD:.2%}, halves {hd.H1:.4f} / {hd.H2:.4f},"
            f" OOS {hd.OOS_CAGR:.2%} / {hd.OOS_Sharpe:.4f}, turnover {hd.turnover_yr:.2f}x/yr")

    # ------------------------------------------------------------ A. the books and comparands
    say("\n=== A. THE COMMITTED CELL (cap 0.020, g 0.75, W, 10 bps) ON EVERY PANEL AND WINDOW ===")
    say("  window panel | book       |   CAGR |  Sharpe |   MaxDD |    Vol |   H1   /   H2  |"
        "  OOS CAGR | OOS Sharpe")
    for win, pname, _ in arms:
        q0 = df[(df.window == win) & (df.panel == pname) & (df.cadence == "W")
                & (df.cap == cname(HEAD_CAP)) & (df.gross == HEAD_G)
                & (df.cost_bps == HEAD_RUNG)]
        c0 = q0.iloc[0]
        say(f"  {win:6s} {pname:5s} | CANDIDATE  | {c0.CAGR:6.2%} | {c0.Sharpe:7.4f} |"
            f" {c0.MaxDD:7.2%} | {c0.Vol:6.2%} | {c0.H1:6.3f} / {c0.H2:6.3f} |"
            f" {c0.OOS_CAGR:9.2%} | {c0.OOS_Sharpe:10.4f}")
        say(f"  {win:6s} {pname:5s} | live v2    | {c0.base_CAGR:6.2%} | {c0.base_Sharpe:7.4f} |"
            f" {c0.base_MaxDD:7.2%} | {'':6s} | {c0.base_H1:6.3f} / {c0.base_H2:6.3f} |"
            f" {c0.base_OOS_CAGR:9.2%} | {c0.base_OOS_Sharpe:10.4f}")
        for cn in COMPARANDS:
            q = q0[q0.comparand == cn].iloc[0]
            say(f"  {win:6s} {pname:5s} | {cn:10s} | {q.x_CAGR:6.2%} | {q.x_Sharpe:7.4f} |"
                f" {q.x_MaxDD:7.2%} | {q.x_Vol:6.2%} | {q.x_H1:6.3f} / {q.x_H2:6.3f} |"
                f" {q.x_OOS_CAGR:9.2%} | {q.x_OOS_Sharpe:10.4f}")

    say("\n  BOOK FACTS at the same cell (why the cap does or does not bite):")
    say("  window panel | mean panel names | mean names held | mean risk gross | cap binds |"
        " turnover x/yr")
    for win, pname, _ in arms:
        f0 = fdf[(fdf.window == win) & (fdf.panel == pname) & (fdf.cadence == "W")
                 & (fdf.cap == cname(HEAD_CAP)) & (fdf.gross == HEAD_G)].iloc[0]
        say(f"  {win:6s} {pname:5s} | {f0.mean_panel_names:16.1f} | {f0.mean_names:15.1f} |"
            f" {f0.mean_risk_gross:15.4f} | {f0.cap_bind_share:9.1%} | {f0.turnover_yr:13.2f}")

    # ------------------------------------------------------------ B. the verdict
    say("\n=== B. THE VERDICT — 4b UNDER EVERY COMPARAND, BY PANEL AND WINDOW ===")
    say("  Each (window, panel) carries 64 book-rows (2 cadences x 4 caps x 2 gross x 4 rungs).")
    say("  window panel | comparand | 4b-PROTO | 4b-STRICT | L_H1 f | L_H2 f | L_OOS f | L_DD f |"
        " L_CAGR f | first-binding leg")
    ORDER = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
    for win, pname, _ in arms:
        for cn in COMPARANDS:
            q = df[(df.window == win) & (df.panel == pname) & (df.comparand == cn)]
            fb = {}
            for _, r in q[~q.pass4b].iterrows():
                for lg in ORDER:
                    if not r[lg]:
                        fb[lg] = fb.get(lg, 0) + 1
                        break
            say(f"  {win:6s} {pname:5s} | {cn:9s} | {int(q.pass4b.sum()):8d} |"
                f" {int(q.pass4b_strict.sum()):9d} | {int((~q.L_H1).sum()):6d} |"
                f" {int((~q.L_H2).sum()):6d} | {int((~q.L_OOS).sum()):7d} |"
                f" {int((~q.L_DD).sum()):6d} | {int((~q.L_CAGR).sum()):8d} | "
                + ", ".join(f"{k} {v}" for k, v in sorted(fb.items(), key=lambda kv: -kv[1])))
    say("\n  PATH 4a (vs the live RULES v2 book on the SAME panel), out of 64 per arm:")
    for win, pname, _ in arms:
        q = df[(df.window == win) & (df.panel == pname) & (df.comparand == "SPY")]
        say(f"    {win:6s} {pname:5s}: {int(q.pass4a.sum())} of {len(q)}")

    # ------------------------------------------------------------ C. the reversal, measured
    say("\n=== C. DOES THE EWBH FAILURE REVERSE?  SHARE OF THE 64 BOOK-ROWS THE CANDIDATE LEADS")
    say("    (4b-STRICT legs), UNDER EWBH — SMALL AGAINST THE TWO MEGACAP PANELS ===")
    say("  window panel | comparand | Sharpe H1 | Sharpe H2 | Sharpe OOS | MaxDD no worse |"
        " CAGR no lower | median dCAGR pp | median dSharpe | median dMaxDD pp")
    for win, pname, _ in arms:
        for cn in ("EWBH", "EWRB"):
            q = df[(df.window == win) & (df.panel == pname) & (df.comparand == cn)]
            say(f"  {win:6s} {pname:5s} | {cn:9s} | {q.S_H1.mean():9.1%} | {q.S_H2.mean():9.1%} |"
                f" {q.S_OOS.mean():10.1%} | {q.S_DD.mean():14.1%} | {q.S_CAGR.mean():13.1%} |"
                f" {100 * (q.CAGR - q.x_CAGR).median():15.2f} |"
                f" {(q.Sharpe - q.x_Sharpe).median():14.4f} |"
                f" {100 * (q.MaxDD - q.x_MaxDD).median():16.2f}")
    say("\n  THE SURVIVORSHIP PREMIUM, PANEL BY PANEL (EWBH minus SPY, the thing 2516 measured):")
    say("  window panel | EWBH CAGR | SPY CAGR | d CAGR pp | EWBH Sharpe | SPY Sharpe |"
        " EWBH MaxDD | SPY MaxDD | 4b CAGR floor | 4b DD cap")
    for win, pname, _ in arms:
        q = df[(df.window == win) & (df.panel == pname)]
        e = q[q.comparand == "EWBH"].iloc[0]; s = q[q.comparand == "SPY"].iloc[0]
        say(f"  {win:6s} {pname:5s} | {e.x_CAGR:9.2%} | {s.x_CAGR:8.2%} |"
            f" {100 * (e.x_CAGR - s.x_CAGR):9.2f} | {e.x_Sharpe:11.4f} | {s.x_Sharpe:10.4f} |"
            f" {e.x_MaxDD:10.2%} | {s.x_MaxDD:9.2%} |"
            f" {CAGR_FLOOR * s.x_CAGR:7.2%} -> {CAGR_FLOOR * e.x_CAGR:6.2%} |"
            f" {DD_CAP * s.x_MaxDD:6.2%} -> {DD_CAP * e.x_MaxDD:6.2%}")

    # ------------------------------------------------------------ D. the dial ladder on SMALL
    say("\n=== D. THE FULL DIAL GRID ON SMALL (g 0.75 and 1.00, W, every cap, every rung) ===")
    say("  cap   |    g | rung |   CAGR |  Sharpe |   MaxDD |   H1  /   H2  | OOS Sharpe |"
        " mean gross | 4b vs SPY | 4b vs EWBH | 4b-S vs EWBH | 4a")
    for cap in CAPS:
        for g in GROSSES:
            for rung in RUNGS:
                q = df[(df.window == "OWN") & (df.panel == "SMALL") & (df.cadence == "W")
                       & (df.cap == cname(cap)) & (df.gross == g) & (df.cost_bps == rung)]
                sp = q[q.comparand == "SPY"].iloc[0]; ew = q[q.comparand == "EWBH"].iloc[0]
                f0 = fdf[(fdf.window == "OWN") & (fdf.panel == "SMALL") & (fdf.cadence == "W")
                         & (fdf.cap == cname(cap)) & (fdf.gross == g)].iloc[0]
                say(f"  {cname(cap):5s} | {g:4.2f} | {rung:4.0f} | {sp.CAGR:6.2%} |"
                    f" {sp.Sharpe:7.4f} | {sp.MaxDD:7.2%} | {sp.H1:5.3f} / {sp.H2:5.3f} |"
                    f" {sp.OOS_Sharpe:10.4f} | {f0.mean_risk_gross:10.4f} |"
                    f" {'Y' if sp.pass4b else '.':^9s} | {'Y' if ew.pass4b else '.':^10s} |"
                    f" {'Y' if ew.pass4b_strict else '.':^12s} | {'Y' if sp.pass4a else '.':^2s}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 WALK-FORWARD — the two dials (cap, gross) fitted on warm-up..2016-12-31")
    say("    ONLY, 2017-2026 read ONCE, separately at every (window, panel, cadence, rung).")
    say("    NOTE: SMALL's price cache starts 2010-01-04, so its IS window is ~6 years against")
    say("    ~7 for the megacap panels on their own dates.  Stated, not adjusted for. ===")
    wf = []
    for win, pname, _ in arms:
        for cad in CADENCES:
            for rung in RUNGS:
                q = df[(df.window == win) & (df.panel == pname) & (df.cadence == cad)
                       & (df.cost_bps == rung) & (df.comparand == "SPY")]
                for ch, keyf in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    p = q.loc[q[keyf].idxmax()]
                    sel = df[(df.window == win) & (df.panel == pname) & (df.cadence == cad)
                             & (df.cost_bps == rung) & (df.cap == p.cap)
                             & (df.gross == p.gross)].set_index("comparand")
                    wf.append(dict(window=win, panel=pname, cadence=cad, cost_bps=rung,
                                   chooser=ch, pick_cap=p.cap, pick_gross=p.gross,
                                   OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe,
                                   OOS_MaxDD=p.OOS_MaxDD,
                                   base_OOS_CAGR=p.base_OOS_CAGR,
                                   base_OOS_Sharpe=p.base_OOS_Sharpe,
                                   base_OOS_MaxDD=p.base_OOS_MaxDD,
                                   spy_OOS_CAGR=sel.loc["SPY"].x_OOS_CAGR,
                                   spy_OOS_Sharpe=sel.loc["SPY"].x_OOS_Sharpe,
                                   spy_OOS_MaxDD=sel.loc["SPY"].x_OOS_MaxDD,
                                   ewbh_OOS_CAGR=sel.loc["EWBH"].x_OOS_CAGR,
                                   ewbh_OOS_Sharpe=sel.loc["EWBH"].x_OOS_Sharpe,
                                   ewbh_OOS_MaxDD=sel.loc["EWBH"].x_OOS_MaxDD,
                                   beats_base=bool(p.OOS_Sharpe > p.base_OOS_Sharpe),
                                   beats_spy=bool(p.OOS_Sharpe > sel.loc["SPY"].x_OOS_Sharpe),
                                   beats_ewbh=bool(p.OOS_Sharpe > sel.loc["EWBH"].x_OOS_Sharpe),
                                   beats_ewrb=bool(p.OOS_Sharpe > sel.loc["EWRB"].x_OOS_Sharpe),
                                   full4b_spy=bool(sel.loc["SPY"].pass4b),
                                   full4b_ewbh=bool(sel.loc["EWBH"].pass4b),
                                   full4bS_ewbh=bool(sel.loc["EWBH"].pass4b_strict),
                                   full4b_ewrb=bool(sel.loc["EWRB"].pass4b)))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("  window panel | picks (cap/g)               | OOS CAGR | OOS Sharpe | OOS MaxDD |"
        " > live | > SPY | > EWBH | > EWRB | full4b SPY | full4b EWBH")
    for win, pname, _ in arms:
        q = wfd[(wfd.window == win) & (wfd.panel == pname)]
        top = q.groupby(["pick_cap", "pick_gross"]).size().sort_values(ascending=False)
        desc = ", ".join(f"{a}/{b:.2f}:{c}" for (a, b), c in top.items())
        say(f"  {win:6s} {pname:5s} | {desc:27s} | {q.OOS_CAGR.mean():8.2%} |"
            f" {q.OOS_Sharpe.mean():10.4f} | {q.OOS_MaxDD.mean():9.2%} |"
            f" {int(q.beats_base.sum()):3d}/{len(q):<3d}| {int(q.beats_spy.sum()):2d}/{len(q):<3d}|"
            f" {int(q.beats_ewbh.sum()):3d}/{len(q):<3d}| {int(q.beats_ewrb.sum()):3d}/{len(q):<3d}|"
            f" {int(q.full4b_spy.sum()):6d}/{len(q):<4d}| {int(q.full4b_ewbh.sum()):7d}/{len(q)}")
    for win, pname, _ in arms:
        q = wfd[(wfd.window == win) & (wfd.panel == pname)]
        say(f"  {win}/{pname} OOS (2017-2026, read ONCE): pick {q.OOS_CAGR.mean():.2%} /"
            f" {q.OOS_Sharpe.mean():.4f} / {q.OOS_MaxDD.mean():.2%}  |  live baseline"
            f" {q.base_OOS_CAGR.mean():.2%} / {q.base_OOS_Sharpe.mean():.4f} /"
            f" {q.base_OOS_MaxDD.mean():.2%}  |  SPY {q.spy_OOS_CAGR.mean():.2%} /"
            f" {q.spy_OOS_Sharpe.mean():.4f} / {q.spy_OOS_MaxDD.mean():.2%}  |  EWBH"
            f" {q.ewbh_OOS_CAGR.mean():.2%} / {q.ewbh_OOS_Sharpe.mean():.4f} /"
            f" {q.ewbh_OOS_MaxDD.mean():.2%}")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
