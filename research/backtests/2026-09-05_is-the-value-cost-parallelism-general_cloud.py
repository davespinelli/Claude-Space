#!/usr/bin/env python3
"""QUEUE idea 167 — is-the-value-cost-parallelism-general  (cloud, 2026-09-05).

QUESTION (pre-registered, verbatim from QUEUE.md idea 167)
    "idea 159 found the value and the cost of the vol tilt decay at the SAME rate in book share
     (d = slope(log g) - slope(log c) straddles zero 6 of 6), which makes 'stops paying above m'
     undefined for that tilt.  If the mechanism is arithmetic (both scale with the names the
     instrument moves) it must hold for every instrument the project prices, not just a tilt:
     re-run the same d-statistic for the 200d gate, the 3% band, de-grossing and the per-name
     trailing stop from idea 74's insurance menu.  If d straddles zero everywhere, idea 74's
     whole exchange-rate framing is a ratio, not a threshold, and no drawdown budget can be
     quoted as a level.  Max 2 params."

WHAT IS AT STAKE.
    Idea 74/94's price list quotes each instrument at a RATE (pp CAGR per pp MaxDD) and RULES
    has been asked (idea 69) to state gross as a drawdown BUDGET — a level.  A level is only
    meaningful if an instrument's value and its cost move apart somewhere on the axis the
    project varies.  Idea 159 showed they do not for the vol tilt.  If they do not for the
    gates, the de-gross lever or the stop either, then every entry on idea 74's menu is a
    scale-free ratio and no threshold ("stop using this above m", "spend this much drawdown")
    can be quoted from any of them.

THE STATISTIC (idea 159's, re-run, not re-derived).  For an instrument at book share m:
    g(m) = |CAGR(ON @ 0 bps) - CAGR(OFF @ 0 bps)|          realised magnitude, pp/yr
    c(m) = the cost of running it, two bars (both reported):
      BAR-INC  exact incremental cost, idea 159's honest bar and its primary:
               [CAGR(ON@0)-CAGR(ON@10)] - [CAGR(OFF@0)-CAGR(OFF@10)].  May be <= 0.
      BAR-TO   10 bps x |annualised turnover(ON) - annualised turnover(OFF)|.  ALWAYS >= 0, so
               log c exists at every share; this is the bar the log-slope test is run on.
    d = slope(log g on m) - slope(log c on m), OLS, then a circular block bootstrap (block 21
    trading days, 2000 replicates, seed 167) of d, resampling the two return paths on the SAME
    block index and holding c at its point estimate — idea 159's scheme exactly.
    d < 0 (distinguishably) is REQUIRED for "the instrument stops paying above some share".

DEVIATION FROM IDEA 159, STATED NOT BURIED.  Idea 159's second bar was BAR-OVL, 10 bps x the
    annualised weight distance |w_tilt - w_NONE| between two TARGET books.  Three of this run's
    four instruments (de-grossing aside) are execution overlays, and the per-name stop changes
    no target weight at all, so BAR-OVL is identically zero for it and cannot be the common
    bar.  BAR-TO is the same quantity read off realised trading instead of targets, and it is
    what an overlay actually costs.  BAR-INC is unchanged from idea 159.

INSTRUMENTS — idea 74/94's menu, four of them, each an OVERLAY on the SAME ungated base book,
    run through idea 94's committed `run()` simulator (imported, not retyped):
      G200    per-name 200d MA gate, de-gross convention (gated-out weight -> cash)
      BAND3   200d MA with a +/-3% re-entry band, de-gross convention (idea 57's instrument)
      DEGROSS static gross multiplier 0.75 of the base book (i.e. hold 25% less; idea 66's
              exact lever, the price list's reference instrument)
      STOP15  per-name 15% trailing stop (idea 9's instrument)
    OFF (the control) is the same base book with no overlay, at the same share.

BOOK SHARE AXIS — idea 159's grid, m in {0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.53, 0.70, 0.85,
    1.00}, n = max(2, round(m x N_tradable)).  The base book is idea 78/94's TOP20 ranking
    generalised in n: composite (no vol scaler), UNGATED, top-n at 0.75/n.  Ungated is forced:
    idea 94 showed a gated base book makes the gate instruments invisible.

TUNED PARAMETERS — exactly two: the INSTRUMENT (4) and the SHARE m (10).  Every grid point is
    reported.  Panel is a corpus axis (u56, broad, small), as in ideas 153/159.

REPRODUCTION GATE, asserted before any new number is read
    [a] mean weekly eligible names per panel: idea 153/159 published 37.5 / 91.5 / 141.2.
    [b] idea 94's published `EWall + band3-rw` cell on u56 @10 bps: 12.2% / 1.161 / -17.7%,
        halves 1.210/1.129, OOS 1.203 — re-run through the imported simulator.
    [c] the cost-derivation identity r_c = r_0 - turnover x c/1e4 against a fresh 10 bps run,
        for the base book AND for the STOP arm (whose state machine reads prices, not equity,
        so the identity must hold there too).  This is what makes every gross/net pair below
        the SAME book rather than two runs.

WALK-FORWARD (PROTOCOL rule 8), fixed before any OOS number is read
    d and the implied crossing m* are re-estimated on 2009/2010-2016 ONLY; the OOS window
    2017-2026 is read once.  Three arms per (panel, instrument): ALWAYS (run the instrument at
    every share), NEVER (the base book), GATED (run it only at m <= m*_IS, else the base book).
    OOS CAGR/Sharpe/MaxDD reported per arm against RULES v1 on the same panel and against SPY.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
    P1  Reproduction [a]-[c] all pass.
    P2  d straddles zero (bootstrap 5-95 interval contains 0) in the large majority of (panel,
        instrument) cells — idea 159's arithmetic generalises.
    P3  DEGROSS is the one possible exception in the OTHER direction: it is an exact lever
        (idea 66) whose cost is a pure turnover saving, so its c may be negative or flat and
        its d undefined rather than zero.  Reported as such, not forced.
    P4  The per-name STOP is the instrument most likely to show d < 0, because its firing rate
        rises with holding-episode length (idea 76) which is not proportional to share.
    P5  No new book and no KEEP: nothing here proposes a rule change.

CAVEATS carried, not buried
    * SURVIVORSHIP: all three panels are current-constituent lists (idea 54); the small panel is
      the sub-$2B screen's SURVIVORS since 2010 (44 tickers with max_1d_move >= 1.0 dropped
      first).  Levels are biased up; the d-statistic compares shares WITHIN a panel.
    * The eligibility gate is INVERTED on the small panel (ideas 39/49), so the G200/BAND3
      numbers there describe an instrument that is known not to work on that panel.  That is
      the point of including it, and it is flagged in every table.
    * A block bootstrap on ONE realised path measures sampling error around that path, not
      uncertainty across worlds (idea 159's caveat, carried).
    * c is held at its point estimate inside the bootstrap (idea 159's scheme), so the interval
      understates the uncertainty in d.  A wider true interval only strengthens "straddles 0".
    * m = 1.00 forces every share's book onto the whole panel, so ON and OFF differ only by the
      overlay; g does not go to zero there as it did for a tilt.
    * Ideas 38 (calendar-day index) and 126 (t+1 execution) carry over unchanged.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .curve.csv, .dslope.csv,
.walkforward.csv.
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import rules_v1_weights  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-05_is-the-value-cost-parallelism-general_cloud"
OUT = ROOT / "research" / "backtests"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


H = _load(OUT / "2026-09-04_drawdown-insurance-price-list_B.py", "i94")     # run(), targets(), gates
C = _load(OUT / "2026-09-05_cagr-floor-calibration_B.py", "i129")           # panel(), bars, margins
I159 = _load(OUT / "2026-09-05_the-share-at-which-ranking-stops-paying_B.py", "i159")

FREQ = H.FREQ                       # "W"
GROSS, MAX_VOL = H.GROSS, H.MAX_VOL  # 0.75, 0.60
IS_END, OOS_START = H.IS_END, H.OOS_START
COSTS = [10.0, 25.0]
PHI0, DELTA0 = 0.70, 0.60
PANELS = ["u56", "broad", "small"]
SHARES = I159.SHARES                                       # tuned parameter 1 (10 values)
INSTR = ["G200", "BAND3", "DEGROSS", "STOP15"]             # tuned parameter 2 (4 values)
BLOCK, NBOOT, SEED = I159.BLOCK, I159.NBOOT, 167           # 21d blocks, 2000 replicates

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 70)
pd.set_option("display.max_rows", 1200)

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


def net(r0, to, c):
    """Idea 159's cost-derivation identity: the engine/simulator is linear in cost."""
    return r0 - to * c / 1e4


def cagr(r):
    return metrics(r)["CAGR"] if len(r) >= 60 else np.nan


def base_targets(px, n):
    """Idea 94's TOP20 book generalised in n: composite (no vol scaler), UNGATED, top-n."""
    rank = H.composite(px).rank(axis=1, ascending=False)
    return (rank <= n).astype(float) * (GROSS / n)


def arm_run(px, W, instr):
    """One overlay on the base book, at 0 bps.  Idea 94's simulator, imported."""
    if instr == "OFF":
        return H.run(px, W, bps=0.0)
    if instr == "G200":
        return H.run(px, W.where(H.gate_mask(px, "g200"), 0.0), bps=0.0)
    if instr == "BAND3":
        return H.run(px, W.where(H.gate_mask(px, "band3"), 0.0), bps=0.0)
    if instr == "DEGROSS":
        return H.run(px, W, m=0.75, bps=0.0)
    if instr == "STOP15":
        return H.run(px, W, stop=0.15, bps=0.0)
    raise ValueError(instr)


def logslopes(ms, g, c):
    """OLS of log g and log c on m; returns (slope_g, slope_c, d)."""
    ms, g, c = (np.asarray(x, float) for x in (ms, g, c))
    k = np.isfinite(g) & np.isfinite(c) & (g > 0) & (c > 0)
    if k.sum() < 3:
        return np.nan, np.nan, np.nan
    X = np.column_stack([np.ones(k.sum()), ms[k]])
    bg = np.linalg.lstsq(X, np.log(g[k]), rcond=None)[0][1]
    bc = np.linalg.lstsq(X, np.log(c[k]), rcond=None)[0][1]
    return float(bg), float(bc), float(bg - bc)


def main():
    t0 = time.time()
    say("=" * 190)
    say(f"IDEA 167 — is-the-value-cost-parallelism-general   ({STEM})")
    say("Idea 159's d = slope(log g) - slope(log c) re-run for four instruments off idea 74's "
        "menu (200d gate, 3% band, de-grossing, per-name trailing stop) on three panels.")
    say("PRE-REGISTERED: 2 tuned params (instrument x 4, book share m x 10).  Panel is a corpus "
        "axis.  Every grid point reported.")
    say("=" * 190)

    ok, ref, RET = {}, {}, {}
    grid_rows, curve_rows, d_rows, wf_rows = [], [], [], []

    for pk in PANELS:
        px, spy_full, desc = C.panel(pk)
        start = px.index[260]
        spy = spy_full.reindex(px.index).fillna(0.0).loc[start:]
        bfull, bIS, bOOS = (C.bars_win(spy, w) for w in ("full", "IS", "OOS"))
        v1res = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        v1r0, v1to = v1res["returns"].loc[start:], v1res["turnover"].loc[start:]
        v1 = {c: net(v1r0, v1to, c) for c in COSTS}
        N = px.shape[1]
        nmap = {m: max(2, int(round(m * N))) for m in SHARES}
        _, above, vol = H.composite(px), (px > px.rolling(200).mean()), H.vol20(px)
        n_elig = float((above & (vol < MAX_VOL)).loc[start:].sum(axis=1).mean())
        ref[pk] = dict(px=px, start=start, spy=spy, bfull=bfull, bIS=bIS, bOOS=bOOS, v1=v1,
                       nmap=nmap, N=N, desc=desc)
        ms_, mso_ = metrics(spy), metrics(spy.loc[OOS_START:])
        say(f"\n[panel] {pk} = {desc}: {N} tradable cols, eval {start.date()} .. "
            f"{px.index[-1].date()}, mean weekly eligible {n_elig:.1f}")
        say("    share -> n:  " + ", ".join(f"{m:.2f}->{nmap[m]}" for m in SHARES))
        say(f"    SPY  full {ms_['CAGR']:7.2%}/{ms_['Sharpe']:.3f}/{ms_['MaxDD']:8.2%}  halves "
            f"{bfull['s1']:.3f}/{bfull['s2']:.3f} | OOS {mso_['CAGR']:7.2%}/"
            f"{mso_['Sharpe']:.3f}/{mso_['MaxDD']:8.2%}")
        for c in COSTS:
            a_, b_ = metrics(v1[c]), metrics(v1[c].loc[OOS_START:])
            say(f"    RULES v1 @{int(c)}bps: {a_['CAGR']:7.2%}/{a_['Sharpe']:.3f}/"
                f"{a_['MaxDD']:8.2%} | OOS {b_['CAGR']:7.2%}/{b_['Sharpe']:.3f}/{b_['MaxDD']:8.2%}")
        pub_e = {"u56": 37.5, "broad": 91.5, "small": 141.2}[pk]
        ok[f"a:{pk}"] = abs(n_elig - pub_e) < 0.15
        say(f"[a] mean weekly eligible: idea 153/159 published {pub_e}, this run {n_elig:.1f} -> "
            f"{'MATCH' if ok[f'a:{pk}'] else 'MISMATCH'}")

        # ---------------------------------------------------------- the grid
        for m in SHARES:
            n = nmap[m]
            W = base_targets(px, n)
            for instr in ["OFF"] + INSTR:
                res = arm_run(px, W, instr)
                r0, to = res["r"].loc[start:], res["to"].loc[start:]
                RET[(pk, m, instr)] = (r0, to)
                yrs = len(r0) / 252
                row = dict(panel=pk, m=m, n=n, instr=instr, CAGR_0=cagr(r0),
                           to_yr=float(to.sum() / yrs), n_stops=res["n_stops"],
                           gross_mean=float(res["gross"].loc[start:].mean()))
                for c in COSTS:
                    rc = net(r0, to, c)
                    mm, mo = metrics(rc), metrics(rc.loc[OOS_START:])
                    h1, h2 = H.halves(rc)
                    bs, (bh1, bh2) = metrics(v1[c]), H.halves(v1[c])
                    mg = C.margins_at(rc, bfull, PHI0, DELTA0, "full")
                    mgo = C.margins_at(rc, bOOS, PHI0, DELTA0, "OOS")
                    row.update({
                        f"CAGR_{int(c)}": mm["CAGR"], f"Sharpe_{int(c)}": mm["Sharpe"],
                        f"MaxDD_{int(c)}": mm["MaxDD"], f"H1_{int(c)}": h1, f"H2_{int(c)}": h2,
                        f"OOSCAGR_{int(c)}": mo["CAGR"], f"OOSSharpe_{int(c)}": mo["Sharpe"],
                        f"OOSMaxDD_{int(c)}": mo["MaxDD"],
                        f"pass4a_{int(c)}": bool(h1 > bh1 and h2 > bh2
                                                 and mm["MaxDD"] >= bs["MaxDD"]),
                        f"pass4b_{int(c)}": len(C.fails(mg)) == 0,
                        f"fail4b_{int(c)}": "|".join(C.fails(mg)) or "-",
                        f"pass4bOOS_{int(c)}": len(C.fails(mgo)) == 0,
                    })
                grid_rows.append(row)
        say(f"    grid done ({time.time() - t0:.0f}s)")

        # ---------------------------------------------------------- reproduction [b] and [c]
        if pk == "u56":
            Wb = H.targets(px, "EWall", "band3", "rw")
            rb = H.run(px, Wb, bps=10.0)["r"].loc[start:]
            mb, hb = metrics(rb), H.halves(rb)
            hit = (abs(mb["CAGR"] - 0.122) < 0.001 and abs(mb["Sharpe"] - 1.161) < 0.003
                   and abs(mb["MaxDD"] + 0.177) < 0.002 and abs(hb[0] - 1.210) < 0.003
                   and abs(hb[1] - 1.129) < 0.003)
            ok["b"] = hit
            say(f"[b] idea 94 `EWall+band3-rw` u56@10: published 12.2%/1.161/-17.7% "
                f"({1.210:.3f}/{1.129:.3f}); this run {mb['CAGR']:.1%}/{mb['Sharpe']:.3f}/"
                f"{mb['MaxDD']:.1%} ({hb[0]:.3f}/{hb[1]:.3f}) -> "
                f"{'MATCH' if hit else 'MISMATCH'}")
            for instr in ("OFF", "STOP15"):
                r0, to = RET[(pk, 0.53, instr)]
                W = base_targets(px, nmap[0.53])
                fresh = (H.run(px, W, bps=10.0) if instr == "OFF"
                         else H.run(px, W, stop=0.15, bps=10.0))["r"].loc[start:]
                err = float((net(r0, to, 10.0) - fresh).abs().max())
                ok[f"c:{instr}"] = err < 1e-12
                say(f"[c] cost-derivation identity ({instr}, u56 m=0.53): max|derived - fresh "
                    f"10bps| = {err:.2e} -> {'MATCH' if ok[f'c:{instr}'] else 'MISMATCH'}")

    G = pd.DataFrame(grid_rows)
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say("\n" + "=" * 190)
    say("REPRODUCTION GATE: " + ("ALL PASS" if all(ok.values()) else "FAILURES -> "
                                 + ", ".join(k for k, v in ok.items() if not v)))
    say(f"  {sum(ok.values())} of {len(ok)} checks match.  Grid: {len(G)} books "
        f"({len(PANELS)} panels x {len(SHARES)} shares x {len(INSTR) + 1} arms), every cost rung "
        f"derived from the same 0 bps path.")
    say("=" * 190)

    # ================================================================ the curves g(m), c(m)
    say("\n### THE CURVES: value g(m) and cost c(m) of each instrument, by share")
    say("    g     = |CAGR(ON@0bps) - CAGR(OFF@0bps)|, pp/yr")
    say("    c_INC = exact incremental 10 bps cost of the instrument over its control (may be <=0)")
    say("    c_TO  = 10 bps x |annualised turnover(ON) - annualised turnover(OFF)|  (always >=0)")
    for pk in PANELS:
        for m in SHARES:
            r0n, ton = RET[(pk, m, "OFF")]
            for instr in INSTR:
                r0t, tot = RET[(pk, m, instr)]
                yrs = len(r0t) / 252
                sg = cagr(r0t) - cagr(r0n)
                c10t, c10n = net(r0t, tot, 10.0), net(r0n, ton, 10.0)
                c_inc = (cagr(r0t) - cagr(c10t)) - (cagr(r0n) - cagr(c10n))
                c_to = abs(float(tot.sum() - ton.sum())) / yrs * 10.0 / 1e4
                dd_t, dd_n = metrics(c10t)["MaxDD"], metrics(c10n)["MaxDD"]
                curve_rows.append(dict(
                    panel=pk, instr=instr, m=m, n=ref[pk]["nmap"][m],
                    g=abs(sg), signed_dCAGR=sg, c_INC=c_inc, c_TO=c_to,
                    dSharpe=metrics(c10t)["Sharpe"] - metrics(c10n)["Sharpe"],
                    dMaxDD_pp=abs(dd_n) - abs(dd_t),
                    rate=((cagr(c10n) - cagr(c10t)) / (abs(dd_n) - abs(dd_t))
                          if abs(abs(dd_n) - abs(dd_t)) > 1e-9 else np.nan),
                    ratio_INC=(abs(sg) / c_inc if c_inc > 0 else np.nan),
                    ratio_TO=(abs(sg) / c_to if c_to > 0 else np.nan)))
    CV = pd.DataFrame(curve_rows)
    CV.to_csv(OUT / f"{STEM}.curve.csv", index=False)
    for pk in PANELS:
        sub = CV[CV.panel == pk]
        say(f"\n[{pk}] g, c_INC, c_TO by share (x100 = pp/yr)"
            + ("   [NOTE: the 200d/vol gate is INVERTED on this panel, ideas 39/49]"
               if pk == "small" else ""))
        say(sub.pivot_table(index="m", columns="instr", values=["g", "c_INC", "c_TO"])
            .to_string(float_format=lambda x: f"{x * 100:+.3f}"))
        say(f"[{pk}] ratio g/c_TO by share  (flat => value and cost are the same function of m)")
        say(sub.pivot_table(index="m", columns="instr", values="ratio_TO")
            .to_string(float_format=lambda x: f"{x:.2f}"))
        for instr in INSTR:
            s = sub[sub.instr == instr].sort_values("m")
            say(f"    Spearman(m, g) {instr:<8} {I159.spearman(s.m, s.g):+.3f}   "
                f"Spearman(m, c_TO) {I159.spearman(s.m, s.c_TO):+.3f}   "
                f"Spearman(m, ratio) {I159.spearman(s.m, s.ratio_TO):+.3f}")

    # ================================================================ d and its bootstrap
    say("\n" + "=" * 190)
    say(f"THE d-STATISTIC — d = slope(log g) - slope(log c) on m.  d < 0 is REQUIRED for a "
        f"crossing.  Bootstrap: circular block {BLOCK}d, {NBOOT} reps, seed {SEED}, g resampled, "
        f"c at its point estimate (idea 159's scheme).")
    say("=" * 190)
    for pk in PANELS:
        for instr in INSTR:
            s = CV[(CV.panel == pk) & (CV.instr == instr)].sort_values("m")
            paths = [(RET[(pk, m, instr)][0].values, RET[(pk, m, "OFF")][0].values)
                     for m in SHARES]
            nobs = len(paths[0][0])
            yrs = nobs / 252
            for bar in ("TO", "INC"):
                cc = s[f"c_{bar}"].values
                bg, bc, dpt = logslopes(SHARES, s.g.values, cc)
                rng = np.random.default_rng(SEED + 1000 * INSTR.index(instr)
                                            + 10 * PANELS.index(pk) + (0 if bar == "TO" else 5))
                ds = []
                if np.isfinite(dpt):
                    for _ in range(NBOOT):
                        idx = I159.block_idx(nobs, rng)
                        gb = [abs(((1 + a[idx]).prod() ** (1 / yrs) - 1)
                                  - ((1 + b[idx]).prod() ** (1 / yrs) - 1)) for a, b in paths]
                        _, _, dv = logslopes(SHARES, gb, cc)
                        if np.isfinite(dv):
                            ds.append(dv)
                ds = np.array(ds)
                lo = float(np.percentile(ds, 5)) if len(ds) else np.nan
                hi = float(np.percentile(ds, 95)) if len(ds) else np.nan
                d_rows.append(dict(panel=pk, instr=instr, bar=bar, slope_log_g=bg,
                                   slope_log_c=bc, d_point=dpt,
                                   d_boot_median=(float(np.median(ds)) if len(ds) else np.nan),
                                   lo5=lo, hi95=hi,
                                   frac_d_lt_0=(float((ds < 0).mean()) if len(ds) else np.nan),
                                   n_pos_c=int((np.isfinite(cc) & (cc > 0)).sum()),
                                   straddles_zero=bool(np.isfinite(lo) and lo <= 0 <= hi),
                                   crossing_possible=bool(np.isfinite(hi) and hi < 0)))
        say(f"  {pk} done ({time.time() - t0:.0f}s)")
    D = pd.DataFrame(d_rows)
    D.to_csv(OUT / f"{STEM}.dslope.csv", index=False)
    say("")
    say(D.to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
    fin = D[(D.bar == "TO") & D.d_point.notna()]
    say(f"\n  BAR-TO: d straddles zero in {int(fin.straddles_zero.sum())} of {len(fin)} "
        f"(panel, instrument) cells;  a crossing is distinguishable (hi95 < 0) in "
        f"{int(fin.crossing_possible.sum())} of {len(fin)}.")
    fin2 = D[(D.bar == "INC") & D.d_point.notna()]
    say(f"  BAR-INC: computable in {len(fin2)} of {len(PANELS) * len(INSTR)} cells (log c needs "
        f"c > 0 at >= 3 shares); straddles zero in {int(fin2.straddles_zero.sum())} of "
        f"{len(fin2)}.")
    say("  idea 159's vol-tilt reference: d straddles zero 6 of 6 (u56 INV +0.032 "
        "[-1.186,+1.097], broad INV +0.173 [-0.781,+1.274], broad POS -0.590 [-2.116,+0.688]).")

    # ================================================================ rule 8 walk-forward
    say("\n" + "=" * 190)
    say("RULE 8 WALK-FORWARD — d and the implied crossing m* estimated on the IS window only "
        f"(<= {IS_END}); OOS ({OOS_START} ->) read once.")
    say("=" * 190)
    for pk in PANELS:
        v1o = metrics(ref[pk]["v1"][10.0].loc[OOS_START:])
        spo = metrics(ref[pk]["spy"].loc[OOS_START:])
        for instr in INSTR:
            gIS, cIS = [], []
            for m in SHARES:
                r0t, tot = RET[(pk, m, instr)]
                r0n, ton = RET[(pk, m, "OFF")]
                a, b = r0t.loc[:IS_END], r0n.loc[:IS_END]
                gIS.append(abs(cagr(a) - cagr(b)))
                cIS.append(abs(float(tot.loc[:IS_END].sum() - ton.loc[:IS_END].sum()))
                           / (len(a) / 252) * 10.0 / 1e4)
            _, _, d_is = logslopes(SHARES, gIS, cIS)
            m_star = I159.cross_empirical(np.array(SHARES), np.array(gIS), np.array(cIS))
            for arm in ("NEVER", "ALWAYS", "GATED"):
                rr = []
                for m in SHARES:
                    use = (arm == "ALWAYS") or (arm == "GATED" and np.isfinite(m_star)
                                                and m <= m_star)
                    r0, to = RET[(pk, m, instr if use else "OFF")]
                    rr.append(net(r0, to, 10.0).loc[OOS_START:])
                mo = [metrics(x) for x in rr]
                wf_rows.append(dict(
                    panel=pk, instr=instr, arm=arm, d_IS=d_is, m_star_IS=m_star,
                    shares_using=(len(SHARES) if arm == "ALWAYS" else
                                  (0 if arm == "NEVER" else
                                   int(sum(1 for m in SHARES if np.isfinite(m_star)
                                           and m <= m_star)))),
                    OOS_CAGR=float(np.mean([x["CAGR"] for x in mo])),
                    OOS_Sharpe=float(np.mean([x["Sharpe"] for x in mo])),
                    OOS_MaxDD=float(np.mean([x["MaxDD"] for x in mo])),
                    base_OOS_Sharpe=v1o["Sharpe"], base_OOS_CAGR=v1o["CAGR"],
                    base_OOS_MaxDD=v1o["MaxDD"], spy_OOS_Sharpe=spo["Sharpe"],
                    spy_OOS_CAGR=spo["CAGR"], spy_OOS_MaxDD=spo["MaxDD"]))
    WF = pd.DataFrame(wf_rows)
    WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    say(WF[["panel", "instr", "arm", "d_IS", "m_star_IS", "shares_using", "OOS_CAGR",
            "OOS_Sharpe", "OOS_MaxDD", "base_OOS_Sharpe", "spy_OOS_Sharpe"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    piv = WF.pivot_table(index=["panel", "instr"], columns="arm", values="OOS_Sharpe")
    say("\n  paired OOS Sharpe vs the do-nothing NEVER control (mean over the 10 shares):")
    for arm in ("ALWAYS", "GATED"):
        dd = piv[arm] - piv["NEVER"]
        say(f"    {arm:<7} mean {dd.mean():+.4f}  median {dd.median():+.4f}  "
            f"wins {int((dd > 0).sum())}/{len(dd)}")
    say(f"  IS-estimated d sign stability: d_IS < 0 in "
        f"{int((WF.drop_duplicates(['panel', 'instr']).d_IS < 0).sum())} of "
        f"{WF.drop_duplicates(['panel', 'instr']).shape[0]} cells; full-sample d < 0 in "
        f"{int((fin.d_point < 0).sum())} of {len(fin)}.")

    # ================================================================ the ratio's LEVEL
    say("\n" + "=" * 190)
    say("THE RATIO'S LEVEL — g/c at every grid point.  A crossing needs the ratio to reach 1 "
        "SOMEWHERE, whatever the slopes do.")
    say("=" * 190)
    for bar in ("TO", "INC"):
        r = CV[f"ratio_{bar}"].dropna()
        say(f"  BAR-{bar}: {len(r)} of {len(CV)} points have c > 0;  min g/c {r.min():.2f}, "
            f"median {r.median():.2f}, max {r.max():.1f};  points with g/c < 1: "
            f"{int((r < 1).sum())}")
    say(pd.concat([CV.groupby(['panel', 'instr']).ratio_TO.min().rename('min_g/c_TO'),
                   CV.groupby(['panel', 'instr']).ratio_INC.min().rename('min_g/c_INC')],
                  axis=1).to_string(float_format=lambda x: f"{x:.2f}"))
    say("  (idea 159's vol tilt on the honest bar: g/c = 16 to 4254 on u56, 9 to 193 on broad.)")

    # ============================================ KEEP-candidate walk-forward over (instr, m)
    say("\n" + "=" * 190)
    say("KEEP-CANDIDATE WALK-FORWARD — the (instrument, share) PICK made on the IS window only "
        f"(<= {IS_END}), read once on OOS.  Two pre-registered selectors, plus the do-nothing "
        "control.")
    say("=" * 190)
    kc_rows = []
    for pk in PANELS:
        bIS, bOOS = ref[pk]["bIS"], ref[pk]["bOOS"]
        v1o = metrics(ref[pk]["v1"][10.0].loc[OOS_START:])
        spo = metrics(ref[pk]["spy"].loc[OOS_START:])
        cand = []
        for m in SHARES:
            for instr in ["OFF"] + INSTR:
                r0, to = RET[(pk, m, instr)]
                rc = net(r0, to, 10.0)
                mi = C.margins_at(rc, bIS, PHI0, DELTA0, "IS")
                cand.append(dict(instr=instr, m=m, rc=rc,
                                 IS_Sharpe=metrics(rc.loc[:IS_END])["Sharpe"],
                                 IS_min_margin=min(mi[k] for k in
                                                   ("H1", "H2", "OOS", "DD", "CAGR")),
                                 IS_pass=len(C.fails(mi)) == 0))
        Cd = pd.DataFrame(cand)
        picks = {
            "IS_SHARPE": Cd.sort_values(["IS_Sharpe", "m"], ascending=[False, True]).iloc[0],
            "IS_4bMARGIN": Cd.sort_values(["IS_min_margin", "m"],
                                          ascending=[False, True]).iloc[0],
            "CONTROL_OFF_m053": Cd[(Cd.instr == "OFF") & (Cd.m == 0.53)].iloc[0],
        }
        for nm, row in picks.items():
            rc = row.rc
            mo = metrics(rc.loc[OOS_START:])
            mgo = C.margins_at(rc, bOOS, PHI0, DELTA0, "OOS")
            kc_rows.append(dict(panel=pk, selector=nm, instr=row.instr, m=row.m,
                                IS_Sharpe=row.IS_Sharpe, IS_4b_pass=row.IS_pass,
                                OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                OOS_MaxDD=mo["MaxDD"],
                                OOS_4b_pass=len(C.fails(mgo)) == 0,
                                OOS_4b_fails="|".join(C.fails(mgo)) or "-",
                                base_OOS_Sharpe=v1o["Sharpe"], spy_OOS_Sharpe=spo["Sharpe"],
                                spy_OOS_CAGR=spo["CAGR"], spy_OOS_MaxDD=spo["MaxDD"]))
    KC = pd.DataFrame(kc_rows)
    KC.to_csv(OUT / f"{STEM}.keepcandidate.csv", index=False)
    say(KC.to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # ================================================================ both KEEP paths
    say("\n" + "=" * 190)
    say("BOTH KEEP PATHS, every grid point (arm x share x panel x cost)")
    say("=" * 190)
    for c in COSTS:
        say(f"  @{int(c)} bps: 4a passes {int(G[f'pass4a_{int(c)}'].sum())} of {len(G)};  "
            f"4b (full sample) {int(G[f'pass4b_{int(c)}'].sum())};  4b (OOS window) "
            f"{int(G[f'pass4bOOS_{int(c)}'].sum())}")
    p = G[G.pass4b_10]
    if len(p):
        say("\n  4b passers @10 bps (full sample):")
        say(p[["panel", "instr", "m", "n", "CAGR_10", "Sharpe_10", "MaxDD_10", "H1_10", "H2_10",
               "OOSSharpe_10", "to_yr", "pass4a_10", "pass4b_25"]]
            .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    say(f"\n  4b passers that are NOT the base book (i.e. an instrument earns the pass): "
        f"{int((p.instr != 'OFF').sum())} of {len(p)}")

    say("\n" + "=" * 190)
    say("CENSUS")
    say("=" * 190)
    say(f"  grid rows {len(G)};  curve rows {len(CV)};  d rows {len(D)};  wf rows {len(WF)}")
    say(f"  cost 10/25 bps derived from one 0 bps path per book, weekly, t+1, no shorting, "
        f"no leverage;  runtime {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")
    print(f"\nwrote {STEM}.{{console.txt,grid.csv,curve.csv,dslope.csv,walkforward.csv}}")


if __name__ == "__main__":
    main()
