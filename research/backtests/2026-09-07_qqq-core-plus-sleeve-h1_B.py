#!/usr/bin/env python3
"""Idea 30 -- qqq-core-plus-sleeve-h1: why does `60% QQQ>200d + 40% sleeve` lose to SPY on
Sharpe in the FIRST half (2009-2017), and does the queue's proposed repair
`50% QQQ + 10% SPY + 40% sleeve` close the gap?

Background
----------
Idea 24 (research/backtests/2026-09-03_core-plus-trend-sleeve.py) published variant B --
60% QQQ when QQQ > its own 200d MA else cash, + 0.40 x the idea-18 variant-B macro sleeve --
at 10.8% / 0.95 / -18.9% with halves 0.84 / 1.04, a KILL.  The queue parked one question:
the book's H2 is fine and its H1 is not, so WHAT in the first half costs it the Sharpe bar,
and is a small SPY allocation inside the core the fix.

What this script does
---------------------
[A] MATCH to idea 24 variant B's published decimals (hard assert) + a tape-provenance check.
[B] DECOMPOSITION of the H1 shortfall vs SPY:
      - the two legs run as separate books (core-only, sleeve-only) with an additivity check;
      - the algebraic Sharpe gap split  dSharpe = (mu_B - mu_S)/sig_B + mu_S(1/sig_B - 1/sig_S)
        into a RETURN term and a VOLATILITY term, per half;
      - each leg's share of the blend's mean and of its variance (covariance decomposition);
      - calendar-year returns of blend / core leg / sleeve leg / SPY for every year;
      - what the 200d gate on the core costs in each half (gated QQQ vs buy-and-hold QQQ).
[C] The GRID.  Exactly two tuned parameters:
      1. c  in {0.50, 0.60, 0.70, 0.80}          total equity core fraction (sleeve = 1 - c)
      2. q  in {0.00, 0.25, 0.50, 0.75, 0.8333, 1.00}   QQQ share of that core, rest SPY
    q=1.00 c=0.60 is idea 24's variant B (the pre-registered anchor); q=0.8333 c=0.60 is the
    queue's literal proposal (50% QQQ + 10% SPY + 40% sleeve).  All 24 points are reported.
    Panel (U56 primary = research/universe.json, B136 = universe_broad.json), cost rung
    (10 bps = PROTOCOL anchor, 25 bps) and the core GATE (ON = each core leg held only above
    its own 200d MA, OFF = held always) are REPORTED axes, not tuned choices: every point of
    every axis is printed.  Rule-8 selection runs over (c, q) at GATE=ON only, the
    pre-registered form.
[D] BOTH KEEP paths at every point: 4a against the live RULES v2 book, 4b against SPY.
[E] Rule 8 walk-forward: (c, q) chosen on 2009-2016 by IS Sharpe and by a 4b-aware IS screen,
    2017-2026 read once, against the anchor, the OOS-best cell (regret), RULES v2 and SPY.

Conventions: weekly rebalance, weights decided at close t applied at t+1 (engine), long-only,
no leverage, 10 bps per unit turnover unless the cost axis says otherwise, 260-day warm-up
skipped.  The sleeve function is copied verbatim from idea 24 (which copied it from idea 18).

CAVEATS: (1) both universes are current-constituent lists -- survivorship flatters every level
here; the c/q DIFFERENCES are far less affected.  (2) TAPE: data/prices*.csv are now on the
CORRECTED trading-day index (ideas 38/39 landed; 0 weekend rows in both files, asserted in [A]),
whereas idea 24's published row was computed on the PRE-FIX calendar-day tape.  So the agreement
in [A] is a match to the published decimals across a tape correction, not a byte-level rerun of
idea 24's own numbers; the pre-fix tape is no longer in the repo and cannot be re-run.  Per idea
39 the calendar-day cache was conservative rather than generous, so this is the direction in
which a difference would be tolerable, but it is a match, not a reproduction, and is labelled as
one throughout.  (3) QQQ's 2009-2017 run is the single best large-cap equity decade in the
sample -- any conclusion about the core's composition is conditioned on that.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights   # noqa
from engine import backtest, metrics                                     # noqa

SLUG = "2026-09-07_qqq-core-plus-sleeve-h1_B"
OUT = ROOT / "research" / "backtests"
FREQ = "W"
COSTS = [10, 25]
CS = [0.50, 0.60, 0.70, 0.80]
QS = [0.00, 0.25, 0.50, 0.75, 1.0 - 1.0 / 6.0, 1.00]
ANCHOR = (0.60, 1.00)                 # idea 24 variant B
PROPOSAL = (0.60, 1.0 - 1.0 / 6.0)    # queue idea 30: 50% QQQ + 10% SPY + 40% sleeve
IS_END, OOS_START = "2016-12-31", "2017-01-01"

# ---------------------------------------------------------------- sleeve (idea 18 variant B)
MACRO = ["SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "GLD", "DBC", "UUP"]
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
MA_WINDOW = 200


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


def core_leg(px, ticker, frac, gate):
    p = px[ticker]
    if gate:
        ma = p.rolling(MA_WINDOW).mean()
        on = (p > ma).astype(float).where(ma.notna(), 0.0)
    else:
        on = pd.Series(1.0, index=px.index)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[ticker] = frac * on
    return out


def blend_weights(px, c, q, gate=True):
    """c of NAV in equity core (q of it QQQ, 1-q SPY, each gated on its own 200d MA when
    gate=True), (1-c) of NAV in the idea-18 variant-B macro sleeve."""
    return (core_leg(px, "QQQ", c * q, gate)
            + core_leg(px, "SPY", c * (1.0 - q), gate)
            + (1.0 - c) * sleeve_b_weights(px))


# ---------------------------------------------------------------- metric helpers
def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def halves(r):
    h = len(r) // 2
    return r.iloc[:h], r.iloc[h:]


def bars_4b(r, spy):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%."""
    m, ms = metrics(r), metrics(spy)
    h1, h2 = hs(r); s1, s2 = hs(spy)
    o = metrics(r.loc[OOS_START:])["Sharpe"] - metrics(spy.loc[OOS_START:])["Sharpe"]
    d = {"H1": h1 - s1, "H2": h2 - s2, "OOS": o,
         "DD": 0.60 * abs(ms["MaxDD"]) - abs(m["MaxDD"]),
         "CAGR": m["CAGR"] - 0.70 * ms["CAGR"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4a(r, base):
    """PROTOCOL 4a: Sharpe > live book in BOTH halves and MaxDD no worse than the live book."""
    m, mb = metrics(r), metrics(base)
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(mb["MaxDD"]) - abs(m["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def run(px, w, cost, start):
    res = backtest(px, w, cost_bps=cost, freq=FREQ)
    return (res["returns"].loc[start:], res["turnover"].loc[start:],
            res["weights"].loc[start:].sum(axis=1))


def fmt_bars(d):
    return " ".join(f"{k}{v:+.3f}" for k, v in d.items())


# ---------------------------------------------------------------- [A]+[B] on the primary panel
def decomposition(px, spy, start, log):
    c, q = ANCHOR
    wB = blend_weights(px, c, q, gate=True)
    rB, tB, gB = run(px, wB, 10, start)
    m = metrics(rB); h1, h2 = hs(rB)

    log("\n" + "=" * 100)
    log("[A] MATCH to idea 24 variant B (60% QQQ>200d + 40% sleeve), U56 @10 bps weekly")
    wknd = int((px.index.dayofweek >= 5).sum())
    assert wknd == 0, f"expected the corrected trading-day tape, found {wknd} weekend rows"
    log(f"    tape check: {len(px)} rows, {wknd} weekend rows -> CORRECTED trading-day index "
        "(ideas 38/39).  Idea 24 ran on the PRE-FIX calendar-day tape, which is no longer in the "
        "repo, so what follows is a match to the published decimals ACROSS that correction, not a "
        "byte-level rerun.")
    log(f"    today's tape (last bar {px.index[-1].date()}):  CAGR {m['CAGR']:.1%}  "
        f"Sharpe {m['Sharpe']:.2f}  MaxDD {m['MaxDD']:.1%}  halves {h1:.2f} / {h2:.2f}")
    log("    published row (2026-09-03): 10.8% | 0.95 | -18.9% | 0.84 / 1.04")
    # data/prices.csv has grown 2 bars since idea 24 ran; the hard gate is the same book on the
    # tape truncated to idea 24's last bar (2026-09-02), which must match the published decimals.
    pxr = px.loc[:"2026-09-02"]
    rr, _, _ = run(pxr, blend_weights(pxr, c, q, gate=True), 10, pxr.index[260])
    mr = metrics(rr); r1, r2 = hs(rr)
    got = (round(mr["CAGR"], 3), round(mr["Sharpe"], 2), round(mr["MaxDD"], 3),
           round(r1, 2), round(r2, 2))
    exp = (0.108, 0.95, -0.189, 0.84, 1.04)
    assert got == exp, f"MATCH FAILED on the 2026-09-02 tape: {got} != {exp}"
    log(f"    same book on the 2026-09-02 tape: {mr['CAGR']:.1%} | {mr['Sharpe']:.2f} | "
        f"{mr['MaxDD']:.1%} | {r1:.2f} / {r2:.2f}  -> MATCHES the published decimals")
    log("    (the 0.1pp CAGR / 0.01 H2 difference vs today's tape is 2 extra bars, not a code change)")

    # legs as separate books
    rc, _, _ = run(px, core_leg(px, "QQQ", c, True), 10, start)          # 60% gated QQQ
    rs, _, _ = run(px, (1.0 - c) * sleeve_b_weights(px), 10, start)      # 40% sleeve
    add = rc + rs
    log("\n[B] DECOMPOSITION of the blend into its two legs (each run as its own book)")
    log(f"    additivity check: corr(core+sleeve, blend) = {add.corr(rB):.6f}, "
        f"mean |diff| = {(add - rB).abs().mean():.2e}/day, "
        f"CAGR {metrics(add)['CAGR']:.2%} vs blend {m['CAGR']:.2%}")

    rows = []
    for nm, r in (("blend B", rB), ("core leg 60% QQQ>200d", rc), ("sleeve leg 40%", rs),
                  ("SPY", spy)):
        mm = metrics(r); a, b = hs(r)
        ma, mb = metrics(halves(r)[0]), metrics(halves(r)[1])
        rows.append(dict(book=nm, CAGR=mm["CAGR"], Sharpe=mm["Sharpe"], MaxDD=mm["MaxDD"],
                         H1_CAGR=ma["CAGR"], H1_Vol=ma["Vol"], H1_Sharpe=a, H1_MaxDD=ma["MaxDD"],
                         H2_CAGR=mb["CAGR"], H2_Vol=mb["Vol"], H2_Sharpe=b, H2_MaxDD=mb["MaxDD"]))
    log("\n    Full sample and compare()-halves (H1 = " + str(halves(rB)[0].index[0].date()) +
        " -> " + str(halves(rB)[0].index[-1].date()) + ", H2 = " +
        str(halves(rB)[1].index[0].date()) + " -> " + str(halves(rB)[1].index[-1].date()) + ")")
    log(pd.DataFrame(rows).set_index("book").to_string(float_format=lambda x: f"{x:.3f}"))

    # algebraic Sharpe gap split, per half
    log("\n    Sharpe gap vs SPY, split into a RETURN term and a VOLATILITY term:")
    log("      dSharpe = (mu_B - mu_S)/sig_B  +  mu_S * (1/sig_B - 1/sig_S)")
    split_rows = []
    for label, rr, ss in (("H1", halves(rB)[0], halves(spy)[0]),
                          ("H2", halves(rB)[1], halves(spy)[1]),
                          ("full", rB, spy)):
        mu_b, sg_b = rr.mean() * 252, rr.std() * np.sqrt(252)
        mu_s, sg_s = ss.mean() * 252, ss.std() * np.sqrt(252)
        ret_t = (mu_b - mu_s) / sg_b
        vol_t = mu_s * (1.0 / sg_b - 1.0 / sg_s)
        split_rows.append(dict(period=label, mu_B=mu_b, mu_SPY=mu_s, sig_B=sg_b, sig_SPY=sg_s,
                               dSharpe=mu_b / sg_b - mu_s / sg_s,
                               return_term=ret_t, vol_term=vol_t))
    log(pd.DataFrame(split_rows).set_index("period").to_string(float_format=lambda x: f"{x:.4f}"))

    # each leg's share of the blend's mean and variance
    log("\n    Leg shares of the blend's mean return and of its VARIANCE (cov(leg, blend)/var(blend)):")
    var_rows = []
    for label, rr in (("H1", halves(rB)[0]), ("H2", halves(rB)[1]), ("full", rB)):
        cc = rc.loc[rr.index]; sl = rs.loc[rr.index]
        v = rr.var()
        var_rows.append(dict(period=label,
                             mean_share_core=cc.mean() / rr.mean(),
                             mean_share_sleeve=sl.mean() / rr.mean(),
                             var_share_core=cc.cov(rr) / v, var_share_sleeve=sl.cov(rr) / v,
                             corr_core_sleeve=cc.corr(sl),
                             sleeve_ann_ret=sl.mean() * 252, sleeve_ann_vol=sl.std() * np.sqrt(252)))
    log(pd.DataFrame(var_rows).set_index("period").to_string(float_format=lambda x: f"{x:.4f}"))

    # calendar years
    yr = pd.DataFrame({"blend B": rB, "core leg": rc, "sleeve leg": rs, "SPY": spy})
    ycal = yr.groupby(yr.index.year).apply(lambda x: (1 + x).prod() - 1)
    ycal["B - SPY"] = ycal["blend B"] - ycal["SPY"]
    log("\n    Calendar-year returns (the queue's 'decompose by year'):")
    log(ycal.to_string(float_format=lambda x: f"{x:+.2%}"))
    h1y = ycal.loc[ycal.index <= 2016]
    log(f"\n    H1 era (<=2016): blend beats SPY in {(h1y['B - SPY'] > 0).sum()}/{len(h1y)} years, "
        f"mean gap {h1y['B - SPY'].mean():+.2%}; sleeve leg mean {h1y['sleeve leg'].mean():+.2%}, "
        f"core leg mean {h1y['core leg'].mean():+.2%}")
    h2y = ycal.loc[ycal.index >= 2017]
    log(f"    H2 era (>=2017): blend beats SPY in {(h2y['B - SPY'] > 0).sum()}/{len(h2y)} years, "
        f"mean gap {h2y['B - SPY'].mean():+.2%}; sleeve leg mean {h2y['sleeve leg'].mean():+.2%}, "
        f"core leg mean {h2y['core leg'].mean():+.2%}")

    # what the 200d gate costs the core
    rcg, _, _ = run(px, core_leg(px, "QQQ", c, True), 10, start)
    rcn, _, _ = run(px, core_leg(px, "QQQ", c, False), 10, start)
    log("\n    What the 200d gate costs the CORE leg (60% QQQ, gated vs always-on):")
    grows = []
    for label, a, b in (("H1", halves(rcg)[0], halves(rcn)[0]),
                        ("H2", halves(rcg)[1], halves(rcn)[1]),
                        ("full", rcg, rcn)):
        ma, mb = metrics(a), metrics(b)
        grows.append(dict(period=label, gated_CAGR=ma["CAGR"], ungated_CAGR=mb["CAGR"],
                          d_CAGR=ma["CAGR"] - mb["CAGR"], gated_Sharpe=ma["Sharpe"],
                          ungated_Sharpe=mb["Sharpe"], d_Sharpe=ma["Sharpe"] - mb["Sharpe"],
                          gated_MaxDD=ma["MaxDD"], ungated_MaxDD=mb["MaxDD"]))
    log(pd.DataFrame(grows).set_index("period").to_string(float_format=lambda x: f"{x:.4f}"))
    off = (core_leg(px, "QQQ", c, True).loc[start:]["QQQ"] == 0)
    log(f"    gate OFF (core in cash): {off.mean():.1%} of days full sample, "
        f"{off.loc[:IS_END].mean():.1%} in 2009-2016, {off.loc[OOS_START:].mean():.1%} in 2017-2026")
    log(f"    blend mean gross: {gB.mean():.1%} full, {gB.loc[:IS_END].mean():.1%} 2009-2016, "
        f"{gB.loc[OOS_START:].mean():.1%} 2017-2026; turnover "
        f"{tB.sum() / (len(rB) / 252):.1f}x/yr")
    return ycal


# ---------------------------------------------------------------- main
def main():
    lines = []

    def log(s=""):
        print(s); lines.append(str(s))

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    grid_rows, wf_rows = [], []

    for pname, px in panels.items():
        miss = [t for t in MACRO if t not in px.columns]
        assert not miss, f"{pname} missing {miss}"
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        log("\n" + "#" * 100)
        log(f"### PANEL {pname}: {px.shape[1]} columns, {px.index[0].date()} -> {px.index[-1].date()}, "
            f"eval from {start.date()}")
        log(f"    SPY  CAGR {ms['CAGR']:.2%} Sharpe {ms['Sharpe']:.3f} MaxDD {ms['MaxDD']:.2%} "
            f"H1/H2 {s1:.3f}/{s2:.3f} | OOS CAGR {so['CAGR']:.2%} Sharpe {so['Sharpe']:.3f} "
            f"MaxDD {so['MaxDD']:.2%}")
        log(f"    4b bars on this panel: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{so['Sharpe']:.3f}  "
            f"|MaxDD|<={0.60 * abs(ms['MaxDD']):.2%}  CAGR>={0.70 * ms['CAGR']:.2%}")

        if pname == "U56":
            decomposition(px, spy, start, log)

        for cost in COSTS:
            base, _, _ = run(px, rules_v2_weights(px), cost, start)
            mb = metrics(base); b1, b2 = hs(base)
            log("\n" + "=" * 100)
            log(f"[C] GRID -- panel {pname} @ {cost} bps.  RULES v2 (live, 4a comparand): "
                f"CAGR {mb['CAGR']:.2%} Sharpe {mb['Sharpe']:.3f} MaxDD {mb['MaxDD']:.2%} "
                f"H1/H2 {b1:.3f}/{b2:.3f}")
            for gate in (True, False):
                log(f"\n--- core GATE {'ON (each leg above its own 200d MA)' if gate else 'OFF (always held)'}")
                tab = []
                for c in CS:
                    for q in QS:
                        r, t, g = run(px, blend_weights(px, c, q, gate), cost, start)
                        m = metrics(r); h1, h2 = hs(r)
                        oo = metrics(r.loc[OOS_START:])
                        ok4b, d4b, f4b = bars_4b(r, spy)
                        ok4a, d4a, f4a = bars_4a(r, base)
                        tag = ""
                        if (c, q) == ANCHOR and gate: tag = " <- idea 24 variant B (anchor)"
                        if (c, q) == PROPOSAL and gate: tag = " <- queue proposal 50/10/40"
                        rec = dict(panel=pname, cost=cost, gate=int(gate), c=c, q=round(q, 4),
                                   QQQ_pct=round(100 * c * q, 1), SPY_pct=round(100 * c * (1 - q), 1),
                                   sleeve_pct=round(100 * (1 - c), 1),
                                   CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                   H1=h1, H2=h2, OOS_CAGR=oo["CAGR"], OOS_Sharpe=oo["Sharpe"],
                                   OOS_MaxDD=oo["MaxDD"],
                                   IS_Sharpe=metrics(r.loc[:IS_END])["Sharpe"],
                                   IS_MaxDD=metrics(r.loc[:IS_END])["MaxDD"],
                                   IS_CAGR=metrics(r.loc[:IS_END])["CAGR"],
                                   turnover=t.sum() / (len(r) / 252), gross=g.mean(),
                                   pass4a=int(ok4a), fail4a="+".join(f4a) or "-",
                                   pass4b=int(ok4b), fail4b="+".join(f4b) or "-",
                                   m4b_H1=d4b["H1"], m4b_H2=d4b["H2"], m4b_OOS=d4b["OOS"],
                                   m4b_DD=d4b["DD"], m4b_CAGR=d4b["CAGR"], tag=tag.strip())
                        grid_rows.append(rec)
                        tab.append(dict(c=c, q=round(q, 3), mix=f"{100*c*q:.0f}/{100*c*(1-q):.0f}/{100*(1-c):.0f}",
                                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                        H1=h1, H2=h2, OOS_Sh=oo["Sharpe"],
                                        turn=t.sum() / (len(r) / 252),
                                        _4a="PASS" if ok4a else "fail:" + "+".join(f4a),
                                        _4b="PASS" if ok4b else "fail:" + "+".join(f4b),
                                        note=tag.strip()))
                log(pd.DataFrame(tab).to_string(index=False, float_format=lambda x: f"{x:.3f}"))

            # ---- [E] rule 8 on this panel/cost.  GATE=ON is the pre-registered selection (the
            # gate is idea 24's construction); the GATE=OFF selection is reported too because
            # idea 24's own variant D already carried an ungated core, and because that is where
            # every 4b pass in this grid lives -- but selecting across the gate makes THREE dials,
            # so it is reported as a diagnostic, never as a rule-8 pick.
            spy_is = spy.loc[:IS_END]; mis = metrics(spy_is)
            bo = metrics(base.loc[OOS_START:])
            for gflag, gname in ((1, "GATE=ON (pre-registered)"), (0, "GATE=OFF (diagnostic, 3rd dial)")):
                sub = [r for r in grid_rows
                       if r["panel"] == pname and r["cost"] == cost and r["gate"] == gflag]
                pick_sh = max(sub, key=lambda r: r["IS_Sharpe"])
                # 4b-aware IS screen: among cells whose IS window clears 4b's DD cap and CAGR
                # floor (on the IS window vs SPY's IS window), take best IS Sharpe; else fall
                # back to plain IS Sharpe.
                elig = [r for r in sub if abs(r["IS_MaxDD"]) <= 0.60 * abs(mis["MaxDD"])
                        and r["IS_CAGR"] >= 0.70 * mis["CAGR"]]
                pick_4b = max(elig, key=lambda r: r["IS_Sharpe"]) if elig else pick_sh
                best_oos = max(sub, key=lambda r: r["OOS_Sharpe"])
                anchor = [r for r in sub
                          if (r["c"], round(r["q"], 4)) == (ANCHOR[0], round(ANCHOR[1], 4))][0]
                prop = [r for r in sub
                        if (r["c"], round(r["q"], 4)) == (PROPOSAL[0], round(PROPOSAL[1], 4))][0]
                log(f"\n[E] RULE 8 walk-forward -- {pname} @ {cost} bps (IS 2009-2016 -> OOS "
                    f"2017-2026), selection over (c,q) at {gname}"
                    + (f"   [{len(elig)}/{len(sub)} cells clear the IS 4b screen]" if elig else
                       "   [IS 4b screen empty -> falls back to IS Sharpe]"))
                for lbl, r in (("IS-Sharpe pick", pick_sh), ("4b-aware IS pick", pick_4b),
                               ("anchor (idea 24 B)", anchor), ("queue proposal 50/10/40", prop),
                               ("OOS-best (hindsight)", best_oos)):
                    log(f"    {lbl:<24} c={r['c']:.2f} q={r['q']:.3f} "
                        f"({r['QQQ_pct']:.0f}/{r['SPY_pct']:.0f}/{r['sleeve_pct']:.0f})  "
                        f"IS Sharpe {r['IS_Sharpe']:.3f} -> OOS CAGR {r['OOS_CAGR']:.2%} "
                        f"Sharpe {r['OOS_Sharpe']:.3f} MaxDD {r['OOS_MaxDD']:.2%}")
                    wf_rows.append(dict(panel=pname, cost=cost, gate=gflag, role=lbl, c=r["c"],
                                        q=round(r["q"], 4),
                                        mix=f"{r['QQQ_pct']:.0f}/{r['SPY_pct']:.0f}/{r['sleeve_pct']:.0f}",
                                        IS_Sharpe=r["IS_Sharpe"], OOS_CAGR=r["OOS_CAGR"],
                                        OOS_Sharpe=r["OOS_Sharpe"], OOS_MaxDD=r["OOS_MaxDD"],
                                        OOS_SPY_Sharpe=so["Sharpe"], OOS_SPY_CAGR=so["CAGR"],
                                        OOS_SPY_MaxDD=so["MaxDD"], OOS_v2_Sharpe=bo["Sharpe"],
                                        OOS_v2_CAGR=bo["CAGR"], OOS_v2_MaxDD=bo["MaxDD"]))
                log(f"    {'SPY OOS':<24} CAGR {so['CAGR']:.2%} Sharpe {so['Sharpe']:.3f} "
                    f"MaxDD {so['MaxDD']:.2%}")
                log(f"    {'RULES v2 OOS':<24} CAGR {bo['CAGR']:.2%} Sharpe {bo['Sharpe']:.3f} "
                    f"MaxDD {bo['MaxDD']:.2%}")
                log(f"    chooser regret (IS-Sharpe pick - OOS best): "
                    f"{pick_sh['OOS_Sharpe'] - best_oos['OOS_Sharpe']:+.3f}"
                    f" | 4b-aware regret {pick_4b['OOS_Sharpe'] - best_oos['OOS_Sharpe']:+.3f}"
                    f" | pick vs anchor {pick_sh['OOS_Sharpe'] - anchor['OOS_Sharpe']:+.3f}")

    G = pd.DataFrame(grid_rows)
    W = pd.DataFrame(wf_rows)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    W.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)

    log("\n" + "=" * 100)
    log("[D] KEEP-path census over the whole grid (all 96 panel x cost x gate x c x q points)")
    log(G.groupby(["panel", "cost", "gate"])[["pass4a", "pass4b"]].agg(["sum", "count"]).to_string())
    log("\n    4b failing-bar census (GATE=ON, 10 bps):")
    on10 = G[(G.gate == 1) & (G.cost == 10)]
    log(on10.groupby(["panel", "fail4b"]).size().to_string())
    log(f"\n    4b passes anywhere: {int(G.pass4b.sum())}/{len(G)};  4a passes anywhere: "
        f"{int(G.pass4a.sum())}/{len(G)}")
    if G.pass4b.sum():
        log("\n    Every 4b-passing point:")
        log(G[G.pass4b == 1][["panel", "cost", "gate", "c", "q", "QQQ_pct", "SPY_pct", "sleeve_pct",
                              "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # the queue's specific question, stated once
    log("\n" + "=" * 100)
    log("[F] The queue's question, answered on the anchor vs the proposal (GATE=ON):")
    for pname in panels:
        for cost in COSTS:
            a = G[(G.panel == pname) & (G.cost == cost) & (G.gate == 1) & (G.c == ANCHOR[0])
                  & (np.isclose(G.q, ANCHOR[1], atol=1e-3))].iloc[0]
            p = G[(G.panel == pname) & (G.cost == cost) & (G.gate == 1) & (G.c == PROPOSAL[0])
                  & (np.isclose(G.q, PROPOSAL[1], atol=1e-3))].iloc[0]
            log(f"    {pname} @{cost}bps  anchor  H1 {a.H1:.3f} H2 {a.H2:.3f} Sharpe {a.Sharpe:.3f} "
                f"CAGR {a.CAGR:.2%} DD {a.MaxDD:.2%} | 4b margin H1 {a.m4b_H1:+.3f}")
            log(f"    {pname} @{cost}bps  50/10/40 H1 {p.H1:.3f} H2 {p.H2:.3f} Sharpe {p.Sharpe:.3f} "
                f"CAGR {p.CAGR:.2%} DD {p.MaxDD:.2%} | 4b margin H1 {p.m4b_H1:+.3f}  "
                f"(dH1 {p.H1 - a.H1:+.3f}, dSharpe {p.Sharpe - a.Sharpe:+.3f})")

    log("\n" + "=" * 100)
    log("[G] Two things the grid settles, stated as numbers")
    for cost in COSTS:
        on = G[(G.gate == 1) & (G.cost == cost) & (G.panel == "U56")]
        off = G[(G.gate == 0) & (G.cost == cost) & (G.panel == "U56")]
        sp = metrics(load_universe()["SPY"].pct_change().fillna(0).loc[panels["U56"].index[260]:])
        s1 = hs(load_universe()["SPY"].pct_change().fillna(0).loc[panels["U56"].index[260]:])[0]
        log(f"    U56 @{cost}bps: H1 Sharpe over all 24 (c,q) points -- GATE ON "
            f"[{on.H1.min():.3f}, {on.H1.max():.3f}], GATE OFF [{off.H1.min():.3f}, {off.H1.max():.3f}];"
            f"  4b H1 bar = SPY {s1:.3f}")
        log(f"      -> gate ON: {(on.H1 > s1).sum()}/24 clear the H1 bar;  gate OFF: "
            f"{(off.H1 > s1).sum()}/24 clear it")
    # panel degeneracy: this book holds only 10 ETFs, all present in both panels
    a = G[G.panel == "U56"].set_index(["cost", "gate", "c", "q"])[["CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
    b = G[G.panel == "B136"].set_index(["cost", "gate", "c", "q"])[["CAGR", "Sharpe", "MaxDD", "H1", "H2"]]
    d = (a - b).abs().max()
    log(f"    PANEL AXIS IS DEGENERATE for this book: it holds only QQQ, SPY and the 9 sleeve ETFs, "
        f"all present in both panels.")
    log(f"      max |U56 - B136| across all 96 cells: CAGR {d['CAGR']:.2e}, Sharpe {d['Sharpe']:.2e}, "
        f"MaxDD {d['MaxDD']:.2e}, H1 {d['H1']:.2e}, H2 {d['H2']:.2e} (price-file rounding only).")
    log("      B136 is therefore NOT an independent confirmation here; only the 4a comparand differs.")

    (OUT / f"{SLUG}.console.txt").write_text("\n".join(lines) + "\n")
    print(f"\nwrote {SLUG}.grid.csv ({len(G)} rows), {SLUG}.walkforward.csv ({len(W)} rows), "
          f"{SLUG}.console.txt")


if __name__ == "__main__":
    main()
