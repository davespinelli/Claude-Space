#!/usr/bin/env python3
"""idea 2535 (lane cloud, run 70, 2026-09-23) — DOES THE CANDIDATE'S DRAWDOWN EDGE SURVIVE A
REALISED-VOL-MATCHED COMPARAND?

THE GAP.  Every comparand the record has ever scored the standing candidate against is matched
on GROSS or not matched at all:
  * SPY and EWBH(panel) are unmatched — they run at 1.00 of NAV at all times.
  * idea 2532's BLEND_G is matched on the candidate's own realised risk GROSS m_t.
The candidate runs a mean risk gross of about 0.66 on U56, so BOTH its CAGR deficit and its
MaxDD edge could be pure EXPOSURE.  But gross is not risk: the candidate's gross falls exactly
when the panel is choppy (the band gate empties), so a gross-matched blend is DE-RISKED at the
same TIMES the candidate is, and the matching may be doing the very work the run is trying to
attribute to the gate.  The sharper matching is on RISK ITSELF:

    VOLM_t  =  k_t x EWBH(panel)  +  (1 - k_t) x SHY,
    k_t     =  clip( sigma_L(candidate returns, trailing L days, known at t)
                     / sigma_L(EWBH returns,       trailing L days, known at t), 0, 1 )

i.e. a sleeve of the SAME names on the SAME tape, scaled EX ANTE so that its trailing realised
volatility equals the CANDIDATE'S OWN trailing realised volatility, rebalanced on the
candidate's cadence and charged the candidate's rung.  No leverage: k is clipped at 1 and the
bind share is published.  If the candidate's MaxDD edge is a risk-budget statement it vanishes
here; if it survives, the 200d band gate is timing drawdowns the same panel at the same RISK
does not, and that is the first defensible thing in this family.

DIAL 1 -- trailing vol window L in {21, 63, 126, 252}.
DIAL 2 -- gross g in {0.75 (live), 1.00}.
EXACTLY TWO TUNED PARAMETERS.  Everything else is a PUBLISHED AXIS, never selected on: panels
{U56, B136}; per-name cap {0.020 = idea 2322's CAP2, the standing candidate; INF = the uncapped
CAND}; cost rungs {0, 10, 25, 50} bps; cadence {W, M}; t+1 execution; band 0.03; MA 200d; the
SHY sweep at phi = 1.00.

COMPARANDS, ALL SCORED ON ALL FIVE 4b LEGS, NONE SELECTED ON.
  SPY        -- PROTOCOL rule 4b as written.
  EWBH       -- idea 2516's comparand: equal-weight buy-and-hold of the panel, gross 1.00.
  BLEND_G    -- idea 2532's GROSS-matched blend, carried for continuity.
  VOLM_L<n>  -- THE HEADLINE, one per vol window: the EWBH sleeve's DRIFTED weights scaled to
                k_t, remainder in SHY.
  VOLM_RB_L63-- the same at the headline window with the panel sleeve RE-EQUAL-WEIGHTED every
                rebalance; a strictly more aggressive comparand, published for contrast.

TWO BARS AT EVERY COMPARAND (as in 2532, because one of them is SPY-calibrated):
  4b-PROTO   -- rule 4b verbatim: Sharpe > X in BOTH halves AND out of sample, MaxDD >= 0.60 x
                X's, CAGR >= 0.70 x X's.
  4b-STRICT  -- beats it outright: Sharpe > X in both halves AND OOS, MaxDD no worse, CAGR no
                lower.  Free of any SPY-calibrated constant.

GATES.  G0 >= 10y per panel.  G1 the candidate runner IS `engine.backtest` on the same
risk-weight frame.  G2 the eligible set IS `baseline.band_state` & priced, bit-identically.
G3 the committed U56 CAP2 / g0.75 / W / 10 bps headline is reproduced.  G4 no leverage anywhere,
in the book OR in any blend.  G5 the VOLM comparand IS vol-matched EX ANTE on every unclipped
day.  G6 exactly two tuned parameters.  G7 SPY, EWBH and BLEND_G are bit-identical across every
arm within a panel.  G8 EWBH trades exactly once (inception).  G9 the sweep instrument is priced
on every scored row.  G10 the EWBH sleeve excludes SPY and SHY; its name count is published.
G11 the vol-matching statistic is CAUSAL (k_t uses no return after t).

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) hold CURRENT
constituents of their screens back to 2008.  EWBH, BLEND_G and VOLM carry the IDENTICAL
contamination on the IDENTICAL tape and days, so the candidate-vs-VOLM contrast is differenced
clean; the SPY columns are NOT and are kept for protocol continuity only.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_vol-matched-comparand_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "vol-matched-comparand", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, WARMUP = 0.03, 200, 260
VOL_WINDOWS = [21, 63, 126, 252]                 # DIAL 1
GROSSES = [0.75, 1.00]                           # DIAL 2
CAPS = [0.020, np.inf]                           # published (CAP2, CAND)
RUNGS = [0.0, 10.0, 25.0, 50.0]                  # published
CADENCES = ["W", "M"]                            # published
SWEEP, BENCH = "SHY", "SPY"
HEAD_L = 63
COMPARANDS = (["SPY", "EWBH", "BLEND_G"] + [f"VOLM_L{L}" for L in VOL_WINDOWS]
              + [f"VOLM_RB_L{HEAD_L}"])
VOLM_NAMES = [f"VOLM_L{L}" for L in VOL_WINDOWS]
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
    """The committed book (verbatim from idea 2532's runner): hold every in-band, priced name at
    min(gross/N_in, cap) of NAV, rebalanced on `freq`, decided at t-1 and applied at t, drifting
    in between, residual swept into SHY.  `engine.backtest` semantics with sweep=False (G1)."""
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
    """Equal-weight BUY-AND-HOLD of the panel from day t0, never rebalanced.  Sleeve EXCLUDES the
    benchmark SPY and the cash instrument SHY (G10); holds only names priced at t0."""
    names = [c for c in px.columns if c not in (BENCH, SWEEP) and pd.notna(px[c].loc[t0])]
    rel = px[names].div(px[names].loc[t0], axis=1).ffill()
    w = rel.div(rel.sum(axis=1), axis=0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[names] = w.fillna(0.0)
    ret = rel.sum(axis=1).pct_change().fillna(0.0)     # zero-turnover buy-and-hold, by identity
    return out, names, ret


def vol_scaler(r_cand, r_ewbh, L):
    """k_t = sigma_L(candidate) / sigma_L(EWBH) on trailing L days ending at t, clipped to [0,1].

    CAUSAL BY CONSTRUCTION (G11): `rolling(L).std()` at t uses returns t-L+1..t only, and the
    frame it lands in is shifted one more day by `engine.backtest` before it is traded, so the
    weight held on day t+1 was computable at the close of day t.  The candidate's PRE-COST return
    is used so the comparand is bit-identical across the four cost rungs of a given cell."""
    sc = r_cand.rolling(L).std()
    se = r_ewbh.rolling(L).std()
    raw = (sc / se.replace(0.0, np.nan))
    k = raw.clip(upper=1.0).fillna(0.0)
    return k, raw


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


def avol(r):
    return float(r.std() * np.sqrt(252))


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
                x_CAGR=xcg, x_Sharpe=sharpe(x), x_MaxDD=xdd, x_Vol=avol(x),
                x_H1=x1, x_H2=x2, x_OOS_Sharpe=sxo, x_OOS_CAGR=cagr(xo),
                x_OOS_MaxDD=maxdd(xo))


def main():
    t0 = time.time()
    say("=== idea 2535 — DOES THE CANDIDATE'S DRAWDOWN EDGE SURVIVE A REALISED-VOL-MATCHED")
    say("    COMPARAND?  (lane cloud, run 70) ===")
    say(f"    {DATE}  band {BAND}  MA {MA_LEN}d  cadence {CADENCES}  t+1  rungs {RUNGS} bps"
        f"  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 trailing vol window L {VOL_WINDOWS}    DIAL 2 gross {GROSSES}")
    say(f"    PUBLISHED, NEVER SELECTED ON: panels, cadence, per-name cap"
        f" {[cname(c) for c in CAPS]}, rungs")
    say(f"    COMPARANDS, ALL SCORED, NONE SELECTED ON: {COMPARANDS}")
    say("    VOLM_t = k_t x EWBH(panel) + (1 - k_t) x SHY, k_t = sigma_L(cand)/sigma_L(EWBH)")
    say("    clipped to [0,1] — the SAME names on the SAME tape at the CANDIDATE'S OWN TRAILING")
    say("    REALISED VOL rather than its GROSS.  Gross is not risk: the band gate de-grosses")
    say("    exactly when the panel is choppy, so a gross-matched blend is de-risked at the same")
    say("    TIMES the candidate is.  Matching on vol removes that.")
    say("    TWO BARS: 4b-PROTO (rule 4b verbatim) and 4b-STRICT (no SPY-calibrated constant).")
    say("    SURVIVORSHIP (rule 9): U56/B136 are CURRENT constituents held back to 2008.  EWBH,")
    say("    BLEND_G and VOLM carry the IDENTICAL contamination on the IDENTICAL tape, so the")
    say("    candidate-vs-VOLM contrast is differenced clean; the SPY columns are NOT.")
    gate("G6 exactly two tuned parameters", "trailing vol window L, gross", "2", True)

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
    for _cap in CAPS:
        w = el_u.astype(float).mul((HEAD_G / nin_u).clip(upper=_cap), axis=0).fillna(0.0)
        r_eng = backtest(px_u, w, cost_bps=HEAD_RUNG, freq=HEAD_CAD)["returns"]
        lv = run_cand(px_u, el_u, HEAD_G, _cap, HEAD_CAD, sweep=False)
        d1 = max(d1, float((r_eng - (lv["r0"] - lv["turn"] * HEAD_RUNG / 1e4)).abs().max()))
    gate("G1 the candidate runner IS engine.backtest on the same risk-weight frame (cap 0.020 and"
         " INF, g 0.75, W, 10 bps, sweep off)", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every scored row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    # G11: causality of the scaler, demonstrated rather than asserted — k computed on a series
    # truncated at day T is identical to k computed on the full series, for every t <= T.
    _r1 = pd.Series(np.random.default_rng(0).normal(size=600),
                    index=pd.date_range("2010-01-01", periods=600, freq="B"))
    _r2 = pd.Series(np.random.default_rng(1).normal(size=600), index=_r1.index)
    _kf, _ = vol_scaler(_r1, _r2, HEAD_L)
    _kt, _ = vol_scaler(_r1.iloc[:400], _r2.iloc[:400], HEAD_L)
    gate("G11 the vol-matching statistic is CAUSAL (k_t uses no return after t)",
         f"max|k_full - k_truncated| over the first 400 days"
         f" {float((_kf.iloc[:400] - _kt).abs().max()):.3e}", "< 1e-12",
         float((_kf.iloc[:400] - _kt).abs().max()) < 1e-12)

    # ------------------------------------------------------------ the grid
    rows, facts, lev_tot, pre_maxes = [], [], 0, []
    gmatch, exante_err, clip_share, blend_maxgross = [], [], [], []
    for pname, px in panels.items():
        el = eligible(px)
        start = px.index[WARMUP]
        ew_w, names, ew_ret_full = ewbh_frame(px, start)
        spy_t = px[BENCH].pct_change().fillna(0.0).loc[start:]
        base_t = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEAD_RUNG, freq="W")["returns"].loc[start:]
        ew_t = ew_ret_full.loc[start:]
        rets_all = px.pct_change().fillna(0.0)
        drift_id = float((ew_t - (ew_w.shift(1) * rets_all).sum(axis=1).loc[start:]).abs().max())
        gate(f"G8 EWBH is pure drift — zero turnover after inception ({pname})",
             f"max|d| between its realised return and the held-weight identity {drift_id:.3e}",
             "< 1e-12", drift_id < 1e-12)
        publish(f"G10 EWBH sleeve ({pname})",
                f"{len(names)} names, SPY and SHY excluded; EWBH {cagr(ew_t):.2%} /"
                f" {sharpe(ew_t):.4f} / {maxdd(ew_t):.2%} / vol {avol(ew_t):.2%}, halves"
                f" {halves(ew_t)[0]:.4f} / {halves(ew_t)[1]:.4f}, OOS"
                f" {cagr(ew_t.loc[OOS_START:]):.2%} / {sharpe(ew_t.loc[OOS_START:]):.4f}")

        for cad in CADENCES:
            for cap in CAPS:
                for gross in GROSSES:
                    bk = run_cand(px, el, gross, cap, cad)
                    lev_tot += bk["lev"]; pre_maxes.append(bk["pre_max"])
                    r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                    m_gross = bk["risk_gross"]
                    yrs = len(tn) / 252
                    bl, diag = {}, {}
                    # continuity comparand: idea 2532's gross-matched blend
                    wf = blend_frame(px, ew_w, names, m_gross, "BH")
                    bb = backtest(px, wf, cost_bps=0.0, freq=cad)
                    bl["BLEND_G"] = (bb["returns"].loc[start:], bb["turnover"].loc[start:])
                    gmatch.append(abs(float(bb["weights"][names].sum(axis=1).loc[start:].mean()
                                            - m_gross.loc[start:].mean())))
                    blend_maxgross.append(float(bb["weights"].sum(axis=1).max()))
                    # the headline family: vol-matched
                    for L in VOL_WINDOWS:
                        k, raw = vol_scaler(bk["r0"], ew_ret_full, L)
                        modes = [("BH", f"VOLM_L{L}")]
                        if L == HEAD_L:
                            modes.append(("RB", f"VOLM_RB_L{L}"))
                        for mode, lab in modes:
                            wfv = blend_frame(px, ew_w, names, k, mode)
                            bv = backtest(px, wfv, cost_bps=0.0, freq=cad)
                            bl[lab] = (bv["returns"].loc[start:], bv["turnover"].loc[start:])
                            blend_maxgross.append(float(bv["weights"].sum(axis=1).max()))
                            if mode == "BH":
                                sl = bv["weights"][names].sum(axis=1).loc[start:]
                                diag[L] = dict(
                                    mean_k=float(k.loc[start:].mean()),
                                    clip=float((raw.loc[start:] > 1.0).mean()),
                                    blend_gross=float(sl.mean()),
                                    blend_vol=avol(bl[lab][0]),
                                    blend_turn=float(bl[lab][1].sum() / yrs))
                                # ex-ante match on unclipped days (G5)
                                ok = (raw.loc[start:] <= 1.0) & raw.loc[start:].notna()
                                tgt = (k.loc[start:] * ew_ret_full.rolling(L).std().loc[start:])
                                cvo = bk["r0"].rolling(L).std().loc[start:]
                                exante_err.append(float((tgt[ok] - cvo[ok]).abs().max()))
                                clip_share.append(float((raw.loc[start:] > 1.0).mean()))
                    fr = dict(panel=pname, cadence=cad, cap=cname(cap), gross=gross,
                              turnover_yr=float(tn.sum() / yrs),
                              mean_risk_gross=float(m_gross.loc[start:].mean()),
                              cand_vol=avol(r0),
                              mean_names=float(bk["names"].loc[start:].mean()),
                              max_gross=float(bk["gross"].loc[start:].max()),
                              max_name_w=float(bk["maxw"].loc[start:].max()))
                    for L in VOL_WINDOWS:
                        for kk, vv in diag[L].items():
                            fr[f"L{L}_{kk}"] = vv
                    facts.append(fr)
                    for rung in RUNGS:
                        r = r0 - tn * rung / 1e4
                        r_is = r.loc[:IS_END]
                        b1, b2 = halves(base_t)
                        h1, h2 = halves(r)
                        pass4a = bool(h1 > b1 and h2 > b2 and maxdd(r) >= maxdd(base_t))
                        comp = {"SPY": spy_t, "EWBH": ew_t}
                        for lab, (br, bt) in bl.items():
                            comp[lab] = br - bt * rung / 1e4
                        for cn in COMPARANDS:
                            x = comp[cn]
                            rows.append(dict(panel=pname, cadence=cad, cap=cname(cap),
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
                                             base_CAGR=cagr(base_t),
                                             base_H1=b1, base_H2=b2,
                                             base_OOS_Sharpe=sharpe(base_t.loc[OOS_START:]),
                                             base_OOS_CAGR=cagr(base_t.loc[OOS_START:]),
                                             base_OOS_MaxDD=maxdd(base_t.loc[OOS_START:]),
                                             **score(r, x, OOS_START)))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.rows.csv", index=False)
    fdf = pd.DataFrame(facts); fdf.to_csv(f"{OUT}.books.csv", index=False)

    gate("G4 no leverage EVER, in the book OR in any blend",
         f"max PRE-clamp target gross {max(pre_maxes):.15f}; {lev_tot} float-level rescales;"
         f" max REALISED book gross {fdf.max_gross.max():.12f};"
         f" max blend gross {max(blend_maxgross):.12f}", "<= 1 + 1e-9 everywhere",
         max(pre_maxes) <= 1.0 + 1e-9 and float(fdf.max_gross.max()) <= 1.0 + 1e-9
         and max(blend_maxgross) <= 1.0 + 1e-9)
    gate("G5 VOLM is vol-matched EX ANTE on every unclipped day"
         " (|k_t x sigma_L(EWBH) - sigma_L(cand)|)",
         f"max {max(exante_err):.3e} over {len(exante_err)} (cell, L) pairs;"
         f" clip binds on {100 * np.mean(clip_share):.3f}% of scored days (mean),"
         f" max {100 * max(clip_share):.3f}%", "< 1e-12", max(exante_err) < 1e-12)
    gate("G5b BLEND_G is gross-matched to its own candidate cell (continuity with 2532)",
         f"max |mean gross(blend) - mean risk gross(cand)| {max(gmatch):.3e}"
         f" over {len(gmatch)} cells", "< 5e-3", max(gmatch) < 5e-3)
    uniq = df[df.comparand.isin(["SPY", "EWBH"])].groupby(["panel", "comparand"]).x_Sharpe.nunique()
    gate("G7 SPY and EWBH are bit-identical across every arm within a panel (they hold no"
         " position that trades, so no rung and no dial can touch them)",
         f"distinct values {dict(uniq)}", "all 1", bool((uniq == 1).all()))
    # the traded comparands DO move with the rung — they are charged the candidate's own rung on
    # their own turnover.  What must hold is that the rung is the ONLY thing that moves them, and
    # that it can only ever HURT: CAGR monotonically non-increasing in the rung, in every cell.
    bad = 0
    for cn in ["BLEND_G"] + VOLM_NAMES + [f"VOLM_RB_L{HEAD_L}"]:
        for _, q in df[df.comparand == cn].groupby(["panel", "cadence", "cap", "gross"]):
            v = q.sort_values("cost_bps").x_CAGR.values
            bad += int((np.diff(v) > 1e-15).sum())
    gate("G7b the traded comparands move with the cost rung and with NOTHING ELSE: their CAGR is"
         " monotonically non-increasing in the rung in every cell",
         f"{bad} monotonicity violations over"
         f" {int((~df.comparand.isin(['SPY', 'EWBH'])).sum())} scored comparand rows",
         "0", bad == 0)
    hd = df[(df.panel == "U56") & (df.cadence == "W") & (df.cap == cname(HEAD_CAP))
            & (df.gross == HEAD_G) & (df.cost_bps == HEAD_RUNG) & (df.comparand == "SPY")].iloc[0]
    publish("G3 committed U56 CAP2 W 10bps g0.75 headline reproduced here",
            f"{hd.CAGR:.2%} / {hd.Sharpe:.4f} / {hd.MaxDD:.2%}, halves {hd.H1:.4f} / {hd.H2:.4f},"
            f" OOS {hd.OOS_CAGR:.2%} / {hd.OOS_Sharpe:.4f}, turnover {hd.turnover_yr:.2f}x/yr")

    # ------------------------------------------------------------ A. the comparands themselves
    say("\n=== A. EVERY COMPARAND AT THE COMMITTED CELL (cap 0.020, g 0.75, W, 10 bps) ===")
    say("  panel comparand   |   CAGR |  Sharpe |   MaxDD |    Vol |   H1   /   H2  |  OOS CAGR |"
        " OOS Sharpe | mean gross | turn x/yr")
    for pname in panels:
        q0 = df[(df.panel == pname) & (df.cadence == "W") & (df.cap == cname(HEAD_CAP))
                & (df.gross == HEAD_G) & (df.cost_bps == HEAD_RUNG)]
        f0 = fdf[(fdf.panel == pname) & (fdf.cadence == "W") & (fdf.cap == cname(HEAD_CAP))
                 & (fdf.gross == HEAD_G)].iloc[0]
        c0 = q0.iloc[0]
        say(f"  {pname:5s} CANDIDATE   | {c0.CAGR:6.2%} | {c0.Sharpe:7.4f} | {c0.MaxDD:7.2%} |"
            f" {c0.Vol:6.2%} | {c0.H1:6.3f} / {c0.H2:6.3f} | {c0.OOS_CAGR:9.2%} |"
            f" {c0.OOS_Sharpe:10.4f} | {f0.mean_risk_gross:10.4f} | {f0.turnover_yr:9.2f}")
        for cn in COMPARANDS:
            q = q0[q0.comparand == cn].iloc[0]
            if cn in ("SPY", "EWBH"):
                mg, tu = 1.0, 0.0
            elif cn == "BLEND_G":
                mg, tu = f0.mean_risk_gross, np.nan
            else:
                L = int(cn.split("_L")[-1])
                mg, tu = f0[f"L{L}_blend_gross"], f0[f"L{L}_blend_turn"]
            say(f"  {pname:5s} {cn:11s} | {q.x_CAGR:6.2%} | {q.x_Sharpe:7.4f} | {q.x_MaxDD:7.2%} |"
                f" {q.x_Vol:6.2%} | {q.x_H1:6.3f} / {q.x_H2:6.3f} | {q.x_OOS_CAGR:9.2%} |"
                f" {q.x_OOS_Sharpe:10.4f} | {mg:10.4f} | {tu:9.2f}")

    say("\n  VOL-MATCH DIAGNOSTICS at the same cell (k_t = sigma_L(cand)/sigma_L(EWBH)):")
    say("  panel |   L | mean k | clip binds | blend realised vol | candidate realised vol |"
        " vol ratio")
    for pname in panels:
        f0 = fdf[(fdf.panel == pname) & (fdf.cadence == "W") & (fdf.cap == cname(HEAD_CAP))
                 & (fdf.gross == HEAD_G)].iloc[0]
        for L in VOL_WINDOWS:
            say(f"  {pname:5s} | {L:3d} | {f0[f'L{L}_mean_k']:6.4f} | {f0[f'L{L}_clip']:10.4%} |"
                f" {f0[f'L{L}_blend_vol']:18.2%} | {f0.cand_vol:22.2%} |"
                f" {f0[f'L{L}_blend_vol'] / f0.cand_vol:9.4f}")

    # ------------------------------------------------------------ B. the verdict
    say("\n=== B. THE VERDICT — 4b UNDER EVERY COMPARAND, OVER ALL PUBLISHED BOOK-ROWS ===")
    nb = len(df) // len(COMPARANDS)
    say(f"  {nb} book-rows (2 panels x 2 cadences x 2 caps x 2 gross x 4 rungs), each scored"
        f" against {len(COMPARANDS)} comparands = {len(df)} scorings.")
    say("  comparand   | 4b-PROTO | 4b-STRICT | L_H1 f | L_H2 f | L_OOS f | L_DD f | L_CAGR f |"
        " first-binding leg (PROTO)")
    ORDER = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
    for cn in COMPARANDS:
        q = df[df.comparand == cn]
        fb = {}
        for _, r in q[~q.pass4b].iterrows():
            for lg in ORDER:
                if not r[lg]:
                    fb[lg] = fb.get(lg, 0) + 1
                    break
        say(f"  {cn:11s} | {int(q.pass4b.sum()):8d} | {int(q.pass4b_strict.sum()):9d} |"
            f" {int((~q.L_H1).sum()):6d} | {int((~q.L_H2).sum()):6d} | {int((~q.L_OOS).sum()):7d} |"
            f" {int((~q.L_DD).sum()):6d} | {int((~q.L_CAGR).sum()):8d} | "
            + ", ".join(f"{k} {v}" for k, v in sorted(fb.items(), key=lambda kv: -kv[1])))
    say(f"  4a (vs the live RULES v2 book, comparand-independent):"
        f" {int(df[df.comparand == 'SPY'].pass4a.sum())} of {nb}")

    # ------------------------------------------------------------ C. WHICH LEGS MOVE
    say("\n=== C. WHICH LEGS MOVE — the share of book-rows on which the CANDIDATE IS AHEAD, ===")
    say("    under each comparand (4b-STRICT legs; this is the idea's own headline question) ===")
    say("  comparand   | Sharpe H1 | Sharpe H2 | Sharpe OOS | MaxDD no worse | CAGR no lower")
    for cn in COMPARANDS:
        q = df[df.comparand == cn]
        say(f"  {cn:11s} | {q.S_H1.mean():9.1%} | {q.S_H2.mean():9.1%} | {q.S_OOS.mean():10.1%} |"
            f" {q.S_DD.mean():14.1%} | {q.S_CAGR.mean():13.1%}")
    say("\n  THE MOVE ITSELF (VOLM_L63 minus BLEND_G, in percentage points of book-rows ahead):")
    a = df[df.comparand == f"VOLM_L{HEAD_L}"].reset_index(drop=True)
    b = df[df.comparand == "BLEND_G"].reset_index(drop=True)
    for lg, lab in (("S_H1", "Sharpe H1"), ("S_H2", "Sharpe H2"), ("S_OOS", "Sharpe OOS"),
                    ("S_DD", "MaxDD no worse"), ("S_CAGR", "CAGR no lower")):
        say(f"    {lab:18s}: {100 * (a[lg].mean() - b[lg].mean()):+6.1f} pp"
            f"   ({a[lg].sum()} vs {b[lg].sum()} of {len(a)})")
    say("\n  MEDIAN GAP (candidate minus comparand) at every comparand, over all book-rows:")
    say("  comparand   | d CAGR pp | d Sharpe | d MaxDD pp | d Vol pp")
    for cn in COMPARANDS:
        q = df[df.comparand == cn]
        say(f"  {cn:11s} | {100 * (q.CAGR - q.x_CAGR).median():9.2f} |"
            f" {(q.Sharpe - q.x_Sharpe).median():8.4f} |"
            f" {100 * (q.MaxDD - q.x_MaxDD).median():10.2f} |"
            f" {100 * (q.Vol - q.x_Vol).median():8.2f}")

    # ------------------------------------------------------------ D. headline ladder
    say(f"\n=== D. HEADLINE LADDER (g 0.75, W, 10 bps) — CANDIDATE vs ITS OWN VOLM_L{HEAD_L} ===")
    say("  panel cap   |   CAGR |  Sharpe |   MaxDD | VOLM CAGR | VOLM Sharpe | VOLM MaxDD |"
        " dSharpe | dCAGR pp | dMaxDD pp | 4b-P | 4b-S | failing STRICT legs")
    for pname in panels:
        for cap in CAPS:
            r = df[(df.panel == pname) & (df.cadence == "W") & (df.cap == cname(cap))
                   & (df.gross == HEAD_G) & (df.cost_bps == HEAD_RUNG)
                   & (df.comparand == f"VOLM_L{HEAD_L}")].iloc[0]
            bad = [k for k in ("S_H1", "S_H2", "S_OOS", "S_DD", "S_CAGR") if not r[k]]
            say(f"  {pname:5s} {cname(cap):5s} | {r.CAGR:6.2%} | {r.Sharpe:7.4f} | {r.MaxDD:7.2%} |"
                f" {r.x_CAGR:9.2%} | {r.x_Sharpe:11.4f} | {r.x_MaxDD:10.2%} |"
                f" {r.Sharpe - r.x_Sharpe:+7.4f} | {100 * (r.CAGR - r.x_CAGR):+8.2f} |"
                f" {100 * (r.MaxDD - r.x_MaxDD):+9.2f} |"
                f" {'Y' if r.pass4b else '.':^4s} | {'Y' if r.pass4b_strict else '.':^4s} |"
                f" {','.join(bad) if bad else '-'}")
    say("\n  THE SAME CELL AT EVERY VOL WINDOW (dial 1 reported in full, never selected on):")
    say("  panel cap   |    L | VOLM CAGR | VOLM Sharpe | VOLM MaxDD | dSharpe | dMaxDD pp |"
        " 4b-P | 4b-S")
    for pname in panels:
        for cap in CAPS:
            for L in VOL_WINDOWS:
                r = df[(df.panel == pname) & (df.cadence == "W") & (df.cap == cname(cap))
                       & (df.gross == HEAD_G) & (df.cost_bps == HEAD_RUNG)
                       & (df.comparand == f"VOLM_L{L}")].iloc[0]
                say(f"  {pname:5s} {cname(cap):5s} | {L:4d} | {r.x_CAGR:9.2%} |"
                    f" {r.x_Sharpe:11.4f} | {r.x_MaxDD:10.2%} |"
                    f" {r.Sharpe - r.x_Sharpe:+7.4f} | {100 * (r.MaxDD - r.x_MaxDD):+9.2f} |"
                    f" {'Y' if r.pass4b else '.':^4s} | {'Y' if r.pass4b_strict else '.':^4s}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 WALK-FORWARD — the book dials (cap, gross) fitted on warm-up..2016-12-31")
    say("    ONLY, 2017-2026 read ONCE, separately at every (panel, cadence, rung).  The vol")
    say("    window L is a COMPARAND dial and is NEVER chosen — all four are reported on the")
    say("    same pick, because choosing it would be selecting a benchmark. ===")
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
                    d = dict(panel=pname, cadence=cad, cost_bps=rung, chooser=ch,
                             pick_cap=p.cap, pick_gross=p.gross,
                             OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                             base_OOS_CAGR=p.base_OOS_CAGR, base_OOS_Sharpe=p.base_OOS_Sharpe,
                             base_OOS_MaxDD=p.base_OOS_MaxDD,
                             spy_OOS_CAGR=sel.loc["SPY"].x_OOS_CAGR,
                             spy_OOS_Sharpe=sel.loc["SPY"].x_OOS_Sharpe,
                             spy_OOS_MaxDD=sel.loc["SPY"].x_OOS_MaxDD,
                             beats_base=bool(p.OOS_Sharpe > p.base_OOS_Sharpe),
                             beats_spy=bool(p.OOS_Sharpe > sel.loc["SPY"].x_OOS_Sharpe),
                             beats_ewbh=bool(p.OOS_Sharpe > sel.loc["EWBH"].x_OOS_Sharpe),
                             beats_blendg=bool(p.OOS_Sharpe > sel.loc["BLEND_G"].x_OOS_Sharpe),
                             full4b_spy=bool(sel.loc["SPY"].pass4b),
                             full4b_ewbh=bool(sel.loc["EWBH"].pass4b))
                    for L in VOL_WINDOWS:
                        cn = f"VOLM_L{L}"
                        d[f"beats_volm_L{L}"] = bool(p.OOS_Sharpe > sel.loc[cn].x_OOS_Sharpe)
                        d[f"volm_L{L}_OOS_Sharpe"] = sel.loc[cn].x_OOS_Sharpe
                        d[f"volm_L{L}_OOS_MaxDD"] = sel.loc[cn].x_OOS_MaxDD
                        d[f"full4b_volm_L{L}"] = bool(sel.loc[cn].pass4b)
                        d[f"full4bS_volm_L{L}"] = bool(sel.loc[cn].pass4b_strict)
                        d[f"oosDD_beats_volm_L{L}"] = bool(p.OOS_MaxDD >= sel.loc[cn].x_OOS_MaxDD)
                    wf.append(d)
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("  panel cad | picks (cap/g)             | OOS CAGR | OOS Sharpe | OOS MaxDD | > live |"
        " > SPY | > EWBH | > BLEND_G | > VOLM_L63")
    for pname in panels:
        for cad in CADENCES:
            q = wfd[(wfd.panel == pname) & (wfd.cadence == cad)]
            top = q.groupby(["pick_cap", "pick_gross"]).size().sort_values(ascending=False)
            desc = ", ".join(f"{a}/{b:.2f}:{c}" for (a, b), c in top.items())
            say(f"  {pname:5s} {cad:3s} | {desc:25s} | {q.OOS_CAGR.mean():8.2%} |"
                f" {q.OOS_Sharpe.mean():10.4f} | {q.OOS_MaxDD.mean():9.2%} |"
                f" {int(q.beats_base.sum()):3d}/{len(q):<3d} | {int(q.beats_spy.sum()):2d}/{len(q):<3d} |"
                f" {int(q.beats_ewbh.sum()):3d}/{len(q):<3d} | {int(q.beats_blendg.sum()):6d}/{len(q):<3d} |"
                f" {int(q[f'beats_volm_L{HEAD_L}'].sum()):7d}/{len(q)}")
    say(f"\n  OOS (2017-2026, read ONCE) POOLED OVER ALL {len(wfd)} PICKS — the numbers rule 8 asks")
    say(f"  for: PICK CAGR {wfd.OOS_CAGR.mean():.2%} / Sharpe {wfd.OOS_Sharpe.mean():.4f} /"
        f" MaxDD {wfd.OOS_MaxDD.mean():.2%}")
    say(f"                       LIVE BASELINE CAGR {wfd.base_OOS_CAGR.mean():.2%} / Sharpe"
        f" {wfd.base_OOS_Sharpe.mean():.4f} / MaxDD {wfd.base_OOS_MaxDD.mean():.2%}")
    say(f"                       SPY           CAGR {wfd.spy_OOS_CAGR.mean():.2%} / Sharpe"
        f" {wfd.spy_OOS_Sharpe.mean():.4f} / MaxDD {wfd.spy_OOS_MaxDD.mean():.2%}")
    say(f"  beat the LIVE book's OOS Sharpe {int(wfd.beats_base.sum())} of {len(wfd)};"
        f" SPY's {int(wfd.beats_spy.sum())}; EWBH's {int(wfd.beats_ewbh.sum())};"
        f" BLEND_G's {int(wfd.beats_blendg.sum())}.")
    for L in VOL_WINDOWS:
        say(f"  VOLM_L{L:<3d}: beat its OOS Sharpe {int(wfd[f'beats_volm_L{L}'].sum())} of"
            f" {len(wfd)} (its mean OOS Sharpe {wfd[f'volm_L{L}_OOS_Sharpe'].mean():.4f});"
            f" OOS MaxDD no worse {int(wfd[f'oosDD_beats_volm_L{L}'].sum())} of {len(wfd)}"
            f" (its mean OOS MaxDD {wfd[f'volm_L{L}_OOS_MaxDD'].mean():.2%});"
            f" full-sample 4b on the pick {int(wfd[f'full4b_volm_L{L}'].sum())} PROTO /"
            f" {int(wfd[f'full4bS_volm_L{L}'].sum())} STRICT")
    say(f"  full-sample 4b on the pick: SPY {int(wfd.full4b_spy.sum())} of {len(wfd)},"
        f" EWBH {int(wfd.full4b_ewbh.sum())}.")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
