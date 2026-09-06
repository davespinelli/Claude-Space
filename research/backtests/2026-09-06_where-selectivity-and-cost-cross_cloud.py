#!/usr/bin/env python3
"""IDEA 155  where-selectivity-and-cost-cross   (cloud, 2026-09-06)

THE QUESTION
------------
Idea 78 found two monotone curves that must cross:

    * GROSS selection spread RISES as the book gets more selective
      (at matched count, q = 0.25 pays +0.0366/+0.0334/+0.0359 as k goes 20 -> 40 -> 80;
       Spearman(q, spread) = -0.975 vs Spearman(k, spread) = +0.685)
    * NET Sharpe premium FALLS after costs
      (Spearman(k, net premium) = -0.358 at n=5 and -0.601 at n=20 at 10 bps; the
       full-panel ordering inverts to EWall 1.026 > CAND20 0.957 > CAND5 0.880)

The queue asks where they cross, in the one coordinate that makes the answer a number a rule
could carry:

    sweep SELECTIVITY q against the COST RUNG (0-30 bps) and report the q that maximises NET
    premium at each rung.  If the argmax q is at or near 1.0 at 10 bps, that is a THIRD
    independent derivation of idea 82's "drop the ranking" and it comes with a number.

  Q1  REPRODUCTION.  Rebuild idea 78's panels, eligibility gate, composite key and both KEEP
      bars with its own code, and re-derive its published full-panel control ordering
      (EWall 1.026 > CAND20 0.957 > CAND5 0.880) before any new number is read.
  Q2  THE TWO CURVES.  Gross (0 bps) premium and turnover against q, per panel.  If the gross
      curve does not rise into selectivity there is nothing to cross.
  Q3  THE CROSSING.  argmax_q net premium at every rung 0/5/10/15/20/25/30 bps, every grid
      point printed; and the dual reading -- the BREAKEVEN cost c*(q) at which each
      selectivity stops paying, which is the same crossing seen along the other axis.
  Q4  IS THE ARGMAX A DRAW OR A RESULT?  72 seeded sub-panels (k = 20/40/80 x 24 draws from
      B136, idea 78's own construction) give the argmax q a distribution rather than one
      point per panel.
  Q5  RULE 8.  q chosen on IS <= 2016-12-31 at each rung, OOS >= 2017-01-01 read ONCE, against
      the q = 1.00 do-nothing control, a random-q control (idea 151), RULES v1 and SPY.
  Q6  BOTH KEEP PATHS on every (panel, q, rung) book.

DESIGN
------
Idea 78's script is IMPORTED, not re-implemented: `build_panels`, `eligible_mask`,
`weights_ewall`, `fail_4a`, `fail_4b`, `spearman`, `tstat`, its composite key (`score` with
vol_scale=False, per ideas 1/2/80/81), its 200d / vol20 < 0.60 gate, GROSS = 0.75, weekly
rebalance and t+1 execution all execute the parent's own code.

  SELECTIVITY  the book holds the top n_t = max(1, round(q * E_t)) eligible names, equal
               weighted at gross/n_t.  At q = 1.00 that is EXACTLY idea 78's `weights_ewall`
               (asserted, not assumed): the no-ranking control is a point of the sweep, not a
               separate arm, so the premium is a within-family difference.
               n_t <= E_t always, so this construction never de-grosses -- idea 81's `dg`
               artefact and idea 160's dg/rw distinction cannot enter.
  q grid       0.05 0.10 0.15 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.90 1.00   (12, all printed)
  cost rungs   0 5 10 15 20 25 30 bps, DERIVED EXACTLY from one 0 bps simulation per book by
               net(c) = gross - turnover * c / 1e4 (identity asserted direct-vs-derived first)
  panels       U56, B136 primary (idea 78's); ETF36, BSTK100 secondary; SMALL439 secondary,
               rebuilt HERE with the max_1d_move >= 1.0 screen applied (idea 78's SMALL484
               does not apply it) -- reported separately, never pooled with the large caps.
  sub-panels   k = 20/40/80 x 24 seeded draws from B136 = 72 books, idea 78's construction
  windows      IS <= 2016-12-31 chooses; OOS >= 2017-01-01 read ONCE

  TUNED PARAMETER 1: q       -- 12 grid points, ALL reported; it is the output, not a setting.
  TUNED PARAMETER 2: the cost rung c -- 7 grid points, ALL reported; it is the queue's own axis.
  GROSS = 0.75, the gate, the key, the cadence, the panels and the sub-panel seeds are
  INHERITED from idea 78, not chosen here.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
---------------------------------------------------------------------
  P1  Idea 78's full-panel control ordering re-derives (EWall > CAND20 > CAND5 on B136 at
      10 bps) to within 0.005 of Sharpe.
  P2  The gross (0 bps) premium is POSITIVE and rises as q falls on both primary panels --
      i.e. the selection key does carry information before costs.
  P3  At 10 bps the argmax q is >= 0.80 on both primary panels (the queue's "at or near 1.0").
  P4  The argmax q is non-decreasing in the cost rung on both primary panels.
  P5  The breakeven cost c*(q) is DECREASING in selectivity: the more selective the book, the
      lower the cost at which its edge dies.
  P6  Rule 8: choosing q on the IS window does NOT beat the q = 1.00 do-nothing control on
      mean OOS Sharpe at 10 bps (ideas 132/141/151/160's standing result).

CAVEATS carried, not buried
---------------------------
  * SURVIVORSHIP (idea 54): every panel is a current-constituent list with no delistings.  It
    runs AGAINST the less selective arm -- q = 1.00 holds the whole eligible set including the
    names a delisting-aware panel would kill -- so a survivorship-free panel would move the
    argmax q DOWN, not up.  That is the direction that matters for this run's conclusion and
    it is stated, not adjusted.  No LEVEL here is a tradable estimate.
  * The small panel is secondary throughout: ideas 39/49/136 show the 200d/vol20 gate is
    INVERTED there, so its q curve is not evidence about the large-cap rule.
  * Costs are a flat linear bps charge on turnover; real cost is spread plus impact and is
    convex in size, so a 30 bps rung is not "trading 30 bps wide" (idea 126).
  * The sub-panel draws share a parent (B136) and overlap heavily, so the spread of the argmax
    across draws is a sampling band, not 72 independent experiments.
  * At q = 1.00 the premium is 0 by construction; the sweep is therefore a test of whether ANY
    q < 1 beats holding the eligible set, not a horse race between two free arms.
  * Idea 144 (a re-dialled book is the same book), idea 38's calendar-day index and idea 126's
    t+1-only execution carry over.

Deterministic, standalone.  Writes .console.txt, .grid.csv, .breakeven.csv, .subpanels.csv,
.walkforward.csv, .keep.csv
"""
import importlib.util
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics  # noqa: E402

STEM = "2026-09-06_where-selectivity-and-cost-cross_cloud"
OUT = ROOT / "research" / "backtests"
P78_STEM = "2026-09-05_candidate-count-vs-dispersion_B"
P171_STEM = "2026-09-05_do-gross-choice-rules-lose-to-constants-in-general_C"

QS = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
RUNGS = [0, 5, 10, 15, 20, 25, 30]
BASE_RUNG = 10
GROSS = 0.75
FREQ = "W"
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
PRIMARY = ["U56", "B136"]
SECONDARY = ["ETF36", "BSTK100", "SMALL439"]
SUB_KS = [20, 40, 80]
SUB_DRAWS = 24
SUB_SEED = 155_500
RAND_SEED = 155_900

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 4000)

_lines: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def _load(stem, name):
    spec = importlib.util.spec_from_file_location(name, OUT / f"{stem}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


p78 = _load(P78_STEM, "p78")
p171 = _load(P171_STEM, "p171")
p78.P = P
p171.P = P
# idea 171's vectorised equivalent of engine.backtest, asserted identical on THIS run's own
# weight matrices in Q1 [d] before it is used for anything.
fast_backtest = p171.fast_backtest

eligible_mask = p78.eligible_mask
weights_ewall = p78.weights_ewall
weights_cand = p78.weights_cand
fail_4a, fail_4b = p78.fail_4a, p78.fail_4b
spearman, tstat = p78.spearman, p78.tstat


# ------------------------------------------------------------------- the selectivity book
def rankable(px, tradable):
    """Idea 78's eligibility mask INTERSECTED with "the key can see this name".

    A name can clear the 200d/vol20 gate while its composite is NaN (it has 200 days of
    history but not the 252 the 12-1 momentum leg needs).  Idea 78's `weights_ewall` HOLDS
    those names; no ranked book can.  Comparing a ranked book to that EWall therefore mixes a
    ranking effect with a coverage effect.  Every arm in this run uses the rankable set, so
    q = 1.00 is EWall on exactly the names the key can order, and the premium is pure ranking.
    The size of the difference is measured and printed in Q1, not assumed away.
    """
    elig = eligible_mask(px, tradable)
    key = score(px, vol_scale=False)[0].where(elig)
    return (elig & key.notna()), key


def weights_q(px, tradable, q, gross=GROSS):
    """Top q-share of that week's rankable-eligible set, equal weighted at full gross.

    n_t = max(1, round(q * E_t)) <= E_t, so the book is always fully invested and idea 81's
    de-grossing artefact cannot enter.  At q = 1.00 this is EWall on the rankable set.
    """
    elig, key = rankable(px, tradable)
    rank = key.where(elig).rank(axis=1, ascending=False)
    E = elig.sum(axis=1)
    n_t = np.maximum(1, np.round(q * E)).where(E > 0, 0)
    sel = rank.le(n_t, axis=0) & elig
    cnt = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(cnt, axis=0).mul(gross).fillna(0.0)


def weights_ewall_rankable(px, tradable, gross=GROSS):
    elig, _ = rankable(px, tradable)
    cnt = elig.sum(axis=1).replace(0, np.nan)
    return elig.astype(float).div(cnt, axis=0).mul(gross).fillna(0.0)


def halves(x):
    h = len(x) // 2
    return metrics(x.iloc[:h])["Sharpe"], metrics(x.iloc[h:])["Sharpe"]


class Panel:
    """Eligibility mask and composite rank computed ONCE per panel; weights_q is then a
    cheap slice of them.  `w(q)` is asserted equal to the uncached weights_q in Q1 [c]."""

    def __init__(self, px, tradable):
        self.px = px
        self.elig, key = rankable(px, tradable)
        self.rank = key.where(self.elig).rank(axis=1, ascending=False)
        self.E = self.elig.sum(axis=1)

    def w(self, q, gross=GROSS):
        n_t = np.maximum(1, np.round(q * self.E)).where(self.E > 0, 0)
        sel = self.rank.le(n_t, axis=0) & self.elig
        cnt = sel.sum(axis=1).replace(0, np.nan)
        return sel.astype(float).div(cnt, axis=0).mul(gross).fillna(0.0)


def run_book(pan, q, start):
    """One 0 bps simulation; every rung derived by subtraction."""
    res = fast_backtest(pan.px, pan.w(q), 0.0, FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def rung_rows(g, tn, spy, base_by_rung, panel, q, nm_extra=None):
    out = []
    for cb in RUNGS:
        r = g - tn * cb / 1e4
        r_is, r_oos = r.loc[:IS_END], r.loc[OOS_START:]
        m, mi, mo = metrics(r), metrics(r_is), metrics(r_oos)
        h1, h2 = halves(r)
        row = dict(panel=panel, q=q, cost_bps=cb,
                   CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                   turnover=float(tn.sum() / m["Years"]),
                   IS_Sharpe=mi["Sharpe"],
                   OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                   fail4a=fail_4a(r, base_by_rung[cb]),
                   fail4b=fail_4b(r, spy, r_oos, spy.loc[OOS_START:]))
        if nm_extra:
            row.update(nm_extra)
        out.append(row)
    return out


# ==================================================================================== run
def main():
    t0 = time.time()
    P("=" * 118)
    P("IDEA 155  where-selectivity-and-cost-cross   (cloud, 2026-09-06)")
    P("=" * 118)

    P("\nbuilding idea 78's panels (its own build_panels, imported) ...")
    panels = p78.build_panels()
    # the small panel is rebuilt HERE with the max_1d_move screen idea 78 does not apply
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]
    P(f"  SMALL439: {len([c for c in pxs.columns if c != 'SPY'])} names, dropped "
      f"{len([c for c in pxs.columns if c in bad])} with max_1d_move >= 1.0 -> {len(s_stk)} "
      "tradable (SURVIVORSHIP: current constituents only, no delistings)")
    panels["SMALL439"] = (pxs[s_stk + ["SPY"]].dropna(how="all").ffill(), set(s_stk))
    for nm in PRIMARY + SECONDARY:
        px, tr = panels[nm]
        P(f"  {nm:9s} {px.shape[1]:4d} columns, {len(tr):4d} tradable, "
          f"{px.index[0].date()} -> {px.index[-1].date()}")

    # ------------------------------------------------------------------ Q1 reproduction
    P("\n" + "=" * 118)
    P("Q1  REPRODUCTION, asserted before any new number is read")
    P("=" * 118)

    px, tr = panels["B136"]
    start = px.index[260]
    P("\n  [a] q = 1.00 IS EWall on the rankable set (not merely similar), and the coverage")
    P("      gap against idea 78's own EWall is measured rather than assumed away")
    dw = float((weights_q(px, tr, 1.00) - weights_ewall_rankable(px, tr)).abs().max().max())
    P(f"      max |dw| vs weights_ewall_rankable over the whole B136 matrix = {dw:.3e}")
    _e0 = eligible_mask(px, tr)
    _e1, _ = rankable(px, tr)
    _gap = (_e0.sum(axis=1) - _e1.sum(axis=1))
    P(f"      idea 78's EWall holds eligible-but-UNRANKABLE names on {int((_gap != 0).sum())} "
      f"of {len(_gap)} days (last {_gap[_gap != 0].index.max().date() if (_gap != 0).any() else None}, "
      f"max {int(_gap.max())} names) -- a coverage effect, not a ranking one")
    for _nm, _w in [("idea 78 EWall", weights_ewall(px, tr)),
                    ("EWall rankable", weights_ewall_rankable(px, tr))]:
        _r = fast_backtest(px, _w, 10.0, FREQ)["returns"].loc[start:]
        P(f"      B136 @10bps  {_nm:16s} Sharpe {metrics(_r)['Sharpe']:.4f}")

    P("\n  [b] cost additivity: net(c) == gross - turnover*c/1e4, direct vs derived")
    dmax = 0.0
    for q in (0.10, 1.00):
        w = weights_q(px, tr, q)
        z = backtest(px, w, cost_bps=0.0, freq=FREQ)
        for cb in RUNGS:
            direct = backtest(px, w, cost_bps=float(cb), freq=FREQ)["returns"]
            der = z["returns"] - z["turnover"] * cb / 1e4
            dmax = max(dmax, float((direct - der).abs().max()))
    P(f"      max |direct - derived| over 2 q x 7 rungs = {dmax:.3e}")

    P("\n  [c] idea 171's fast_backtest == engine.backtest, and the cached Panel weights ==")
    P("      the uncached weights_q, on this run's own construction")
    dfb, dwc = 0.0, 0.0
    _pan = Panel(px, tr)
    for q in (0.10, 0.50, 1.00):
        wq = weights_q(px, tr, q)
        dwc = max(dwc, float((_pan.w(q) - wq).abs().max().max()))
        a = fast_backtest(px, wq, 10.0, FREQ)["returns"]
        b = backtest(px, wq, cost_bps=10.0, freq=FREQ)["returns"]
        dfb = max(dfb, float((a - b).abs().max()))
    P(f"      max |dret| fast vs engine = {dfb:.3e};  max |dw| cached vs uncached = {dwc:.3e}")

    P("\n  [d] idea 78's published full-panel control ordering on B136 @10 bps")
    ctl = {}
    for nm, w in [("EWall", weights_ewall(px, tr)),
                  ("CAND20", weights_cand(px, tr, 20)),
                  ("CAND5", weights_cand(px, tr, 5))]:
        r = backtest(px, w, cost_bps=10.0, freq=FREQ)["returns"].loc[start:]
        ctl[nm] = metrics(r)["Sharpe"]
        P(f"      {nm:7s} Sharpe {ctl[nm]:.4f}")
    pub = {"EWall": 1.026, "CAND20": 0.957, "CAND5": 0.880}
    dpub = max(abs(ctl[k] - pub[k]) for k in pub)
    order_ok = ctl["EWall"] > ctl["CAND20"] > ctl["CAND5"]
    P(f"      published 1.026 / 0.957 / 0.880 -> max |d| {dpub:.4f}; "
      f"ordering {'REPRODUCES' if order_ok else 'DOES NOT REPRODUCE'}")
    repro_ok = (dw < 1e-12) and (dmax < 1e-12) and (dfb < 1e-12) and (dwc < 1e-12) \
        and order_ok and (dpub < 0.005)
    P(f"      REPRODUCTION {'PASS' if repro_ok else 'FAIL'}")
    if not repro_ok:
        P("\n*** the parent does not reproduce.  Stopping before any new number is read. ***")
        (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
        return

    # ------------------------------------------------------------------------ the sweep
    P("\n" + "=" * 118)
    P("Q2/Q3  THE SWEEP.  12 q x 7 rungs x 5 panels; every grid point printed.")
    P("=" * 118)
    rows = []
    PAN = {}
    for nm in PRIMARY + SECONDARY:
        px, tr = panels[nm]
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:]
        bres = fast_backtest(px, rules_v1_weights(px), 0.0, FREQ)
        bg, bt = bres["returns"].loc[st:], bres["turnover"].loc[st:]
        base_by_rung = {cb: bg - bt * cb / 1e4 for cb in RUNGS}
        PAN[nm] = Panel(px, tr)
        for q in QS:
            g, tn = run_book(PAN[nm], q, st)
            names = float((PAN[nm].w(q).loc[st:] > 0).sum(axis=1).replace(0, np.nan).mean())
            for r in rung_rows(g, tn, spy, base_by_rung, nm, q):
                r["mean_names"] = names
                rows.append(r)
        P(f"   {nm} done ({time.time() - t0:.0f}s)")
    G = pd.DataFrame(rows)
    # net premium against the q = 1.00 (no-ranking) point of the SAME panel and rung
    ref = G[G.q == 1.00].set_index(["panel", "cost_bps"])["Sharpe"]
    G["premium"] = G.Sharpe - G.set_index(["panel", "cost_bps"]).index.map(ref).to_numpy()
    refc = G[G.q == 1.00].set_index(["panel", "cost_bps"])["CAGR"]
    G["premium_CAGR"] = G.CAGR - G.set_index(["panel", "cost_bps"]).index.map(refc).to_numpy()
    reft = G[G.q == 1.00].set_index(["panel", "cost_bps"])["turnover"]
    G["dturnover"] = G.turnover - G.set_index(["panel", "cost_bps"]).index.map(reft).to_numpy()
    G.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    P("\n  Q2  THE GROSS CURVE (0 bps): does the key carry information before costs?")
    P(f"  {'panel':9s} {'q':>5s} {'Sharpe':>8s} {'premium':>9s} {'CAGR':>8s} "
      f"{'prem CAGR':>10s} {'turnover':>9s} {'d turnover':>11s}")
    for nm in PRIMARY + SECONDARY:
        s = G[(G.panel == nm) & (G.cost_bps == 0)].sort_values("q")
        for _, r in s.iterrows():
            P(f"  {nm:9s} {r.q:5.2f} {r.Sharpe:8.4f} {r.premium:+9.4f} {r.CAGR:8.2%} "
              f"{r.premium_CAGR:+10.2%} {r.turnover:9.2f} {r.dturnover:+11.2f}")
        rho = spearman(s.q, s.premium)
        P(f"  {nm:9s} Spearman(q, gross premium) = {rho:+.3f}  "
          f"(negative = more selective pays more, gross)")
        P("")

    P("\n  Q3  NET PREMIUM (Sharpe vs the q=1.00 no-ranking book on the same panel and rung).")
    for nm in PRIMARY + SECONDARY:
        P(f"\n  --- {nm} " + "-" * 92)
        P("  " + f"{'q':>5s}" + "".join(f"{cb:>10d} bps" for cb in RUNGS))
        for q in QS:
            s = G[(G.panel == nm) & (G.q == q)].set_index("cost_bps")
            P("  " + f"{q:5.2f}" + "".join(f"{s.loc[cb, 'premium']:+14.4f}" for cb in RUNGS))
        P("  " + f"{'argmax':>5s}" + "".join(
            f"{G[(G.panel == nm) & (G.cost_bps == cb)].sort_values('premium').iloc[-1].q:14.2f}"
            for cb in RUNGS))
        P("  " + f"{'best':>5s}" + "".join(
            f"{G[(G.panel == nm) & (G.cost_bps == cb)].premium.max():+14.4f}" for cb in RUNGS))

    P("\n  ARGMAX q BY RUNG (the answer the queue asked for):")
    P(f"  {'panel':9s}" + "".join(f"{cb:>8d}bps" for cb in RUNGS))
    for nm in PRIMARY + SECONDARY:
        P(f"  {nm:9s}" + "".join(
            f"{G[(G.panel == nm) & (G.cost_bps == cb)].sort_values('premium').iloc[-1].q:11.2f}"
            for cb in RUNGS))

    P("\n  BREAKEVEN COST c*(q): the highest rung at which selectivity q still beats q=1.00")
    P("  (linear interpolation between rungs on the premium; '>30' = still positive at 30 bps,")
    P("   '<0' = already negative with zero costs).")
    brows = []
    for nm in PRIMARY + SECONDARY:
        for q in QS:
            if q == 1.00:
                continue
            s = G[(G.panel == nm) & (G.q == q)].sort_values("cost_bps")
            pr = s.premium.to_numpy()
            cb = s.cost_bps.to_numpy(float)
            if pr[0] <= 0:
                star, lab = 0.0, "<0"
            elif pr[-1] > 0:
                star, lab = np.inf, ">30"
            else:
                i = int(np.argmax(pr <= 0))
                x0, x1, y0, y1 = cb[i - 1], cb[i], pr[i - 1], pr[i]
                star = float(x0 + (x1 - x0) * y0 / (y0 - y1))
                lab = f"{star:.1f}"
            brows.append(dict(panel=nm, q=q, gross_premium=float(pr[0]),
                              breakeven_bps=star, label=lab))
    B = pd.DataFrame(brows)
    B.to_csv(OUT / f"{STEM}.breakeven.csv", index=False)
    P(f"  {'panel':9s}" + "".join(f"{q:>8.2f}" for q in QS[:-1]))
    for nm in PRIMARY + SECONDARY:
        s = B[B.panel == nm].set_index("q")
        P(f"  {nm:9s}" + "".join(f"{s.loc[q, 'label']:>8s}" for q in QS[:-1]))
    for nm in PRIMARY + SECONDARY:
        s = B[(B.panel == nm) & np.isfinite(B.breakeven_bps)]
        P(f"  {nm:9s} Spearman(q, breakeven) = {spearman(s.q, s.breakeven_bps):+.3f} "
          f"over {len(s)} finite points  (positive = LESS selective survives MORE cost)")

    # ------------------------------------------------------- Q4 the argmax as a distribution
    P("\n" + "=" * 118)
    P("Q4  IS THE ARGMAX A DRAW OR A RESULT?  72 seeded sub-panels of B136 "
      f"(k = {SUB_KS}, {SUB_DRAWS} draws each).")
    P("=" * 118)
    pxb, trb = panels["B136"]
    pool = sorted(trb)
    stb = pxb.index[260]
    spyb = pxb["SPY"].pct_change().fillna(0.0).loc[stb:]
    srows = []
    for k in SUB_KS:
        rng = np.random.default_rng(SUB_SEED + k)
        for d in range(SUB_DRAWS):
            sub = sorted(rng.choice(pool, size=k, replace=False).tolist())
            pxx = pxb[list(dict.fromkeys(sub + ["SPY"]))].dropna(how="all").ffill()
            trx = set(sub)
            bres = fast_backtest(pxx, rules_v1_weights(pxx), 0.0, FREQ)
            bg, bt = bres["returns"].loc[stb:], bres["turnover"].loc[stb:]
            base_by_rung = {cb: bg - bt * cb / 1e4 for cb in RUNGS}
            spy = spyb.reindex(pxx.loc[stb:].index).fillna(0.0)
            pan = Panel(pxx, trx)
            for q in QS:
                g, tn = run_book(pan, q, stb)
                for r in rung_rows(g, tn, spy, base_by_rung, f"B136k{k}d{d:02d}", q,
                                   dict(k=k, draw=d)):
                    srows.append(r)
        P(f"   k={k} done ({time.time() - t0:.0f}s)")
    S = pd.DataFrame(srows)
    sref = S[S.q == 1.00].set_index(["panel", "cost_bps"])["Sharpe"]
    S["premium"] = S.Sharpe - S.set_index(["panel", "cost_bps"]).index.map(sref).to_numpy()
    S.to_csv(OUT / f"{STEM}.subpanels.csv", index=False)

    P(f"\n  {'rung':>5s} {'mean argmax q':>14s} {'median':>8s} {'sd':>7s} "
      f"{'argmax=1.00':>12s} {'argmax>=0.80':>13s} {'mean best prem':>15s} "
      f"{'draws with any q<1 ahead':>25s}")
    for cb in RUNGS:
        s = S[S.cost_bps == cb]
        am, bp, anyw = [], [], 0
        for bkn, gsub in s.groupby("panel"):
            top = gsub.sort_values("premium").iloc[-1]
            am.append(top.q)
            bp.append(top.premium)
            if float(gsub[gsub.q < 1.0].premium.max()) > 0:
                anyw += 1
        am = np.array(am)
        P(f"  {cb:5d} {am.mean():14.3f} {np.median(am):8.2f} {am.std():7.3f} "
          f"{np.mean(am == 1.0):12.1%} {np.mean(am >= 0.80):13.1%} "
          f"{np.mean(bp):+15.4f} {anyw:20d}/72")

    P(f"\n  By sub-panel size k (mean argmax q):")
    P(f"  {'k':>4s}" + "".join(f"{cb:>8d}bps" for cb in RUNGS))
    for k in SUB_KS:
        vals = []
        for cb in RUNGS:
            s = S[(S.cost_bps == cb) & (S.k == k)]
            vals.append(np.mean([gsub.sort_values("premium").iloc[-1].q
                                 for _, gsub in s.groupby("panel")]))
        P(f"  {k:4d}" + "".join(f"{v:11.3f}" for v in vals))

    P("\n  Mean net premium by q and rung over the 72 sub-panels (all grid points):")
    P("  " + f"{'q':>5s}" + "".join(f"{cb:>10d} bps" for cb in RUNGS))
    for q in QS:
        P("  " + f"{q:5.2f}" + "".join(
            f"{S[(S.q == q) & (S.cost_bps == cb)].premium.mean():+14.4f}" for cb in RUNGS))
    P("  " + f"{'t':>5s}" + "".join(
        f"{tstat(S[(S.q == 0.20) & (S.cost_bps == cb)].premium):+14.2f}" for cb in RUNGS)
      + "   <- t of the q=0.20 row")

    # ------------------------------------------------------------------------- Q5 rule 8
    P("\n" + "=" * 118)
    P("Q5  RULE 8.  q chosen on IS <= 2016-12-31 at each rung; OOS >= 2017-01-01 read ONCE.")
    P("=" * 118)
    rng = np.random.default_rng(RAND_SEED)
    wrows = []
    for cb in RUNGS:
        for scope, names in [("primary", PRIMARY), ("all panels", PRIMARY + SECONDARY),
                             ("sub-panels", sorted(S.panel.unique()))]:
            src = G if scope != "sub-panels" else S
            for arm in ["S1 IS-Sharpe", "S0 q=1.00 (no ranking)", "S2 random q",
                        "S3 ORACLE (OOS argmax)"]:
                oos_s, oos_c, oos_d, picks = [], [], [], []
                for nm in names:
                    s = src[(src.panel == nm) & (src.cost_bps == cb)].set_index("q")
                    if arm == "S1 IS-Sharpe":
                        q = float(s.IS_Sharpe.idxmax())
                    elif arm == "S0 q=1.00 (no ranking)":
                        q = 1.00
                    elif arm == "S2 random q":
                        q = QS[int(rng.integers(len(QS)))]
                    else:
                        q = float(s.OOS_Sharpe.idxmax())
                    picks.append(q)
                    oos_s.append(float(s.loc[q, "OOS_Sharpe"]))
                    oos_c.append(float(s.loc[q, "OOS_CAGR"]))
                    oos_d.append(float(s.loc[q, "OOS_MaxDD"]))
                wrows.append(dict(cost_bps=cb, scope=scope, arm=arm, n=len(names),
                                  OOS_Sharpe=float(np.mean(oos_s)),
                                  OOS_CAGR=float(np.mean(oos_c)),
                                  OOS_MaxDD=float(np.mean(oos_d)),
                                  mean_pick_q=float(np.mean(picks)),
                                  pick_q_1=float(np.mean(np.array(picks) == 1.0))))
    W = pd.DataFrame(wrows)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    for scope in ["primary", "all panels", "sub-panels"]:
        P(f"\n  --- {scope} " + "-" * 90)
        P(f"  {'rung':>5s} {'arm':24s} {'OOS Sharpe':>11s} {'OOS CAGR':>9s} "
          f"{'OOS MaxDD':>10s} {'mean q':>7s} {'q=1 picks':>10s}")
        for cb in RUNGS:
            for arm in ["S3 ORACLE (OOS argmax)", "S0 q=1.00 (no ranking)", "S1 IS-Sharpe",
                        "S2 random q"]:
                r = W[(W.cost_bps == cb) & (W.scope == scope) & (W.arm == arm)].iloc[0]
                P(f"  {cb:5d} {arm:24s} {r.OOS_Sharpe:11.4f} {r.OOS_CAGR:9.2%} "
                  f"{r.OOS_MaxDD:10.2%} {r.mean_pick_q:7.2f} {r.pick_q_1:10.1%}")

    P("\n  Benchmarks (OOS window, same start):")
    P(f"  {'panel':9s} {'series':10s} {'cost':>5s} {'OOS CAGR':>9s} {'OOS Sharpe':>11s} "
      f"{'OOS MaxDD':>10s}")
    for nm in PRIMARY + SECONDARY:
        px, tr = panels[nm]
        st = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[st:].loc[OOS_START:]
        m = metrics(spy)
        P(f"  {nm:9s} {'SPY':10s} {'-':>5s} {m['CAGR']:9.2%} {m['Sharpe']:11.4f} "
          f"{m['MaxDD']:10.2%}")
        br = fast_backtest(px, rules_v1_weights(px), 0.0, FREQ)
        bg = br["returns"].loc[st:].loc[OOS_START:]
        bt = br["turnover"].loc[st:].loc[OOS_START:]
        for cb in (10, 25):
            m = metrics(bg - bt * cb / 1e4)
            P(f"  {nm:9s} {'RULES v1':10s} {cb:5d} {m['CAGR']:9.2%} {m['Sharpe']:11.4f} "
              f"{m['MaxDD']:10.2%}")

    # ------------------------------------------------------------------- Q6 KEEP paths
    P("\n" + "=" * 118)
    P("Q6  BOTH KEEP PATHS on every (panel, q, rung) book")
    P("=" * 118)
    ALL = pd.concat([G.assign(family="panel"), S.assign(family="subpanel")],
                    ignore_index=True)
    krows = []
    for fam in ("panel", "subpanel"):
        for cb in RUNGS:
            s = ALL[(ALL.family == fam) & (ALL.cost_bps == cb)]
            krows.append(dict(family=fam, cost_bps=cb, rows=len(s),
                              pass4a=int((s.fail4a == "-").sum()),
                              pass4b=int((s.fail4b == "-").sum())))
    K = pd.DataFrame(krows)
    K.to_csv(OUT / f"{STEM}.keep.csv", index=False)
    P(f"  {'family':9s} {'cost':>5s} {'rows':>6s} {'4a pass':>8s} {'4b pass':>8s}")
    for _, r in K.iterrows():
        P(f"  {r.family:9s} {int(r.cost_bps):5d} {int(r.rows):6d} {int(r.pass4a):8d} "
          f"{int(r.pass4b):8d}")
    P("\n  4b passes among the 5 named panels, by panel and q (10 bps):")
    s = G[(G.cost_bps == BASE_RUNG) & (G.fail4b == "-")]
    if len(s):
        for _, r in s.sort_values("Sharpe", ascending=False).iterrows():
            P(f"    {r.panel:9s} q={r.q:4.2f}  {r.CAGR:7.2%} / {r.Sharpe:.4f} / "
              f"{r.MaxDD:7.2%}  halves {r.H1:.3f}/{r.H2:.3f}  OOS {r.OOS_Sharpe:.4f}  "
              f"turnover {r.turnover:.1f}x")
    else:
        P("    none")
    P("\n  first-failing-bar census on 4b over all rows:")
    fb = ALL[ALL.fail4b != "-"].fail4b.str.split(",").str[0].value_counts()
    P("    " + ", ".join(f"{k} {v}" for k, v in fb.items()))
    P("\n  small panel (SMALL439) 4b passes at any rung: "
      f"{int((G[(G.panel == 'SMALL439')].fail4b == '-').sum())} of "
      f"{len(G[G.panel == 'SMALL439'])}   (ideas 39/49/136)")

    # --------------------------------------------------------------------- predictions
    P("\n" + "=" * 118)
    P("PRE-REGISTERED PREDICTIONS")
    P("=" * 118)

    def argmax_q(nm, cb, src=G):
        s = src[(src.panel == nm) & (src.cost_bps == cb)]
        return float(s.sort_values("premium").iloc[-1].q)

    gross_rho = {nm: spearman(G[(G.panel == nm) & (G.cost_bps == 0)].q,
                              G[(G.panel == nm) & (G.cost_bps == 0)].premium)
                 for nm in PRIMARY}
    gross_pos = {nm: float(G[(G.panel == nm) & (G.cost_bps == 0) & (G.q < 1)].premium.max())
                 for nm in PRIMARY}
    am10 = {nm: argmax_q(nm, BASE_RUNG) for nm in PRIMARY}
    mono = all(all(argmax_q(nm, RUNGS[i + 1]) >= argmax_q(nm, RUNGS[i])
                   for i in range(len(RUNGS) - 1)) for nm in PRIMARY)
    be_rho = {nm: spearman(B[(B.panel == nm) & np.isfinite(B.breakeven_bps)].q,
                           B[(B.panel == nm) & np.isfinite(B.breakeven_bps)].breakeven_bps)
              for nm in PRIMARY}
    s1 = float(W[(W.cost_bps == BASE_RUNG) & (W.scope == "primary")
                 & (W.arm == "S1 IS-Sharpe")].OOS_Sharpe.iloc[0])
    s0 = float(W[(W.cost_bps == BASE_RUNG) & (W.scope == "primary")
                 & (W.arm == "S0 q=1.00 (no ranking)")].OOS_Sharpe.iloc[0])
    preds = [
        ("P1 idea 78's EWall>CAND20>CAND5 ordering re-derives within 0.005", repro_ok,
         f"max |d| {dpub:.4f}, ordering {order_ok}"),
        ("P2 gross premium positive and rising as q falls, both primary",
         all(gross_pos[nm] > 0 for nm in PRIMARY) and all(gross_rho[nm] < 0 for nm in PRIMARY),
         "best q<1 gross premium " + ", ".join(f"{nm} {gross_pos[nm]:+.4f}" for nm in PRIMARY)
         + "; rho " + ", ".join(f"{nm} {gross_rho[nm]:+.3f}" for nm in PRIMARY)),
        ("P3 argmax q >= 0.80 at 10 bps on both primary panels",
         all(am10[nm] >= 0.80 for nm in PRIMARY),
         ", ".join(f"{nm} {am10[nm]:.2f}" for nm in PRIMARY)),
        ("P4 argmax q non-decreasing in the cost rung, both primary", mono,
         " | ".join(f"{nm} " + "/".join(f"{argmax_q(nm, cb):.2f}" for cb in RUNGS)
                    for nm in PRIMARY)),
        ("P5 breakeven cost decreasing in selectivity (rho(q, c*) > 0)",
         all(np.isfinite(be_rho[nm]) and be_rho[nm] > 0 for nm in PRIMARY),
         ", ".join(f"{nm} {be_rho[nm]:+.3f}" for nm in PRIMARY)),
        ("P6 IS-chosen q does NOT beat q=1.00 on OOS Sharpe at 10 bps", s1 <= s0,
         f"S1 {s1:.4f} vs S0 {s0:.4f}"),
    ]
    hits = 0
    for name, ok, detail in preds:
        hits += int(bool(ok))
        P(f"  [{'HIT ' if ok else 'MISS'}]  {name:<60s}  {detail}")
    P(f"  {hits}/{len(preds)} predictions hit")

    P(f"\nDONE in {time.time() - t0:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
