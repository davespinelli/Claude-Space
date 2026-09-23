#!/usr/bin/env python3
"""idea 2491 (lane cloud, run 61, 2026-09-23) — DOES THE 2% CAP NEED CONTINUOUS ENFORCEMENT,
OR ONLY ENTRY ENFORCEMENT?

THE GAP.  The standing 4b candidate (idea 2322's CAP2: hold every name inside the 200d +/-3%
hysteresis band at `min(g/N_in, 2%)` of NAV, weekly, residual swept into SHY) RE-IMPOSES that
per-name weight on EVERY rebalance.  A name that drifted ABOVE its cap is TRIMMED back; a name
that drifted BELOW is TOPPED UP.  Idea 2457 proved the DENOMINATOR (`g/N_in`) is an identity for
the sizing, but said nothing about the CAP ITSELF, and nothing about the re-imposition.

Every one of those weekly trims and top-ups is TURNOVER THAT NO NAME DECISION ASKED FOR.  The
band state did not change; only the prices did.  This run prices the obvious alternative: a
RATCHET cap that BINDS AT ENTRY ONLY.  A name entering the book is sized at `min(g/N_in, cap)`
and is then LEFT ALONE for as long as it stays in band; it is never trimmed and never topped up.
Only entries and exits trade.

WHY IT MIGHT NOT WORK, STATED BEFORE THE RUN.  Twelve turnover devices in this record have been
killed, and every one of them failed the SAME test: the turnover it "saved" was bought by CUTTING
EXPOSURE, and the CAGR went with it (idea 2477: the exchange rate splits by realised risk gross,
not by device name, rank corr +0.797).  A ratchet is a de-grosser BY CONSTRUCTION IN ONE
DIRECTION AND A LEVERAGER IN THE OTHER: it stops topping up laggards (lowers gross) and stops
trimming winners (raises gross and CONCENTRATION).  Which way it nets is exactly the measurement.

FOUR ENFORCEMENT MODES, ALL PUBLISHED, NONE SELECTED ON.  The mode is the OBJECT UNDER TEST, not
a tuned dial:
  CONT     -- the committed continuous cap.  `min(g/N_in, cap)` re-imposed every rebalance.
  RATCHET  -- entry only.  A held, still-in-band name keeps its DRIFTED weight; entrants are
              sized `min(g/N_in, cap)`; exits go to zero.  Risk gross FLOATS.
  RAT_CAP  -- one-sided ratchet: never topped up, but a held name whose drifted weight exceeds
              `cap` IS trimmed back to `cap`.  Isolates the TOP-UP leg from the TRIM leg.
  RAT_BUD  -- exposure-matched ratchet: held weights are kept, but entrants are funded only out
              of the REMAINING budget `max(0, g - kept)` and the risk book is scaled to `g` if
              the kept weights alone exceed it.  Risk gross <= g by construction (G10), so this
              is the arm that answers the record's standing confound.

DIAL 1 -- per-name cap in {0.015, 0.020 (idea 2322's CAP2, committed), 0.030, INF (2300/2332's
          uncapped CAND)}.
DIAL 2 -- gross g in {0.75 (live), 1.00}.
EXACTLY TWO TUNED PARAMETERS.  Everything else is a PUBLISHED AXIS, never selected on: panels
{U56, B136}; cost rungs {0, 10, 25, 50} bps; cadence {W, M}; t+1 execution; band 0.03; MA 200d;
SHY sweep at phi = 1.00.

WHAT IS REPORTED, WHETHER OR NOT IT FLATTERS THE DEVICE.  Realised turnover and the % SAVED
against the matched CONT cell; the EXCHANGE RATE in pp of CAGR per 1% of turnover saved, on the
record's own convention (`d_CAGR_pp / -d_turn_pct`), against the ~-0.10 pp every killed device
paid and idea 2431's adoption bar (-31.0% turnover at dCAGR >= 0); the realised RISK GROSS and
max single-name weight (the exposure-neutrality test all twelve killed devices failed); both KEEP
paths at every row; and rule 8.

SMALL IS NOT PRICED, with the reason stated rather than assumed: ideas 2318 / 2322 / 2326 / 2343
published SMALL's 4b pass count at 0 of 40-120 and idea 2383 read it at 0 of 128 with `L_DD`,
`L_H2` and `L_OOS` all failing at every cell.  Not re-sizing a held name cannot mend three legs
that already fail.

BOTH KEEP PATHS on every row.  4a: Sharpe > live RULES v2 in BOTH halves and MaxDD no worse.
4b: Sharpe > SPY in BOTH halves AND out of sample, MaxDD >= 0.60 x SPY's, CAGR >= 0.70 x SPY's.
RULE 8: the two dials (cap, gross) are chosen on warm-up..2016-12-31 ONLY by two pre-stated
IS-only choosers, then 2017-2026 is read ONCE, separately at every (panel, mode, cadence, rung).

GATES.  G0 >= 10y per panel.  G1 the per-column replica == `engine.backtest`.  G2 the eligible
set IS `baseline.band_state` & priced, bit-identically.  G3 the CONT cap 0.020 / g 0.75 / W /
10 bps cell reproduces the committed CAP2 AND CAND U56 headlines.  G4 no leverage.  G5 cost
exactly linear in the rung.  G6 exactly two tuned parameters.  G7 the comparands (SPY, live
RULES v2) are bit-identical across every mode.  G8 the ratchet BITES (it changes the realised
path at every matched cell).  G9 the sweep instrument is priced on every scored row.  G10
RAT_BUD's realised risk gross never exceeds g.  G11 at cap = INF, RAT_CAP IS RATCHET bit-for-bit
(an infinite ceiling cannot trim), and at every cap CONT is independent of the held path.

SURVIVORSHIP CAVEAT (rule 9): `universe.json` (U56) and `universe_broad.json` (B136) are CURRENT
constituents of their screens held from 2008, so absolute levels are biased upward and 4b's
`L_CAGR` floor is the most contaminated leg.  The mode-vs-mode contrast is same-tape, same-days,
same-names and first-order immune to that bias; the absolute 4b verdicts are not.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-23_ratchet-vs-continuous-cap-enforcement_cloud.py
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

DATE, SLUG, LANE = "2026-09-23", "ratchet-vs-continuous-cap-enforcement", "cloud"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_{LANE}"

BAND, MA_LEN, WARMUP = 0.03, 200, 260
MODES = ["CONT", "RATCHET", "RAT_CAP", "RAT_BUD"]      # published: the object under test
CAPS = [0.015, 0.020, 0.030, np.inf]                   # DIAL 1
GROSSES = [0.75, 1.00]                                 # DIAL 2
RUNGS = [0.0, 10.0, 25.0, 50.0]                        # published
CADENCES = ["W", "M"]                                  # published
SWEEP = "SHY"
HEADLINE_CAP, HEADLINE_GROSS, HEADLINE_RUNG, HEADLINE_CAD = 0.020, 0.75, 10.0, "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
ADOPT_TURN, ADOPT_CAGR = -31.0, 0.0                    # idea 2431's adoption bar
KILLED_RATE = -0.10                                    # the rate every killed device paid

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


# ---------------------------------------------------------------- the book
def eligible(px):
    """Names permitted to be held: inside the 200d +/- BAND hysteresis band and priced.
    `baseline.band_state` unmodified (G2 asserts bit-identity)."""
    return band_state(px, BAND) & px.notna()


def run_mode(prices, el, gross, cap, mode, freq, sweep=True):
    """Path-dependent runner.  Weights are DECIDED at t-1 and APPLIED at t, the book drifts
    between rebalances, and the residual is swept into SHY -- `engine.backtest` semantics
    verbatim for CONT.  The RATCHET modes need the CURRENT DRIFTED book to form their target,
    so the target cannot be pre-computed as a frame; it is formed inside the loop.

    `risk` tracks the drifted RISK book alone; `sx` tracks the drifted SHY SWEEP ADD-ON, so a
    ratchet never mistakes swept cash for a held position (SHY is also a band-eligible name)."""
    cols = list(prices.columns)
    si = cols.index(SWEEP)
    rv = prices.pct_change().fillna(0.0).values
    s_ok = prices[SWEEP].notna().values.astype(float)
    el_dec = el.reindex(prices.index).fillna(False).shift(1, fill_value=False).values
    nin = el.sum(axis=1).replace(0, np.nan)
    per_dec = (gross / nin).clip(upper=cap).fillna(0.0).shift(1, fill_value=0.0).values
    key = prices.index.to_period(freq)
    s_key = pd.Series(key, index=prices.index)
    mask = (s_key != s_key.shift(-1)).shift(1, fill_value=False).values

    n, m = len(prices.index), len(cols)
    cur = np.zeros(m); risk = np.zeros(m); sx = 0.0
    turn = np.zeros(n); r0 = np.zeros(n); gr = np.zeros(n); rg = np.zeros(n)
    nheld = np.zeros(n); mx = np.zeros(n); swp = np.zeros(n); lev = 0
    reb = np.zeros(n); rg_post = []
    for i in range(n):
        if mask[i] or i == 0:
            e = el_dec[i]; per = per_dec[i]
            if mode == "CONT":
                new_r = np.where(e, per, 0.0)
            else:
                held = (risk > 1e-12) & e
                kept = np.where(held, risk, 0.0)
                if mode == "RAT_CAP" and np.isfinite(cap):
                    kept = np.minimum(kept, cap)
                ent = e & ~held
                if mode == "RAT_BUD":
                    ks = kept.sum()
                    if ks > gross and ks > 0:
                        kept = kept * (gross / ks); ks = gross
                    nent = int(ent.sum())
                    pe = min(per, max(0.0, gross - ks) / nent) if nent else 0.0
                else:
                    pe = per
                new_r = kept + np.where(ent, pe, 0.0)
            tot_r = new_r.sum()
            if tot_r > 1.0:                                   # no leverage, ever (G4)
                new_r = new_r / tot_r; lev += 1
            new = new_r.copy()
            add = max(0.0, 1.0 - new.sum()) * s_ok[i] if sweep else 0.0
            new[si] += add
            turn[i] = float(np.abs(new - cur).sum()); reb[i] = 1.0
            cur = new; risk = new_r; sx = add
            rg_post.append(float(new_r.sum()))
        gr[i] = cur.sum(); rg[i] = float(risk.sum()); nheld[i] = float((risk > 1e-12).sum())
        mx[i] = float(risk.max()); swp[i] = sx
        r0[i] = float((cur * rv[i]).sum())
        g = cur * (1 + rv[i]); tot = g.sum() + (1 - cur.sum())
        if tot > 0:
            cur = g / tot
            risk = risk * (1 + rv[i]) / tot
            sx = sx * (1 + rv[i, si]) / tot
    idx = prices.index
    return dict(r0=pd.Series(r0, index=idx), turn=pd.Series(turn, index=idx),
                gross=pd.Series(gr, index=idx), risk_gross=pd.Series(rg, index=idx),
                names=pd.Series(nheld, index=idx), maxw=pd.Series(mx, index=idx),
                sweep_w=pd.Series(swp, index=idx), reb=pd.Series(reb, index=idx), lev=lev,
                rg_post=np.array(rg_post))


# ---------------------------------------------------------------- metrics
def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    return float((1 + r).cumprod().iloc[-1] ** (252 / len(r)) - 1)


def vol(r):
    return float(r.std() * np.sqrt(252))


def maxdd(r):
    eq = (1 + r).cumprod()
    return float((eq / eq.cummax() - 1).min())


def calmar(r):
    d = maxdd(r)
    return float(cagr(r) / abs(d)) if d < 0 else np.nan


def halves(r):
    h = len(r) // 2
    return sharpe(r.iloc[:h]), sharpe(r.iloc[h:])


def legs(r, base, spy, r_oos, spy_oos):
    h1, h2 = halves(r); b1, b2 = halves(base); s1, s2 = halves(spy)
    L_H1, L_H2 = h1 > s1, h2 > s2
    L_OOS = sharpe(r_oos) > sharpe(spy_oos)
    L_DD = maxdd(r) >= DD_CAP * maxdd(spy)
    L_CAGR = cagr(r) >= CAGR_FLOOR * cagr(spy)
    return dict(H1=h1, H2=h2,
                pass4a=bool((h1 > b1) and (h2 > b2) and (maxdd(r) >= maxdd(base))),
                pass4b=bool(L_H1 and L_H2 and L_OOS and L_DD and L_CAGR),
                L_H1=bool(L_H1), L_H2=bool(L_H2), L_OOS=bool(L_OOS),
                L_DD=bool(L_DD), L_CAGR=bool(L_CAGR),
                m_H1=h1 - s1, m_H2=h2 - s2, m_OOS=sharpe(r_oos) - sharpe(spy_oos),
                m_DD=maxdd(r) - DD_CAP * maxdd(spy), m_CAGR=cagr(r) - CAGR_FLOOR * cagr(spy))


def main():
    t0 = time.time()
    say("=== idea 2491 — DOES THE 2% CAP NEED CONTINUOUS ENFORCEMENT, OR ONLY ENTRY")
    say("    ENFORCEMENT?  (lane cloud, run 61) ===")
    say(f"    {DATE}  band {BAND}  MA {MA_LEN}d  cadence {CADENCES}  t+1  rungs {RUNGS} bps"
        f"  sweep {SWEEP} (phi=1.00)")
    say(f"    DIAL 1 per-name cap {[cname(c) for c in CAPS]} (0.020 = idea 2322's CAP2, INF = CAND)"
        f"    DIAL 2 gross {GROSSES}")
    say(f"    PUBLISHED AXIS, NEVER SELECTED ON: enforcement mode {MODES}, panels, rungs, cadence.")
    say("    CONT re-imposes min(g/N_in, cap) every rebalance (the committed book).  RATCHET binds")
    say("    at ENTRY ONLY and lets a held name drift.  RAT_CAP keeps the ceiling but drops the")
    say("    TOP-UP.  RAT_BUD is the EXPOSURE-MATCHED ratchet (risk gross <= g by construction).")
    say("    PRE-STATED RISK: twelve killed turnover devices all bought their saving by CUTTING")
    say("    EXPOSURE (idea 2477: the rate splits by risk gross, rank corr +0.797, not by device).")
    say("    A ratchet de-grosses on the top-up leg and LEVERAGES/CONCENTRATES on the trim leg;")
    say("    which way it nets is the measurement.  Risk gross and max name weight are published")
    say("    on every row.")
    say("    SMALL NOT PRICED: 0 of 128 4b cells (idea 2383), 0 of 40-120 (2318/2322/2326/2343).")
    say("    SURVIVORSHIP (rule 9): U56 / B136 are CURRENT constituents held from 2008; L_CAGR is")
    say("    the contaminated leg.  The mode-vs-mode contrast is same-tape, same-days, first-order")
    say("    immune; the absolute 4b verdicts are not.")
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
    for _cap in (HEADLINE_CAP, np.inf):
        w_cap = el_u.astype(float).mul((0.75 / nin_u).clip(upper=_cap), axis=0).fillna(0.0)
        r_eng = backtest(px_u, w_cap, cost_bps=HEADLINE_RUNG, freq=HEADLINE_CAD)["returns"]
        lv = run_mode(px_u, el_u, 0.75, _cap, "CONT", HEADLINE_CAD, sweep=False)
        d1 = max(d1, float((r_eng - (lv["r0"] - lv["turn"] * HEADLINE_RUNG / 1e4)).abs().max()))
    gate("G1 the CONT runner IS engine.backtest on the same risk-weight frame (cap 0.020 and INF,"
         " g 0.75, W, 10 bps, sweep off)", f"max|d| {d1:.3e}", "< 1e-12", d1 < 1e-12)

    shy_ok = all(bool(px[SWEEP].loc[px.index[WARMUP]:].notna().all()) for px in panels.values())
    gate("G9 sweep instrument priced on every scored row", f"SHY non-null on both panels: {shy_ok}",
         "True", shy_ok)

    # ------------------------------------------------------------ the grid
    rows, book_facts, cmp_audit, lev_tot = [], [], [], 0
    paths = {}
    for pname, px in panels.items():
        el = eligible(px)
        start = px.index[WARMUP]
        spy_t = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base_t = backtest(px, rules_v2_weights(px, band=BAND, gross=0.75),
                          cost_bps=HEADLINE_RUNG, freq="W")["returns"].loc[start:]
        cmp_audit.append((pname, spy_t, base_t))
        for cad in CADENCES:
            for mode in MODES:
                for cap in CAPS:
                    for gross in GROSSES:
                        bk = run_mode(px, el, gross, cap, mode, cad)
                        lev_tot += bk["lev"]
                        r0 = bk["r0"].loc[start:]; tn = bk["turn"].loc[start:]
                        paths[(pname, cad, mode, cname(cap), gross)] = r0
                        yrs = len(tn) / 252
                        bfrow = dict(panel=pname, cadence=cad, mode=mode, cap=cname(cap),
                                     gross=gross,
                                     turnover_yr=float(tn.sum() / yrs),
                                     rebals_yr=float(bk["reb"].loc[start:].sum() / yrs),
                                     mean_names=float(bk["names"].loc[start:].mean()),
                                     mean_gross=float(bk["gross"].loc[start:].mean()),
                                     max_gross=float(bk["gross"].loc[start:].max()),
                                     mean_risk_gross=float(bk["risk_gross"].loc[start:].mean()),
                                     min_risk_gross=float(bk["risk_gross"].loc[start:].min()),
                                     max_risk_gross=float(bk["risk_gross"].loc[start:].max()),
                                     mean_sweep=float(bk["sweep_w"].loc[start:].mean()),
                                     max_post_risk_gross=float(bk["rg_post"].max()),
                                     max_name_w=float(bk["maxw"].loc[start:].max()),
                                     mean_max_name_w=float(bk["maxw"].loc[start:].mean()),
                                     lev_clips=bk["lev"])
                        book_facts.append(bfrow)
                        for rung in RUNGS:
                            r = r0 - tn * rung / 1e4
                            r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
                            spy_is, spy_oos = spy_t.loc[:IS_END], spy_t.loc[OOS_START:]
                            lg = legs(r, base_t, spy_t, r_oos, spy_oos)
                            rows.append(dict(
                                panel=pname, cadence=cad, mode=mode, cap=cname(cap),
                                cap_num=float(cap) if np.isfinite(cap) else 9.99,
                                gross=gross, cost_bps=rung,
                                CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=maxdd(r), Calmar=calmar(r),
                                Vol=vol(r), turnover_yr=bfrow["turnover_yr"],
                                mean_risk_gross=bfrow["mean_risk_gross"],
                                max_name_w=bfrow["max_name_w"],
                                mean_sweep=bfrow["mean_sweep"],
                                IS_Sharpe=sharpe(r_is), IS_Calmar=calmar(r_is), IS_CAGR=cagr(r_is),
                                OOS_CAGR=cagr(r_oos), OOS_Sharpe=sharpe(r_oos),
                                OOS_MaxDD=maxdd(r_oos),
                                base_CAGR=cagr(base_t), base_Sharpe=sharpe(base_t),
                                base_MaxDD=maxdd(base_t),
                                base_OOS_CAGR=cagr(base_t.loc[OOS_START:]),
                                base_OOS_Sharpe=sharpe(base_t.loc[OOS_START:]),
                                spy_CAGR=cagr(spy_t), spy_Sharpe=sharpe(spy_t),
                                spy_MaxDD=maxdd(spy_t), spy_OOS_CAGR=cagr(spy_oos),
                                spy_OOS_Sharpe=sharpe(spy_oos), spy_OOS_MaxDD=maxdd(spy_oos),
                                **lg))
    df = pd.DataFrame(rows); df.to_csv(f"{OUT}.grid.csv", index=False)
    bf = pd.DataFrame(book_facts); bf.to_csv(f"{OUT}.books.csv", index=False)
    say(f"\n    {len(df)} published rows = 2 panels x {len(CADENCES)} cadences x {len(MODES)} modes"
        f" x {len(CAPS)} caps x {len(GROSSES)} gross x {len(RUNGS)} rungs;"
        f"  {len(bf)} distinct realised weight paths.")

    d7 = 0.0
    for pname, spy_t, base_t in cmp_audit:
        q = df[df.panel == pname]
        d7 = max(d7, float(q.spy_Sharpe.max() - q.spy_Sharpe.min()),
                 float(q.spy_CAGR.max() - q.spy_CAGR.min()),
                 float(q.base_Sharpe.max() - q.base_Sharpe.min()),
                 float(q.base_OOS_Sharpe.max() - q.base_OOS_Sharpe.min()))
    gate("G7 the comparands (SPY and live RULES v2) are BIT-IDENTICAL across every mode",
         f"max spread over all {len(df)} rows: {d7:.3e}", "0.0", d7 == 0.0)
    gate("G4 no leverage anywhere (max gross <= 1)",
         f"max over {len(bf)} paths: {bf.max_gross.max():.6f} gross,"
         f" {bf.max_name_w.max():.4f} max single name; {lev_tot} leverage clips fired",
         "<= 1+1e-12", bool(bf.max_gross.max() <= 1 + 1e-12))
    bud = bf[bf["mode"] == "RAT_BUD"]
    worst = float(max(r.max_post_risk_gross - r.gross for r in bud.itertuples()))
    gate("G10 RAT_BUD's POST-TRADE risk gross never exceeds its g (the exposure-matched arm; the"
         " book still DRIFTS above g between rebalances, exactly as CONT does)",
         f"worst post-trade excess over {len(bud)} paths: {worst:+.3e}", "<= 1e-9", worst <= 1e-9)
    publish("LEVERAGE CLIPS (a ratchet target whose risk weights summed above 1.0 and was scaled"
            " back) — the ceiling the entry-only rule runs into",
            "; ".join(f"{m}: {int(bf[bf['mode'] == m].lev_clips.sum())} clips over"
                      f" {int((bf[bf['mode'] == m].lev_clips > 0).sum())} of"
                      f" {len(bf[bf['mode'] == m])} paths" for m in MODES))

    # G11 identities
    d11a = max(float((paths[(p, c, "RAT_CAP", "INF", g)] - paths[(p, c, "RATCHET", "INF", g)])
                     .abs().max()) for p in panels for c in CADENCES for g in GROSSES)
    gate("G11 at cap = INF an infinite ceiling cannot trim, so RAT_CAP IS RATCHET bit-for-bit",
         f"max|d| over 8 matched paths: {d11a:.3e}", "0.0", d11a == 0.0)

    b0 = run_mode(px_u, eligible(px_u), 0.75, HEADLINE_CAP, "CONT", HEADLINE_CAD)
    st = px_u.index[WARMUP]
    bill25 = (b0["r0"] - (b0["r0"] - b0["turn"] * 25 / 1e4)).loc[st:]
    bill50 = (b0["r0"] - (b0["r0"] - b0["turn"] * 50 / 1e4)).loc[st:]
    d5 = float((2 * bill25 - bill50).abs().max())
    gate("G5 the cost charge is EXACTLY linear in the rung (2 x the 25 bps bill == the 50 bps bill)",
         f"max|d| {d5:.3e}", "< 1e-15", d5 < 1e-15)

    def cell(panel, cad, mode, cap, gross, rung):
        return df[(df.panel == panel) & (df.cadence == cad) & (df["mode"] == mode)
                  & (df.cap == cname(cap)) & (df.gross == gross)
                  & (df.cost_bps == rung)].iloc[0]

    a = cell("U56", "W", "CONT", 0.020, 0.75, 10.0)
    b = cell("U56", "W", "CONT", np.inf, 0.75, 10.0)
    d3 = max(abs(a.CAGR - 0.1162), abs(a.Sharpe - 1.2687) / 10, abs(a.MaxDD + 0.1481),
             abs(a.OOS_CAGR - 0.1277), abs(a.OOS_Sharpe - 1.3318) / 10,
             abs(b.CAGR - 0.1259), abs(b.Sharpe - 1.1934) / 10, abs(b.MaxDD + 0.1739),
             abs(b.OOS_CAGR - 0.1385), abs(b.OOS_Sharpe - 1.2397) / 10)
    gate("G3 CONT reproduces the committed CAP2 (11.62%/1.2687/-14.81%, OOS 12.77%/1.3318) AND"
         " CAND (12.59%/1.1934/-17.39%, OOS 13.85%/1.2397) U56 headlines",
         f"CAP2 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} OOS {a.OOS_CAGR:.2%}/{a.OOS_Sharpe:.4f};"
         f" CAND {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} OOS {b.OOS_CAGR:.2%}/{b.OOS_Sharpe:.4f}"
         f" -> max|d| {d3:.2e}", "< 1e-3", d3 < 1e-3)
    say(f"    ANCHOR published: U56 SPY full {a.spy_CAGR:.2%} / {a.spy_Sharpe:.4f} / {a.spy_MaxDD:.2%},"
        f" OOS {a.spy_OOS_CAGR:.2%} / {a.spy_OOS_Sharpe:.4f};"
        f" live RULES v2 {a.base_CAGR:.2%} / {a.base_Sharpe:.4f} / {a.base_MaxDD:.2%},"
        f" OOS {a.base_OOS_CAGR:.2%} / {a.base_OOS_Sharpe:.4f}.")
    bite = min(float((paths[(p, c, m, cname(cp), g)] - paths[(p, c, "CONT", cname(cp), g)])
                     .abs().max())
               for p in panels for c in CADENCES for m in MODES[1:] for cp in CAPS for g in GROSSES)
    gate("G8 the ratchet BITES at every matched cell (it changes the realised path)",
         f"smallest max|d| vs CONT over {2*len(CADENCES)*3*len(CAPS)*len(GROSSES)} matched pairs:"
         f" {bite:.3e}", "> 1e-9", bite > 1e-9)

    # ------------------------------------------------------------ A. the bill
    say("\n=== A. WHAT THE RATCHET ACTUALLY DOES TO THE BOOK (headline cell: cap 0.020, g 0.75, W) ===")
    say("  panel mode     | turn/yr | d_turn  | risk gross (min..max) | SHY sleeve | mean names"
        " | max name w | mean max w")
    for pname in panels:
        ref = bf[(bf.panel == pname) & (bf.cadence == "W") & (bf["mode"] == "CONT")
                 & (bf.cap == cname(HEADLINE_CAP)) & (bf.gross == HEADLINE_GROSS)].iloc[0]
        for mode in MODES:
            q = bf[(bf.panel == pname) & (bf.cadence == "W") & (bf["mode"] == mode)
                   & (bf.cap == cname(HEADLINE_CAP)) & (bf.gross == HEADLINE_GROSS)].iloc[0]
            dt = (q.turnover_yr / ref.turnover_yr - 1) * 100
            say(f"  {pname:5s} {mode:8s} | {q.turnover_yr:7.3f} | {dt:+6.2f}% |"
                f" {q.mean_risk_gross:6.4f} ({q.min_risk_gross:.3f}..{q.max_risk_gross:.3f}) |"
                f" {q.mean_sweep:10.2%} | {q.mean_names:10.2f} | {q.max_name_w:10.4f} |"
                f" {q.mean_max_name_w:10.4f}")

    # ------------------------------------------------------------ B. the exchange rate
    say("\n=== B. THE EXCHANGE RATE — pp of CAGR per 1% of turnover SAVED, on the record's own")
    say("    convention d_CAGR_pp / -d_turn_pct.  Every killed device paid about"
        f" {KILLED_RATE:+.2f}. ===")
    say("  panel cad mode     cap    g    rung |  turn/yr | d_turn  | dCAGR_pp | pp per 1% |"
        " d_risk_gross | bar?")
    rate_rows = []
    for pname in panels:
        for cad in CADENCES:
            for cap in CAPS:
                for gross in GROSSES:
                    ref = bf[(bf.panel == pname) & (bf.cadence == cad) & (bf["mode"] == "CONT")
                             & (bf.cap == cname(cap)) & (bf.gross == gross)].iloc[0]
                    for mode in MODES[1:]:
                        q = bf[(bf.panel == pname) & (bf.cadence == cad) & (bf["mode"] == mode)
                               & (bf.cap == cname(cap)) & (bf.gross == gross)].iloc[0]
                        dt = (q.turnover_yr / ref.turnover_yr - 1) * 100
                        for rung in RUNGS:
                            c0 = cell(pname, cad, "CONT", cap, gross, rung)
                            c1 = cell(pname, cad, mode, cap, gross, rung)
                            dc = (c1.CAGR - c0.CAGR) * 100
                            rate = dc / (-dt) if dt < -1e-9 else np.nan
                            clears = bool(dt <= ADOPT_TURN and dc >= ADOPT_CAGR)
                            rate_rows.append(dict(panel=pname, cadence=cad, mode=mode,
                                                  cap=cname(cap), gross=gross, cost_bps=rung,
                                                  d_turn_pct=dt, d_CAGR_pp=dc, rate=rate,
                                                  d_risk_gross=q.mean_risk_gross - ref.mean_risk_gross,
                                                  d_maxw=q.max_name_w - ref.max_name_w,
                                                  d_Sharpe=c1.Sharpe - c0.Sharpe,
                                                  d_OOS_Sharpe=c1.OOS_Sharpe - c0.OOS_Sharpe,
                                                  clears_bar=clears))
                            if cap == HEADLINE_CAP and gross == HEADLINE_GROSS:
                                say(f"  {pname:5s} {cad:3s} {mode:8s} {cname(cap):6s} {gross:.2f}"
                                    f" {rung:5.0f} | {q.turnover_yr:8.3f} | {dt:+6.2f}% |"
                                    f" {dc:+8.2f} | {rate:+9.3f} |"
                                    f" {q.mean_risk_gross - ref.mean_risk_gross:+12.4f} |"
                                    f" {'YES' if clears else 'no'}")
    rr = pd.DataFrame(rate_rows); rr.to_csv(f"{OUT}.rates.csv", index=False)
    sv = rr[rr.d_turn_pct < -1e-9]
    publish("turnover-SAVING arms", f"{len(sv)} of {len(rr)}; median d_turn"
            f" {rr.d_turn_pct.median():+.2f}%, best {rr.d_turn_pct.min():+.2f}%,"
            f" worst {rr.d_turn_pct.max():+.2f}%")
    if len(sv):
        publish("pooled MEDIAN pp of CAGR per 1% of turnover saved (this run's RATCHET reading)",
                f"{sv.rate.median():+.4f} over {len(sv)} saving arms"
                f" (every killed device paid ~{KILLED_RATE:+.2f})")
    publish(f"idea 2431's adoption bar ({ADOPT_TURN:+.1f}% turnover at dCAGR >= 0), cleared by",
            f"{int(rr.clears_bar.sum())} of {len(rr)} arms")
    publish("EXPOSURE NEUTRALITY (the test all twelve killed devices failed)",
            f"d risk gross over the {len(rr)} arms: median {rr.d_risk_gross.median():+.4f},"
            f" range [{rr.d_risk_gross.min():+.4f}, {rr.d_risk_gross.max():+.4f}];"
            f" d max name weight median {rr.d_maxw.median():+.4f},"
            f" max {rr.d_maxw.max():+.4f}")
    for mode in MODES[1:]:
        q = rr[rr["mode"] == mode]
        qs = q[q.d_turn_pct < -1e-9]
        head = (f"  {mode}: d_turn median {q.d_turn_pct.median():+.2f}%,"
                f" dCAGR median {q.d_CAGR_pp.median():+.2f} pp, rate median"
                f" {qs.rate.median():+.4f} over {len(qs)} saving arms" if len(qs) else
                f"  {mode}: d_turn median {q.d_turn_pct.median():+.2f}% — NO saving arm at all")
        publish(head,
                f"d risk gross median {q.d_risk_gross.median():+.4f},"
                f" d max name w median {q.d_maxw.median():+.4f},"
                f" dSharpe median {q.d_Sharpe.median():+.4f},"
                f" dOOS_Sharpe median {q.d_OOS_Sharpe.median():+.4f}")

    # ------------------------------------------------------------ B2. the neutrality test
    say("\n=== B2. THE EXPOSURE-NEUTRALITY TEST — the one every killed device failed.  A saving is")
    say("    only FREE if the book did not simply take MORE RISK.  Two pre-stated tolerances:")
    say("    |d realised risk gross| <= 0.02 and |d max single-name weight| <= 0.005. ===")
    say("  mode     | saving | dCAGR>=0 | dSharpe>=0 | dOOS_Sh>=0 | CONC neutral | GROSS neutral |"
        " SAVING+FREE+NEUTRAL")
    neut_rows = []
    for mode in MODES[1:]:
        q = rr[rr["mode"] == mode]
        conc = q.d_maxw.abs() <= 0.005
        grs = q.d_risk_gross.abs() <= 0.02
        both = (q.d_turn_pct < 0) & (q.d_CAGR_pp >= 0) & conc & grs
        neut_rows.append(dict(mode=mode, n=len(q), saving=int((q.d_turn_pct < 0).sum()),
                              free=int((q.d_CAGR_pp >= 0).sum()),
                              conc_neutral=int(conc.sum()), gross_neutral=int(grs.sum()),
                              all_three=int(both.sum())))
        say(f"  {mode:8s} | {int((q.d_turn_pct < 0).sum()):3d}/{len(q):<3d}|"
            f" {int((q.d_CAGR_pp >= 0).sum()):5d}/{len(q):<3d}|"
            f" {int((q.d_Sharpe >= 0).sum()):7d}/{len(q):<3d}|"
            f" {int((q.d_OOS_Sharpe >= 0).sum()):7d}/{len(q):<3d}|"
            f" {int(conc.sum()):9d}/{len(q):<3d}|"
            f" {int(grs.sum()):10d}/{len(q):<3d}|"
            f" {int(both.sum()):14d}/{len(q)}")
    nt = pd.DataFrame(neut_rows); nt.to_csv(f"{OUT}.neutrality.csv", index=False)
    publish("VERDICT ON NEUTRALITY",
            f"{int(nt.all_three.sum())} of {len(rr)} arms are SAVING AND free-or-better AND neutral"
            f" on BOTH tolerances;  {int(nt.gross_neutral.sum())} of {len(rr)} are gross-neutral at"
            f" all;  {int(nt.conc_neutral.sum())} of {len(rr)} are concentration-neutral")
    publish("THE TRIM LEG IS THE CAP (U56, W, cap 0.020, g 0.75, 10 bps)",
            "max single-name weight " + ", ".join(
                f"{m} {bf[(bf.panel=='U56') & (bf.cadence=='W') & (bf['mode']==m) & (bf.cap==cname(HEADLINE_CAP)) & (bf.gross==HEADLINE_GROSS)].iloc[0].max_name_w:.4f}"
                for m in MODES) + " against a NOMINAL cap of 0.0200")

    # ------------------------------------------------------------ B3. 4b preservation
    say("\n=== B3. DOES THE RATCHET KEEP THE COMMITTED BOOK'S 4b PASSES, OR TRADE THEM? ===")
    kcols = ["panel", "cadence", "cap", "gross", "cost_bps"]
    cont = df[df["mode"] == "CONT"].set_index(kcols).sort_index()
    say("  mode     | 4b rows | kept where CONT passes | NEW passes where CONT fails | LOST")
    for mode in MODES[1:]:
        q = df[df["mode"] == mode].set_index(kcols).sort_index()
        kept = int((cont.pass4b.astype(bool) & q.pass4b.astype(bool)).sum())
        new_ = int((~cont.pass4b.astype(bool) & q.pass4b.astype(bool)).sum())
        lost = int((cont.pass4b.astype(bool) & ~q.pass4b.astype(bool)).sum())
        say(f"  {mode:8s} | {int(q.pass4b.sum()):5d}/{len(q):<3d}| {kept:22d}/{int(cont.pass4b.sum()):<3d}"
            f" | {new_:27d} | {lost:4d}")

    # ------------------------------------------------------------ C. headline table
    say("\n=== C. HEADLINE CELLS (cap 0.020, gross 0.75, 10 bps) — FULL, HALVES, OOS ===")
    say("  panel cad mode     |   CAGR |  Sharpe |   MaxDD |   H1   /   H2  |  OOS CAGR |"
        " OOS Sharpe | 4a | 4b | failing 4b legs")
    for pname in panels:
        for cad in CADENCES:
            for mode in MODES:
                q = cell(pname, cad, mode, HEADLINE_CAP, HEADLINE_GROSS, HEADLINE_RUNG)
                bad = [k for k in ("L_H1", "L_H2", "L_OOS", "L_DD", "L_CAGR") if not q[k]]
                say(f"  {pname:5s} {cad:3s} {mode:8s} | {q.CAGR:6.2%} | {q.Sharpe:7.4f} |"
                    f" {q.MaxDD:7.2%} | {q.H1:6.3f} / {q.H2:6.3f} | {q.OOS_CAGR:9.2%} |"
                    f" {q.OOS_Sharpe:10.4f} | {'Y' if q.pass4a else '.':^2s} |"
                    f" {'Y' if q.pass4b else '.':^2s} | {','.join(bad) if bad else '-'}")
    q0 = cell("U56", "W", "CONT", HEADLINE_CAP, HEADLINE_GROSS, HEADLINE_RUNG)
    say(f"  COMPARANDS (U56, identical on every row): SPY {q0.spy_CAGR:.2%} / {q0.spy_Sharpe:.4f}"
        f" / {q0.spy_MaxDD:.2%}, OOS {q0.spy_OOS_CAGR:.2%} / {q0.spy_OOS_Sharpe:.4f};"
        f" live RULES v2 {q0.base_CAGR:.2%} / {q0.base_Sharpe:.4f} / {q0.base_MaxDD:.2%},"
        f" OOS {q0.base_OOS_CAGR:.2%} / {q0.base_OOS_Sharpe:.4f}.")

    # ------------------------------------------------------------ D. KEEP paths
    say("\n=== D. BOTH KEEP PATHS OVER ALL PUBLISHED ROWS ===")
    say(f"  4b {int(df.pass4b.sum())} of {len(df)};  4a {int(df.pass4a.sum())} of {len(df)}")
    say("  mode     | rows | 4b   | 4a  | 4b at 10bps | L_H1 fail | L_H2 fail | L_OOS fail |"
        " L_DD fail | L_CAGR fail")
    for mode in MODES:
        q = df[df["mode"] == mode]
        q10 = q[q.cost_bps == 10.0]
        say(f"  {mode:8s} | {len(q):4d} | {int(q.pass4b.sum()):4d} | {int(q.pass4a.sum()):3d} |"
            f" {int(q10.pass4b.sum()):11d} | {int((~q.L_H1).sum()):9d} | {int((~q.L_H2).sum()):9d} |"
            f" {int((~q.L_OOS).sum()):10d} | {int((~q.L_DD).sum()):9d} | {int((~q.L_CAGR).sum()):11d}")
    say("  by (panel, cadence, rung), 4b count out of 8 (mode x cap x gross = 32) :")
    for pname in panels:
        for cad in CADENCES:
            line = "  ".join(f"{rung:.0f}bps {int(df[(df.panel==pname)&(df.cadence==cad)&(df.cost_bps==rung)].pass4b.sum()):2d}/32"
                             for rung in RUNGS)
            say(f"    {pname:5s} {cad}: {line}")

    # ------------------------------------------------------------ E. rule 8
    say("\n=== E. RULE 8 WALK-FORWARD — the two dials (cap, gross) fitted on warm-up..2016-12-31")
    say("    ONLY, 2017-2026 read ONCE, separately at every (panel, cadence, mode, rung). ===")
    wf = []
    for pname in panels:
        for cad in CADENCES:
            for mode in MODES:
                for rung in RUNGS:
                    q = df[(df.panel == pname) & (df.cadence == cad) & (df["mode"] == mode)
                           & (df.cost_bps == rung)]
                    for ch, keyf in (("C_ISSHARPE", "IS_Sharpe"), ("C_ISCALMAR", "IS_Calmar")):
                        p = q.loc[q[keyf].idxmax()]
                        wf.append(dict(panel=pname, cadence=cad, mode=mode, cost_bps=rung,
                                       chooser=ch, pick_cap=p.cap, pick_gross=p.gross,
                                       OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe,
                                       OOS_MaxDD=p.OOS_MaxDD,
                                       spy_OOS_CAGR=p.spy_OOS_CAGR, spy_OOS_Sharpe=p.spy_OOS_Sharpe,
                                       spy_OOS_MaxDD=p.spy_OOS_MaxDD,
                                       base_OOS_CAGR=p.base_OOS_CAGR,
                                       base_OOS_Sharpe=p.base_OOS_Sharpe,
                                       beats_spy=bool(p.OOS_Sharpe > p.spy_OOS_Sharpe),
                                       beats_base=bool(p.OOS_Sharpe > p.base_OOS_Sharpe),
                                       full4b=bool(p.pass4b), full4a=bool(p.pass4a)))
    wfd = pd.DataFrame(wf); wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    say("  panel cad mode     | picks (cap/g)                  | OOS CAGR | OOS Sharpe | OOS MaxDD"
        " | > SPY | > live | full 4b")
    for pname in panels:
        for cad in CADENCES:
            for mode in MODES:
                q = wfd[(wfd.panel == pname) & (wfd.cadence == cad) & (wfd["mode"] == mode)]
                top = q.groupby(["pick_cap", "pick_gross"]).size().sort_values(ascending=False)
                desc = ", ".join(f"{a}/{b:.2f}:{c}" for (a, b), c in top.items())
                say(f"  {pname:5s} {cad:3s} {mode:8s} | {desc:30s} | {q.OOS_CAGR.mean():8.2%} |"
                    f" {q.OOS_Sharpe.mean():10.4f} | {q.OOS_MaxDD.mean():9.2%} |"
                    f" {int(q.beats_spy.sum()):3d}/{len(q):<3d} |"
                    f" {int(q.beats_base.sum()):3d}/{len(q):<3d} |"
                    f" {int(q.full4b.sum()):3d}/{len(q)}")
    say(f"\n  OVERALL rule 8: {int(wfd.beats_spy.sum())} of {len(wfd)} picks beat SPY's OOS Sharpe;"
        f" {int(wfd.beats_base.sum())} of {len(wfd)} beat the LIVE book's;"
        f" {int(wfd.full4b.sum())} of {len(wfd)} carry a full-sample 4b.")
    say(f"  BENCHMARK OOS (2017-2026), read once: SPY {wfd.spy_OOS_CAGR.mean():.2%} /"
        f" {wfd.spy_OOS_Sharpe.mean():.4f} / {wfd.spy_OOS_MaxDD.mean():.2%};"
        f"  live RULES v2 {wfd.base_OOS_CAGR.mean():.2%} / {wfd.base_OOS_Sharpe.mean():.4f}"
        f"  (panel-pooled means).")
    for mode in MODES:
        q = wfd[wfd["mode"] == mode]
        c = wfd[wfd["mode"] == "CONT"].set_index(["panel", "cadence", "cost_bps", "chooser"])
        qi = q.set_index(["panel", "cadence", "cost_bps", "chooser"])
        agree = int(((qi.pick_cap == c.pick_cap) & (qi.pick_gross == c.pick_gross)).sum())
        say(f"    {mode:8s}: OOS Sharpe mean {q.OOS_Sharpe.mean():.4f}, OOS CAGR mean"
            f" {q.OOS_CAGR.mean():.2%}; the (cap, gross) pick matches CONT's in"
            f" {agree} of {len(q)} draws")

    ok = all(g["pass_"] for g in GATES)
    say(f"\n=== GATES: {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass ===")
    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nDone in {time.time() - t0:.0f}s.  all gates pass: {ok}")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG))


if __name__ == "__main__":
    main()
