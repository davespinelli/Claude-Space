#!/usr/bin/env python3
"""Idea 331: is CADENCE the real dial behind idea 325's no-trade BAND?

Idea 329 found that on B136 the band's whole effect is dominated by cadence: moving weekly ->
monthly shifted the H2 margin by +0.189 where the widest band (m=40) shifted it by +0.015, and
its by-product `U56 top-20 NORM g/k @0.75 MONTHLY m=0` cleared all five 4b bars at 0, 10 and 25
bps with a 68.6-bps breakeven -- the record's highest -- while EVERY weekly band cell topped out
at 48 bps.  Both instruments cut turnover.  If the band is only a slower-rebalancing device
wearing a different name, it must add nothing once cadence is free to move.

THE TEST, pre-registered before any number was read:

  [A] FREE THE CADENCE.  Run cadence in {D, W, 2W, M, 6W, Q} against m in {0, 20} at n=20 on all
      three panels.  Two tuned parameters, no more (cadence, m).  Panel and cost rung {0, 10, 25}
      are reported axes, not tuned choices; every point of every axis is printed and written to
      `<slug>.grid.csv`.

  [B] DOES THE BAND ADD ANYTHING?  Three readings, in increasing strictness:
      B1  raw dSharpe(m=20) - dSharpe(m=0) at fixed cadence -- the band's own effect;
      B2  TURNOVER-MATCHED: for each banded cell, the m=0 cadence-only cell with the closest
          annual turnover.  If the cadence-only twin matches or beats the banded cell, the band
          buys nothing a slower calendar does not already buy;
      B3  4b/4a ADMISSION: does any banded cell clear a KEEP path that no m=0 cell clears?
      The band survives only if it wins B2 or B3.  B1 alone is not enough -- a band that merely
      slows the book down is the cadence dial by another name, which is the queue's own claim.

  [C] BREAKEVEN c*, the largest whole bps at which all five 4b bars still hold, on every cell
      that clears 4b at 25 bps.  Idea 329's claim "every weekly band cell tops out at 48, monthly
      m=0 reaches 68.6" is re-measured here on the same convention.

  [D] RULE 8 walk-forward: (cadence, m) chosen on 2008-2016 by IS Sharpe at 10 bps, 2017-2026
      read once, against the (W, m=0) anchor, the OOS-best cell (regret), RULES v2 (live) and SPY.

Book (fixed, idea 329's convention, never tuned): top-20 eligible by the RULES v1 composite with
the vol scaler OFF, RULES v1 eligibility (above the 200d MA, vol20 < 0.60), NORM weights
w_i = g/k_t at g = 0.75 so cadence and m cannot smuggle in a gross change, next-day execution.
The band (idea 273): a name enters at rank <= n and is held until its rank passes n+m or it
leaves the eligible set; free slots refill from the best-ranked eligible name not held.  m=0
nests the hard rank cut EXACTLY (asserted in section [0]).

REPRODUCTION GATES (section [0], all asserted or printed before any new number is read):
  * fast_backtest == engine.backtest to 1e-12 on returns and turnover, and the derived cost rung
    r(c) = r(0) - turnover*c/1e4 == engine.backtest(cost_bps=c) to 1e-12;
  * sel_band(n=20, m=0) == sel_hard(n=20) on every rebalance day, 0 disagreements;
  * idea 329's published U56 MONTHLY m=0 by-product: 15.30% / 1.213 / -19.51%, H1/H2
    1.200/1.232, OOS 1.307, breakeven 68.6 bps;
  * idea 329's published B136 WEEKLY m=0 cell: 14.27% / 1.009 / -20.43%, H2 0.817.

CAVEATS: (1) all three panels are current-constituent lists -- SURVIVORSHIP -- which flatters
every momentum book; the CAGR levels are optimistic, the cadence- and m-DIFFERENCES much less so.
The small panel is the worst offender (sub-$2B names that survived to 2026-09) and the 44 tickers
with `max_1d_move >= 1.0` in data/small_meta.csv are dropped before anything is run.
(2) SMALL439 starts 2010-01-04, so its halves are not the same calendar halves as U56/B136.
(3) The 2W and 6W cadences are defined by decimating the weekly rebalance mask (every 2nd / 6th
week-end), so they nest inside W's calendar exactly and are phase-anchored to the panel's first
week; a different phase is a different (unreported) choice, noted not tested.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os, sys
from pathlib import Path
import numpy as np, pandas as pd

RESUME = os.environ.get("RESUME") == "1"     # re-print [A]-[D] from the committed CSVs
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                      # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_is-CADENCE-the-real-dial-behind-the-band_cloud"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS, N = 0.60, 0.75, 20
BASE_FREQ = "W"                              # the LIVE book's cadence; never moved
CADENCES = ["D", "W", "2W", "M", "6W", "Q"]
MS = [0, 20]
COSTS = [0, 10, 25]
ANCHOR_CAD, ANCHOR_M = "W", 0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260


# ---------------------------------------------------------------- cadence
def reb_mask(idx, cadence):
    """True on the last trading day of each rebalance period.

    D/W/M/Q are engine.rebalance_mask verbatim (so W and M reproduce idea 329 exactly).
    2W and 6W decimate the WEEKLY mask -- every 2nd / 6th week-end -- so they nest inside the
    weekly calendar and are phase-anchored to the panel's first complete week."""
    if cadence in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, cadence)
    k = {"2W": 2, "6W": 6}[cadence]
    w = rebalance_mask(idx, "W")
    pos = np.where(w.values)[0][k - 1::k]
    s = pd.Series(False, index=idx)
    s.iloc[pos] = True
    return s


# ---------------------------------------------------------------- panels
def small_panel():
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    px = load_universe(small=True)
    keep = [c for c in px.columns if c not in bad]
    print(f"    SMALL: dropped {len(bad)} tickers with max_1d_move >= 1.0 -> {len(keep)-1} names + SPY")
    return px[keep]


# ---------------------------------------------------------------- the book
def rank_frame(px, drop_spy=False):
    """Composite rank among eligible names (v1 composite, vol scaler OFF; RULES v1 eligibility).

    drop_spy: on U56/B136 SPY is a genuine universe constituent and the record's books can hold
    it, so it is left eligible (idea 44's convention, needed for the reproduction gate).  On the
    small panel SPY is joined ONLY as a benchmark (see baseline.load_universe) and is removed."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    if drop_spy and "SPY" in px.columns:
        elig = elig.copy(); elig["SPY"] = False
    return s.where(elig).rank(axis=1, ascending=False), elig


def sel_hard(rk, n):
    """The record's book: hard top-n rank cut, recomputed from scratch every rebalance."""
    return rk <= n


def sel_band(px, rk, n, m, cadence):
    """No-trade band (idea 273): enter at rank <= n, hold until rank passes n+m or the name
    leaves the eligible set; free slots refill from the best-ranked eligible name not held.
    Evaluated on rebalance days only and forward-filled.

    The slot count each day is the parent's OWN count k_t = |{rank <= n}| rather than a flat n,
    so the band arm stays name-count-matched to the hard-cut arm day by day and m is a pure
    TURNOVER dial, not a second width dial.  m = 0 then nests sel_hard(n) EXACTLY."""
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


# ---------------------------------------------------------------- fast backtester
def fast_backtest(px, w, cost_bps=0.0, cadence="W"):
    """Vectorised-loop clone of engine.backtest (same semantics, numpy arrays).
    Asserted against engine.backtest in section [0]."""
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
    """PROTOCOL 4a: Sharpe > the LIVE book in BOTH halves and MaxDD no worse."""
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def breakeven(r0, t0, spy, hi=200):
    """Largest whole bps at which all five 4b bars still hold (None if it fails at 0)."""
    cstar, bar = None, ""
    for c in range(0, hi + 1):
        ok, _, f = bars_4b(r0 - t0 * c / 1e4, spy)
        if ok:
            cstar = c
        else:
            bar = ",".join(f)
            break
    return cstar, bar


def spearman(a, b):
    x, y = pd.Series(list(a)).rank(), pd.Series(list(b)).rank()
    return float(x.corr(y))


# ---------------------------------------------------------------- run
def main():
    print(f"=== {SLUG}")
    print(f"Book: top-{N} eligible by the v1 composite (vol scaler OFF), NORM weights g/k_t at "
          f"g={GROSS}, next-day execution.  Band m: sell only past rank n+m.")
    print(f"Tuned: cadence in {CADENCES} x m in {MS}.  Reported axes: panel, cost {COSTS} bps.")

    print("\n[panels]")
    panels = {"U56": load_universe(), "B136": load_universe(broad=True), "SMALL439": small_panel()}

    gcsv, ccsv = OUT / f"{SLUG}.grid.csv", OUT / f"{SLUG}.ctx.csv"
    if RESUME and gcsv.exists() and ccsv.exists():
        analyse(pd.read_csv(gcsv), pd.read_csv(ccsv).set_index("panel"), panels)
        return

    rows, ctx_rows = [], []
    for pname, px in panels.items():
        start = px.index[WARMUP]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms_ = metrics(spy); s1, s2 = hs(spy); so = metrics(spy.loc[OOS_START:])
        rk, elig = rank_frame(px, drop_spy=(pname == "SMALL439"))
        nel = elig.sum(axis=1).loc[start:]
        print(f"\n================ {pname}: {px.shape[1]-1} names + SPY, "
              f"{px.index[0].date()} -> {px.index[-1].date()}, eval from {start.date()}")
        print(f"    eligible/day mean {nel.mean():.1f} min {nel.min()} max {nel.max()}")
        print(f"    SPY CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} MaxDD {ms_['MaxDD']:.2%} "
              f"H1/H2 {s1:.3f}/{s2:.3f} | OOS Sharpe {so['Sharpe']:.3f} CAGR {so['CAGR']:.2%} "
              f"MaxDD {so['MaxDD']:.2%}")

        br, bt, _, _ = fast_backtest(px, rules_v2_weights(px), 0.0, BASE_FREQ)
        base10 = (br - bt * 10 / 1e4).loc[start:]
        bm = metrics(base10); b1, b2 = hs(base10); bo = metrics(base10.loc[OOS_START:])
        print(f"    RULES v2 (live, weekly, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
              f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {bo['Sharpe']:.3f} "
              f"CAGR {bo['CAGR']:.2%} MaxDD {bo['MaxDD']:.2%}")

        # ------------------------------------------------ [0] gates, once per panel
        if pname == "U56":
            print("\n[0] GATES")
            wA = weights_from(sel_hard(rk, N))
            eng = backtest(px, wA, cost_bps=0.0, freq="W")
            f_r, f_t, _, _ = fast_backtest(px, wA, 0.0, "W")
            d1 = np.abs(eng["returns"].loc[start:] - f_r.loc[start:]).max()
            d2 = np.abs(eng["turnover"].loc[start:] - f_t.loc[start:]).max()
            print(f"    fast_backtest vs engine.backtest: max|dr| {d1:.3e}  max|dturnover| {d2:.3e}")
            assert d1 < 1e-12 and d2 < 1e-12
            eng25 = backtest(px, wA, cost_bps=25.0, freq="W")
            d3 = np.abs(eng25["returns"].loc[start:] - (f_r - f_t * 25 / 1e4).loc[start:]).max()
            print(f"    derived rung r(25) vs live backtest(cost_bps=25): max|d| {d3:.3e}")
            assert d3 < 1e-12
            for fq in CADENCES:
                sb = sel_band(px, rk, N, 0, fq); sh = sel_hard(rk, N)
                reb = reb_mask(px.index, fq)
                dd = int((sb[reb] != sh[reb]).values.sum())
                print(f"    sel_band(m=0) nests sel_hard on {fq:>2} rebalance days: {dd} "
                      f"disagreements of {int(reb.sum()) * px.shape[1]} ({int(reb.sum())} reb days)")
                assert dd == 0
            # idea 329's published U56 MONTHLY m=0 by-product
            r0, t0, _, _ = fast_backtest(px, weights_from(sel_hard(rk, N)), 0.0, "M")
            r0, t0 = r0.loc[start:], t0.loc[start:]
            r10 = r0 - t0 * 10 / 1e4
            mm = metrics(r10); q1, q2 = hs(r10)
            cst, _ = breakeven(r0, t0, spy)
            print(f"    idea 329 U56 MONTHLY m=0 @10bps: {mm['CAGR']:.2%} / {mm['Sharpe']:.3f} / "
                  f"{mm['MaxDD']:.2%}  H1/H2 {q1:.3f}/{q2:.3f}  OOS "
                  f"{metrics(r10.loc[OOS_START:])['Sharpe']:.3f}  c* {cst} bps "
                  f"[published 15.30% / 1.213 / -19.51%, 1.200/1.232, OOS 1.307, c* 68.6]")

        # ------------------------------------------------ the grid
        print(f"\n[A] GRID {pname} (every point; ann.turnover = mean yearly sum|dw|)")
        print(f"    {'cad':>4} {'m':>3} {'reb/yr':>7} {'turn/yr':>8} {'names':>6} {'gross':>6} | "
              + " | ".join(f"c={c:<2} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1/H2':>13} {'OOS':>6} 4b 4a"
                           for c in COSTS))
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
                                f"m4b_CAGR_{c}": d4b["CAGR"],
                                f"m4a_H1_{c}": d4a["H1"], f"m4a_H2_{c}": d4a["H2"],
                                f"m4a_DD_{c}": d4a["DD"]})
                cst, cbar = breakeven(r0, t0, spy)
                rec["breakeven_bps"] = cst if cst is not None else -1
                rec["breakeven_first_fail"] = cbar
                print(line + f" c*={rec['breakeven_bps']:>3}")
                rows.append(rec)

            # reproduction gates for idea 329's PRE-REGISTERED B136 cell, which was n=20 m=20
            PUB329 = {"W": "14.27% / 1.009 / -20.43%, H2 0.817",
                      "M": "16.77% / 1.108 / -26.31%, H2 1.006, OOS 1.092",
                      "Q": "15.41% / 1.002 / -27.38%, H2 0.819"}
            if pname == "B136" and fq in PUB329:
                w = [r for r in rows if r["panel"] == "B136" and r["cadence"] == fq and r["m"] == 20][0]
                print(f"    [gate] idea 329 B136 {fq} m=20 (its pre-registered cell) @10bps: "
                      f"{w['CAGR_10']:.2%} / {w['Sharpe_10']:.3f} / {w['MaxDD_10']:.2%} "
                      f"H2 {w['H2_10']:.3f} OOS {w['OOS_Sharpe_10']:.3f}  [published {PUB329[fq]}]")

        ctx_rows.append(dict(panel=pname, spy_oos_sharpe=so["Sharpe"], spy_oos_cagr=so["CAGR"],
                             spy_oos_dd=so["MaxDD"], base_oos_sharpe=bo["Sharpe"],
                             base_oos_cagr=bo["CAGR"], base_oos_dd=bo["MaxDD"],
                             spy_sharpe=ms_["Sharpe"], spy_cagr=ms_["CAGR"], spy_dd=ms_["MaxDD"],
                             base_sharpe=bm["Sharpe"], base_cagr=bm["CAGR"], base_dd=bm["MaxDD"]))

    df = pd.DataFrame(rows); df.to_csv(gcsv, index=False)
    ctx = pd.DataFrame(ctx_rows).set_index("panel"); ctx.to_csv(ccsv)
    analyse(df, ctx, panels)


# ---------------------------------------------------------------- analysis
def analyse(df, ctx, panels):
    ORD = {c: i for i, c in enumerate(CADENCES)}

    # ---------------------------------------------------------- [B1] the band's own effect
    print("\n\n[B1] THE BAND'S OWN EFFECT at fixed cadence: dSharpe(m=20) - (m=0), 10 bps, and the")
    print("     same for the H2 margin over SPY.  Compare with what CADENCE moves at fixed m=0.")
    b1 = []
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        parts = []
        for fq in CADENCES:
            a = d[(d.cadence == fq) & (d.m == 0)].iloc[0]
            b = d[(d.cadence == fq) & (d.m == 20)].iloc[0]
            parts.append(f"{fq:>2} dS {b.Sharpe_10-a.Sharpe_10:+.3f} dH2 {b.m4b_H2_10-a.m4b_H2_10:+.3f}")
            b1.append(dict(panel=pname, cadence=fq, band_dS=b.Sharpe_10 - a.Sharpe_10,
                           band_dH2=b.m4b_H2_10 - a.m4b_H2_10,
                           band_dturn=b.turn_per_yr - a.turn_per_yr))
        print(f"    {pname:9s} BAND   | " + "  ".join(parts))
        w = d[(d.cadence == "W") & (d.m == 0)].iloc[0]
        parts = []
        for fq in CADENCES:
            a = d[(d.cadence == fq) & (d.m == 0)].iloc[0]
            parts.append(f"{fq:>2} dS {a.Sharpe_10-w.Sharpe_10:+.3f} dH2 {a.m4b_H2_10-w.m4b_H2_10:+.3f}")
        print(f"    {pname:9s} CADENCE| " + "  ".join(parts) + "   (vs W, m=0)")
    pd.DataFrame(b1).to_csv(OUT / f"{SLUG}.band_effect.csv", index=False)
    print("    READ: if |band move| << |cadence move| everywhere, the band is the weaker instrument;")
    print("          B2 then asks whether it is a DISTINCT one at all.")

    # ---------------------------------------------------------- [B2] turnover matching
    print("\n[B2] TURNOVER-MATCHED TWIN: for each banded cell, the m=0 cadence-only cell with the")
    print("     nearest annual turnover.  'band wins' = banded Sharpe > its cadence-only twin.")
    print(f"    {'panel':9s} {'banded cell':>14} {'turn':>7} {'Sharpe':>7} | {'m=0 twin':>10} "
          f"{'turn':>7} {'Sharpe':>7} | {'dSharpe (band-twin)':>20} {'winner':>8}")
    mt_rows = []
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        pool = d[d.m == 0]
        for fq in CADENCES:
            b = d[(d.cadence == fq) & (d.m == 20)].iloc[0]
            j = (pool.turn_per_yr - b.turn_per_yr).abs().idxmin()
            t = d.loc[j]
            dS = b.Sharpe_10 - t.Sharpe_10
            print(f"    {pname:9s} {fq+' m=20':>14} {b.turn_per_yr:>7.2f} {b.Sharpe_10:>7.3f} | "
                  f"{t.cadence+' m=0':>10} {t.turn_per_yr:>7.2f} {t.Sharpe_10:>7.3f} | "
                  f"{dS:>+20.4f} {'BAND' if dS > 0 else 'cadence':>8}")
            mt_rows.append(dict(panel=pname, cadence=fq, band_turn=b.turn_per_yr,
                                band_sharpe=b.Sharpe_10, twin_cadence=t.cadence,
                                twin_turn=t.turn_per_yr, twin_sharpe=t.Sharpe_10, d=dS))
    mt = pd.DataFrame(mt_rows); mt.to_csv(OUT / f"{SLUG}.matched.csv", index=False)
    wins = int((mt.d > 0).sum())
    print(f"    BAND wins {wins} of {len(mt)} turnover-matched comparisons "
          f"(median dSharpe {mt.d.median():+.4f}, mean {mt.d.mean():+.4f})")

    print("\n[B2b] TURNOVER IS THE ORDERING KEY?  Spearman(turn/yr, Sharpe_10) within each panel,")
    print("      over all 12 cells, and separately over the 6 m=0 cells.")
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        z = d[d.m == 0]
        print(f"    {pname:9s} all 12: rho {spearman(d.turn_per_yr, d.Sharpe_10):+.3f}   "
              f"m=0 only: rho {spearman(z.turn_per_yr, z.Sharpe_10):+.3f}   "
              f"turnover range {d.turn_per_yr.min():.2f}x - {d.turn_per_yr.max():.2f}x")

    # ---------------------------------------------------------- [B3] admission census
    print("\n[B3] KEEP-path census: does the BAND admit any cell the CADENCE dial alone does not?")
    for c in COSTS:
        d = df
        print(f"    c={c:>2} bps: 4b {int(d[f'keep4b_{c}'].sum())}/{len(d)}  "
              f"(m=0 {int(d[(d.m==0)][f'keep4b_{c}'].sum())}/{len(d[d.m==0])}, "
              f"m=20 {int(d[(d.m==20)][f'keep4b_{c}'].sum())}/{len(d[d.m==20])})   "
              f"4a {int(d[f'keep4a_{c}'].sum())}/{len(d)}  "
              f"(m=0 {int(d[(d.m==0)][f'keep4a_{c}'].sum())}, m=20 {int(d[(d.m==20)][f'keep4a_{c}'].sum())})")
    fails = {}
    for _, r in df.iterrows():
        for k in str(r["fail4b_10"]).split(","):
            if k:
                fails[k] = fails.get(k, 0) + 1
    print("    binding 4b bars at 10 bps:", ", ".join(f"{k} {v}/{len(df)}" for k, v in
                                                      sorted(fails.items(), key=lambda x: -x[1])))
    for c in COSTS:
        d = df[df[f"keep4b_{c}"]]
        if d.empty:
            print(f"    4b passes at {c} bps: none")
            continue
        print(f"    4b passes at {c} bps:")
        for _, r in d.iterrows():
            print(f"      {r.panel:9s} {r.cadence:>2} m={int(r.m):>2} turn {r.turn_per_yr:5.2f}x "
                  f"{r[f'CAGR_{c}']:.2%} / {r[f'Sharpe_{c}']:.3f} / {r[f'MaxDD_{c}']:.2%} "
                  f"H1/H2 {r[f'H1_{c}']:.3f}/{r[f'H2_{c}']:.3f} OOS {r[f'OOS_Sharpe_{c}']:.3f} "
                  f"c*={int(r.breakeven_bps)}")
    # the decisive B3 line
    kb = df[df.keep4b_10 & (df.m == 20)]
    ka = df[df.keep4b_10 & (df.m == 0)]
    uniq = []
    for _, r in kb.iterrows():
        twin = ka[(ka.panel == r.panel)]
        if twin.empty:
            uniq.append(f"{r.panel}/{r.cadence}")
    print(f"    BANDED 4b passes on a panel where NO m=0 cell passes @10 bps: "
          f"{len(uniq)} ({', '.join(uniq) if uniq else 'none'})")

    # ---------------------------------------------------------- [C] breakeven ladder
    print("\n[C] BREAKEVEN c* (largest whole bps at which all five 4b bars hold), every cell.")
    print(f"    {'panel':9s} " + "".join(f"{fq+' m0':>9}{fq+' m20':>10}" for fq in CADENCES))
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        cells = []
        for fq in CADENCES:
            for m in MS:
                r = d[(d.cadence == fq) & (d.m == m)].iloc[0]
                v = int(r.breakeven_bps)
                cells.append(f"{'--' if v < 0 else v:>9}" if m == 0 else f"{'--' if v < 0 else v:>10}")
        print(f"    {pname:9s} " + "".join(cells))
    best = df[df.breakeven_bps >= 0].sort_values("breakeven_bps", ascending=False)
    if not best.empty:
        print("    highest breakevens:")
        for _, r in best.head(6).iterrows():
            print(f"      {r.panel:9s} {r.cadence:>2} m={int(r.m):>2} c*={int(r.breakeven_bps):>3} bps"
                  f"  first bar to fail above it: {r.breakeven_first_fail}")
    print("    ('--' = the cell already fails 4b at 0 bps, so it has no breakeven.)")

    # ---------------------------------------------------------- [D] rule 8 walk-forward
    print("\n[D] RULE 8 WALK-FORWARD: (cadence, m) chosen on IS <= 2016 by Sharpe @10 bps, "
          "OOS 2017+ read once.")
    wf = []
    for pname in df.panel.unique():
        d = df[df.panel == pname]
        pick = d.loc[d["IS_Sharpe_10"].idxmax()]
        best = d.loc[d["OOS_Sharpe_10"].idxmax()]
        anch = d[(d.cadence == ANCHOR_CAD) & (d.m == ANCHOR_M)].iloc[0]
        pick0 = d[d.m == 0].loc[d[d.m == 0]["IS_Sharpe_10"].idxmax()]   # cadence-only chooser
        cx = ctx.loc[pname]
        print(f"\n    --- {pname}")
        print(f"    {'arm':34s} {'OOS CAGR':>9} {'OOS Sharpe':>11} {'OOS MaxDD':>10}")
        for lab, r in [(f"IS-chosen {pick.cadence} m={int(pick.m)}", pick),
                       (f"IS-chosen, m=0 only: {pick0.cadence}", pick0),
                       (f"anchor {ANCHOR_CAD} m={ANCHOR_M}", anch),
                       (f"OOS-best {best.cadence} m={int(best.m)}", best)]:
            print(f"    {lab:34s} {r.OOS_CAGR_10:>9.2%} {r.OOS_Sharpe_10:>11.3f} {r.OOS_MaxDD_10:>10.2%}")
        print(f"    {'RULES v2 (live)':34s} {cx.base_oos_cagr:>9.2%} {cx.base_oos_sharpe:>11.3f} "
              f"{cx.base_oos_dd:>10.2%}")
        print(f"    {'SPY':34s} {cx.spy_oos_cagr:>9.2%} {cx.spy_oos_sharpe:>11.3f} {cx.spy_oos_dd:>10.2%}")
        print(f"    regret (IS-chosen - OOS-best) {pick.OOS_Sharpe_10-best.OOS_Sharpe_10:+.4f}; "
              f"vs anchor {pick.OOS_Sharpe_10-anch.OOS_Sharpe_10:+.4f}; "
              f"band-free chooser costs {pick0.OOS_Sharpe_10-pick.OOS_Sharpe_10:+.4f}")
        wf.append(dict(panel=pname, pick_cadence=pick.cadence, pick_m=int(pick.m),
                       pick_oos_sharpe=pick.OOS_Sharpe_10, pick_oos_cagr=pick.OOS_CAGR_10,
                       pick_oos_dd=pick.OOS_MaxDD_10, pick0_cadence=pick0.cadence,
                       pick0_oos_sharpe=pick0.OOS_Sharpe_10, anchor_oos_sharpe=anch.OOS_Sharpe_10,
                       best_cadence=best.cadence, best_m=int(best.m),
                       best_oos_sharpe=best.OOS_Sharpe_10, spy_oos_sharpe=cx.spy_oos_sharpe,
                       base_oos_sharpe=cx.base_oos_sharpe))
    w = pd.DataFrame(wf); w.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    print(f"\n    chooser picks a BANDED cell on {int((w.pick_m == 20).sum())} of {len(w)} panels; "
          f"beats the anchor OOS on {int((w.pick_oos_sharpe > w.anchor_oos_sharpe).sum())}/{len(w)}, "
          f"SPY on {int((w.pick_oos_sharpe > w.spy_oos_sharpe).sum())}/{len(w)}, "
          f"the live book on {int((w.pick_oos_sharpe > w.base_oos_sharpe).sum())}/{len(w)}")
    print(f"\nwrote {SLUG}.grid.csv ({len(df)} rows), .band_effect.csv, .matched.csv, .walkforward.csv")


if __name__ == "__main__":
    main()
