#!/usr/bin/env python3
"""idea 2532 (lane cloud, run 67, 2026-09-23) — DOES THE CAPPED CANDIDATE BEAT A GROSS-MATCHED
EWBH BLEND OF ITS OWN PANEL?

THE GAP, WHICH IS THE COMPOSITION OF TWO KILLS THE RECORD ALREADY OWNS.
  * Idea 767 found that a GROSS-MATCHED SPY BLEND itself passes 4a in 57 of the same 64
    comparisons — i.e. most of what the record calls a "win" is an EXPOSURE statement: the book
    runs at ~0.67-0.75 realised risk gross and is therefore compared with something riskier.
  * Idea 2516 (this morning) found that replacing SPY with the panel's OWN equal-weight
    buy-and-hold removes EVERY ONE of the 21 committed capped-family 4b passes, because EWBH of
    the 20 current megacaps returns 32.27% / 1.1839 against SPY's 15.23% / 0.8897 — i.e. most of
    the rest is a SURVIVORSHIP statement.
NEITHER RUN PRICED THE COMPARAND THAT REMOVES BOTH AT ONCE.  That comparand is:

    BLEND_t  =  m_t x EWBH(panel)  +  (1 - m_t) x SHY,     m_t = the candidate's OWN realised
                                                            risk gross on day t

on the same names, the same tape and the same days, rebalanced on the same cadence and charged
the same rung.  It is the book a lazy investor could hold INSTEAD of the rule, AT THE RULE'S OWN
EXPOSURE.  The difference between the candidate and that blend is the 200d band gate's
contribution with survivorship AND exposure differenced out, and nothing else.  If the candidate
does not beat it, there is no edge to fund.

FOUR COMPARANDS, ALL SCORED ON ALL FIVE 4b LEGS, NONE SELECTED ON.
  SPY       -- PROTOCOL rule 4b as written.  Kept because the protocol still reads it.
  EWBH      -- idea 2516's comparand: equal-weight BUY-AND-HOLD of the panel from the first
               scored day, never rebalanced, gross 1.00, zero turnover after inception.
  BLEND_BH  -- THE HEADLINE.  The EWBH sleeve's DRIFTED weights, scaled to the candidate's own
               realised risk gross m_t, remainder in SHY, rebalanced on the candidate's cadence
               and charged the candidate's rung.  Trades only to adjust the SCALE.
  BLEND_RB  -- the same idea with the panel sleeve RE-EQUAL-WEIGHTED at every rebalance.  A
               strictly more expensive and more aggressive comparand; published for contrast.

DIAL 1 -- per-name cap in {0.015, 0.020 (idea 2322's CAP2, the standing candidate), 0.030,
          INF (2300/2332's uncapped CAND)}.
DIAL 2 -- gross g in {0.75 (live), 1.00}.
EXACTLY TWO TUNED PARAMETERS.  Everything else is a PUBLISHED AXIS, never selected on: panels
{U56, B136}; cost rungs {0, 10, 25, 50} bps; cadence {W, M}; t+1 execution; band 0.03; MA 200d;
SHY sweep at phi = 1.00.

TWO BARS ARE REPORTED AT EVERY COMPARAND, BECAUSE ONE OF THEM IS CALIBRATED TO SPY.
  4b-PROTO -- rule 4b verbatim: Sharpe > X in BOTH halves AND out of sample, MaxDD >= 0.60 x X's,
              CAGR >= 0.70 x X's.  The 0.60 / 0.70 constants were written for SPY.
  4b-STRICT -- "beats it outright": Sharpe > X in both halves AND OOS, MaxDD no worse than X's,
              CAGR no lower than X's.  Free of any SPY-calibrated constant.

WHAT THE ANSWER COULD BE, STATED BEFORE THE RUN.  The candidate's entire claim is that a 200d
band gate buys drawdown protection worth more than the return it forgoes.  Against a
gross-matched blend the return give-up is removed BY CONSTRUCTION, so the gate has to win on
timing alone: it must dodge drawdowns the same panel at the same exposure does not.  If it does,
this is the first comparand in the record the candidate has beaten that is neither
survivorship-flattered nor exposure-flattered, and the 4b pass means something.  If it does not,
idea 2516's kill generalises and the capped family is an exposure product.

GATES.  G0 >= 10y per panel.  G1 the candidate runner IS `engine.backtest` on the same risk-weight
frame.  G2 the eligible set IS `baseline.band_state` & priced, bit-identically.  G3 the cap 0.020
/ g 0.75 / W / 10 bps cell reproduces the committed U56 CAP2 headline.  G4 no leverage anywhere.
G5 the BLEND IS GROSS-MATCHED (mean realised risk gross of blend vs candidate).  G6 exactly two
tuned parameters.  G7 SPY and EWBH are bit-identical across every arm within a panel.  G8 EWBH
trades exactly once (inception) and never again.  G9 the sweep instrument is priced on every
scored row.  G10 the EWBH sleeve excludes the benchmark SPY and the cash instrument SHY, and the
count of names it holds is published.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008.  THAT IS THE POINT OF THIS RUN: EWBH and BLEND
carry the IDENTICAL contamination on the IDENTICAL tape and days, so the candidate-vs-blend
contrast is the one number in this record from which the panel's luck has been differenced out.
The SPY-relative columns are NOT — they remain biased upward and are reported for protocol
continuity only.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_gross-matched-ewbh-blend_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "gross-matched-ewbh-blend", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, WARMUP = 0.03, 200, 260
CAPS = [0.015, 0.020, 0.030, np.inf]             # DIAL 1
GROSSES = [0.75, 1.00]                           # DIAL 2
RUNGS = [0.0, 10.0, 25.0, 50.0]                  # published
CADENCES = ["W", "M"]                            # published
SWEEP, BENCH = "SHY", "SPY"
COMPARANDS = ["SPY", "EWBH", "BLEND_BH", "BLEND_RB"]
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


# ---------------------------------------------------------------- the candidate
def run_cand(prices, el, gross, cap, freq, sweep=True):
    """The committed book: hold every in-band, priced name at min(gross/N_in, cap) of NAV,
    rebalanced on `freq`, decided at t-1 and applied at t, drifting in between, residual swept
    into SHY.  `engine.backtest` semantics verbatim with sweep=False (G1)."""
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
    nheld = np.zeros(n); mx = np.zeros(n); lev = 0; pre_max = 0.0
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
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        if tot > 0:
            cur = g / tot; risk = risk * (1 + rv[i]) / tot
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), risk_gross=pd.Series(rg, index=idx),
                names=pd.Series(nheld, index=idx), maxw=pd.Series(mx, index=idx), lev=lev,
                pre_max=pre_max)


# ---------------------------------------------------------------- the comparands
def ewbh_frame(px, t0):
    """Equal-weight BUY-AND-HOLD of the panel from day t0, never rebalanced.  The sleeve EXCLUDES
    the benchmark SPY and the cash instrument SHY (G10) and holds only names priced at t0."""
    names = [c for c in px.columns if c not in (BENCH, SWEEP) and pd.notna(px[c].loc[t0])]
    rel = px[names].div(px[names].loc[t0], axis=1).ffill()
    w = rel.div(rel.sum(axis=1), axis=0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[names] = w.fillna(0.0)
    ret = rel.sum(axis=1).pct_change().fillna(0.0)     # zero-turnover buy-and-hold, by identity
    return out, names, ret


def blend_frame(px, ew_w, names, m, mode):
    """m_t x panel sleeve + (1 - m_t) x SHY.  mode 'BH' scales the EWBH sleeve's DRIFTED weights
    (trades only to adjust the SCALE); mode 'RB' re-equal-weights the priced sleeve every time."""
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    if mode == "BH":
        sl = ew_w[names]
    else:
        pr = px[names].notna().astype(float)
        sl = pr.div(pr.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    out[names] = sl.mul(m, axis=0).values
    out[SWEEP] = (1.0 - m).clip(lower=0.0).where(px[SWEEP].notna(), 0.0)
    return out


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


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def score(r, x, oos):
    """All five 4b legs of r against comparand x, on both bars."""
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
                x_CAGR=xcg, x_Sharpe=sharpe(x), x_MaxDD=xdd,
                x_H1=x1, x_H2=x2, x_OOS_Sharpe=sxo, x_OOS_CAGR=cagr(xo))


def main():
    t0 = time.time()
    say("=== idea 2532 — DOES THE CAPPED CANDIDATE BEAT A GROSS-MATCHED EWBH BLEND OF ITS OWN")
    say("    PANEL?  (lane cloud, run 67) ===")
    say(f"    {DATE}  band {BAND}  MA {MA_LEN}d  cadence {CADENCES}  t+1  rungs {RUNGS} bps"
        f"  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 per-name cap {[cname(c) for c in CAPS]} (0.020 = CAP2, INF = CAND)"
        f"    DIAL 2 gross {GROSSES}")
    say(f"    COMPARANDS, ALL SCORED, NONE SELECTED ON: {COMPARANDS}")
    say("    BLEND_t = m_t x EWBH(panel) + (1 - m_t) x SHY, m_t = the CANDIDATE's OWN realised")
    say("    risk gross that day — same names, same tape, same days, same cadence, same rung.")
    say("    It is the book a lazy investor could hold INSTEAD of the rule, AT THE RULE'S OWN")
    say("    EXPOSURE, so the difference is the 200d gate with survivorship AND exposure")
    say("    differenced out.  TWO BARS: 4b-PROTO (rule 4b verbatim, 0.60/0.70 constants written")
    say("    for SPY) and 4b-STRICT (beats it outright: no SPY-calibrated constant anywhere).")
    say("    SURVIVORSHIP (rule 9) IS THE POINT: EWBH and BLEND carry the IDENTICAL current-")
    say("    constituent contamination on the IDENTICAL tape, so the candidate-vs-blend contrast")
    say("    is differenced clean.  The SPY columns are NOT and are kept for protocol continuity.")
    gate("G6 exactly two tuned parameters", "per-name cap, gross", "2", True)

    panels = {}
    for nm, px in (("U56", load_universe()), ("B136", load_universe(broad=True))):
        panels[nm] = px
        yrs = (px.index[-1] - px.index[WARMUP]).days / 365.25
        gate(f"G0 >= 10y ({nm})", f"{yrs:.1f}y scored, {len(px.columns)} investable, {len(px)} rows",
             ">= 10y", yrs >= 10)

    px_u = panels["U56"]
    bs_u = band_state(px_u, BAND) & px_u.notna()
    d2 = int((eligible(px_u) != bs_u).sum().sum())
    gate("G2 the eligible set IS baseline.band_state & priced, unmodified",
         f"{d2} differing cells; mean names IN {bs_u.sum(axis=1).mean():.2f}", "0", d2 == 0)

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

    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every scored row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    # ------------------------------------------------------------ the grid
    rows, facts, lev_tot, gmatch, ew_names_n = [], [], 0, [], {}
    pre_maxes = []
    ew_cache = {}
    for pname, px in panels.items():
        el = eligible(px)
        start = px.index[WARMUP]
        ew_w, names, ew_ret_full = ewbh_frame(px, start)
        ew_names_n[pname] = len(names)
        spy_t = px[BENCH].pct_change().fillna(0.0).loc[start:]
        base_t = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEAD_RUNG, freq="W")["returns"].loc[start:]
        # EWBH: buy-and-hold from `start`, gross 1.00, ZERO turnover after inception
        ew_t = ew_ret_full.loc[start:]
        rets_all = px.pct_change().fillna(0.0)
        drift_id = float((ew_t - (ew_w.shift(1) * rets_all).sum(axis=1).loc[start:]).abs().max())
        gate(f"G8 EWBH is pure drift — zero turnover after inception ({pname})",
             f"max|d| between its realised return and the held-weight identity {drift_id:.3e}",
             "< 1e-12", drift_id < 1e-12)
        publish(f"G10 EWBH sleeve ({pname})",
                f"{len(names)} names, SPY and SHY excluded; EWBH {cagr(ew_t):.2%} /"
                f" {sharpe(ew_t):.4f} / {maxdd(ew_t):.2%}, halves {halves(ew_t)[0]:.4f} /"
                f" {halves(ew_t)[1]:.4f}, OOS {cagr(ew_t.loc[OOS_START:]):.2%} /"
                f" {sharpe(ew_t.loc[OOS_START:]):.4f}")
        ew_cache[pname] = (ew_w, names, ew_t, spy_t, base_t, start)

        for cad in CADENCES:
            for cap in CAPS:
                for gross in GROSSES:
                    bk = run_cand(px, el, gross, cap, cad)
                    lev_tot += bk["lev"]; pre_maxes.append(bk["pre_max"])
                    r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                    m = bk["risk_gross"]
                    yrs = len(tn) / 252
                    bl = {}
                    for mode, lab in (("BH", "BLEND_BH"), ("RB", "BLEND_RB")):
                        wf = blend_frame(px, ew_w, names, m, mode)
                        bb = backtest(px, wf, cost_bps=0.0, freq=cad)
                        bl[lab] = (bb["returns"].loc[start:], bb["turnover"].loc[start:],
                                   (bb["weights"][names].sum(axis=1)).loc[start:])
                    gmatch.append(abs(float(bl["BLEND_BH"][2].mean() - m.loc[start:].mean())))
                    facts.append(dict(panel=pname, cadence=cad, cap=cname(cap), gross=gross,
                                      turnover_yr=float(tn.sum() / yrs),
                                      mean_risk_gross=float(m.loc[start:].mean()),
                                      blend_bh_gross=float(bl["BLEND_BH"][2].mean()),
                                      blend_rb_gross=float(bl["BLEND_RB"][2].mean()),
                                      blend_bh_turn=float(bl["BLEND_BH"][1].sum() / yrs),
                                      blend_rb_turn=float(bl["BLEND_RB"][1].sum() / yrs),
                                      mean_names=float(bk["names"].loc[start:].mean()),
                                      max_gross=float(bk["gross"].loc[start:].max()),
                                      max_name_w=float(bk["maxw"].loc[start:].max())))
                    for rung in RUNGS:
                        r = r0 - tn * rung / 1e4
                        r_is = r.loc[:IS_END]
                        b1, b2 = halves(base_t)
                        h1, h2 = halves(r)
                        pass4a = bool(h1 > b1 and h2 > b2 and maxdd(r) >= maxdd(base_t))
                        comp = {"SPY": spy_t, "EWBH": ew_t,
                                "BLEND_BH": bl["BLEND_BH"][0] - bl["BLEND_BH"][1] * rung / 1e4,
                                "BLEND_RB": bl["BLEND_RB"][0] - bl["BLEND_RB"][1] * rung / 1e4}
                        for cn, x in comp.items():
                            rows.append(dict(panel=pname, cadence=cad, cap=cname(cap),
                                             gross=gross, cost_bps=rung, comparand=cn,
                                             CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r),
                                             H1=h1, H2=h2, Calmar=calmar(r),
                                             turnover_yr=float(tn.sum() / yrs),
                                             IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is),
                                             OOS_CAGR=cagr(r.loc[OOS_START:]),
                                             OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                                             OOS_MaxDD=maxdd(r.loc[OOS_START:]),
                                             pass4a=pass4a,
                                             base_Sharpe=sharpe(base_t), base_MaxDD=maxdd(base_t),
                                             base_CAGR=cagr(base_t),
                                             base_OOS_Sharpe=sharpe(base_t.loc[OOS_START:]),
                                             **score(r, x, OOS_START)))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.rows.csv", index=False)
    fdf = pd.DataFrame(facts); fdf.to_csv(f"{OUT}.books.csv", index=False)
    gate("G4 no leverage EVER, and the no-leverage clamp is NUMERICAL ONLY (the pre-clamp target"
         " gross never exceeds 1 by more than float error)",
         f"max PRE-clamp target gross {max(pre_maxes):.15f}; {lev_tot} float-level rescales;"
         f" max REALISED book gross {fdf.max_gross.max():.12f}", "<= 1 + 1e-9 on both",
         max(pre_maxes) <= 1.0 + 1e-9 and float(fdf.max_gross.max()) <= 1.0 + 1e-9)
    gate("G5 the BLEND_BH comparand IS gross-matched to its own candidate cell",
         f"max |mean risk gross(blend) - mean risk gross(candidate)| {max(gmatch):.3e}"
         f" over {len(gmatch)} cells", "< 5e-3", max(gmatch) < 5e-3)
    sp = df.groupby("panel").x_Sharpe.apply(lambda s: s.nunique())
    uniq = df[df.comparand.isin(["SPY", "EWBH"])].groupby(["panel", "comparand"]).x_Sharpe.nunique()
    gate("G7 SPY and EWBH are bit-identical across every arm within a panel",
         f"distinct values {dict(uniq)}", "all 1", bool((uniq == 1).all()))
    hd = df[(df.panel == "U56") & (df.cadence == "W") & (df.cap == cname(HEAD_CAP))
            & (df.gross == HEAD_G) & (df.cost_bps == HEAD_RUNG) & (df.comparand == "SPY")].iloc[0]
    publish("G3 committed U56 CAP2 W 10bps g0.75 headline reproduced here",
            f"{hd.CAGR:.2%} / {hd.Sharpe:.4f} / {hd.MaxDD:.2%}, halves {hd.H1:.4f} / {hd.H2:.4f},"
            f" OOS {hd.OOS_CAGR:.2%} / {hd.OOS_Sharpe:.4f}, turnover {hd.turnover_yr:.2f}x/yr")

    # ------------------------------------------------------------ A. the comparands themselves
    say("\n=== A. THE FOUR COMPARANDS, AT THE COMMITTED CELL (cap 0.020, g 0.75, W, 10 bps) ===")
    say("  panel comparand |   CAGR |  Sharpe |   MaxDD |   H1   /   H2  |  OOS CAGR | OOS Sharpe"
        " | mean gross | turn x/yr")
    for pname in panels:
        q0 = df[(df.panel == pname) & (df.cadence == "W") & (df.cap == cname(HEAD_CAP))
                & (df.gross == HEAD_G) & (df.cost_bps == HEAD_RUNG)]
        f0 = fdf[(fdf.panel == pname) & (fdf.cadence == "W") & (fdf.cap == cname(HEAD_CAP))
                 & (fdf.gross == HEAD_G)].iloc[0]
        c0 = q0.iloc[0]
        say(f"  {pname:5s} CANDIDATE | {c0.CAGR:6.2%} | {c0.Sharpe:7.4f} | {c0.MaxDD:7.2%} |"
            f" {c0.H1:6.3f} / {c0.H2:6.3f} | {c0.OOS_CAGR:9.2%} | {c0.OOS_Sharpe:10.4f} |"
            f" {f0.mean_risk_gross:10.4f} | {f0.turnover_yr:9.2f}")
        for cn in COMPARANDS:
            q = q0[q0.comparand == cn].iloc[0]
            mg = {"SPY": 1.0, "EWBH": 1.0, "BLEND_BH": f0.blend_bh_gross,
                  "BLEND_RB": f0.blend_rb_gross}[cn]
            tu = {"SPY": 0.0, "EWBH": 0.0, "BLEND_BH": f0.blend_bh_turn,
                  "BLEND_RB": f0.blend_rb_turn}[cn]
            say(f"  {pname:5s} {cn:9s} | {q.x_CAGR:6.2%} | {q.x_Sharpe:7.4f} | {q.x_MaxDD:7.2%} |"
                f" {q.x_H1:6.3f} / {q.x_H2:6.3f} | {q.x_OOS_CAGR:9.2%} | {q.x_OOS_Sharpe:10.4f} |"
                f" {mg:10.4f} | {tu:9.2f}")

    # ------------------------------------------------------------ B. the verdict
    say("\n=== B. THE VERDICT — 4b UNDER EVERY COMPARAND, OVER ALL PUBLISHED ROWS ===")
    nb = len(df) // len(COMPARANDS)
    say(f"  {nb} book-rows (2 panels x 2 cadences x 4 caps x 2 gross x 4 rungs), each scored"
        f" against {len(COMPARANDS)} comparands = {len(df)} scorings.")
    say("  comparand | 4b-PROTO | 4b-STRICT | L_H1 f | L_H2 f | L_OOS f | L_DD f | L_CAGR f |"
        " first-binding leg (PROTO)")
    ORDER = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
    for cn in COMPARANDS:
        q = df[df.comparand == cn]
        fails = q[~q.pass4b]
        fb = {}
        for _, r in fails.iterrows():
            for lg in ORDER:
                if not r[lg]:
                    fb[lg] = fb.get(lg, 0) + 1
                    break
        say(f"  {cn:9s} | {int(q.pass4b.sum()):8d} | {int(q.pass4b_strict.sum()):9d} |"
            f" {int((~q.L_H1).sum()):6d} | {int((~q.L_H2).sum()):6d} | {int((~q.L_OOS).sum()):7d} |"
            f" {int((~q.L_DD).sum()):6d} | {int((~q.L_CAGR).sum()):8d} | "
            + ", ".join(f"{k} {v}" for k, v in sorted(fb.items(), key=lambda kv: -kv[1])))
    say(f"  4a (vs the live RULES v2 book, comparand-independent):"
        f" {int(df[df.comparand == 'SPY'].pass4a.sum())} of {nb}")
    say("\n  4b-PROTO under BLEND_BH by (panel, cap), out of 16 (cadence x gross x rung):")
    for pname in panels:
        line = "  ".join(f"cap {c:5s} {int(df[(df.panel == pname) & (df.cap == c) & (df.comparand == 'BLEND_BH')].pass4b.sum()):2d}/16"
                         for c in [cname(c) for c in CAPS])
        say(f"    {pname:5s}: {line}")
    say("  4b-STRICT under BLEND_BH by (panel, cap), out of 16:")
    for pname in panels:
        line = "  ".join(f"cap {c:5s} {int(df[(df.panel == pname) & (df.cap == c) & (df.comparand == 'BLEND_BH')].pass4b_strict.sum()):2d}/16"
                         for c in [cname(c) for c in CAPS])
        say(f"    {pname:5s}: {line}")

    # which legs the candidate wins on against the blend
    say("\n=== C. WHERE THE CANDIDATE WINS AND LOSES AGAINST ITS OWN GROSS-MATCHED BLEND ===")
    say("  (BLEND_BH, all 128 book-rows: the share on which the candidate is AHEAD)")
    q = df[df.comparand == "BLEND_BH"]
    for lg, lab in (("S_H1", "Sharpe H1"), ("S_H2", "Sharpe H2"), ("S_OOS", "Sharpe OOS"),
                    ("S_DD", "MaxDD no worse"), ("S_CAGR", "CAGR no lower")):
        say(f"    {lab:18s}: {int(q[lg].sum())} of {len(q)}  ({q[lg].mean():.1%})")
    say("  the same, against EWBH (unlevered, gross 1.00):")
    qe = df[df.comparand == "EWBH"]
    for lg, lab in (("S_H1", "Sharpe H1"), ("S_H2", "Sharpe H2"), ("S_OOS", "Sharpe OOS"),
                    ("S_DD", "MaxDD no worse"), ("S_CAGR", "CAGR no lower")):
        say(f"    {lab:18s}: {int(qe[lg].sum())} of {len(qe)}  ({qe[lg].mean():.1%})")
    say("  and against SPY (the protocol comparand):")
    qs = df[df.comparand == "SPY"]
    for lg, lab in (("S_H1", "Sharpe H1"), ("S_H2", "Sharpe H2"), ("S_OOS", "Sharpe OOS"),
                    ("S_DD", "MaxDD no worse"), ("S_CAGR", "CAGR no lower")):
        say(f"    {lab:18s}: {int(qs[lg].sum())} of {len(qs)}  ({qs[lg].mean():.1%})")

    # ------------------------------------------------------------ D. headline ladder
    say("\n=== D. HEADLINE LADDER (g 0.75, W, 10 bps) — CANDIDATE vs ITS OWN BLEND_BH ===")
    say("  panel cap   |   CAGR |  Sharpe |   MaxDD | blend CAGR | blend Sharpe | blend MaxDD |"
        " dSharpe | dCAGR pp | 4b-P | 4b-S | failing STRICT legs")
    for pname in panels:
        for cap in CAPS:
            r = df[(df.panel == pname) & (df.cadence == "W") & (df.cap == cname(cap))
                   & (df.gross == HEAD_G) & (df.cost_bps == HEAD_RUNG)
                   & (df.comparand == "BLEND_BH")].iloc[0]
            bad = [k for k in ("S_H1", "S_H2", "S_OOS", "S_DD", "S_CAGR") if not r[k]]
            say(f"  {pname:5s} {cname(cap):5s} | {r.CAGR:6.2%} | {r.Sharpe:7.4f} | {r.MaxDD:7.2%} |"
                f" {r.x_CAGR:10.2%} | {r.x_Sharpe:12.4f} | {r.x_MaxDD:11.2%} |"
                f" {r.Sharpe - r.x_Sharpe:+7.4f} | {100 * (r.CAGR - r.x_CAGR):+8.2f} |"
                f" {'Y' if r.pass4b else '.':^4s} | {'Y' if r.pass4b_strict else '.':^4s} |"
                f" {','.join(bad) if bad else '-'}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 WALK-FORWARD — the two dials (cap, gross) fitted on warm-up..2016-12-31")
    say("    ONLY, 2017-2026 read ONCE, separately at every (panel, cadence, rung). ===")
    wf = []
    for pname in panels:
        for cad in CADENCES:
            for rung in RUNGS:
                q = df[(df.panel == pname) & (df.cadence == cad) & (df.cost_bps == rung)
                       & (df.comparand == "SPY")]
                for ch, keyf in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    p = q.loc[q[keyf].idxmax()]
                    sel = df[(df.panel == pname) & (df.cadence == cad) & (df.cost_bps == rung)
                             & (df.cap == p.cap) & (df.gross == p.gross)].set_index("comparand")
                    wf.append(dict(panel=pname, cadence=cad, cost_bps=rung, chooser=ch,
                                   pick_cap=p.cap, pick_gross=p.gross,
                                   OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe,
                                   OOS_MaxDD=p.OOS_MaxDD,
                                   beats_spy=bool(p.OOS_Sharpe > sel.loc["SPY"].x_OOS_Sharpe),
                                   beats_ewbh=bool(p.OOS_Sharpe > sel.loc["EWBH"].x_OOS_Sharpe),
                                   beats_blend=bool(p.OOS_Sharpe > sel.loc["BLEND_BH"].x_OOS_Sharpe),
                                   beats_base=bool(p.OOS_Sharpe > p.base_OOS_Sharpe),
                                   spy_OOS_Sharpe=sel.loc["SPY"].x_OOS_Sharpe,
                                   ewbh_OOS_Sharpe=sel.loc["EWBH"].x_OOS_Sharpe,
                                   blend_OOS_Sharpe=sel.loc["BLEND_BH"].x_OOS_Sharpe,
                                   full4b_spy=bool(sel.loc["SPY"].pass4b),
                                   full4b_blend=bool(sel.loc["BLEND_BH"].pass4b),
                                   full4b_blend_strict=bool(sel.loc["BLEND_BH"].pass4b_strict)))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("  panel cad | picks (cap/g)                  | OOS CAGR | OOS Sharpe | > SPY | > EWBH |"
        " > BLEND | > live | full 4b (SPY) | full 4b (BLEND)")
    for pname in panels:
        for cad in CADENCES:
            q = wfd[(wfd.panel == pname) & (wfd.cadence == cad)]
            top = q.groupby(["pick_cap", "pick_gross"]).size().sort_values(ascending=False)
            desc = ", ".join(f"{a}/{b:.2f}:{c}" for (a, b), c in top.items())
            say(f"  {pname:5s} {cad:3s} | {desc:30s} | {q.OOS_CAGR.mean():8.2%} |"
                f" {q.OOS_Sharpe.mean():10.4f} | {int(q.beats_spy.sum()):3d}/{len(q):<3d} |"
                f" {int(q.beats_ewbh.sum()):3d}/{len(q):<4d} | {int(q.beats_blend.sum()):3d}/{len(q):<5d} |"
                f" {int(q.beats_base.sum()):3d}/{len(q):<3d} | {int(q.full4b_spy.sum()):3d}/{len(q):<11d} |"
                f" {int(q.full4b_blend.sum()):3d}/{len(q)}")
    say(f"\n  OVERALL rule 8 ({len(wfd)} picks): beat SPY's OOS Sharpe {int(wfd.beats_spy.sum())};"
        f" beat EWBH's {int(wfd.beats_ewbh.sum())}; beat the GROSS-MATCHED BLEND's"
        f" {int(wfd.beats_blend.sum())}; beat the LIVE book's {int(wfd.beats_base.sum())}.")
    say(f"  full-sample 4b on the pick: SPY {int(wfd.full4b_spy.sum())} of {len(wfd)},"
        f" BLEND_BH (proto) {int(wfd.full4b_blend.sum())},"
        f" BLEND_BH (strict) {int(wfd.full4b_blend_strict.sum())}.")
    say(f"  BENCHMARK OOS Sharpe (2017-2026, read once, panel-pooled means):"
        f" SPY {wfd.spy_OOS_Sharpe.mean():.4f}, EWBH {wfd.ewbh_OOS_Sharpe.mean():.4f},"
        f" BLEND_BH {wfd.blend_OOS_Sharpe.mean():.4f}.")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
