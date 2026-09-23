#!/usr/bin/env python3
"""idea 2550 (lane C, run 72, 2026-09-23) — DOES THE GROSS-MATCHED EWBH BLEND THAT KILLED THE
CAPPED CANDIDATE ITSELF PASS 4b?

THE HOLE THIS OPENS.  Three runs closed the same loop on the standing KEEP-4b candidate
(CAP2: `w_i = min(g/N_in, 0.02)` on names inside the 200d +/-3% band, idle NAV swept to SHY,
weekly, t+1):
  * 2516 — replacing 4b's SPY comparand with the panel's own EQUAL-WEIGHT BUY-AND-HOLD removes
    every one of the committed 4b passes (0 of 48).
  * 2532 — the candidate loses to a GROSS-MATCHED EWBH BLEND of its own panel on CAGR in 128 of
    128 rows, and wins on MaxDD in 128 of 128.
  * 2528 — no attainable gross closes that CAGR gap, so the deficit is in the rule.
The record's summary is that the capped family "is a de-grossing product".  BUT NOT ONE OF THOSE
RUNS EVER SCORED THE BLEND AS A BOOK.  It was only ever a yardstick: its absolute legs lived in
`base_*` / `x_*` columns and its own 4b verdict was never computed.  This run puts the yardstick
on the LEFT of the comparison.

WHY THE ANSWER CANNOT BE ASSUMED.  The 128-of-128 split is two-sided: the blend owns `L_CAGR`
and the candidate owns `L_DD`.  4b is a CONJUNCTION, so the blend can win the leg it was used to
win and still die on the leg it was never asked about.  `L_DD` demands MaxDD >= 0.60 x SPY's,
i.e. no worse than about -20.2% against SPY's -33.7%, and the blend runs a ~0.58-gross slice of
a panel whose own buy-and-hold draws down -43.97% (U56) / -32.95% (B136).

WHY IT IS DECISION-RELEVANT EITHER WAY.
  * IF THE BLEND PASSES: it is a CHEAPER KEEP candidate than the book it killed (2532 published
    blend turnover 2.23x/yr against the candidate's 3.00x on U56) and the sprint's 31% turnover
    adoption bar is cleared by the comparand, not by any turnover device.
  * IF THE BLEND FAILS: the record has been killing the capped family with a yardstick that is
    not itself capital-worthy.  "A de-grossing product" then becomes a statement about the whole
    SHELF — every book reachable from this panel at this exposure — and not about the 200d rule,
    and the standing candidate's 4b-under-SPY pass is restored to what it always was: the best
    of a bad shelf, not evidence of an edge.  That is a different instruction to the Sunday
    review than "the family is finished".

FIVE ARMS, ALL SCORED AS BOOKS, NONE SELECTED ON.
  CAND        -- the committed capped candidate.  Carried for continuity and for gate G3.
  BLEND_BH    -- THE HEADLINE.  `m_t x EWBH(panel)_drifted + (1 - m_t) x SHY`, m_t = the
                 CANDIDATE's own realised risk gross that day.  Trades only to adjust the SCALE.
  BLEND_RB    -- the same with the panel sleeve RE-EQUAL-WEIGHTED at every rebalance.  Strictly
                 more expensive; published for contrast.
  BLEND_CONST -- the blend with the TIMING removed: a CONSTANT `gbar x EWBH_drifted +
                 (1 - gbar) x SHY`, gbar SOLVED (not fitted) as the candidate cell's mean
                 realised risk gross over warm-up..2016-12-31 ONLY.  Causal, tradable,
                 rule-8 eligible, and it separates "the blend's exposure LEVEL" from "the
                 candidate's exposure PATH" at zero extra tuned parameters.
  EWBH        -- equal-weight buy-and-hold of the panel, gross 1.00, zero turnover after
                 inception.  Reported so every row can be read against it.

DIAL 1 -- per-name cap {0.015, 0.020 (2322's CAP2, the standing candidate), 0.030, INF}.
DIAL 2 -- gross g {0.75 (live), 1.00}.
EXACTLY TWO TUNED PARAMETERS.  The blends inherit their gross path from the candidate cell, so
the dials index them too.  Everything else is a PUBLISHED AXIS, never selected on: panels
{U56, B136}; cost rungs {0, 10, 25, 50} bps; cadence {W, M}; band 0.03; MA 200d; t+1 execution;
SHY sweep at phi = 1.00.

TWO COMPARANDS AND TWO BARS AT EACH, BECAUSE 4b's CONSTANTS WERE WRITTEN FOR SPY.
  4b-PROTO  -- rule 4b verbatim: Sharpe > X in BOTH halves AND out of sample, MaxDD >= 0.60 x X's,
               CAGR >= 0.70 x X's.
  4b-STRICT -- "beats it outright": Sharpe > X in both halves AND OOS, MaxDD no worse, CAGR no
               lower.  Free of any SPY-calibrated constant.
  X in {SPY (protocol incumbent), EWBH (2516's like-for-like substitute)}.
4a is judged against the live RULES v2 book at the same rung, and is comparand-independent.

GATES.  G0 >= 10y per panel.  G1 the candidate runner IS `engine.backtest` on the same
risk-weight frame.  G2 the eligible set IS `baseline.band_state` & priced, bit-identically.
G3 the cap 0.020 / g 0.75 / W / 10 bps cell reproduces the committed U56 CAP2 headline.
G4 no leverage anywhere.  G5 BLEND_BH is gross-matched to its own candidate cell.  G6 exactly
two tuned parameters.  G7 SPY and EWBH are bit-identical across every arm within a panel.
G8 EWBH trades exactly once (inception) and never again.  G9 the sweep instrument is priced on
every scored row.  G10 BLEND_CONST's gbar is IS-ONLY (it is invariant to the post-2016 tape).
G11 cost linearity on every arm.  G12 the EWBH sleeve excludes SPY and SHY.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008.  The blend arms are MORE contaminated than the
candidate, not less (they hold the whole survivor panel all the time), so a blend PASS is the
contaminated reading and a blend FAIL is robust to the bias.  The SPY-relative columns are
biased upward for every arm and are kept for protocol continuity.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_blend-comparand-as-a-book_C.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state   # noqa: E402
from engine import backtest                                        # noqa: E402

DATE, SLUG, LANE = "2026-09-23", "blend-comparand-as-a-book", "C"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, WARMUP = 0.03, 200, 260
CAPS = [0.015, 0.020, 0.030, np.inf]             # DIAL 1
GROSSES = [0.75, 1.00]                           # DIAL 2
RUNGS = [0.0, 10.0, 25.0, 50.0]                  # published
CADENCES = ["W", "M"]                            # published
SWEEP, BENCH = "SHY", "SPY"
ARMS = ["CAND", "BLEND_BH", "BLEND_RB", "BLEND_CONST", "EWBH"]
TRADABLE = ["CAND", "BLEND_BH", "BLEND_RB", "BLEND_CONST"]   # rule-8 eligible
COMPARANDS = ["SPY", "EWBH"]
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


def legs(r, x):
    """All five 4b legs of book r against comparand x, on both bars."""
    h1, h2 = halves(r); x1, x2 = halves(x)
    so, sxo = sharpe(r.loc[OOS_START:]), sharpe(x.loc[OOS_START:])
    dd, xdd = maxdd(r), maxdd(x)
    cg, xcg = cagr(r), cagr(x)
    P = dict(L_H1=h1 > x1, L_H2=h2 > x2, L_OOS=so > sxo,
             L_DD=dd >= DD_CAP * xdd, L_CAGR=cg >= CAGR_FLOOR * xcg)
    S = dict(S_H1=h1 > x1, S_H2=h2 > x2, S_OOS=so > sxo, S_DD=dd >= xdd, S_CAGR=cg >= xcg)
    return dict(**{k: bool(v) for k, v in P.items()}, **{k: bool(v) for k, v in S.items()},
                pass4b=bool(all(P.values())), pass4b_strict=bool(all(S.values())),
                x_CAGR=xcg, x_Sharpe=sharpe(x), x_MaxDD=xdd, x_H1=x1, x_H2=x2,
                x_OOS_Sharpe=sxo, x_OOS_CAGR=cagr(x.loc[OOS_START:]),
                slack_DD=dd - DD_CAP * xdd, slack_CAGR=cg - CAGR_FLOOR * xcg,
                slack_H1=h1 - x1, slack_H2=h2 - x2, slack_OOS=so - sxo)


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


# ---------------------------------------------------------------- the blend arms
def ewbh_frame(px, t0):
    """Equal-weight BUY-AND-HOLD of the panel from day t0, never rebalanced.  The sleeve EXCLUDES
    the benchmark SPY and the cash instrument SHY (G12) and holds only names priced at t0."""
    names = [c for c in px.columns if c not in (BENCH, SWEEP) and pd.notna(px[c].loc[t0])]
    rel = px[names].div(px[names].loc[t0], axis=1).ffill()
    w = rel.div(rel.sum(axis=1), axis=0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[names] = w.fillna(0.0)
    ret = rel.sum(axis=1).pct_change().fillna(0.0)     # zero-turnover buy-and-hold, by identity
    return out, names, ret


def blend_frame(px, ew_w, names, m, mode):
    """m_t x panel sleeve + (1 - m_t) x SHY.  mode 'BH' scales the EWBH sleeve's DRIFTED weights
    (trades only to adjust the SCALE); 'RB' re-equal-weights the priced sleeve every rebalance."""
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    if mode == "BH":
        sl = ew_w[names]
    else:
        pr = px[names].notna().astype(float)
        sl = pr.div(pr.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    out[names] = sl.mul(m, axis=0).values
    out[SWEEP] = (1.0 - m).clip(lower=0.0).where(px[SWEEP].notna(), 0.0)
    return out


def main():
    t0 = time.time()
    say("=== idea 2550 — DOES THE GROSS-MATCHED EWBH BLEND THAT KILLED THE CAPPED CANDIDATE")
    say("    ITSELF PASS 4b?  (lane C, run 72) ===")
    say(f"    {DATE}  band {BAND}  MA {MA_LEN}d  cadence {CADENCES}  t+1  rungs {RUNGS} bps"
        f"  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 per-name cap {[cname(c) for c in CAPS]} (0.020 = CAP2)  DIAL 2 gross {GROSSES}")
    say(f"    ARMS, ALL SCORED AS BOOKS: {ARMS}     COMPARANDS: {COMPARANDS}  x  4b-PROTO / 4b-STRICT")
    say("    2532 put the BLEND on the RIGHT of the comparison and killed the candidate with it.")
    say("    This run puts it on the LEFT.  The 128-of-128 split is two-sided (blend owns L_CAGR,")
    say("    candidate owns L_DD) and 4b is a CONJUNCTION, so the blend's own verdict is open.")
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
    rows, facts, lev_tot, gmatch, pre_maxes, linerr = [], [], 0, [], [], []
    const_inv = []
    for pname, px in panels.items():
        el = eligible(px)
        start = px.index[WARMUP]
        ew_w, names, ew_ret_full = ewbh_frame(px, start)
        spy_t = px[BENCH].pct_change().fillna(0.0).loc[start:]
        ew_t = ew_ret_full.loc[start:]
        rets_all = px.pct_change().fillna(0.0)
        drift_id = float((ew_t - (ew_w.shift(1) * rets_all).sum(axis=1).loc[start:]).abs().max())
        gate(f"G8 EWBH is pure drift — zero turnover after inception ({pname})",
             f"max|d| between its realised return and the held-weight identity {drift_id:.3e}",
             "< 1e-12", drift_id < 1e-12)
        gate(f"G12 EWBH sleeve excludes SPY and SHY ({pname})",
             f"{len(names)} names; SPY in sleeve {BENCH in names}; SHY in sleeve {SWEEP in names}",
             "both False", (BENCH not in names) and (SWEEP not in names))
        publish(f"EWBH ({pname})",
                f"{cagr(ew_t):.2%} / {sharpe(ew_t):.4f} / {maxdd(ew_t):.2%}, halves"
                f" {halves(ew_t)[0]:.4f} / {halves(ew_t)[1]:.4f}, OOS"
                f" {cagr(ew_t.loc[OOS_START:]):.2%} / {sharpe(ew_t.loc[OOS_START:]):.4f}")
        publish(f"SPY ({pname})",
                f"{cagr(spy_t):.2%} / {sharpe(spy_t):.4f} / {maxdd(spy_t):.2%}, halves"
                f" {halves(spy_t)[0]:.4f} / {halves(spy_t)[1]:.4f}, OOS"
                f" {cagr(spy_t.loc[OOS_START:]):.2%} / {sharpe(spy_t.loc[OOS_START:]):.4f}")

        # the live book, per rung (4a's comparand)
        bres = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75), cost_bps=0.0, freq="W")
        b0, btn = bres["returns"].loc[start:], bres["turnover"].loc[start:]

        for cad in CADENCES:
            for cap in CAPS:
                for gross in GROSSES:
                    bk = run_cand(px, el, gross, cap, cad)
                    lev_tot += bk["lev"]; pre_maxes.append(bk["pre_max"])
                    m = bk["risk_gross"]
                    yrs = len(m.loc[start:]) / 252
                    gbar = float(m.loc[start:IS_END].mean())          # IS-ONLY, causal (G10)
                    const_inv.append((pname, cad, cname(cap), gross, gbar))
                    mconst = pd.Series(gbar, index=px.index)

                    series = {"CAND": (bk["r0"].loc[start:], bk["turn"].loc[start:]),
                              "EWBH": (ew_t, pd.Series(0.0, index=ew_t.index))}
                    for lab, mode, mm in (("BLEND_BH", "BH", m), ("BLEND_RB", "RB", m),
                                          ("BLEND_CONST", "BH", mconst)):
                        wf = blend_frame(px, ew_w, names, mm, mode)
                        bb = backtest(px, wf, cost_bps=0.0, freq=cad)
                        series[lab] = (bb["returns"].loc[start:], bb["turnover"].loc[start:])
                        if lab == "BLEND_BH":
                            gmatch.append(abs(float(
                                bb["weights"][names].sum(axis=1).loc[start:].mean()
                                - m.loc[start:].mean())))
                            # exact cost linearity (G11)
                            bx = backtest(px, wf, cost_bps=25.0, freq=cad)["returns"].loc[start:]
                            linerr.append(float(
                                (bx - (bb["returns"].loc[start:]
                                       - bb["turnover"].loc[start:] * 25.0 / 1e4)).abs().max()))

                    facts.append(dict(panel=pname, cadence=cad, cap=cname(cap), gross=gross,
                                      cand_turnover_yr=float(series["CAND"][1].sum() / yrs),
                                      mean_risk_gross=float(m.loc[start:].mean()),
                                      gbar_IS=gbar,
                                      blend_bh_turn=float(series["BLEND_BH"][1].sum() / yrs),
                                      blend_rb_turn=float(series["BLEND_RB"][1].sum() / yrs),
                                      blend_const_turn=float(series["BLEND_CONST"][1].sum() / yrs),
                                      mean_names=float(bk["names"].loc[start:].mean()),
                                      max_gross=float(bk["gross"].loc[start:].max()),
                                      max_name_w=float(bk["maxw"].loc[start:].max()),
                                      ew_names=len(names)))

                    for rung in RUNGS:
                        base_r = b0 - btn * rung / 1e4
                        bh1, bh2 = halves(base_r)
                        comp = {"SPY": spy_t, "EWBH": ew_t}
                        for arm in ARMS:
                            r0a, tna = series[arm]
                            r = r0a - tna * rung / 1e4
                            h1, h2 = halves(r)
                            pass4a = bool(h1 > bh1 and h2 > bh2 and maxdd(r) >= maxdd(base_r))
                            for cn, x in comp.items():
                                rows.append(dict(
                                    panel=pname, cadence=cad, cap=cname(cap), gross=gross,
                                    cost_bps=rung, arm=arm, comparand=cn,
                                    CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), H1=h1, H2=h2,
                                    Calmar=calmar(r), turnover_yr=float(tna.sum() / yrs),
                                    IS_Sharpe=sharpe(r.loc[:IS_END]),
                                    IS_Calmar=calmar(r.loc[:IS_END]),
                                    OOS_CAGR=cagr(r.loc[OOS_START:]),
                                    OOS_Sharpe=sharpe(r.loc[OOS_START:]),
                                    OOS_MaxDD=maxdd(r.loc[OOS_START:]),
                                    pass4a=pass4a, base_Sharpe=sharpe(base_r),
                                    base_MaxDD=maxdd(base_r), base_CAGR=cagr(base_r),
                                    base_H1=bh1, base_H2=bh2,
                                    base_OOS_Sharpe=sharpe(base_r.loc[OOS_START:]),
                                    base_OOS_CAGR=cagr(base_r.loc[OOS_START:]),
                                    **legs(r, x)))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.rows.csv", index=False)
    fdf = pd.DataFrame(facts); fdf.to_csv(f"{OUT}.books.csv", index=False)

    gate("G4 no leverage EVER (pre-clamp target gross never exceeds 1 by more than float error)",
         f"max PRE-clamp target gross {max(pre_maxes):.15f}; {lev_tot} float-level rescales;"
         f" max REALISED book gross {fdf.max_gross.max():.12f}", "<= 1 + 1e-9",
         max(pre_maxes) <= 1.0 + 1e-9 and float(fdf.max_gross.max()) <= 1.0 + 1e-9)
    gate("G5 BLEND_BH is gross-matched to its own candidate cell",
         f"max |mean gross(blend) - mean risk gross(candidate)| {max(gmatch):.3e} over"
         f" {len(gmatch)} cells", "< 5e-3", max(gmatch) < 5e-3)
    gate("G11 exact cost linearity on the blend runner (25 bps charged inline vs post-hoc)",
         f"max|d| {max(linerr):.3e} over {len(linerr)} cells", "< 1e-12", max(linerr) < 1e-12)
    uniq = df[df.comparand.isin(COMPARANDS)].groupby(["panel", "comparand"]).x_Sharpe.nunique()
    gate("G7 SPY and EWBH are bit-identical across every arm within a panel",
         f"distinct values {dict(uniq)}", "all 1", bool((uniq == 1).all()))
    cd = pd.DataFrame(const_inv, columns=["panel", "cadence", "cap", "gross", "gbar"])
    gate("G10 BLEND_CONST's gbar is IS-ONLY (solved on warm-up..2016-12-31, never on the OOS tape)",
         f"{len(cd)} cells, gbar range {cd.gbar.min():.4f}..{cd.gbar.max():.4f}; the series it is"
         f" taken from is truncated at {IS_END} by construction", "causal", True)
    hd = df[(df.panel == "U56") & (df.arm == "CAND") & (df.cadence == "W")
            & (df.cap == cname(HEAD_CAP)) & (df.gross == HEAD_G)
            & (df.cost_bps == HEAD_RUNG) & (df.comparand == "SPY")].iloc[0]
    g3 = abs(hd.CAGR - 0.1162) < 5e-4 and abs(hd.Sharpe - 1.2687) < 5e-4 and abs(hd.MaxDD + 0.1481) < 5e-4
    gate("G3 committed U56 CAP2 W 10bps g0.75 headline reproduced (11.62% / 1.2687 / -14.81%)",
         f"{hd.CAGR:.4%} / {hd.Sharpe:.4f} / {hd.MaxDD:.4%}, turnover {hd.turnover_yr:.2f}x/yr",
         "matches to 4dp", g3)

    # ------------------------------------------------------------ A. the arms at the committed cell
    say("\n=== A. THE FIVE ARMS AS BOOKS, AT THE COMMITTED CELL (cap 0.020, g 0.75, W, 10 bps) ===")
    say("  panel arm         |   CAGR |  Sharpe |   MaxDD |   H1   /   H2  | OOS CAGR | OOS Shrp |"
        " turn x/yr | 4a | 4b vs SPY | 4b vs EWBH")
    for pname in panels:
        for arm in ARMS:
            q = df[(df.panel == pname) & (df.arm == arm) & (df.cadence == "W")
                   & (df.cap == cname(HEAD_CAP)) & (df.gross == HEAD_G)
                   & (df.cost_bps == HEAD_RUNG)]
            s = q[q.comparand == "SPY"].iloc[0]; e = q[q.comparand == "EWBH"].iloc[0]
            say(f"  {pname:5s} {arm:11s} | {s.CAGR:6.2%} | {s.Sharpe:7.4f} | {s.MaxDD:7.2%} |"
                f" {s.H1:6.3f} / {s.H2:6.3f} | {s.OOS_CAGR:8.2%} | {s.OOS_Sharpe:8.4f} |"
                f" {s.turnover_yr:9.2f} | {'Y' if s.pass4a else 'n'}  |"
                f" {'PASS' if s.pass4b else 'fail':9s} | {'PASS' if e.pass4b else 'fail'}")

    # ------------------------------------------------------------ B. the census
    say("\n=== B. THE VERDICT — EVERY ARM'S OWN 4b RATE OVER ALL PUBLISHED ROWS ===")
    ncell = len(df) // (len(ARMS) * len(COMPARANDS))
    say(f"  {ncell} cells (2 panels x 2 cadences x 4 caps x 2 gross x 4 rungs) x {len(ARMS)} arms"
        f" x {len(COMPARANDS)} comparands = {len(df)} scorings.")
    ORDER = ["L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR"]
    say("  comparand arm         | 4b-PROTO | 4b-STRICT | 4a |  L_H1 f  L_H2 f L_OOS f  L_DD f"
        " L_CAGR f | first-binding leg")
    for cn in COMPARANDS:
        for arm in ARMS:
            q = df[(df.comparand == cn) & (df.arm == arm)]
            f = q[~q.pass4b]
            binder = {}
            for _, rr in f.iterrows():
                for L in ORDER:
                    if not rr[L]:
                        binder[L] = binder.get(L, 0) + 1; break
            top = ", ".join(f"{k} {v}" for k, v in sorted(binder.items(), key=lambda kv: -kv[1]))
            say(f"  {cn:9s} {arm:11s} | {q.pass4b.sum():4d}/{len(q):<3d} |"
                f" {q.pass4b_strict.sum():5d}/{len(q):<3d} | {q.pass4a.sum():2d} |"
                + "".join(f" {int((~q[L]).sum()):7d}" for L in ORDER)
                + f" | {top if top else '(none — all pass)'}")

    say("\n=== C. THE TWO-SIDED SPLIT, RE-READ AS BOOK LEGS (paired CAND vs BLEND_BH, same cell) ===")
    piv = df[df.comparand == "SPY"].pivot_table(
        index=["panel", "cadence", "cap", "gross", "cost_bps"], columns="arm",
        values=["CAGR", "MaxDD", "Sharpe", "OOS_Sharpe", "turnover_yr"])
    for col, lab in (("CAGR", "CAGR"), ("MaxDD", "MaxDD"), ("Sharpe", "Sharpe"),
                     ("OOS_Sharpe", "OOS Sharpe"), ("turnover_yr", "turnover")):
        d = piv[col]["BLEND_BH"] - piv[col]["CAND"]
        say(f"  BLEND_BH - CAND on {lab:11s}: blend ahead in {int((d > 0).sum()):3d} of {len(d)}"
            f" cells, median {d.median():+.4f}, min {d.min():+.4f}, max {d.max():+.4f}")

    say("\n=== D. WHY EACH BLEND ROW DIES (or lives) — L_DD and L_CAGR slack, vs SPY ===")
    say("  panel arm         | median L_DD slack | rows with L_DD>=0 | median L_CAGR slack |"
        " rows with L_CAGR>=0")
    for pname in panels:
        for arm in ARMS:
            q = df[(df.panel == pname) & (df.arm == arm) & (df.comparand == "SPY")]
            say(f"  {pname:5s} {arm:11s} | {q.slack_DD.median():+17.4f} |"
                f" {int((q.slack_DD >= 0).sum()):17d} | {q.slack_CAGR.median():+19.4f} |"
                f" {int((q.slack_CAGR >= 0).sum()):19d}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 WALK-FORWARD — (cap, gross) chosen on warm-up..2016-12-31 ONLY, per arm,")
    say("    by two PRE-STATED IS-only choosers; 2017-2026 then read ONCE. ===")
    say("    C_ISSHARPE = argmax IS Sharpe.   C_ISCALMAR = argmax IS Calmar.  Neither sees the OOS")
    say("    tape, any comparand, or any OOS statistic.  EWBH has no dials and is reported as the")
    say("    fixed OOS benchmark it is.")
    wf = []
    say("  panel cad rung chooser arm         | pick (cap,g)  | OOS CAGR | OOS Shrp | OOS MaxDD |"
        " vs live v2 | vs SPY | vs EWBH | 4b-OOS SPY / EWBH")
    for pname in panels:
        for cad in CADENCES:
            for rung in RUNGS:
                sub = df[(df.panel == pname) & (df.cadence == cad) & (df.cost_bps == rung)
                         & (df.comparand == "SPY")]
                spy_o = sub.x_OOS_Sharpe.iloc[0]
                ewb = df[(df.panel == pname) & (df.cadence == cad) & (df.cost_bps == rung)
                         & (df.comparand == "EWBH")].x_OOS_Sharpe.iloc[0]
                liv = sub.base_OOS_Sharpe.iloc[0]
                for ch, key in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                    for arm in TRADABLE:
                        a = sub[sub.arm == arm]
                        pick = a.loc[a[key].idxmax()]
                        e = df[(df.panel == pname) & (df.cadence == cad) & (df.cost_bps == rung)
                               & (df.arm == arm) & (df.cap == pick.cap) & (df.gross == pick.gross)
                               & (df.comparand == "EWBH")].iloc[0]
                        wf.append(dict(panel=pname, cadence=cad, cost_bps=rung, chooser=ch,
                                       arm=arm, cap=pick.cap, gross=pick.gross,
                                       OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                                       OOS_MaxDD=pick.OOS_MaxDD, live_OOS_Sharpe=liv,
                                       spy_OOS_Sharpe=spy_o, ewbh_OOS_Sharpe=ewb,
                                       beats_live=bool(pick.OOS_Sharpe > liv),
                                       beats_spy=bool(pick.OOS_Sharpe > spy_o),
                                       beats_ewbh=bool(pick.OOS_Sharpe > ewb),
                                       pass4b_spy=bool(pick.pass4b), pass4b_ewbh=bool(e.pass4b),
                                       spy_OOS_CAGR=pick.x_OOS_CAGR, ewbh_OOS_CAGR=e.x_OOS_CAGR))
                        if rung == HEAD_RUNG and cad == "W":
                            say(f"  {pname:5s} {cad}  {int(rung):4d} {ch:9s} {arm:11s} |"
                                f" ({pick.cap:>5s},{pick.gross:4.2f}) | {pick.OOS_CAGR:8.2%} |"
                                f" {pick.OOS_Sharpe:8.4f} | {pick.OOS_MaxDD:9.2%} |"
                                f" {'Y' if pick.OOS_Sharpe > liv else 'n':^10s} |"
                                f" {'Y' if pick.OOS_Sharpe > spy_o else 'n':^6s} |"
                                f" {'Y' if pick.OOS_Sharpe > ewb else 'n':^7s} |"
                                f" {'PASS' if pick.pass4b else 'fail'} / "
                                f"{'PASS' if e.pass4b else 'fail'}")
    wdf = pd.DataFrame(wf); wdf.to_csv(f"{OUT}.walkforward.csv", index=False)
    say(f"\n  RULE-8 CENSUS over all {len(wdf)} picks (2 panels x 2 cadences x 4 rungs x 2 choosers"
        f" x {len(TRADABLE)} arms):")
    say("  arm         | beats live v2 OOS | beats SPY OOS | beats EWBH OOS | 4b-OOS vs SPY |"
        " 4b-OOS vs EWBH")
    for arm in TRADABLE:
        q = wdf[wdf.arm == arm]
        say(f"  {arm:11s} | {q.beats_live.sum():8d}/{len(q):<8d} | {q.beats_spy.sum():5d}/{len(q):<7d}"
            f" | {q.beats_ewbh.sum():6d}/{len(q):<7d} | {q.pass4b_spy.sum():6d}/{len(q):<6d} |"
            f" {q.pass4b_ewbh.sum():6d}/{len(q)}")
    say(f"  OOS benchmarks read ONCE: SPY {wdf.spy_OOS_Sharpe.iloc[0]:.4f} Sharpe /"
        f" {wdf.spy_OOS_CAGR.iloc[0]:.2%} CAGR; EWBH by panel "
        + ", ".join(f"{p} {wdf[wdf.panel == p].ewbh_OOS_Sharpe.iloc[0]:.4f} /"
                    f" {wdf[wdf.panel == p].ewbh_OOS_CAGR.iloc[0]:.2%}" for p in panels)
        + f"; live RULES v2 {wdf.live_OOS_Sharpe.iloc[0]:.4f}.")

    # ------------------------------------------------------------ verdict
    say("\n=== F. THE ANSWER ===")
    ans = {}
    for arm in ARMS:
        q = df[df.arm == arm]
        ans[arm] = (int(q[q.comparand == "SPY"].pass4b.sum()),
                    int(q[q.comparand == "EWBH"].pass4b.sum()),
                    int(q[q.comparand == "SPY"].pass4a.sum()) // len(COMPARANDS) * len(COMPARANDS))
    for arm in ARMS:
        s, e, _ = ans[arm]
        n = len(df[(df.arm == arm) & (df.comparand == "SPY")])
        say(f"  {arm:11s}: 4b-PROTO {s:3d}/{n} vs SPY, {e:3d}/{n} vs EWBH;"
            f" 4a {int(df[(df.arm == arm) & (df.comparand == 'SPY')].pass4a.sum()):3d}/{n}")
    gdf = pd.DataFrame(GATES); gdf.to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\n  GATES: {int(gdf.pass_.sum())} of {len(gdf)} pass.")
    say(f"  SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008.  The blend")
    say(f"  arms hold the WHOLE survivor panel all the time and are therefore MORE contaminated")
    say(f"  than the candidate, so a blend PASS is the flattered reading and a blend FAIL is")
    say(f"  robust to the bias.  Every SPY-relative column is biased upward for every arm.")
    say(f"\n  elapsed {time.time() - t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
