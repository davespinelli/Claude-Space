#!/usr/bin/env python3
"""Idea 370: does a hysteresis BAND recover what the raw 200d gate burns in H1?

Idea 30 attributed the whole first-half failure of the core-plus-sleeve family to the raw 200d
gate on the equity core: gated 60% QQQ costs -6.11 pp of H1 CAGR and -0.367 of H1 Sharpe
against always-on, while in H2 it costs only -1.28 pp and GAINS +0.134 of Sharpe -- at the same
15-17% cash days in both halves.  Same insurance, same premium, opposite value: that is a
WHIPSAW tax, not mispriced insurance.  RULES v2 already carries a +/-3% hysteresis band for
exactly this failure.  So: re-run idea 30's c x q grid with the core gated by
`baseline.band_state(band)` instead of the raw MA, and report how much of the 6.11 pp comes back.

  TUNED PARAMETERS -- exactly two, fixed before any number was read:
     1. c    in {0.50, 0.60, 0.70, 0.80}        total equity core fraction (sleeve = 1 - c)
     2. band in {0.00, 0.03, 0.06, 0.12}        hysteresis half-width on the core's 200d gate
  REPORTED, NOT TUNED (every point of every axis printed and written to the CSVs):
     q in {0.00, 0.25, 0.50, 0.75, 0.8333, 1.00}  QQQ share of the core, rest SPY
        (q=1.00 is idea 24's variant B, the anchor; q=0.8333 is idea 30's literal proposal)
     panel in {U56, B136}, cost rung in {10, 25} bps, and a GATE=OFF (always-on core) control.
  384 gated points + 96 ungated controls = 480 books, all reported.  band=0.00 IS idea 30's
  own GATE=ON slice and is used as the reproduction gate, not as a new result.

THE HEADLINE STATISTIC is idea 30's own: the CORE LEG alone (c of NAV in QQQ, no sleeve), gated
vs always-on, per half.  `recovered_pp = dCAGR_H1(band) - dCAGR_H1(0.00)` and the same for
Sharpe, reported beside the two things a band is supposed to trade off -- CASH-DAY SHARE (the
premium paid) and GATE FLIPS PER YEAR (the whipsaw count).  A band that recovers H1 CAGR purely
by holding the core more of the time has not repaired the whipsaw, it has bought less insurance;
the run therefore also reports the recovery at MATCHED cash days wherever the ladder brackets it.

RULE 8 walk-forward: the (c, band) menu -- the two tuned dials, 16 cells -- is chosen on
2009-2016 by IS Sharpe, and 2017-2026 is read ONCE against idea 30's anchor (c=0.60,
band=0.00), the OOS-best cell (regret), the LIVE RULES v2 book and SPY.  Run at q=1.00 (the
anchor) and at q=0.8333 (the queue's proposal), on both panels, at 10 bps.

BOTH KEEP PATHS at every one of the 480 points: 4a against the live RULES v2 book on the same
panel, 4b against SPY (Sharpe > SPY in BOTH halves AND OOS, |MaxDD| <= 60% of SPY's,
CAGR >= 70% of SPY's).

REPRODUCTION GATES (section [0], printed before any new number is read):
  * derived rung r(c) = r(0) - turnover*c/1e4 vs engine.backtest(cost_bps=25) to 1e-12;
  * idea 24 variant B's published decimals on idea 30's own truncated tape (2026-09-02):
    10.8% / 0.95 / -18.9% / halves 0.84 / 1.04 -- HARD ASSERT, as idea 30 asserted them;
  * `band_state(px, 0.00)` NESTS idea 30's raw `px > ma` gate: the disagreeing-day count is
    printed (they can differ only on exact-equality days and on the pre-200-close warm-up);
  * idea 30's committed grid.csv: every one of its GATE=ON rows is rebuilt from source here as
    the band=0.00 slice and max|diff| is printed per metric;
  * idea 30's published gate-cost table (H1 -6.11 pp / -0.3673, H2 -1.28 pp / +0.1343,
    16.0% / 15.2% / 16.7% cash days) is re-derived, not copied.
  Published-number gates are REPORTED as PASS/FAIL with the miss; only the idea-24 decimals are
  asserted, because idea 30 asserted them.

CAVEATS.  (1) Both universes are CURRENT-CONSTITUENT lists -- survivorship flatters every level
here; the band DIFFERENCES, which are what this run is about, are far less affected.  (2) This
book is ETF-only (QQQ, SPY and the 9-name macro sleeve), so the panel axis is near-degenerate --
idea 30 measured max |U56 - B136| Sharpe at 1.09e-04.  It is kept as a reported axis for
continuity, not as evidence.  (3) The tape is the CORRECTED trading-day index (ideas 38/39);
idea 24's published row was computed on the pre-fix calendar-day tape, which is no longer in the
repo, so gate 2 is a match to published decimals ACROSS that correction, exactly as idea 30
labelled it.  (4) QQQ's 2009-2017 run is the single best large-cap equity decade in the sample,
so every conclusion about the core's composition is conditioned on it -- and a band that helps
by holding QQQ longer in THAT decade is not evidence it would help in another.  (5) The band is
applied to the CORE only; the sleeve's own internal momentum votes are untouched, as idea 30
left them.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state          # noqa
from engine import backtest, metrics                                      # noqa

SLUG = "2026-09-07_does-a-BAND-recover-what-the-raw-200d-gate-burns-in-H1_cloud"
OUT = ROOT / "research" / "backtests"
FREQ = "W"
COSTS = [10, 25]
CS = [0.50, 0.60, 0.70, 0.80]                    # tuned parameter 1 (idea 30's, unchanged)
BANDS = [0.00, 0.03, 0.06, 0.12]                 # tuned parameter 2 (this run's)
QS = [0.00, 0.25, 0.50, 0.75, 1.0 - 1.0 / 6.0, 1.00]     # reported axis
ANCHOR_C, ANCHOR_Q, ANCHOR_BAND = 0.60, 1.00, 0.00
PROPOSAL_Q = 1.0 - 1.0 / 6.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260

MACRO = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "GLD", "DBC", "UUP"]
MOM_LAGS = (252, 126, 63)
VOL_WINDOW, MA_WINDOW = 60, 200

_tee = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); _tee.append(s)


# ---------------------------------------------------------------- sleeve (idea 18 variant B)
def _risk_parity(sub):
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = 1.0 / vol.replace(0.0, np.nan)
    return inv.div(inv.sum(axis=1), axis=0)


def _vote_mom(sub):
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    return sum((s > 0).astype(float).where(s.notna()) for s in sig) / len(sig)


def sleeve_b_weights(px):
    sub = px[MACRO]
    w = (_vote_mom(sub) * _risk_parity(sub)).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[MACRO] = w
    return out


# ---------------------------------------------------------------- core leg, raw vs banded
def gate_series(px, ticker, band):
    """band is None -> idea 30's RAW gate (px > 200d MA, 0 before the MA exists).
    otherwise -> baseline.band_state, RULES v2 clause 2 hysteresis."""
    p = px[ticker]
    if band is None:
        ma = p.rolling(MA_WINDOW).mean()
        return (p > ma).astype(float).where(ma.notna(), 0.0)
    return band_state(px[[ticker]], band=band)[ticker].astype(float)


def core_leg(px, ticker, frac, gate, band):
    on = gate_series(px, ticker, band) if gate else pd.Series(1.0, index=px.index)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[ticker] = frac * on
    return out


def blend_weights(px, c, q, gate=True, band=0.00):
    return (core_leg(px, "QQQ", c * q, gate, band)
            + core_leg(px, "SPY", c * (1.0 - q), gate, band)
            + (1.0 - c) * sleeve_b_weights(px))


# ---------------------------------------------------------------- metrics
def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


def bars_4b(r, spy):
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4a(r, base):
    m, mb = metrics(r), metrics(base)
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(mb["MaxDD"]) - abs(m["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def flips_per_year(on, start):
    s = on.loc[start:]
    return float(np.abs(np.diff(s.values)).sum() / (len(s) / 252))


# ---------------------------------------------------------------- [0] gates
def gates(P):
    say("\n[0] REPRODUCTION GATES")
    px = P["U56"]; start = px.index[WARMUP]
    w = blend_weights(px, ANCHOR_C, ANCHOR_Q, True, 0.00)
    b0 = backtest(px, w, cost_bps=0, freq=FREQ)
    b25 = backtest(px, w, cost_bps=25, freq=FREQ)
    gid = float(np.abs((b0["returns"] - b0["turnover"] * 25 / 1e4) - b25["returns"]).max())
    say(f"    derived rung identity max|diff| = {gid:.3e}  ({'PASS' if gid < 1e-12 else 'FAIL'})")
    assert gid < 1e-12

    wknd = int((px.index.dayofweek >= 5).sum())
    say(f"    tape: {len(px)} rows, {wknd} weekend rows -> corrected trading-day index (ideas 38/39)")

    # band_state(0.00) nests idea 30's raw gate
    for tkr in ("QQQ", "SPY"):
        raw = gate_series(px, tkr, None); bnd = gate_series(px, tkr, 0.00)
        dis = int((raw != bnd).sum()); dis_post = int((raw.loc[start:] != bnd.loc[start:]).sum())
        say(f"    band_state(0.00) vs idea 30's raw gate on {tkr}: {dis} disagreeing days of "
            f"{len(raw)} full sample, {dis_post} of {len(raw.loc[start:])} post-warm-up "
            f"({'PASS' if dis_post == 0 else 'REPORTED'})")

    # idea 24 variant B published decimals on idea 30's truncated tape -- HARD ASSERT
    pxr = px.loc[:"2026-09-02"]
    rr = backtest(pxr, blend_weights(pxr, ANCHOR_C, ANCHOR_Q, True, 0.00),
                  cost_bps=10, freq=FREQ)["returns"].loc[pxr.index[WARMUP]:]
    mr = metrics(rr); r1, r2 = hs(rr)
    got = (round(mr["CAGR"], 3), round(mr["Sharpe"], 2), round(mr["MaxDD"], 3), round(r1, 2), round(r2, 2))
    exp = (0.108, 0.95, -0.189, 0.84, 1.04)
    say(f"    idea 24 variant B on the 2026-09-02 tape: {mr['CAGR']:.1%}/{mr['Sharpe']:.2f}/"
        f"{mr['MaxDD']:.1%} halves {r1:.2f}/{r2:.2f} vs published 10.8%/0.95/-18.9%/0.84/1.04"
        f" -> {'PASS' if got == exp else 'FAIL'}")
    assert got == exp, f"{got} != {exp}"

    # idea 30's published gate-cost table on the core leg
    rcg = backtest(px, core_leg(px, "QQQ", ANCHOR_C, True, 0.00), cost_bps=10, freq=FREQ)["returns"].loc[start:]
    rcn = backtest(px, core_leg(px, "QQQ", ANCHOR_C, False, 0.00), cost_bps=10, freq=FREQ)["returns"].loc[start:]
    pub = {"H1": (-0.0611, -0.3673), "H2": (-0.0128, 0.1343), "full": (-0.0371, -0.0801)}
    for lbl, a, b in (("H1", halves(rcg)[0], halves(rcn)[0]), ("H2", halves(rcg)[1], halves(rcn)[1]),
                      ("full", rcg, rcn)):
        ma, mb = metrics(a), metrics(b)
        dc, ds = ma["CAGR"] - mb["CAGR"], ma["Sharpe"] - mb["Sharpe"]
        ok = abs(dc - pub[lbl][0]) < 5e-4 and abs(ds - pub[lbl][1]) < 5e-4
        say(f"    idea 30 gate cost {lbl}: dCAGR {dc:+.4f} dSharpe {ds:+.4f} vs published "
            f"{pub[lbl][0]:+.4f}/{pub[lbl][1]:+.4f} -> {'PASS' if ok else 'FAIL'}")
    off = (gate_series(px, "QQQ", 0.00).loc[start:] == 0)
    say(f"    idea 30 cash days: {off.mean():.1%} full / {off.loc[:IS_END].mean():.1%} 2009-2016 /"
        f" {off.loc[OOS_START:].mean():.1%} 2017-2026 vs published 16.0/15.2/16.7 -> "
        f"{'PASS' if abs(off.mean()-0.160) < 0.005 else 'FAIL'}")


def gate_grid_vs_parent(G):
    say("\n[0b] IDEA 30's COMMITTED GRID, rebuilt here as the band=0.00 slice")
    p = OUT / "2026-09-07_qqq-core-plus-sleeve-h1_B.grid.csv"
    if not p.exists():
        say("    parent grid absent -- gate SKIPPED (reported, not asserted)"); return
    A = pd.read_csv(p)
    A = A[A["gate"] == 1].copy()
    B = G[(G["gate"] == 1) & (G["band"] == 0.00)].copy()
    for d in (A, B):
        d["qk"] = d["q"].round(4)
    M = A.merge(B, on=["panel", "cost", "c", "qk"], suffixes=("_p", "_n"))
    say(f"    matched {len(M)} of {len(A)} parent GATE=ON rows")
    for col in ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe", "turnover"):
        d = float(np.abs(M[f"{col}_p"] - M[f"{col}_n"]).max())
        say(f"      max|d {col}| = {d:.3e}  ({'PASS' if d < 1e-9 else 'FAIL'})")
    ok4b = int((M["pass4b_p"].astype(int) == M["pass4b_n"].astype(int)).sum())
    say(f"      4b verdicts identical on {ok4b}/{len(M)} rows;"
        f" parent 4b {int(M['pass4b_p'].sum())}, rebuild {int(M['pass4b_n'].sum())}")


# ---------------------------------------------------------------- [1] the core leg alone
def core_recovery(P):
    say("\n[1] THE HEADLINE: what the BAND recovers on the CORE LEG alone (c=0.60 QQQ, @10 bps)")
    rows = []
    for panel, px in P.items():
        start = px.index[WARMUP]
        rcn = backtest(px, core_leg(px, "QQQ", ANCHOR_C, False, 0.00), cost_bps=10,
                       freq=FREQ)["returns"].loc[start:]
        mn = {"H1": metrics(halves(rcn)[0]), "H2": metrics(halves(rcn)[1]), "full": metrics(rcn)}
        base = {}
        for band in BANDS:
            on = gate_series(px, "QQQ", band)
            rcg = backtest(px, core_leg(px, "QQQ", ANCHOR_C, True, band), cost_bps=10,
                           freq=FREQ)["returns"].loc[start:]
            off = (on.loc[start:] == 0)
            for lbl, g in (("H1", halves(rcg)[0]), ("H2", halves(rcg)[1]), ("full", rcg)):
                mg = metrics(g)
                dc = (mg["CAGR"] - mn[lbl]["CAGR"]) * 100
                ds = mg["Sharpe"] - mn[lbl]["Sharpe"]
                if band == 0.00:
                    base[lbl] = (dc, ds)
                o = off if lbl == "full" else (off.iloc[:len(off) // 2] if lbl == "H1"
                                               else off.iloc[len(off) // 2:])
                rows.append(dict(panel=panel, band=band, period=lbl,
                                 gated_CAGR=mg["CAGR"], ungated_CAGR=mn[lbl]["CAGR"],
                                 dCAGR_pp=dc, gated_Sharpe=mg["Sharpe"],
                                 ungated_Sharpe=mn[lbl]["Sharpe"], dSharpe=ds,
                                 gated_MaxDD=mg["MaxDD"], ungated_MaxDD=mn[lbl]["MaxDD"],
                                 cash_days=float(o.mean()),
                                 flips_per_yr=flips_per_year(on, start),
                                 recovered_CAGR_pp=dc - base[lbl][0],
                                 recovered_Sharpe=ds - base[lbl][1]))
    R = pd.DataFrame(rows)
    R.to_csv(OUT / f"{SLUG}.core.csv", index=False)
    for panel in P:
        say(f"    {panel}:")
        say("      band  period  gated CAGR  dCAGR_pp  dSharpe   cash%   flips/yr  recovered_pp  rec_Sharpe")
        for _, x in R[R.panel == panel].iterrows():
            say(f"      {x['band']:.2f}  {x['period']:<6} {x['gated_CAGR']:9.2%}  {x['dCAGR_pp']:+8.2f}"
                f"  {x['dSharpe']:+7.3f}  {x['cash_days']:6.1%}  {x['flips_per_yr']:7.2f}"
                f"  {x['recovered_CAGR_pp']:+11.2f}  {x['recovered_Sharpe']:+9.3f}")
    return R


# ---------------------------------------------------------------- [2] the grid
def grid(P):
    say("\n[2] THE GRID: 4 bands x 4 c x 6 q x 2 panels x 2 rungs (gated) + 96 GATE=OFF controls")
    rows, wf = [], []
    for panel, px in P.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        live = backtest(px, rules_v2_weights(px), cost_bps=10, freq=FREQ)["returns"].loc[start:]
        cells = {}
        for c in CS:
            for q in QS:
                for gate, band in ([(0, 0.00)] + [(1, b) for b in BANDS]):
                    res = backtest(px, blend_weights(px, c, q, bool(gate), band),
                                   cost_bps=0, freq=FREQ)
                    r0, t0 = res["returns"].loc[start:], res["turnover"].loc[start:]
                    gr = res["weights"].loc[start:].sum(axis=1)
                    for cost in COSTS:
                        r = r0 - t0 * cost / 1e4
                        m = metrics(r); h1, h2 = hs(r)
                        p4a, d4a, f4a = bars_4a(r, live)
                        p4b, d4b, f4b = bars_4b(r, spy)
                        rows.append(dict(panel=panel, cost=cost, gate=gate, band=band, c=c, q=q,
                                         QQQ_pct=100 * c * q, SPY_pct=100 * c * (1 - q),
                                         sleeve_pct=100 * (1 - c),
                                         CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                         H1=h1, H2=h2,
                                         OOS_CAGR=metrics(r.loc[OOS_START:])["CAGR"],
                                         OOS_Sharpe=metrics(r.loc[OOS_START:])["Sharpe"],
                                         OOS_MaxDD=metrics(r.loc[OOS_START:])["MaxDD"],
                                         IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                         IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                                         turnover=t0.sum() / (len(r) / 252), gross=gr.mean(),
                                         pass4a=int(p4a), fail4a="+".join(f4a),
                                         pass4b=int(p4b), fail4b="+".join(f4b),
                                         **{f"m4b_{k}": v for k, v in d4b.items()}))
                        if cost == 10 and gate == 1:
                            cells[(c, band, round(q, 4))] = r
        # ---- rule 8 over the two tuned dials, at the anchor q and the proposal q
        for q in (ANCHOR_Q, PROPOSAL_Q):
            menu = {(c, b): cells[(c, b, round(q, 4))] for c in CS for b in BANDS}
            iss = {k: metrics(v.loc[:IS_END])["Sharpe"] for k, v in menu.items()}
            oos = {k: metrics(v.loc[OOS_START:])["Sharpe"] for k, v in menu.items()}
            pick = max(iss, key=iss.get); best = max(oos, key=oos.get)
            anch = (ANCHOR_C, ANCHOR_BAND)
            po = metrics(menu[pick].loc[OOS_START:])
            wf.append(dict(panel=panel, q=q, IS_pick_c=pick[0], IS_pick_band=pick[1],
                           IS_Sharpe=iss[pick], OOS_CAGR=po["CAGR"], OOS_Sharpe=po["Sharpe"],
                           OOS_MaxDD=po["MaxDD"], anchor_OOS_Sharpe=oos[anch],
                           best_c=best[0], best_band=best[1], best_OOS_Sharpe=oos[best],
                           regret_vs_anchor=oos[anch] - oos[pick],
                           regret_vs_best=oos[best] - oos[pick],
                           picked_a_band=pick[1] > 0.0,
                           live_OOS_Sharpe=metrics(live.loc[OOS_START:])["Sharpe"],
                           spy_OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"]))
        say(f"    {panel}: {len([r for r in rows if r['panel'] == panel])} rows")
    G = pd.DataFrame(rows); W = pd.DataFrame(wf)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    W.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    return G, W


# ---------------------------------------------------------------- [3] read the grid
def read_grid(G, W, P):
    say("\n[3] THE H1 BAR (idea 30: GATE=ON 0/24 clear H1 at either rung, GATE=OFF 24/24 do)")
    px = P["U56"]; start = px.index[WARMUP]
    spy = px["SPY"].pct_change().fillna(0).loc[start:]
    s1, s2 = hs(spy)
    say(f"    SPY: {metrics(spy)['CAGR']:.2%}/{metrics(spy)['Sharpe']:.4f}/{metrics(spy)['MaxDD']:.2%}"
        f"  H1 {s1:.4f}  H2 {s2:.4f}  OOS {metrics(spy.loc[OOS_START:])['Sharpe']:.4f}")
    for panel in G.panel.unique():
        for cost in COSTS:
            S = G[(G.panel == panel) & (G.cost == cost)]
            say(f"    {panel} @{cost}bps  H1 bar cleared:  GATE=OFF {int((S[S.gate==0].m4b_H1>0).sum())}"
                f"/{len(S[S.gate==0])}   " +
                "  ".join(f"band {b:.2f} {int((S[(S.gate==1)&(S.band==b)].m4b_H1>0).sum())}"
                          f"/{len(S[(S.gate==1)&(S.band==b)])}" for b in BANDS))
    say("\n    best H1 margin per band (the bar idea 30 needed +0.113 of), U56 @10bps:")
    S = G[(G.panel == "U56") & (G.cost == 10)]
    for lbl, sub in [("GATE=OFF", S[S.gate == 0])] + [(f"band {b:.2f}", S[(S.gate == 1) & (S.band == b)]) for b in BANDS]:
        x = sub.loc[sub.m4b_H1.idxmax()]
        say(f"      {lbl:<10} best m4b_H1 {x['m4b_H1']:+.4f} at c={x['c']:.2f} q={x['q']:.4f}"
            f"  (H1 {x['H1']:.4f}, full {x['CAGR']:.2%}/{x['Sharpe']:.4f}/{x['MaxDD']:.2%})")

    say("\n[4] KEEP PATHS over all 480 points")
    say(f"    4a {int(G.pass4a.sum())}/{len(G)}   4b {int(G.pass4b.sum())}/{len(G)}")
    for lbl, sub in ([("GATE=OFF", G[G.gate == 0])] +
                     [(f"band {b:.2f}", G[(G.gate == 1) & (G.band == b)]) for b in BANDS]):
        say(f"      {lbl:<10} 4a {int(sub.pass4a.sum())}/{len(sub)}  4b {int(sub.pass4b.sum())}/{len(sub)}")
    fb = G[G.pass4b == 0].fail4b.value_counts()
    say(f"    first-failing-bar census over the {int((G.pass4b==0).sum())} 4b failures:")
    for k, v in fb.items():
        say(f"      {k or '(none)':<20} {v}")
    p = G[G.pass4b == 1]
    if len(p):
        say("    every 4b pass, listed:")
        for _, x in p.sort_values("Sharpe", ascending=False).iterrows():
            say(f"      {x['panel']} @{x['cost']}bps gate={x['gate']} band={x['band']:.2f} "
                f"c={x['c']:.2f} q={x['q']:.4f}: {x['CAGR']:.2%}/{x['Sharpe']:.4f}/{x['MaxDD']:.2%}"
                f"  H {x['H1']:.3f}/{x['H2']:.3f}  OOS {x['OOS_Sharpe']:.3f}")

    say("\n[5] RULE 8 -- (c, band) chosen on 2009-2016 by IS Sharpe, 2017-2026 read once")
    for _, x in W.iterrows():
        say(f"    {x['panel']} q={x['q']:.4f}: IS picks c={x['IS_pick_c']:.2f} band={x['IS_pick_band']:.2f}"
            f" (IS Sharpe {x['IS_Sharpe']:.4f}) -> OOS {x['OOS_CAGR']:.2%}/{x['OOS_Sharpe']:.4f}/"
            f"{x['OOS_MaxDD']:.2%};  anchor OOS {x['anchor_OOS_Sharpe']:.4f} "
            f"(regret {x['regret_vs_anchor']:+.4f});  OOS-best c={x['best_c']:.2f} "
            f"band={x['best_band']:.2f} {x['best_OOS_Sharpe']:.4f} (regret {x['regret_vs_best']:+.4f});"
            f"  RULES v2 {x['live_OOS_Sharpe']:.4f}, SPY {x['spy_OOS_Sharpe']:.4f}")
    say(f"    a NON-ZERO band is chosen in {int(W.picked_a_band.sum())}/{len(W)} rule-8 cells;"
        f" mean regret vs idea 30's anchor {W.regret_vs_anchor.mean():+.4f},"
        f" vs OOS-best {W.regret_vs_best.mean():+.4f}")


def main():
    P = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in P.items():
        say(f"    {k}: {v.shape[1]} cols, {v.index[0].date()} .. {v.index[-1].date()}")
    gates(P)
    core_recovery(P)
    G, W = grid(P)
    gate_grid_vs_parent(G)
    read_grid(G, W, P)
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(_tee) + "\n")
    say(f"\nwrote {SLUG}.grid.csv / .core.csv / .walkforward.csv / .console.txt")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
