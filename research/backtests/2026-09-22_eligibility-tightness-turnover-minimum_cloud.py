#!/usr/bin/env python3
"""Idea 949 (lane cloud, 2026-09-22) — WHY DOES TIGHTENING ELIGIBILITY RAISE TURNOVER ON ALL
THREE PANELS?

WHERE THIS COMES FROM.  Idea 945's direction gate failed 3 of 3 on the eligibility dial:
tightening `max_vol` from 0.60 to 0.35 RAISED realised annual turnover (A/B ratio 0.87 / 0.86 /
0.80 on U56 / B136 / SMALL).  The record treats eligibility tightness as a turnover-REMOVING
dial — a screen that calms a book — and it does the opposite.  945 read two rungs.  Two rungs
cannot tell a MONOTONE relationship from one with an interior minimum, and cannot say WHY.

THE QUESTION.  Map realised annual turnover against the whole threshold ladder on all three
panels, locate the minimum, identify the MECHANISM, and report which committed eligibility
claims sit on the wrong side of it.

THE MECHANISM HYPOTHESIS, STATED BEFORE THE RUN.  An equal-weight book's turnover is roughly
(names entering or leaving per rebalance) x (NAV each name carries) = churn(m) x gross/N(m).
Tightening the screen pushes BOTH terms the wrong way: N(m) falls, so every admission or
expulsion moves MORE NAV, and the threshold moves INTO the dense part of the trailing-vol
distribution, so more names oscillate across it.  If the first channel dominates, the rise is an
arithmetic consequence of RENORMALISING 1/N, not of the screen churning the book.  The run
separates them with a control:
    EWELIG    equal weight over gated names at gross 0.75  (the 1/N channel is LIVE)
    FIXEDW    the SAME gated set, each name at a FIXED weight gross/Nbar, Nbar = that rung's
              own time-mean gated count, row-scaled down if the total would exceed 1.00 (no
              leverage, protocol rule 2).  The WITHIN-rung 1/N renormalisation is dead, but
              Nbar still moves BETWEEN rungs, so this control is only PARTIAL and is reported
              as such.
    FIXEDW0   the strict control: the same gated set at ONE weight gross/Nbar(m=1.00), IDENTICAL
              at every rung, so a name's admission moves exactly the same NAV whatever the
              threshold.  Here turnover is proportional to the raw CHURN COUNT alone.
A rise that survives in EWELIG but vanishes in FIXEDW0 is the renormalisation channel; a rise
that survives in FIXEDW0 is the set churning more names outright.

WHAT IS PRICED.
  DIAL 1 — THRESHOLD LADDER: max_vol m in {0.20, 0.25, ..., 1.00} (17 rungs, 0.05 step).
  DIAL 2 — PANEL: U56 / B136 / SMALL.
REPORTED, NOT TUNED: book kind (EWELIG, FIXEDW control, and V1TOP5 = the record's own
`baseline.rules_v1_weights(n=5, w=0.15, max_vol=m)`), cadence (W / M), gross 0.75, t+1 fills.
= 17 x 3 x 3 x 2 = 306 books, every one published (`*.grid.csv`).  Costs 0 / 10 / 25 / 50 bps,
reconstructed exactly from each book's own cost-0 turnover series (gate G_COST).

PRE-STATED VERDICT RULES (fixed before the run, not adjusted after).
  V1  INTERIOR MINIMUM.  For EWELIG / weekly, realised annual turnover has an INTERIOR argmin
      (not at either end of the ladder) on all 3 panels.  Triggered -> tightness is not a
      monotone turnover dial in either direction and "tighter = calmer" is simply false.
  V2  945 REPLICATION.  turnover(m=0.35) > turnover(m=0.60) on all 3 panels, EWELIG / weekly.
  V3  MECHANISM.  The 0.35-vs-0.60 rise is a RENORMALISATION effect: it holds in EWELIG on 3 of
      3 panels and does NOT hold (ratio <= 1) in the STRICT FIXEDW0 control on >= 2 of 3 panels.
  V3b RATE LAW.  |rho(churn/N, turnover)| over the 17 rungs exceeds |rho(churn, turnover)| on
      3 of 3 panels — i.e. the governing variable is the per-member replacement RATE, not the
      raw count of names crossing the screen.
  V4  CAPITAL.  At least one ladder rung clears 4b FULL and OOS at the PROTOCOL 10 bps rung.
  V5  RULE 8.  The rung chosen on 2009-2016 IS Sharpe beats its own ladder's MEDIAN OOS Sharpe
      on >= 2 of 3 panels (EWELIG / weekly).

PROTOCOL: rule 2 (10 bps, t+1 fills, no shorting, no leverage); rule 3 (live RULES v2 AND SPY,
per panel); rule 4 (both KEEP paths at every rung, <= 2 tuned dials); rule 5 (one idea,
deterministic, standalone); rule 8 (m chosen on 2009-2016 only, 2017-2026 read ONCE); rule 9
(survivorship stated).  RULES.md / scan.py / bot.py / baseline.py NOT modified.

SURVIVORSHIP (rule 9).  U56 = research/universe.json, B136 = research/universe_broad.json and
SMALL = data/prices_small.csv.gz are all CURRENT-CONSTITUENT panels.  SMALL carries 719 cached
names, of which the 54 with max_1d_move >= 1.0 are DROPPED per data/small_meta.csv, leaving 665
investable names; SPY there is a benchmark column, not a constituent.  Every CAGR and MaxDD
LEVEL below is optimistic and both 4b bars are easier than on a point-in-time panel.  The
primary object here is a TURNOVER CURVE against a threshold on one and the same tape, which is
first-order immune to the bias; the 4b pass counts are not.

Run:  python research/backtests/2026-09-22_eligibility-tightness-turnover-minimum_cloud.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score                  # noqa: E402
from engine import backtest as engine_backtest, rebalance_mask               # noqa: E402

DATE, SLUG = "2026-09-22", "eligibility-tightness-turnover-minimum"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

PANELS = ["U56", "B136", "SMALL"]
BOOKS = ["EWELIG", "FIXEDW", "FIXEDW0", "V1TOP5"]
CADENCES = ["W", "M"]
LADDER = [round(0.20 + 0.05 * i, 2) for i in range(17)]        # 0.20 .. 1.00
COSTS = [0, 10, 25, 50]
PROTOCOL_COST = 10
GROSS, TOPN = 0.75, 5
WARMUP = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_RUNG, B_RUNG = 0.35, 0.60                                    # idea 945's own two rungs

_log: list[str] = []
_gates: list[dict] = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _log.append(s)


def gate(name, value, target, ok):
    _gates.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    log(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {value}   (target {target})")
    return bool(ok)


def mets(r):
    r = r.dropna()
    if len(r) < 60:
        return dict(CAGR=np.nan, Sharpe=np.nan, MaxDD=np.nan)
    eq = (1 + r).cumprod()
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252.0)
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs else np.nan,
                Sharpe=(r.mean() * 252.0) / vol if vol else np.nan,
                MaxDD=float((eq / eq.cummax() - 1).min()))


def halves(r):
    h = len(r) // 2
    return mets(r.iloc[:h])["Sharpe"], mets(r.iloc[h:])["Sharpe"]


def panel(name):
    if name == "U56":
        px = load_universe(); inv = list(px.columns)
    elif name == "B136":
        px = load_universe(broad=True); inv = list(px.columns)
    else:
        px = load_universe(small=True)
        meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
        bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])          # mandatory scrub
        inv = [c for c in px.columns if c != "SPY" and c not in bad]
        px = px[[c for c in px.columns if c in inv or c == "SPY"]]
    px = px.dropna(how="all").ffill()
    return px, [c for c in inv if c in px.columns]


def build(book, m, px, inv, comp_vs, above, vol20, elig, nbar_ref):
    """elig = above 200d MA & vol20 < m & priced.  Only `m` moves between rungs."""
    if book == "EWELIG":
        n = elig.sum(axis=1).replace(0, np.nan)
        return elig.astype(float).div(n, axis=0).fillna(0.0) * GROSS
    if book in ("FIXEDW", "FIXEDW0"):
        nbar = (float(elig.sum(axis=1).loc[px.index[WARMUP]:].mean())
                if book == "FIXEDW" else nbar_ref)
        w = elig.astype(float) * (GROSS / max(nbar, 1.0))
        tot = w.sum(axis=1)
        return w.div(tot.where(tot > 1.0, 1.0), axis=0).fillna(0.0)     # no leverage
    # V1TOP5: the record's own RULES v1 book, vol-scaled composite, n=5 at w=0.15
    rank = comp_vs.where(elig).rank(axis=1, ascending=False, method="first")
    return (rank <= TOPN).astype(float) * 0.15


def churn_stats(elig, idx, freq):
    """Set statistics on the rebalance dates only: mean gated count and mean number of names
    entering-or-leaving per rebalance."""
    d = elig.loc[rebalance_mask(idx, freq).values]
    d = d.loc[idx[WARMUP]:]
    v = d.values
    n = v.sum(axis=1)
    ch = np.abs(v[1:].astype(int) - v[:-1].astype(int)).sum(axis=1)
    return float(n.mean()), float(ch.mean())


def main():
    log(f"# Idea 949 (lane cloud, {DATE}) — why does TIGHTENING ELIGIBILITY RAISE TURNOVER on "
        f"all three panels?")
    log(f"# TUNED DIALS (2): THRESHOLD LADDER max_vol {LADDER[0]}..{LADDER[-1]} step 0.05 "
        f"({len(LADDER)} rungs); PANEL {PANELS}.")
    log(f"# reported, not tuned: BOOK {BOOKS} x CADENCE {CADENCES} x COST {COSTS} bps; "
        f"gross {GROSS}; t+1 fills.")
    log(f"# COMPARAND (committed, idea 945, NOT recomputed here): max_vol 0.60 -> 0.35 raises "
        f"realised annual turnover, A/B ratio 0.87 / 0.86 / 0.80 on U56 / B136 / SMALL "
        f"(i.e. turnover(0.35)/turnover(0.60) = 1/0.87 = 1.15x, 1.16x, 1.25x).")

    rows, cost_err = [], 0.0
    for pname in PANELS:
        px, inv = panel(pname)
        comp_vs, above, vol20 = score(px[inv], vol_scale=True)      # RULES v1's own composite
        st = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        S = dict(full=mets(spy), oos=mets(spy.loc[OOS_START:]))
        S["h1"], S["h2"] = halves(spy)
        log(f"\n## PANEL {pname}: {len(inv)} investable names, {px.index[0].date()} -> "
            f"{px.index[-1].date()}, scored from {st.date()}  |  SPY FULL "
            f"{S['full']['CAGR']:.2%} / {S['full']['Sharpe']:.4f} / {S['full']['MaxDD']:.2%}, "
            f"OOS {S['oos']['CAGR']:.2%} / {S['oos']['Sharpe']:.4f} / {S['oos']['MaxDD']:.2%}")

        for freq in CADENCES:
            bres = engine_backtest(px, rules_v2_weights(px), cost_bps=0, freq=freq)
            b0, bt0 = bres["returns"].loc[st:], bres["turnover"].loc[st:]
            LV = {}
            for c in COSTS:
                br = b0 - bt0 * c / 1e4
                lh1, lh2 = halves(br)
                LV[c] = dict(full=mets(br), oos=mets(br.loc[OOS_START:]), h1=lh1, h2=lh2)
            log(f"\n### {pname} / {freq}  RULES v2 baseline @10bps: "
                f"{LV[10]['full']['CAGR']:.2%} / {LV[10]['full']['Sharpe']:.4f} / "
                f"{LV[10]['full']['MaxDD']:.2%}")

            nbar_ref = float((above & (vol20 < LADDER[-1]) & px[inv].notna())
                             .sum(axis=1).loc[st:].mean())
            for m in LADDER:
                elig = above & (vol20 < m) & px[inv].notna()
                nbar, chbar = churn_stats(elig, px.index, freq)
                for book in BOOKS:
                    w = build(book, m, px, inv, comp_vs, above, vol20, elig, nbar_ref)
                    res = engine_backtest(px, w.reindex(columns=px.columns).fillna(0.0),
                                          cost_bps=0, freq=freq)
                    r0, t0 = res["returns"].loc[st:], res["turnover"].loc[st:]
                    if book == "EWELIG" and m == LADDER[0] and freq == "W":
                        chk = engine_backtest(px, w.reindex(columns=px.columns).fillna(0.0),
                                              cost_bps=25, freq=freq)["returns"].loc[st:]
                        cost_err = max(cost_err, float((chk - (r0 - t0 * 25 / 1e4)).abs().max()))
                    turn_yr = float(t0.sum() / (len(t0) / 252.0))
                    gross_real = float(res["weights"].loc[st:].sum(axis=1).mean())
                    for c in COSTS:
                        r = r0 - t0 * c / 1e4
                        mf, mo, mi = mets(r), mets(r.loc[OOS_START:]), mets(r.loc[:IS_END])
                        h1, h2 = halves(r)
                        lv = LV[c]
                        k4bf = (h1 > S["h1"] and h2 > S["h2"]
                                and mf["MaxDD"] >= DD_CAP * S["full"]["MaxDD"]
                                and mf["CAGR"] >= CAGR_FLOOR * S["full"]["CAGR"])
                        k4bo = (mo["Sharpe"] > S["oos"]["Sharpe"]
                                and mo["MaxDD"] >= DD_CAP * S["oos"]["MaxDD"]
                                and mo["CAGR"] >= CAGR_FLOOR * S["oos"]["CAGR"])
                        k4a = (h1 > lv["h1"] and h2 > lv["h2"]
                               and mf["MaxDD"] >= lv["full"]["MaxDD"])
                        rows.append(dict(
                            panel=pname, cadence=freq, book=book, max_vol=m, cost=c,
                            turn_yr=turn_yr, n_bar=nbar, churn_bar=chbar,
                            churn_over_n=chbar / nbar if nbar else np.nan,
                            gross_real=gross_real,
                            CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"],
                            H1=h1, H2=h2, is_Sharpe=mi["Sharpe"],
                            oos_CAGR=mo["CAGR"], oos_Sharpe=mo["Sharpe"], oos_MaxDD=mo["MaxDD"],
                            keep4b_full=k4bf, keep4b_oos=k4bo, keep4b=(k4bf and k4bo),
                            keep4a=k4a))
            log(f"    {pname}/{freq}: {len(LADDER)} rungs x {len(BOOKS)} books priced")

    grid = pd.DataFrame(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    grid.to_csv(f"{OUT}.grid.csv", index=False)
    log(f"\n# GRID: {len(grid)} rows -> {Path(str(OUT)+'.grid.csv').name}")
    gate("G_COST  exact cost reconstruction vs a direct 25 bps engine run",
         f"max |err| = {cost_err:.3e}", "< 1e-12", cost_err < 1e-12)

    z = grid[grid.cost == 0]

    # ------------------------------------------------------------------ the turnover curve
    log("\n## THE TURNOVER CURVE AGAINST max_vol (realised annual turnover, cost-0 book)")
    curve = []
    for (pn, fq, bk), s in z.groupby(["panel", "cadence", "book"]):
        s = s.sort_values("max_vol")
        amin = float(s.loc[s.turn_yr.idxmin()].max_vol)
        interior = LADDER[0] < amin < LADDER[-1]
        tA = float(s[s.max_vol == A_RUNG].turn_yr.iloc[0])
        tB = float(s[s.max_vol == B_RUNG].turn_yr.iloc[0])
        curve.append(dict(panel=pn, cadence=fq, book=bk, m_star=amin, interior=interior,
                          t_min=float(s.turn_yr.min()), t_max=float(s.turn_yr.max()),
                          t_035=tA, t_060=tB, ratio_035_over_060=tA / tB,
                          n_bar_035=float(s[s.max_vol == A_RUNG].n_bar.iloc[0]),
                          n_bar_060=float(s[s.max_vol == B_RUNG].n_bar.iloc[0]),
                          churn_035=float(s[s.max_vol == A_RUNG].churn_bar.iloc[0]),
                          churn_060=float(s[s.max_vol == B_RUNG].churn_bar.iloc[0])))
    cv = pd.DataFrame(curve)
    cv.to_csv(f"{OUT}.curve.csv", index=False)
    for _, r in cv.sort_values(["book", "cadence", "panel"]).iterrows():
        log(f"  {r.panel:5s} {r.cadence} {r.book:6s} argmin m={r.m_star:.2f} "
            f"{'INTERIOR' if r.interior else 'EDGE    '} turnover {r.t_min:.2f}-{r.t_max:.2f}x  "
            f"t(0.35)={r.t_035:.2f} t(0.60)={r.t_060:.2f} ratio={r.ratio_035_over_060:.3f}  "
            f"Nbar {r.n_bar_035:.1f}->{r.n_bar_060:.1f}  churn/rebal "
            f"{r.churn_035:.2f}->{r.churn_060:.2f}")

    ew = cv[(cv.book == "EWELIG") & (cv.cadence == "W")]
    gate("V1 INTERIOR MINIMUM  EWELIG/W turnover argmin is interior on all 3 panels",
         "; ".join(f"{r.panel} m*={r.m_star:.2f} {'INT' if r.interior else 'EDGE'}"
                   for _, r in ew.iterrows()), "3 of 3 interior",
         int(ew.interior.sum()) == 3)
    gate("V2 945 REPLICATION  turnover(0.35) > turnover(0.60) on all 3 panels (EWELIG/W)",
         "; ".join(f"{r.panel} {r.ratio_035_over_060:.3f}x" for _, r in ew.iterrows()),
         "3 of 3 > 1", int((ew.ratio_035_over_060 > 1).sum()) == 3)
    fx = cv[(cv.book == "FIXEDW") & (cv.cadence == "W")]
    f0 = cv[(cv.book == "FIXEDW0") & (cv.cadence == "W")]
    gate("V3 MECHANISM  the 0.35-vs-0.60 rise DIES in the STRICT FIXEDW0 control",
         "EWELIG " + "/".join(f"{r.ratio_035_over_060:.3f}" for _, r in ew.iterrows())
         + " | FIXEDW (partial) " + "/".join(f"{r.ratio_035_over_060:.3f}" for _, r in fx.iterrows())
         + " | FIXEDW0 (strict) " + "/".join(f"{r.ratio_035_over_060:.3f}" for _, r in f0.iterrows()),
         ">= 2 of 3 FIXEDW0 ratios <= 1", int((f0.ratio_035_over_060 <= 1).sum()) >= 2)

    _rate = {}
    log("\n## DECOMPOSITION — turnover vs the two channels (EWELIG / weekly, cost-0)")
    for pn in PANELS:
        s = z[(z.panel == pn) & (z.cadence == "W") & (z.book == "EWELIG")].sort_values("max_vol")
        log(f"  {pn}:  m      Nbar  churn/reb  churn/N   turn/yr")
        for _, r in s.iterrows():
            log(f"        {r.max_vol:.2f}  {r.n_bar:6.1f}  {r.churn_bar:8.2f}  "
                f"{r.churn_over_n:7.4f}  {r.turn_yr:7.2f}")
        rho_n = np.corrcoef(s.n_bar, s.turn_yr)[0, 1]
        rho_c = np.corrcoef(s.churn_bar, s.turn_yr)[0, 1]
        rho_r = np.corrcoef(s.churn_over_n, s.turn_yr)[0, 1]
        _rate[pn] = (abs(rho_r) > abs(rho_c), rho_n, rho_c, rho_r)
        log(f"        rho(Nbar, turnover) = {rho_n:+.4f}   rho(churn, turnover) = {rho_c:+.4f}"
            f"   rho(churn/N, turnover) = {rho_r:+.4f}")

    gate("V3b RATE LAW  |rho(churn/N, turnover)| > |rho(churn, turnover)| on all 3 panels",
         "; ".join(f"{k} {v[3]:+.4f} vs {v[2]:+.4f}" for k, v in _rate.items()),
         "3 of 3", sum(v[0] for v in _rate.values()) == 3)

    # ------------------------------------------------------------------- both KEEP paths
    log("\n## BOTH KEEP PATHS OVER THE WHOLE LADDER @ PROTOCOL 10 bps")
    g10 = grid[grid.cost == PROTOCOL_COST]
    tab = g10.groupby(["panel", "book", "cadence"])[["keep4b_full", "keep4b_oos", "keep4b",
                                                     "keep4a"]].sum()
    log(tab.to_string())
    n4b = int(g10.keep4b.sum())
    gate("V4 CAPITAL  a ladder rung clears 4b FULL and OOS at 10 bps",
         f"4b FULL+OOS {n4b} of {len(g10)} rungs; 4b FULL {int(g10.keep4b_full.sum())}; "
         f"4a FULL {int(g10.keep4a.sum())}", ">= 1", n4b >= 1)
    if n4b:
        best = g10[g10.keep4b].sort_values("Sharpe", ascending=False).head(6)
        log("  best 4b FULL+OOS rungs by Sharpe:")
        for _, r in best.iterrows():
            log(f"    {r.panel:5s} {r.cadence} {r.book:6s} m={r.max_vol:.2f}  FULL {r.CAGR:6.2%}"
                f" / {r.Sharpe:6.4f} / {r.MaxDD:7.2%}  OOS {r.oos_CAGR:6.2%} / "
                f"{r.oos_Sharpe:6.4f} / {r.oos_MaxDD:7.2%}  turn {r.turn_yr:.2f}x  "
                f"4a={str(r.keep4a)}")

    # ------------------------------------------------------------------- rule 8
    log("\n## RULE 8 WALK-FORWARD — m chosen on 2009-2016 IS Sharpe @10 bps, 2017-2026 read ONCE")
    wf = []
    for (pn, fq, bk), s in g10.groupby(["panel", "cadence", "book"]):
        s = s.sort_values("max_vol")
        pick = s.loc[s.is_Sharpe.idxmax()]
        wf.append(dict(panel=pn, cadence=fq, book=bk, is_pick=float(pick.max_vol),
                       full_argmax=float(s.loc[s.Sharpe.idxmax()].max_vol),
                       oos_CAGR=pick.oos_CAGR, oos_Sharpe=pick.oos_Sharpe,
                       oos_MaxDD=pick.oos_MaxDD, ladder_med_oos=float(s.oos_Sharpe.median()),
                       beats_median=bool(pick.oos_Sharpe > s.oos_Sharpe.median()),
                       oos_rank=int((s.oos_Sharpe > pick.oos_Sharpe).sum()) + 1,
                       keep4b=bool(pick.keep4b), keep4a=bool(pick.keep4a),
                       pick_turn=float(pick.turn_yr)))
        log(f"  {pn:5s} {fq} {bk:6s} IS pick m={pick.max_vol:.2f} -> OOS {pick.oos_CAGR:6.2%} / "
            f"{pick.oos_Sharpe:6.4f} / {pick.oos_MaxDD:7.2%}  rank "
            f"{int((s.oos_Sharpe > pick.oos_Sharpe).sum())+1} of {len(s)}  ladder-median OOS "
            f"{s.oos_Sharpe.median():.4f}  4b={str(bool(pick.keep4b)):5s} "
            f"4a={str(bool(pick.keep4a))}")
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)
    eww = wfd[(wfd.book == "EWELIG") & (wfd.cadence == "W")]
    gate("V5 RULE 8  IS-chosen m beats its own ladder's MEDIAN OOS Sharpe (EWELIG/W)",
         "; ".join(f"{r.panel} {'YES' if r.beats_median else 'NO'} "
                   f"({r.oos_Sharpe:.4f} vs {r.ladder_med_oos:.4f})" for _, r in eww.iterrows()),
         ">= 2 of 3", int(eww.beats_median.sum()) >= 2)
    log(f"\n  over all {len(wfd)} (panel x cadence x book) instances: IS pick beats ladder-median "
        f"OOS on {int(wfd.beats_median.sum())}; mean OOS rank {wfd.oos_rank.mean():.2f} of "
        f"{len(LADDER)}; 4b {int(wfd.keep4b.sum())}; 4a {int(wfd.keep4a.sum())}")

    # ------------------------------------------- which committed eligibility claims are wrong side
    log("\n## WHICH COMMITTED ELIGIBILITY CLAIMS SIT ON THE WRONG SIDE OF THE MINIMUM")
    mstar = {r.panel: r.m_star for _, r in ew.iterrows()}
    pat = re.compile(r"max_vol[^0-9\-]{0,12}(0?\.\d+)")
    hits = []
    for f in ["LEADERBOARD.md", "CHANGELOG.md", "QUEUE.md", "PROTOCOL.md"]:
        p = ROOT / "research" / f
        if not p.exists():
            continue
        for i, line in enumerate(p.read_text(errors="ignore").split("\n"), 1):
            for v in pat.findall(line):
                hits.append(dict(file=f, line=i, value=float(v)))
    hd = pd.DataFrame(hits)
    if len(hd):
        hd["below_U56_min"] = hd.value < mstar.get("U56", np.nan)
        hd.to_csv(f"{OUT}.claims.csv", index=False)
        vc = hd.value.value_counts().sort_index()
        log(f"  {len(hd)} committed `max_vol = x` sites across research/*.md; distinct values: "
            + ", ".join(f"{v}x{n}" for v, n in vc.items()))
        log(f"  per-panel EWELIG/W turnover argmin m*: "
            + ", ".join(f"{k} {v:.2f}" for k, v in mstar.items()))
        log(f"  sites quoting a threshold BELOW the U56 minimum (the churn-raising side): "
            f"{int(hd.below_U56_min.sum())} of {len(hd)} "
            f"({hd.below_U56_min.mean():.1%})")
    else:
        log("  no `max_vol = x` sites found by the keyword matcher.")

    pd.DataFrame(_gates).to_csv(f"{OUT}.gates.csv", index=False)
    Path(f"{OUT}.log.txt").write_text("\n".join(_log) + "\n")
    log(f"\n# wrote .grid.csv, .curve.csv, .walkforward.csv, .claims.csv, .gates.csv, .log.txt")


if __name__ == "__main__":
    main()
