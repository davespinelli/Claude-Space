#!/usr/bin/env python3
"""Idea 347: does the no-trade BAND earn its keep at MATCHED CADENCE on a panel the record
has not mined?

Idea 331 asked whether the band is only the cadence dial wearing a different name.  Its
decisive reading [B2] was TURNOVER-MATCHED: for every banded cell, find the m=0 cadence-only
cell with the nearest annual turnover and compare Sharpe.  The band won 10 of 18 -- but those
18 were 3 panels x 6 cadences at m=20 only, and every one of that run's 4b passes sat on U56,
the most-mined panel in the record.  The queue's suspicion is that the band is a U56 artefact.

Reading idea 331's own `matched.csv` first (this is a fact about the parent, not a new number):
the per-panel splits were U56 2/6, B136 4/6, SMALL439 4/6.  So U56 is where the band did
WORST.  The queue's framing ("if it drops to ~9/18 the effect is U56-specific") is therefore
mis-stated in its premise; the honest version of the same test is the one run here:

    on a panel that has never carried this menu, does the band beat its turnover-matched
    cadence-only twin more often than a coin?

THE TEST, pre-registered before any number was read
---------------------------------------------------
[A] GRID.  cadence in {D, W, 2W, M, 6W, Q} x m in {0, 10, 20, 40} at n=20.  Exactly two tuned
    parameters (cadence, m) -- PROTOCOL rule 4.  Panel and cost rung {0, 10, 25} are REPORTED
    axes, not tuned choices.  All 24 cells x 3 panels x 3 rungs are printed and written to
    `<slug>.grid.csv`.

[B] MATCHED-TURNOVER WIN RATE.  For each m>0 cell, the m=0 cell on the SAME panel with the
    nearest annual turnover (idea 331's convention verbatim).  18 comparisons per panel
    (3 m-values x 6 cadences).  Headline = B80held's win rate against the 9/18 coin-flip null,
    two-sided sign test.  Reported beside U56 and B136 run on the identical 18-cell design.
    A separate m=20-only slice (6 per panel) reproduces idea 331's published splits exactly.

[C] BREAKEVEN c* -- the largest whole bps at which all five 4b bars still hold -- for every
    cell, so the win rate can be read against cost tolerance rather than a single rung.

[D] RULE 8 walk-forward (PROTOCOL rule 8): (cadence, m) chosen on <= 2016-12-31 by IS Sharpe
    at 10 bps, 2017-01-01 onward read ONCE.  Reported against the band-free chooser (m=0 pool
    only), the (W, m=0) anchor, the OOS-best cell (regret), RULES v2 (live) and SPY, with OOS
    CAGR / Sharpe / MaxDD for each.  Both KEEP paths (4a vs the live book, 4b vs SPY) are
    evaluated on every cell at every rung.

PANELS
------
    B80held   the 80 B136 names NOT in U56 -- THE HELD-OUT PANEL.  SPY is the benchmark only,
              never a constituent and never rankable (idea 377's convention verbatim).
    U56       research/universe.json      -- idea 331's parent panel (SPY is a constituent).
    B136      research/universe_broad.json -- idea 331's second panel (SPY is a constituent).

BOOK (fixed, idea 331's convention, never tuned): top-20 eligible by the RULES v1 composite
with the vol scaler OFF, RULES v1 eligibility (above the 200d MA, vol20 < 0.60), NORM weights
w_i = g/k_t at g = 0.75 so neither cadence nor m can smuggle in a gross change, next-day
execution at the close, 10 bps per unit turnover unless a rung is named.

REPRODUCTION GATES (section [0], asserted or printed before any new number is read):
  * fast_backtest == engine.backtest to 1e-12 on returns and turnover, and the derived rung
    r(c) = r(0) - turnover*c/1e4 == engine.backtest(cost_bps=c) to 1e-12;
  * sel_band(n=20, m=0) == sel_hard(n=20) on every rebalance day of every cadence, 0 disagreements;
  * idea 331's published U56 M m=20 cell: 13.30% / 1.109 / -18.73%, H1/H2 1.196/1.042, turn 2.76x;
  * idea 331's published U56 6W m=20 sibling: 14.31% / 1.159 / -19.42%, c* = 104 bps;
  * idea 331's published B136 W m=20 and M m=20 cells (its inherited idea-329 gates):
    14.27% / 1.009 / -20.43%, H2 0.817 and 16.77% / 1.108 / -26.31%, H2 1.006, OOS 1.092;
  * idea 331's published matched-turnover splits U56 2/6, B136 4/6 at m=20.

CAVEATS
-------
(1) SURVIVORSHIP: all three panels are current-constituent lists, so every CAGR level is
    optimistic.  This run compares CELLS ON THE SAME PANEL, which is far less exposed than
    the levels; the levels are what a capital decision would use.
(2) B80held is held out from idea 331's menu but is NOT independent of B136 -- it is 80 of its
    136 columns.  A B136 result is roughly a weighted blend of U56 and B80held, so agreement
    between B136 and B80held is weaker evidence than agreement between U56 and B80held.
(3) 2W and 6W decimate the WEEKLY mask (every 2nd / 6th week-end) so they nest inside W's
    calendar exactly and are phase-anchored to the panel's first complete week.  A different
    phase is a different (unreported) choice: noted, not tested.
(4) The sign test treats the 18 comparisons as independent.  They are not -- they share cells
    and twins -- so its p-value is a LOWER bound on the true one, i.e. optimistic.

Deterministic, standalone.  Reads baseline.py and engine; modifies nothing.
"""
import os, sys, math, time
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, score, rules_v2_weights                      # noqa
from engine import backtest, metrics, rebalance_mask                             # noqa

SLUG = "2026-09-07_does-the-BAND-earn-its-keep-on-a-held-out-panel_C"
OUT = ROOT / "research" / "backtests"
MAX_VOL, GROSS, N = 0.60, 0.75, 20
BASE_FREQ = "W"                              # the LIVE book's cadence; never moved
CADENCES = ["D", "W", "2W", "M", "6W", "Q"]
MS = [0, 10, 20, 40]                         # m=0 is the hard cut (the twin pool)
COSTS = [0, 10, 25]
ANCHOR_CAD, ANCHOR_M = "W", 0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
WARMUP = 260

LOG = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); LOG.append(s)


# ---------------------------------------------------------------- cadence
def reb_mask(idx, cadence):
    """True on the last trading day of each rebalance period (idea 331's definition verbatim)."""
    if cadence in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, cadence)
    k = {"2W": 2, "6W": 6}[cadence]
    w = rebalance_mask(idx, "W")
    pos = np.where(w.values)[0][k - 1::k]
    s = pd.Series(False, index=idx)
    s.iloc[pos] = True
    return s


# ---------------------------------------------------------------- panels
def panels():
    u = load_universe()
    b = load_universe(broad=True)
    held = [c for c in b.columns if c not in set(u.columns)]
    bh = b[held].dropna(how="all").ffill()
    return [("B80held", bh, b["SPY"].reindex(bh.index).ffill(), True),   # SPY benchmark only
            ("U56",     u,  u["SPY"], False),                            # SPY is a constituent
            ("B136",    b,  b["SPY"], False)], held


# ---------------------------------------------------------------- the book
def rank_frame(px):
    """Composite rank among eligible names (v1 composite, vol scaler OFF; v1 eligibility)."""
    s = score(px, vol_scale=False)[0]
    _, above, vol20 = score(px)
    elig = above & (vol20 < MAX_VOL) & px.notna()
    return s.where(elig).rank(axis=1, ascending=False), elig


def sel_hard(rk, n):
    return rk <= n


def sel_band(px, rk, n, m, cadence):
    """No-trade band (idea 273 / 331): enter at rank <= n, hold until rank passes n+m or the
    name leaves the eligible set; free slots refill best-rank-first from eligible names not
    held.  Slot count each day is the parent's OWN k_t = |{rank <= n}|, so the band arm stays
    name-count-matched to the hard-cut arm day by day and m is a pure TURNOVER dial.  m = 0
    then nests sel_hard(n) exactly (asserted in [0])."""
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
    """Vectorised-loop clone of engine.backtest (same semantics).  Gated in [0]."""
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


def spy_ref(spy):
    """SPY's five 4b reference numbers, computed once per panel."""
    m = metrics(spy); s1, s2 = hs(spy)
    return dict(H1=s1, H2=s2, OOS=metrics(spy.loc[OOS_START:])["Sharpe"],
                DDcap=0.60 * abs(m["MaxDD"]), CAGRfloor=0.70 * m["CAGR"])


def bars_4b(r, ref):
    """PROTOCOL 4b: Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70%."""
    m = metrics(r); h1, h2 = hs(r)
    d = {"H1": h1 - ref["H1"], "H2": h2 - ref["H2"],
         "OOS": metrics(r.loc[OOS_START:])["Sharpe"] - ref["OOS"],
         "DD": ref["DDcap"] - abs(m["MaxDD"]), "CAGR": m["CAGR"] - ref["CAGRfloor"]}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def bars_4a(r, base):
    """PROTOCOL 4a: Sharpe > the LIVE book in BOTH halves and MaxDD no worse."""
    h1, h2 = hs(r); b1, b2 = hs(base)
    d = {"H1": h1 - b1, "H2": h2 - b2, "DD": abs(metrics(base)["MaxDD"]) - abs(metrics(r)["MaxDD"])}
    f = [k for k, v in d.items() if v < 0]
    return (not f), d, f


def breakeven(r0, t0, ref, hi=200):
    """Largest whole bps at which all five 4b bars still hold (-1 if it fails at 0)."""
    cstar, bar = -1, "at0"
    for c in range(0, hi + 1):
        ok, _, f = bars_4b(r0 - t0 * c / 1e4, ref)
        if ok:
            cstar = c
        else:
            bar = ",".join(f)
            break
    return cstar, bar


def sign_test(w, n):
    """Two-sided exact binomial p at p0 = 0.5 (no scipy in the sandbox)."""
    def pmf(k):
        return math.comb(n, k) * 0.5 ** n
    obs = pmf(w)
    return min(1.0, sum(pmf(k) for k in range(n + 1) if pmf(k) <= obs + 1e-15))


def spearman(a, b):
    x, y = pd.Series(list(a)).rank(), pd.Series(list(b)).rank()
    return float(x.corr(y))


# ---------------------------------------------------------------- run
def main():
    t_start = time.time()
    P("=" * 150)
    P(f"IDEA 347 - {SLUG}")
    P(f"Book: top-{N} eligible by the v1 composite (vol scaler OFF), NORM weights g/k_t at "
      f"g={GROSS}, next-day execution.  Band m: sell only past rank n+m.")
    P(f"Tuned (2): cadence in {CADENCES} x m in {MS}.  Reported axes: panel, cost rung {COSTS} bps.")
    P("Held-out panel = B80held (the 80 B136 names NOT in U56).  U56/B136 are reproduction controls.")

    PN, held_names = panels()
    P(f"\n[panels] B80held = {len(held_names)} names "
      f"({', '.join(held_names[:12])}{' ...' if len(held_names) > 12 else ''})")
    for nm, px, spy, bench_only in PN:
        P(f"    {nm:9s} {px.shape[1]:>3} cols x {px.shape[0]} rows  {px.index[0].date()} -> "
          f"{px.index[-1].date()}  SPY-as-constituent={'no' if bench_only else 'yes'}")

    rows, ctx_rows, gate_ok = [], [], True
    for pname, px, spyfull, bench_only in PN:
        start = px.index[WARMUP]
        spy = spyfull.pct_change().fillna(0).loc[start:]
        ref = spy_ref(spy)
        ms_ = metrics(spy); so = metrics(spy.loc[OOS_START:])
        rk, elig = rank_frame(px)
        nel = elig.sum(axis=1).loc[start:]
        P(f"\n================ {pname}: {px.shape[1]} rankable cols, eval from {start.date()}")
        P(f"    eligible/day mean {nel.mean():.1f} min {int(nel.min())} max {int(nel.max())}")
        P(f"    SPY CAGR {ms_['CAGR']:.2%} Sharpe {ms_['Sharpe']:.3f} MaxDD {ms_['MaxDD']:.2%} "
          f"H1/H2 {ref['H1']:.3f}/{ref['H2']:.3f} | OOS Sharpe {so['Sharpe']:.3f} "
          f"CAGR {so['CAGR']:.2%} MaxDD {so['MaxDD']:.2%}")
        P(f"    4b bars on this panel: DD cap {-ref['DDcap']:.2%}, CAGR floor {ref['CAGRfloor']:.2%}")

        # the live book, run on this panel (4a comparand)
        bpx = px if not bench_only else px.join(spyfull.rename("SPY"))
        br, bt, _, _ = fast_backtest(bpx, rules_v2_weights(bpx), 0.0, BASE_FREQ)
        br, bt = br.loc[start:], bt.loc[start:]
        base10 = br - bt * 10 / 1e4
        bm = metrics(base10); b1, b2 = hs(base10); bo = metrics(base10.loc[OOS_START:])
        P(f"    RULES v2 (live, weekly, 10 bps) CAGR {bm['CAGR']:.2%} Sharpe {bm['Sharpe']:.3f} "
          f"MaxDD {bm['MaxDD']:.2%} H1/H2 {b1:.3f}/{b2:.3f} | OOS Sharpe {bo['Sharpe']:.3f} "
          f"CAGR {bo['CAGR']:.2%} MaxDD {bo['MaxDD']:.2%}")

        # ------------------------------------------------ [0] gates, once
        if pname == "U56":
            P("\n[0] REPRODUCTION GATES")
            wA = weights_from(sel_hard(rk, N))
            eng = backtest(px, wA, cost_bps=0.0, freq="W")
            f_r, f_t, _, _ = fast_backtest(px, wA, 0.0, "W")
            d1 = np.abs(eng["returns"].loc[start:] - f_r.loc[start:]).max()
            d2 = np.abs(eng["turnover"].loc[start:] - f_t.loc[start:]).max()
            P(f"    fast_backtest vs engine.backtest: max|dr| {d1:.3e}  max|dturn| {d2:.3e}")
            assert d1 < 1e-12 and d2 < 1e-12
            eng25 = backtest(px, wA, cost_bps=25.0, freq="W")
            d3 = np.abs(eng25["returns"].loc[start:] - (f_r - f_t * 25 / 1e4).loc[start:]).max()
            P(f"    derived rung r(25) vs engine.backtest(cost_bps=25): max|d| {d3:.3e}")
            assert d3 < 1e-12
            for fq in CADENCES:
                sb = sel_band(px, rk, N, 0, fq); sh = sel_hard(rk, N)
                reb = reb_mask(px.index, fq)
                dd = int((sb[reb] != sh[reb]).values.sum())
                P(f"    sel_band(m=0) nests sel_hard on {fq:>2}: {dd} disagreements over "
                  f"{int(reb.sum())} rebalance days x {px.shape[1]} cols")
                assert dd == 0

        # ------------------------------------------------ the grid
        P(f"\n[A] GRID {pname} (all {len(CADENCES)*len(MS)} cells; turn/yr = mean yearly sum|dw|)")
        P(f"    {'cad':>4} {'m':>3} {'reb/yr':>7} {'turn/yr':>8} {'names':>6} {'gross':>6} | "
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
                    ok4b, d4b, f4b = bars_4b(r, ref)
                    basec = base10 if c == 10 else (br - bt * c / 1e4)
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
                                f"m4b_CAGR_{c}": d4b["CAGR"], f"m4a_H1_{c}": d4a["H1"],
                                f"m4a_H2_{c}": d4a["H2"], f"m4a_DD_{c}": d4a["DD"]})
                cst, cbar = breakeven(r0, t0, ref)
                rec["breakeven_bps"] = cst
                rec["breakeven_first_fail"] = cbar
                P(line + f" c*={cst:>3}")
                rows.append(rec)

        ctx_rows.append(dict(panel=pname, spy_sharpe=ms_["Sharpe"], spy_cagr=ms_["CAGR"],
                             spy_dd=ms_["MaxDD"], spy_oos_sharpe=so["Sharpe"],
                             spy_oos_cagr=so["CAGR"], spy_oos_dd=so["MaxDD"],
                             base_sharpe=bm["Sharpe"], base_cagr=bm["CAGR"], base_dd=bm["MaxDD"],
                             base_oos_sharpe=bo["Sharpe"], base_oos_cagr=bo["CAGR"],
                             base_oos_dd=bo["MaxDD"]))

    df = pd.DataFrame(rows); df.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    ctx = pd.DataFrame(ctx_rows).set_index("panel"); ctx.to_csv(OUT / f"{SLUG}.ctx.csv")

    # ---------------------------------------------------------- [0b] parent gates
    P("\n[0b] IDEA 331 REPRODUCTION (published numbers in brackets)")
    def cell(p, c, m): return df[(df.panel == p) & (df.cadence == c) & (df.m == m)].iloc[0]
    for lab, (p, c, m), pub in [
            ("U56 M m=20 (331's PARK candidate)", ("U56", "M", 20),
             "13.30% / 1.109 / -18.73%, H1/H2 1.196/1.042, turn 2.76x, OOS 1.124, c* 95"),
            ("U56 6W m=20 (331's sibling)", ("U56", "6W", 20),
             "14.31% / 1.159 / -19.42%, H1/H2 1.155/1.175, turn 2.29x, OOS 1.250, c* 104"),
            ("B136 W m=20 (331's inherited gate)", ("B136", "W", 20),
             "14.27% / 1.009 / -20.43%, H2 0.817"),
            ("B136 M m=20 (331's inherited gate)", ("B136", "M", 20),
             "16.77% / 1.108 / -26.31%, H2 1.006, OOS 1.092")]:
        r = cell(p, c, m)
        P(f"    {lab:36s} {r.CAGR_10:.2%} / {r.Sharpe_10:.3f} / {r.MaxDD_10:.2%}  "
          f"H1/H2 {r.H1_10:.3f}/{r.H2_10:.3f}  turn {r.turn_per_yr:.2f}x  OOS {r.OOS_Sharpe_10:.3f}  "
          f"c* {int(r.breakeven_bps)}")
        P(f"        [published: {pub}]")

    analyse(df, ctx)
    P(f"\n[runtime] {time.time()-t_start:.0f}s")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LOG) + "\n")


# ---------------------------------------------------------------- analysis
def matched(df, pname, ms):
    """Idea 331's [B2] convention: nearest-turnover m=0 twin on the same panel."""
    d = df[df.panel == pname]
    pool = d[d.m == 0]
    out = []
    for m in ms:
        for fq in CADENCES:
            b = d[(d.cadence == fq) & (d.m == m)].iloc[0]
            t = d.loc[(pool.turn_per_yr - b.turn_per_yr).abs().idxmin()]
            out.append(dict(panel=pname, cadence=fq, m=m, band_turn=b.turn_per_yr,
                            band_sharpe=b.Sharpe_10, band_sharpe_0=b.Sharpe_0,
                            band_sharpe_25=b.Sharpe_25, twin_cadence=t.cadence,
                            twin_turn=t.turn_per_yr, twin_sharpe=t.Sharpe_10,
                            twin_sharpe_0=t.Sharpe_0, twin_sharpe_25=t.Sharpe_25,
                            turn_gap=b.turn_per_yr - t.turn_per_yr,
                            d=b.Sharpe_10 - t.Sharpe_10,
                            d0=b.Sharpe_0 - t.Sharpe_0, d25=b.Sharpe_25 - t.Sharpe_25,
                            band_cstar=b.breakeven_bps, twin_cstar=t.breakeven_bps))
    return pd.DataFrame(out)


def analyse(df, ctx):
    PANELS = list(df.panel.unique())

    # ---------------------------------------------------------- [B0] reproduce 331's slice
    P("\n\n[B0] IDEA 331's SLICE REPRODUCED (m=20 only, 6 cadences per panel).")
    P("     Published: U56 2/6, B136 4/6, SMALL439 4/6 -> 10/18 pooled.  SMALL439 is not run here.")
    for p in PANELS:
        mt = matched(df, p, [20])
        P(f"    {p:9s} band wins {int((mt.d > 0).sum())}/6  (median d {mt.d.median():+.4f})"
          + ("   <-- HELD OUT" if p == "B80held" else ""))

    # ---------------------------------------------------------- [B] the headline
    P("\n[B] MATCHED-TURNOVER WIN RATE on the 18-cell design (m in {10,20,40} x 6 cadences).")
    P(f"    {'panel':9s} {'cell':>10} {'turn':>7} {'Shrp':>7} | {'m=0 twin':>10} {'turn':>7} "
      f"{'Shrp':>7} | {'gap':>7} {'dSharpe':>9} {'winner':>8}")
    allmt = []
    for p in PANELS:
        mt = matched(df, p, [10, 20, 40])
        for _, r in mt.iterrows():
            P(f"    {p:9s} {r.cadence+' m'+str(int(r.m)):>10} {r.band_turn:>7.2f} {r.band_sharpe:>7.3f} | "
              f"{r.twin_cadence+' m0':>10} {r.twin_turn:>7.2f} {r.twin_sharpe:>7.3f} | "
              f"{r.turn_gap:>+7.2f} {r.d:>+9.4f} {'BAND' if r.d > 0 else 'cadence':>8}")
        allmt.append(mt)
    mt = pd.concat(allmt, ignore_index=True); mt.to_csv(OUT / f"{SLUG}.matched.csv", index=False)

    P("\n    SUMMARY (18 comparisons per panel; null = 9/18; sign-test p is a LOWER bound, "
      "the cells are not independent)")
    P(f"    {'panel':9s} {'wins@10bps':>11} {'p':>7} {'median d':>10} {'mean d':>9} "
      f"{'wins@0':>7} {'wins@25':>8}   {'m=10':>6} {'m=20':>6} {'m=40':>6}")
    sm = []
    for p in PANELS:
        z = mt[mt.panel == p]
        w = int((z.d > 0).sum())
        per_m = [int((z[z.m == m].d > 0).sum()) for m in (10, 20, 40)]
        P(f"    {p:9s} {str(w)+'/18':>11} {sign_test(w, 18):>7.3f} {z.d.median():>+10.4f} "
          f"{z.d.mean():>+9.4f} {str(int((z.d0>0).sum()))+'/18':>7} "
          f"{str(int((z.d25>0).sum()))+'/18':>8}   "
          + " ".join(f"{str(x)+'/6':>6}" for x in per_m)
          + ("   <-- HELD OUT" if p == "B80held" else ""))
        sm.append(dict(panel=p, wins=w, n=18, p=sign_test(w, 18), median_d=z.d.median(),
                       mean_d=z.d.mean(), wins_0bps=int((z.d0 > 0).sum()),
                       wins_25bps=int((z.d25 > 0).sum()),
                       wins_m10=per_m[0], wins_m20=per_m[1], wins_m40=per_m[2]))
    pd.DataFrame(sm).to_csv(OUT / f"{SLUG}.winrate.csv", index=False)
    hz = mt[mt.panel == "B80held"]
    hw = int((hz.d > 0).sum())
    P(f"\n    HEADLINE: on the held-out B80held panel the band wins {hw}/18 turnover-matched "
      f"comparisons (p {sign_test(hw, 18):.3f}), median dSharpe {hz.d.median():+.4f}.")

    P("\n[B1c] WHERE the band wins: matched-turnover wins by the BANDED cell's own cadence "
      "(3 m-values each).")
    P(f"    {'panel':9s} " + " ".join(f"{c:>6}" for c in CADENCES) + "     fast (D,W,2W) vs slow (M,6W,Q)")
    for p in PANELS:
        z = mt[mt.panel == p]
        per = {c: int((z[z.cadence == c].d > 0).sum()) for c in CADENCES}
        fast = sum(per[c] for c in ("D", "W", "2W")); slow = sum(per[c] for c in ("M", "6W", "Q"))
        P(f"    {p:9s} " + " ".join(f"{str(per[c])+'/3':>6}" for c in CADENCES)
          + f"     {fast}/9 vs {slow}/9")
    P("    READ: a band that only wins at SLOW cadences is buying the same thing the calendar")
    P("          buys; a band that wins at FAST cadences too is a distinct turnover instrument.")

    P("\n[B2c] HOW WELL MATCHED IS THE 'MATCHED' COMPARISON?  The m=0 twin pool has a TURNOVER")
    P("      FLOOR (its slowest cell, Q m=0).  A banded cell below that floor is matched to the")
    P("      grid edge and is credited for turnover the cadence dial cannot reach at all.")
    for p in PANELS:
        z = mt[mt.panel == p]
        floor = df[(df.panel == p) & (df.m == 0)].turn_per_yr.min()
        below = z[z.band_turn < floor]
        pinned = z[z.twin_cadence == "Q"]
        P(f"    {p:9s} m=0 turnover floor {floor:.2f}x (Q m=0).  Banded cells BELOW it: "
          f"{len(below)}/18, of which the band wins {int((below.d>0).sum())}.  "
          f"Cells pinned to the Q m=0 twin: {len(pinned)}/18, band wins "
          f"{int((pinned.d>0).sum())}.")
        rel = (z.turn_gap.abs() / z.twin_turn)
        for thr in (0.05, 0.10, 0.20):
            g = z[rel <= thr]
            P(f"        |gap|/twin <= {thr:.0%}: {len(g):>2} cells, band wins "
              f"{int((g.d>0).sum())}"
              + (f" (median d {g.d.median():+.4f})" if len(g) else ""))
    tight = mt[(mt.turn_gap.abs() / mt.twin_turn) <= 0.10]
    P(f"    POOLED over all three panels, |gap|/twin <= 10%: {len(tight)} cells, band wins "
      f"{int((tight.d>0).sum())} (median d {tight.d.median():+.4f} "
      f"vs {mt.d.median():+.4f} over all {len(mt)}).")
    mt.assign(rel_gap=(mt.turn_gap.abs() / mt.twin_turn)).to_csv(
        OUT / f"{SLUG}.matched.csv", index=False)

    # ---------------------------------------------------------- [B2b] turnover as ordering key
    P("\n[B2b] IS TURNOVER THE ORDERING KEY?  Spearman(turn/yr, Sharpe_10) within each panel.")
    for p in PANELS:
        d = df[df.panel == p]; z = d[d.m == 0]
        P(f"    {p:9s} all {len(d)} cells: rho {spearman(d.turn_per_yr, d.Sharpe_10):+.3f}   "
          f"m=0 only ({len(z)}): rho {spearman(z.turn_per_yr, z.Sharpe_10):+.3f}   "
          f"turnover {d.turn_per_yr.min():.2f}x - {d.turn_per_yr.max():.2f}x")

    # ---------------------------------------------------------- [B1] band's own effect
    P("\n[B1] THE BAND'S OWN EFFECT at FIXED cadence (dSharpe vs m=0), against what the CADENCE")
    P("     dial moves at fixed m=0 (vs W).  10 bps.")
    b1 = []
    for p in PANELS:
        d = df[df.panel == p]
        for m in (10, 20, 40):
            parts = []
            for fq in CADENCES:
                a = d[(d.cadence == fq) & (d.m == 0)].iloc[0]
                b = d[(d.cadence == fq) & (d.m == m)].iloc[0]
                parts.append(f"{fq:>2} {b.Sharpe_10-a.Sharpe_10:+.3f}")
                b1.append(dict(panel=p, cadence=fq, m=m, band_dS=b.Sharpe_10 - a.Sharpe_10,
                               band_dturn=b.turn_per_yr - a.turn_per_yr))
            P(f"    {p:9s} BAND m={m:<2}| " + "  ".join(parts))
        w = d[(d.cadence == "W") & (d.m == 0)].iloc[0]
        parts = [f"{fq:>2} {d[(d.cadence==fq)&(d.m==0)].iloc[0].Sharpe_10-w.Sharpe_10:+.3f}"
                 for fq in CADENCES]
        P(f"    {p:9s} CADENCE | " + "  ".join(parts) + "   (m=0, vs W)")
    pd.DataFrame(b1).to_csv(OUT / f"{SLUG}.band_effect.csv", index=False)

    # ---------------------------------------------------------- [B3] KEEP-path census
    P("\n[B3] KEEP-PATH CENSUS: does the BAND admit any cell the cadence dial alone does not?")
    for c in COSTS:
        P(f"    c={c:>2} bps: 4b {int(df[f'keep4b_{c}'].sum())}/{len(df)}  "
          f"(m=0 {int(df[df.m==0][f'keep4b_{c}'].sum())}/{len(df[df.m==0])}, "
          f"m>0 {int(df[df.m>0][f'keep4b_{c}'].sum())}/{len(df[df.m>0])})   |   "
          f"4a {int(df[f'keep4a_{c}'].sum())}/{len(df)}  "
          f"(m=0 {int(df[df.m==0][f'keep4a_{c}'].sum())}, m>0 {int(df[df.m>0][f'keep4a_{c}'].sum())})")
    for p in PANELS:
        d = df[df.panel == p]
        P(f"    {p:9s} 4b @10bps: {int(d.keep4b_10.sum())}/{len(d)}   4a @10bps: "
          f"{int(d.keep4a_10.sum())}/{len(d)}")
    fails = {}
    for _, r in df.iterrows():
        for k in str(r["fail4b_10"]).split(","):
            if k:
                fails[k] = fails.get(k, 0) + 1
    P("    binding 4b bars @10bps: " + ", ".join(f"{k} {v}/{len(df)}" for k, v in
                                                 sorted(fails.items(), key=lambda x: -x[1])))
    kp = df[df.keep4b_10]
    if kp.empty:
        P("    4b passes @10bps: none")
    else:
        P("    4b passes @10bps:")
        for _, r in kp.iterrows():
            P(f"      {r.panel:9s} {r.cadence:>2} m={int(r.m):>2} turn {r.turn_per_yr:5.2f}x "
              f"{r.CAGR_10:.2%} / {r.Sharpe_10:.3f} / {r.MaxDD_10:.2%} H1/H2 "
              f"{r.H1_10:.3f}/{r.H2_10:.3f} OOS {r.OOS_Sharpe_10:.3f} c*={int(r.breakeven_bps)}")
    kp.to_csv(OUT / f"{SLUG}.keeppaths.csv", index=False)
    for p in PANELS:
        d = df[df.panel == p]
        bp = d[d.keep4b_10 & (d.m > 0)]
        zp = d[d.keep4b_10 & (d.m == 0)]
        P(f"    {p:9s} banded 4b passes {len(bp)}, m=0 4b passes {len(zp)} -> band admits a cell "
          f"the cadence dial does not: {'YES' if len(bp) and not len(zp) else 'no'}")

    # ---------------------------------------------------------- [C] breakeven ladder
    P("\n[C] BREAKEVEN c* (largest whole bps at which all five 4b bars hold; '--' = fails at 0).")
    P(f"    {'panel':9s} " + "".join(f"{fq:>7}" for fq in CADENCES) + "     (rows = m)")
    for p in PANELS:
        d = df[df.panel == p]
        for m in MS:
            cells = []
            for fq in CADENCES:
                v = int(d[(d.cadence == fq) & (d.m == m)].iloc[0].breakeven_bps)
                cells.append(f"{'--' if v < 0 else v:>7}")
            P(f"    {p:9s} " + "".join(cells) + f"   m={m}")
    best = df[df.breakeven_bps >= 0].sort_values("breakeven_bps", ascending=False)
    if not best.empty:
        P("    highest breakevens:")
        for _, r in best.head(6).iterrows():
            P(f"      {r.panel:9s} {r.cadence:>2} m={int(r.m):>2} c*={int(r.breakeven_bps):>3} bps "
              f"(first bar to fail above it: {r.breakeven_first_fail})")

    # ---------------------------------------------------------- [D] rule 8
    P("\n[D] RULE 8 WALK-FORWARD: (cadence, m) chosen on IS <= 2016-12-31 by Sharpe @10 bps; "
      "2017+ read ONCE.")
    wf = []
    for p in PANELS:
        d = df[df.panel == p]
        pick = d.loc[d.IS_Sharpe_10.idxmax()]
        best = d.loc[d.OOS_Sharpe_10.idxmax()]
        anch = d[(d.cadence == ANCHOR_CAD) & (d.m == ANCHOR_M)].iloc[0]
        d0 = d[d.m == 0]; pick0 = d0.loc[d0.IS_Sharpe_10.idxmax()]
        cx = ctx.loc[p]
        P(f"\n    --- {p}" + ("   <-- HELD OUT" if p == "B80held" else ""))
        P(f"    {'arm':38s} {'OOS CAGR':>9} {'OOS Sharpe':>11} {'OOS MaxDD':>10}")
        for lab, r in [(f"IS-chosen {pick.cadence} m={int(pick.m)}", pick),
                       (f"IS-chosen, BAND-FREE pool: {pick0.cadence} m=0", pick0),
                       (f"anchor {ANCHOR_CAD} m={ANCHOR_M}", anch),
                       (f"OOS-best {best.cadence} m={int(best.m)} (hindsight)", best)]:
            P(f"    {lab:38s} {r.OOS_CAGR_10:>9.2%} {r.OOS_Sharpe_10:>11.3f} {r.OOS_MaxDD_10:>10.2%}")
        P(f"    {'RULES v2 (live baseline)':38s} {cx.base_oos_cagr:>9.2%} "
          f"{cx.base_oos_sharpe:>11.3f} {cx.base_oos_dd:>10.2%}")
        P(f"    {'SPY':38s} {cx.spy_oos_cagr:>9.2%} {cx.spy_oos_sharpe:>11.3f} {cx.spy_oos_dd:>10.2%}")
        P(f"    regret (IS-chosen - OOS-best) {pick.OOS_Sharpe_10-best.OOS_Sharpe_10:+.4f}; "
          f"vs anchor {pick.OOS_Sharpe_10-anch.OOS_Sharpe_10:+.4f}; "
          f"cost of removing the band from the chooser's menu "
          f"{pick0.OOS_Sharpe_10-pick.OOS_Sharpe_10:+.4f}")
        wf.append(dict(panel=p, pick_cadence=pick.cadence, pick_m=int(pick.m),
                       pick_is_sharpe=pick.IS_Sharpe_10, pick_oos_sharpe=pick.OOS_Sharpe_10,
                       pick_oos_cagr=pick.OOS_CAGR_10, pick_oos_dd=pick.OOS_MaxDD_10,
                       pick0_cadence=pick0.cadence, pick0_oos_sharpe=pick0.OOS_Sharpe_10,
                       pick0_oos_cagr=pick0.OOS_CAGR_10, pick0_oos_dd=pick0.OOS_MaxDD_10,
                       anchor_oos_sharpe=anch.OOS_Sharpe_10, anchor_oos_cagr=anch.OOS_CAGR_10,
                       anchor_oos_dd=anch.OOS_MaxDD_10, best_cadence=best.cadence,
                       best_m=int(best.m), best_oos_sharpe=best.OOS_Sharpe_10,
                       spy_oos_sharpe=cx.spy_oos_sharpe, spy_oos_cagr=cx.spy_oos_cagr,
                       spy_oos_dd=cx.spy_oos_dd, base_oos_sharpe=cx.base_oos_sharpe,
                       base_oos_cagr=cx.base_oos_cagr, base_oos_dd=cx.base_oos_dd))
    w = pd.DataFrame(wf); w.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    P(f"\n    chooser picks a BANDED cell on {int((w.pick_m > 0).sum())}/{len(w)} panels; "
      f"beats the anchor OOS on {int((w.pick_oos_sharpe > w.anchor_oos_sharpe).sum())}/{len(w)}, "
      f"SPY on {int((w.pick_oos_sharpe > w.spy_oos_sharpe).sum())}/{len(w)}, "
      f"the live book on {int((w.pick_oos_sharpe > w.base_oos_sharpe).sum())}/{len(w)}; "
      f"band-free chooser is better OOS on "
      f"{int((w.pick0_oos_sharpe > w.pick_oos_sharpe).sum())}/{len(w)}")
    P(f"\nwrote {SLUG}.grid.csv ({len(df)} rows), .matched.csv, .winrate.csv, .band_effect.csv, "
      f".keeppaths.csv, .walkforward.csv, .ctx.csv, .console.txt")


if __name__ == "__main__":
    main()
