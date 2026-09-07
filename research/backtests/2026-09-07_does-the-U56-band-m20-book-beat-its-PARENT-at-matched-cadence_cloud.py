#!/usr/bin/env python3
"""Idea 386: does the U56 band-m20 book beat its PARENT at MATCHED CADENCE?

THE OWED TEST.  Idea 384's by-product -- U56, top-20 by the v1 composite (vol scaler OFF),
NORM weights g/k_t at g=0.75, WEEKLY, no-trade band m=20 -- passes 4b at 0/10/25 bps and is the
rule-8 chooser's own pick, and a memo was written for it
(`2026-09-07_u56-top20-band-m20_4b_B_MEMO.md`).  That memo's clause 7 names the one test that
stands between it and a KEEP: idea 280 found the U56 buffer arm LOSES to the plain (m=0) parent
at MATCHED TURNOVER on a slower cadence (+0.093 Sharpe to the parent).  Idea 384 could not run
it because cadence was not one of its two dials; idea 331 ran a COARSE cadence ladder
(D/W/2W/M/6W/Q) in which no m=0 cell lands near the candidate's 5.26x/yr turnover -- the two
nearest m=0 rungs are 2W at 7.38x and M at 4.82x, a 2.6x-wide bracket.  This run closes it.

PRE-REGISTERED, before any new number was read:

  [A] FINE CADENCE LADDER on the parent.  cadence in {W, 2W, 3W, 4W, 5W, 6W, 8W, M, Q} x
      m in {0, 20}.  Exactly two tuned parameters (cadence, m).  Panel {U56, B136, SMALL439}
      and cost rung {0, 10, 25} are REPORTED axes, not tuned choices; every point of every
      axis is printed and written to `<slug>.grid.csv`.  The kW rungs decimate the WEEKLY
      mask (every k-th week-end), so they nest inside W's calendar exactly, and 3W/4W/5W/8W
      are the new rungs that bracket 5.26x/yr tightly.

  [B] THE MATCHED-TURNOVER HEAD-TO-HEAD.  Let T* = the candidate's annual turnover.  Three
      readings, in increasing strictness:
      B1  NEAREST twin: the m=0 cell whose turnover is closest to T*;
      B2  BRACKET twin: the two m=0 cells straddling T*, plus the Sharpe LINEARLY INTERPOLATED
          in turnover between them -- the fairest single comparand, because it removes the
          "no rung lands exactly on T*" excuse in both directions;
      B3  DOMINANCE: does ANY m=0 cell at turnover <= T* (i.e. no more trading than the
          candidate) beat the candidate on Sharpe at 10 bps?  If one does, the band is buying
          nothing that a slower calendar does not buy more cheaply.

  [C] DECISION RULE, fixed in advance:
      KEEP  <=> the candidate beats BOTH the nearest twin (B1) and the interpolated twin (B2)
                on Sharpe at 10 bps, AND no m=0 cell at turnover <= T* beats it (B3), AND it
                still clears all five 4b bars at 0/10/25 bps.
      Anything short of that is PARK (the memo stays a comparison, not a promotion), and the
      queue's clause-7 obligation is discharged AGAINST the band.
      Note the asymmetry is deliberate: the candidate is the incumbent claim, so ties go to
      the parent.  A tie means the band is the cadence dial wearing another name.

  [D] RULE 8 WALK-FORWARD (PROTOCOL 8, required).  (cadence, m) chosen on 2008-2016 IS Sharpe
      at 10 bps ALONE, 2017-2026 read once, reported against: the W m=20 candidate's own OOS,
      the OOS-best cell (regret), the (W, m=0) anchor, RULES v2 (live) and SPY.  Run twice --
      with the band on the chooser's menu and with it REMOVED -- because idea 331 found
      removing it was worth +0.183 OOS Sharpe on U56, and that comparison is the walk-forward
      form of this run's question.

  [E] BREAKEVEN c*: largest whole bps at which all five 4b bars still hold, every cell.

BOOK (fixed, idea 329/331/384's convention, never tuned): top-20 eligible names by the RULES v1
composite with the vol scaler OFF, RULES v1 eligibility (above the 200d MA and vol20 < 0.60),
NORM weights w_i = g/k_t at g = 0.75 so neither dial can smuggle in a gross change, next-day
execution.  Band (idea 273): a name enters at rank <= n and is held until its rank passes n+m
or it leaves the eligible set; free slots refill from the best-ranked eligible name not held;
the slot count is the parent's own k_t so m is a pure TURNOVER dial.  m = 0 nests the hard cut
EXACTLY (asserted in [0]).

REPRODUCTION GATES (section [0], asserted or printed before any new number is read):
  * fast_backtest == engine.backtest to 1e-12 on returns and turnover, and the derived rung
    r(c) = r(0) - turnover*c/1e4 == engine.backtest(cost_bps=c) to 1e-12;
  * sel_band(n=20, m=0) == sel_hard(n=20) on every rebalance day of every cadence;
  * idea 331's published U56 grid, re-measured on the shared rungs:
      W  m=0  @10: 12.79% / 1.064 / -18.31%, H1/H2 1.068/1.066, OOS 1.131, turn 11.00, c* 21
      W  m=20 @10: 12.87% / 1.112 / -17.22%, H1/H2 1.144/1.093, OOS 1.187, turn  5.26, c* 47
      2W m=0  @10: 13.31% / 1.075 / -21.55%, turn 7.38
      M  m=0  @10: 15.30% / 1.213 / -19.51%, H1/H2 1.200/1.232, OOS 1.307, turn 4.82, c* 68
      6W m=20 @10: 14.31% / 1.159 / -19.42%, OOS 1.250, c* 104

CAVEATS: (1) all three panels are CURRENT-CONSTITUENT lists -- SURVIVORSHIP -- which flatters
every momentum book; CAGR LEVELS are optimistic, the m- and cadence-DIFFERENCES this run is
about much less so.  The small panel is the worst offender (sub-$2B names that survived to
2026-09); its 44 tickers with `max_1d_move >= 1.0` in data/small_meta.csv are dropped first.
(2) SMALL439 starts 2010-01-04, so its halves are not the same calendar halves as U56/B136.
(3) The kW cadences are phase-anchored to each panel's first complete week; a different weekday
phase is a different (unreported) choice -- noted, not tested, and still owed by the Sep-6 review.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os, sys
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                      # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_does-the-U56-band-m20-book-beat-its-PARENT-at-matched-cadence_cloud"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS, N = 0.60, 0.75, 20
BASE_FREQ = "W"
CADENCES = ["W", "2W", "3W", "4W", "5W", "6W", "8W", "M", "Q"]
MS = [0, 20]
COSTS = [0, 10, 25]
CAND_CAD, CAND_M = "W", 20          # the candidate under test
ANCHOR_CAD, ANCHOR_M = "W", 0       # its plain parent at its own cadence
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260


def reb_mask(idx, cadence):
    """True on the last trading day of each rebalance period.  W/M/Q are engine.rebalance_mask
    verbatim (so the shared rungs reproduce idea 331 exactly); kW decimates the WEEKLY mask."""
    if cadence in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, cadence)
    k = int(cadence[:-1])
    w = rebalance_mask(idx, "W")
    pos = np.where(w.values)[0][k - 1::k]
    s = pd.Series(False, index=idx)
    s.iloc[pos] = True
    return s


def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


def rank_frame(px, drop_spy=False):
    """Composite rank among eligible names (v1 composite, vol scaler OFF; v1 eligibility).
    On U56/B136 SPY is a genuine constituent and stays eligible (idea 44's convention, needed
    for the reproduction gates); on SMALL439 it is a benchmark only and is removed."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def sel_hard(rk, n):
    return rk <= n


def sel_band(px, rk, n, m, cadence):
    """No-trade band (idea 273), evaluated on rebalance days and forward-filled.  Slot count is
    the parent's own k_t = |{rank <= n}|, so m is a pure turnover dial; m = 0 nests sel_hard."""
    reb = reb_mask(px.index, cadence).values
    cols = list(px.columns)
    out = np.zeros((len(px.index), len(cols)))
    rkv = rk.values
    held = []
    last = np.zeros(len(cols))
    for i in range(len(px.index)):
        if reb[i]:
            r = rkv[i]
            cap = int(np.nansum(r <= n))
            held = [j for j in held if r[j] == r[j] and r[j] <= n + m]
            held.sort(key=lambda j: r[j])
            if len(held) > cap:
                held = held[:cap]
            if len(held) < cap:
                order = np.argsort(np.where(np.isnan(r), np.inf, r), kind="stable")
                hs_ = set(held)
                for j in order:
                    if len(held) >= cap:
                        break
                    if r[j] != r[j]:
                        break
                    if j not in hs_:
                        held.append(j); hs_.add(j)
                held.sort(key=lambda j: r[j])
            last = np.zeros(len(cols))
            last[held] = 1.0
        out[i] = last
    return pd.DataFrame(out > 0.5, index=px.index, columns=cols)


def weights_from(sel):
    s = sel.astype(float)
    k = s.sum(axis=1).replace(0, np.nan)
    return GROSS * s.div(k, axis=0).fillna(0.0)


def fast_backtest(px, w, cost_bps=0.0, cadence="W"):
    """Vectorised-loop clone of engine.backtest; asserted against it in [0]."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).values
    mask = reb_mask(px.index, cadence).shift(1, fill_value=False).values
    nT, nC = rets.shape
    held = np.empty((nT, nC)); turn = np.zeros(nT)
    cur = np.zeros(nC)
    for i in range(nT):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = np.nansum(held * rets, axis=1) - turn * cost_bps / 1e4
    idx = px.index
    return (pd.Series(port, index=idx), pd.Series(turn, index=idx),
            pd.Series(np.nansum(held, axis=1), index=idx), pd.Series((held > 0).sum(axis=1), index=idx))


def hs(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


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
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def breakeven(r0, t0, spy, hi=200):
    cstar, bar = None, ""
    for c in range(0, hi + 1):
        ok, _, f = bars_4b(r0 - t0 * c / 1e4, spy)
        if ok:
            cstar = c
        else:
            bar = ",".join(f)
            break
    return cstar, bar


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print(f"Book: top-{N} eligible by the v1 composite (vol scaler OFF), NORM weights g/k_t at "
          f"g={GROSS}, next-day execution.  Band m: sell only past rank n+m.")
    print(f"Tuned (2): cadence in {CADENCES} x m in {MS}.  Reported: panel, cost {COSTS} bps.")
    print(f"Candidate under test: U56 {CAND_CAD} m={CAND_M}.  Comparand: the m=0 parent at matched turnover.")

    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    gcsv, ccsv = OUT / f"{SLUG}.grid.csv", OUT / f"{SLUG}.ctx.csv"
    if RESUME and gcsv.exists() and ccsv.exists():
        analyse(pd.read_csv(gcsv), pd.read_csv(ccsv).set_index("panel"))
        return

    rows, ctx_rows = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms_ = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        rk, elig = rank_frame(px, drop_spy=(pname == "SMALL439"))
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(f"    SPY CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} MaxDD {ms_['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%}")
        print(f"    4b bars on this panel: H1>{s1:.3f}  H2>{s2:.3f}  OOS>{so['Sharpe']:.3f}  "
              f"MaxDD<={0.60*abs(ms_['MaxDD']):.2%}  CAGR>={0.70*ms_['CAGR']:.2%}")

        br, bt, _, _ = fast_backtest(px, rules_v2_weights(px), 0.0, BASE_FREQ)
        base10 = (br - bt * 10 / 1e4).loc[start:]
        bm = metrics(base10); b1, b2 = hs(base10); bo = metrics(base10.loc[OOS_START:])
        print(f"    RULES v2 (live, weekly, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS {bo['Sharpe']:.3f}")

        if pname == "U56":
            print("\n[0] GATES")
            wA = weights_from(sel_hard(rk, N))
            eng = backtest(px, wA, cost_bps=0.0, freq="W")
            f_r, f_t, _, _ = fast_backtest(px, wA, 0.0, "W")
            d1 = np.abs(eng["returns"].loc[start:] - f_r.loc[start:]).max()
            d2 = np.abs(eng["turnover"].loc[start:] - f_t.loc[start:]).max()
            print(f"    fast_backtest vs engine.backtest: max|dr| {d1:.3e}  max|dturn| {d2:.3e}")
            assert d1 < 1e-12 and d2 < 1e-12
            eng25 = backtest(px, wA, cost_bps=25.0, freq="W")
            d3 = np.abs(eng25["returns"].loc[start:] - (f_r - f_t * 25 / 1e4).loc[start:]).max()
            print(f"    derived rung r(25) vs backtest(cost_bps=25): max|d| {d3:.3e}")
            assert d3 < 1e-12
            tot = 0
            for fq in CADENCES:
                sb = sel_band(px, rk, N, 0, fq); sh = sel_hard(rk, N)
                reb = reb_mask(px.index, fq)
                dd = int((sb[reb] != sh[reb]).values.sum())
                tot += dd
            print(f"    sel_band(m=0) nests sel_hard on all {len(CADENCES)} cadences: {tot} disagreements")
            assert tot == 0

        print(f"\n[A] GRID {pname} (every point; ann.turnover = mean yearly sum|dw|)")
        hdr = (f"    {'cad':>4} {'m':>3} {'reb/yr':>7} {'turn/yr':>8} {'names':>6} {'gross':>6} | "
               + " | ".join(f"c={c:<2} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1/H2':>13} {'OOS':>6} 4b 4a"
                            for c in COSTS))
        print(hdr)
        for fq in CADENCES:
            nreb = int(reb_mask(px.index, fq).loc[start:].sum()) / (len(px.loc[start:]) / 252)
            for m in MS:
                sel = sel_hard(rk, N) if m == 0 else sel_band(px, rk, N, m, fq)
                r0, t0, gr, kk = fast_backtest(px, weights_from(sel), 0.0, fq)
                r0, t0 = r0.loc[start:], t0.loc[start:]
                tpy = t0.sum() / (len(r0) / 252)
                line = (f"    {fq:>4} {m:>3} {nreb:>7.1f} {tpy:>8.2f} {kk.loc[start:].mean():>6.1f} "
                        f"{gr.loc[start:].mean():>6.3f} |")
                rec = dict(panel=pname, cadence=fq, m=m, reb_per_yr=nreb, turn_per_yr=tpy,
                           names=kk.loc[start:].mean(), gross=gr.loc[start:].mean())
                for c in COSTS:
                    r = r0 - t0 * c / 1e4
                    mt = metrics(r); h1, h2 = hs(r); oo = metrics(r.loc[OOS_START:])
                    ok4b, d4b, f4b = bars_4b(r, spy)
                    basec = base10 if c == 10 else (br - bt * c / 1e4).loc[start:]
                    ok4a, d4a, f4a = bars_4a(r, basec)
                    line += (f" {mt['CAGR']:>7.2%} {mt['Sharpe']:>6.3f} {mt['MaxDD']:>7.2%} "
                             f"{h1:>6.3f}/{h2:<6.3f} {oo['Sharpe']:>6.3f} "
                             f"{'Y' if ok4b else 'n'}  {'Y' if ok4a else 'n'} |")
                    rec.update({f"CAGR_{c}": mt["CAGR"], f"Sharpe_{c}": mt["Sharpe"],
                                f"MaxDD_{c}": mt["MaxDD"], f"H1_{c}": h1, f"H2_{c}": h2,
                                f"OOS_Sharpe_{c}": oo["Sharpe"], f"OOS_CAGR_{c}": oo["CAGR"],
                                f"OOS_MaxDD_{c}": oo["MaxDD"],
                                f"IS_Sharpe_{c}": metrics(r.loc[:IS_END])["Sharpe"],
                                f"keep4b_{c}": ok4b, f"fail4b_{c}": ",".join(f4b),
                                f"keep4a_{c}": ok4a, f"fail4a_{c}": ",".join(f4a),
                                f"m4b_H1_{c}": d4b["H1"], f"m4b_H2_{c}": d4b["H2"],
                                f"m4b_OOS_{c}": d4b["OOS"], f"m4b_DD_{c}": d4b["DD"],
                                f"m4b_CAGR_{c}": d4b["CAGR"]})
                cst, cbar = breakeven(r0, t0, spy)
                rec["breakeven_bps"] = cst if cst is not None else -1
                rec["breakeven_first_fail"] = cbar
                print(line + f" c*={rec['breakeven_bps']:>3}")
                rows.append(rec)

        ctx_rows.append(dict(panel=pname, spy_sharpe=ms_["Sharpe"], spy_cagr=ms_["CAGR"],
                             spy_dd=ms_["MaxDD"], spy_h1=s1, spy_h2=s2,
                             spy_oos_sharpe=so["Sharpe"], spy_oos_cagr=so["CAGR"],
                             base_sharpe=bm["Sharpe"], base_cagr=bm["CAGR"], base_dd=bm["MaxDD"],
                             base_h1=b1, base_h2=b2, base_oos_sharpe=bo["Sharpe"]))

    df = pd.DataFrame(rows); df.to_csv(gcsv, index=False)
    ctx = pd.DataFrame(ctx_rows).set_index("panel"); ctx.to_csv(ccsv)
    analyse(df, ctx)


def analyse(df, ctx):
    # ------------------------------------------------------------------ [0b] published gates
    print("\n\n[0b] REPRODUCTION GATES vs idea 331's published U56 grid (shared rungs only)")
    PUB = {("W", 0):  (0.1279, 1.064, -0.1831, 1.068, 1.066, 1.131, 11.00, 21),
           ("W", 20): (0.1287, 1.112, -0.1722, 1.144, 1.093, 1.187, 5.26, 47),
           ("2W", 0): (0.1331, 1.075, -0.2155, None, None, None, 7.38, -1),
           ("M", 0):  (0.1530, 1.213, -0.1951, 1.200, 1.232, 1.307, 4.82, 68),
           ("6W", 20): (0.1431, 1.159, -0.1942, None, None, 1.250, 2.29, 104)}
    u = df[df.panel == "U56"]
    worst = 0.0
    for (fq, m), p in PUB.items():
        r = u[(u.cadence == fq) & (u.m == m)]
        if r.empty:
            print(f"    {fq:>2} m={m:<2}  [rung not in this run's ladder]"); continue
        r = r.iloc[0]
        d = max(abs(r.CAGR_10 - p[0]), abs(r.Sharpe_10 - p[1]), abs(r.MaxDD_10 - p[2]),
                abs(r.turn_per_yr - p[6]) / 100)
        worst = max(worst, d)
        print(f"    {fq:>2} m={m:<2} @10bps: {r.CAGR_10:.2%} / {r.Sharpe_10:.3f} / {r.MaxDD_10:.2%} "
              f"turn {r.turn_per_yr:.2f} c* {int(r.breakeven_bps)}   "
              f"[published {p[0]:.2%} / {p[1]:.3f} / {p[2]:.2%} turn {p[6]:.2f} c* {p[7]}]  "
              f"max|d| {d:.4f}")
    print(f"    GATE: worst rounded discrepancy across shared rungs = {worst:.4f} "
          f"(published values are 3-4 s.f., so <= 0.001 is EXACT)")

    # ------------------------------------------------------------------ [B] the head-to-head
    print("\n\n[B] MATCHED-TURNOVER HEAD-TO-HEAD (10 bps; the pre-registered test)")
    mrows = []
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        cand = d[(d.cadence == CAND_CAD) & (d.m == CAND_M)].iloc[0]
        T = cand.turn_per_yr
        par = d[d.m == 0].sort_values("turn_per_yr")
        print(f"\n  --- {pname}: candidate {CAND_CAD} m={CAND_M} -> turnover T* = {T:.3f}x/yr, "
              f"Sharpe {cand.Sharpe_10:.3f}, CAGR {cand.CAGR_10:.2%}, MaxDD {cand.MaxDD_10:.2%}, "
              f"H1/H2 {cand.H1_10:.3f}/{cand.H2_10:.3f}, OOS {cand.OOS_Sharpe_10:.3f}, "
              f"c* {int(cand.breakeven_bps)}")
        print(f"      m=0 parent ladder (turnover-sorted):")
        for _, r in par.iterrows():
            print(f"        {r.cadence:>2}  turn {r.turn_per_yr:>6.3f}  Sharpe {r.Sharpe_10:>6.3f}  "
                  f"CAGR {r.CAGR_10:>7.2%}  MaxDD {r.MaxDD_10:>7.2%}  "
                  f"H1/H2 {r.H1_10:.3f}/{r.H2_10:.3f}  OOS {r.OOS_Sharpe_10:>6.3f}  "
                  f"4b {'Y' if r.keep4b_10 else 'n':>1}  c* {int(r.breakeven_bps):>3}")

        # B1 nearest
        near = par.iloc[(par.turn_per_yr - T).abs().argsort().iloc[0]]
        b1d = cand.Sharpe_10 - near.Sharpe_10
        print(f"      B1 NEAREST m=0 twin: {near.cadence} at {near.turn_per_yr:.3f}x "
              f"(|dturn| {abs(near.turn_per_yr-T):.3f}) Sharpe {near.Sharpe_10:.3f}  "
              f"-> band {b1d:+.3f}  {'BAND WINS' if b1d > 0 else 'PARENT WINS'}")

        # B2 bracket + linear interpolation in turnover
        lo = par[par.turn_per_yr <= T].tail(1)
        hi = par[par.turn_per_yr >= T].head(1)
        if len(lo) and len(hi) and lo.iloc[0].cadence != hi.iloc[0].cadence:
            lo, hi = lo.iloc[0], hi.iloc[0]
            wgt = (T - lo.turn_per_yr) / (hi.turn_per_yr - lo.turn_per_yr)
            interp = lo.Sharpe_10 + wgt * (hi.Sharpe_10 - lo.Sharpe_10)
            icagr = lo.CAGR_10 + wgt * (hi.CAGR_10 - lo.CAGR_10)
            idd = lo.MaxDD_10 + wgt * (hi.MaxDD_10 - lo.MaxDD_10)
            ioos = lo.OOS_Sharpe_10 + wgt * (hi.OOS_Sharpe_10 - lo.OOS_Sharpe_10)
            b2d = cand.Sharpe_10 - interp
            print(f"      B2 BRACKET: {lo.cadence} {lo.turn_per_yr:.3f}x (S {lo.Sharpe_10:.3f}) .. "
                  f"{hi.cadence} {hi.turn_per_yr:.3f}x (S {hi.Sharpe_10:.3f}), w={wgt:.3f} "
                  f"-> INTERPOLATED parent at T*: Sharpe {interp:.3f}, CAGR {icagr:.2%}, "
                  f"MaxDD {idd:.2%}, OOS {ioos:.3f}")
            print(f"         band - interpolated parent: Sharpe {b2d:+.3f}, "
                  f"CAGR {cand.CAGR_10-icagr:+.2%}, OOS {cand.OOS_Sharpe_10-ioos:+.3f}  "
                  f"{'BAND WINS' if b2d > 0 else 'PARENT WINS'}")
        else:
            interp, b2d, ioos, icagr = np.nan, np.nan, np.nan, np.nan
            print(f"      B2 BRACKET: T* is outside the m=0 ladder's turnover range -- no interpolation")

        # B3 dominance: any m=0 cell trading no more than the candidate that beats it
        cheaper = par[par.turn_per_yr <= T]
        best = cheaper.loc[cheaper.Sharpe_10.idxmax()] if len(cheaper) else None
        if best is not None:
            b3d = cand.Sharpe_10 - best.Sharpe_10
            print(f"      B3 DOMINANCE: best m=0 cell at turnover <= T* is {best.cadence} "
                  f"({best.turn_per_yr:.3f}x, Sharpe {best.Sharpe_10:.3f}, CAGR {best.CAGR_10:.2%}, "
                  f"OOS {best.OOS_Sharpe_10:.3f}, 4b {'Y' if best.keep4b_10 else 'n'}) "
                  f"-> band {b3d:+.3f}  {'BAND WINS' if b3d > 0 else 'PARENT WINS'}")
        else:
            b3d = np.nan
            print(f"      B3 DOMINANCE: no m=0 cell trades at or below T*")

        keep4b_all = bool(df[(df.panel == pname) & (df.cadence == CAND_CAD) &
                             (df.m == CAND_M)][["keep4b_0", "keep4b_10", "keep4b_25"]].all(axis=1).iloc[0])
        verdict = "KEEP" if (b1d > 0 and (np.isnan(b2d) or b2d > 0) and
                             (np.isnan(b3d) or b3d > 0) and keep4b_all) else "PARK"
        print(f"      [C] DECISION on {pname}: B1 {b1d:+.3f}, B2 {b2d:+.3f}, B3 {b3d:+.3f}, "
              f"4b@0/10/25 {'Y' if keep4b_all else 'n'}  ==>  {verdict}")
        mrows.append(dict(panel=pname, T_star=T, cand_sharpe=cand.Sharpe_10,
                          cand_cagr=cand.CAGR_10, cand_dd=cand.MaxDD_10,
                          cand_oos=cand.OOS_Sharpe_10, cand_cstar=cand.breakeven_bps,
                          near_cad=near.cadence, near_turn=near.turn_per_yr,
                          near_sharpe=near.Sharpe_10, B1=b1d, interp_sharpe=interp, B2=b2d,
                          best_cheaper_cad=(best.cadence if best is not None else ""),
                          best_cheaper_sharpe=(best.Sharpe_10 if best is not None else np.nan),
                          best_cheaper_oos=(best.OOS_Sharpe_10 if best is not None else np.nan),
                          B3=b3d, cand_4b_all_rungs=keep4b_all, verdict=verdict))
    md = pd.DataFrame(mrows); md.to_csv(OUT / f"{SLUG}.matched.csv", index=False)

    # cost-rung robustness of the head-to-head on U56
    print("\n[B*] the U56 head-to-head at every cost rung (does the answer depend on the rung?)")
    u = df[df.panel == "U56"]
    cand = u[(u.cadence == CAND_CAD) & (u.m == CAND_M)].iloc[0]
    T = cand.turn_per_yr
    par = u[u.m == 0].sort_values("turn_per_yr")
    for c in COSTS:
        near = par.iloc[(par.turn_per_yr - T).abs().argsort().iloc[0]]
        lo = par[par.turn_per_yr <= T].tail(1).iloc[0]; hi = par[par.turn_per_yr >= T].head(1).iloc[0]
        w = (T - lo.turn_per_yr) / (hi.turn_per_yr - lo.turn_per_yr)
        it = lo[f"Sharpe_{c}"] + w * (hi[f"Sharpe_{c}"] - lo[f"Sharpe_{c}"])
        cheaper = par[par.turn_per_yr <= T]
        bst = cheaper.loc[cheaper[f"Sharpe_{c}"].idxmax()]
        print(f"    {c:>2} bps: cand {cand[f'Sharpe_{c}']:.3f} | nearest({near.cadence}) "
              f"{near[f'Sharpe_{c}']:.3f} B1 {cand[f'Sharpe_{c}']-near[f'Sharpe_{c}']:+.3f} | "
              f"interp {it:.3f} B2 {cand[f'Sharpe_{c}']-it:+.3f} | best<=T* ({bst.cadence}) "
              f"{bst[f'Sharpe_{c}']:.3f} B3 {cand[f'Sharpe_{c}']-bst[f'Sharpe_{c}']:+.3f}")

    # ------------------------------------------------------------------ [D] rule 8
    print("\n\n[D] RULE 8 WALK-FORWARD: (cadence, m) chosen on 2008-2016 IS Sharpe @10 bps alone,")
    print("    2017-2026 read ONCE.  Run with the band on the menu and with it REMOVED.")
    wf = []
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        c_ = ctx.loc[pname]
        for menu, sub in (("with band", d), ("band removed", d[d.m == 0])):
            pick = sub.loc[sub.IS_Sharpe_10.idxmax()]
            bestoos = sub.loc[sub.OOS_Sharpe_10.idxmax()]
            anchor = d[(d.cadence == ANCHOR_CAD) & (d.m == ANCHOR_M)].iloc[0]
            cand = d[(d.cadence == CAND_CAD) & (d.m == CAND_M)].iloc[0]
            print(f"    {pname:9s} [{menu:12s}] picks {pick.cadence:>2} m={int(pick.m):<2} "
                  f"(IS {pick.IS_Sharpe_10:.3f}) -> OOS Sharpe {pick.OOS_Sharpe_10:.3f} "
                  f"CAGR {pick.OOS_CAGR_10:.2%} MaxDD {pick.OOS_MaxDD_10:.2%} | "
                  f"regret vs OOS-best ({bestoos.cadence} m={int(bestoos.m)}, "
                  f"{bestoos.OOS_Sharpe_10:.3f}) {pick.OOS_Sharpe_10-bestoos.OOS_Sharpe_10:+.3f} | "
                  f"anchor(W,m=0) {anchor.OOS_Sharpe_10:.3f} | candidate(W,m=20) "
                  f"{cand.OOS_Sharpe_10:.3f} | SPY {c_.spy_oos_sharpe:.3f} | "
                  f"RULES v2 {c_.base_oos_sharpe:.3f}")
            wf.append(dict(panel=pname, menu=menu, pick_cad=pick.cadence, pick_m=int(pick.m),
                           IS_Sharpe=pick.IS_Sharpe_10, OOS_Sharpe=pick.OOS_Sharpe_10,
                           OOS_CAGR=pick.OOS_CAGR_10, OOS_MaxDD=pick.OOS_MaxDD_10,
                           oos_best_cad=bestoos.cadence, oos_best_m=int(bestoos.m),
                           oos_best_sharpe=bestoos.OOS_Sharpe_10,
                           regret=pick.OOS_Sharpe_10 - bestoos.OOS_Sharpe_10,
                           anchor_oos=anchor.OOS_Sharpe_10, cand_oos=cand.OOS_Sharpe_10,
                           spy_oos=c_.spy_oos_sharpe, base_oos=c_.base_oos_sharpe,
                           beats_spy=bool(pick.OOS_Sharpe_10 > c_.spy_oos_sharpe),
                           beats_live=bool(pick.OOS_Sharpe_10 > c_.base_oos_sharpe)))
        a = [r for r in wf if r["panel"] == pname]
        print(f"    {pname:9s} band-on-menu OOS cost: "
              f"{a[0]['OOS_Sharpe'] - a[1]['OOS_Sharpe']:+.3f} Sharpe "
              f"(chooser WITH band minus chooser WITHOUT)")
    pd.DataFrame(wf).to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)

    # ------------------------------------------------------------------ [E] KEEP-path census
    print("\n\n[E] KEEP-path census over the full grid")
    for c in COSTS:
        n4b = int(df[f"keep4b_{c}"].sum()); n4a = int(df[f"keep4a_{c}"].sum())
        byp = df[df[f"keep4b_{c}"]].groupby("panel").size().to_dict()
        bym = df[df[f"keep4b_{c}"]].groupby("m").size().to_dict()
        print(f"    {c:>2} bps: 4b {n4b}/{len(df)}  by panel {byp}  by m {bym}   |  4a {n4a}/{len(df)}")
    print("    breakeven c* (largest whole bps at which all five 4b bars hold; -1 = fails at 0):")
    piv = df.pivot_table(index=["panel", "cadence"], columns="m", values="breakeven_bps")
    print(piv.reindex(pd.MultiIndex.from_product([df.panel.unique(), CADENCES],
                                                 names=["panel", "cadence"])).to_string())

    print("\n\n=== VERDICT")
    for _, r in md.iterrows():
        print(f"    {r.panel:9s} {r.verdict}: B1 {r.B1:+.3f} vs {r.near_cad}, B2 {r.B2:+.3f}, "
              f"B3 {r.B3:+.3f} vs {r.best_cheaper_cad}")


if __name__ == "__main__":
    main()
