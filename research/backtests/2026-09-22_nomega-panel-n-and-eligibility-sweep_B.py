#!/usr/bin/env python3
"""Idea 941 (lane B, 2026-09-22): can-any-U56-BOOK-clear-4b-on-the-36-NAME-NOMEGA-PANEL-at-any-n-or-gross.

QUESTION.  Idea 933 removed the `universe.json:megacap` sleeve (the answer-key 2026 top-20 held
from 2009) and found 4b dies on 0 of 12 cells, with the best rule-8 OOS Sharpe reachable on the
36-name remainder at 0.873 against SPY's 0.874.  But 933 swept only 6 fixed book FORMS x 30 gross
rungs: it never moved book SIZE or ELIGIBILITY.  So the record cannot yet say whether the NOMEGA
panel is 4b-EMPTY (a panel fact: no book of this family clears the bar once the mega-caps go) or
merely UNSEARCHED (a search fact: 933 looked in the wrong place).  This run searches it.

DESIGN (protocol rule 4, max 2 TUNED parameters).
  TUNED PARAM 1  n     = book size, 7 rungs {3, 5, 8, 12, 18, 24, ALL}.
  TUNED PARAM 2  band  = the 200d MA eligibility threshold, 5 rungs {0.00, 0.02, 0.03, 0.05, 0.08}.
  Everything else is a STATED CONVENTION read at values already committed in the record, not a
  dial fitted here:
    gross  {0.75, 1.00}  0.75 is the LIVE RULES v2 value; 1.00 is where every committed 4b pass
                         on this family sits (ideas 2119 / 2121 / 2211).  Reported, not chosen.
    freq   {W, M}        W is the live cadence and the headline; M is a robustness rung.  A pass
                         that exists only at M is reported as PARK, never KEEP.
    cost   {0, 10, 25, 50} bps.  10 bps is PROTOCOL rule 2 and binds every verdict here.
  Reporting the extra conventions can only STRENGTHEN an EMPTY verdict (more cells searched, none
  pass) and would WEAKEN a pass, which is then sent to rule 8 before it is called anything.

BOOK FORM.  RULES v2 generalised by size: at each rebalance hold the top-n names (by the record's
own composite in baseline.score) among those INSIDE the 200d +/- band state, at gross/n of NAV
each; if fewer than n are in band, hold those and leave the rest in CASH (de-gross, never
re-spread - the v2 convention).  n = ALL, band = 0.03, gross = 0.75, W reproduces live RULES v2
on its own panel exactly, so the live book is a cell of this grid rather than an outside object.

PANELS.  NOMEGA = U56 minus universe.json:megacap = 36 tradables (933's REST36; SPY is both the
benchmark and a constituent there, exactly as in 933).  FULL = U56, 56 tradables, run as the
CAPABILITY CONTROL: the same grid, same code, same windows.  If FULL yields 4b passes and NOMEGA
yields none, "empty" is a panel fact and not a bug in the sweep.

CONTROLS on NOMEGA.  EW36 (equal-weight all 36, gross 1.00, no band, zero parameters, weekly),
RAND-n (n names drawn at random each rebalance, 10 md5 seeds) and RULES v2 re-run on NOMEGA give
the base rate a fitted cell has to beat.

KEEP paths, both evaluated (protocol rule 4):
  4a  Sharpe > LIVE RULES v2 (on U56, the live book's own panel) in BOTH halves AND MaxDD no worse.
  4b  Sharpe > SPY in BOTH halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's.
RULE 8.  (n, band) chosen on 2009-2016 IS Sharpe alone, inside each (panel, gross, freq, cost)
instance; 2017-2026 read ONCE.

SURVIVORSHIP (rule 9): U56 is a current-constituent list, so every absolute level is optimistic.
The mega-cap removal is the point of the run: it deletes the sleeve whose membership is most
obviously an answer key, so NOMEGA levels are LESS survivorship-inflated than FULL levels, and a
NOMEGA 4b FAIL is therefore a lower bound on the damage.

Deterministic, standalone, offline (committed caches only).  Writes <stem>.grid.csv,
<stem>.controls.csv, <stem>.walkforward.csv, <stem>.legs.csv, <stem>.log.txt.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score, band_state  # noqa: E402
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from engine import backtest, metrics  # noqa: E402

STEM = Path(__file__).with_suffix("")
LOG: list[str] = []
def P(s=""):
    print(s); LOG.append(str(s))

IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS = [3, 5, 8, 12, 18, 24, "ALL"]
BANDS = [0.00, 0.02, 0.03, 0.05, 0.08]
GROSSES = [0.75, 1.00]
FREQS = ["W", "M"]
COSTS = [0.0, 10.0, 25.0, 50.0]


# ---------------------------------------------------------------- books
def topn_band_weights(px, n, band, gross):
    """Top-n by composite among names inside the 200d +/- band; gross/n each; rest to CASH."""
    s, _, _ = score(px, vol_scale=True)
    inb = band_state(px, band)
    elig = s.where(inb)
    k = len(px.columns) if n == "ALL" else int(n)
    rank = elig.rank(axis=1, ascending=False)
    hold = (rank <= k) & inb
    return hold.astype(float) * (gross / k)


def ew_weights(px, gross=1.0):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def rand_weights(px, n, band, gross, seed):
    """Information-free: n names drawn uniformly at random from those in band, redrawn daily
    (the rebalance mask decides when a draw is actually traded)."""
    inb = band_state(px, band)
    rs = np.random.RandomState(int(hashlib.md5(str(seed).encode()).hexdigest()[:8], 16) % (2**31))
    noise = pd.DataFrame(rs.rand(*px.shape), index=px.index, columns=px.columns)
    elig = noise.where(inb)
    rank = elig.rank(axis=1, ascending=False)
    hold = (rank <= n) & inb
    return hold.astype(float) * (gross / n)


# ---------------------------------------------------------------- metrics
def run(px, w, freq):
    """One backtest at ZERO cost; costs are applied afterwards from the turnover series, which
    is cost-independent (the engine's drift/renormalisation never reads cost_bps)."""
    res = backtest(px, w, cost_bps=0.0, freq=freq)
    return res["returns"], res["turnover"]


def at_cost(r0, tno, bps):
    return r0 - tno * bps / 1e4


def win(r, a=None, b=None):
    return r.loc[a:b] if (a or b) else r


def legs(r, spy, start):
    """All 4b legs plus the raw numbers, on FULL / halves / IS / OOS."""
    r, spy = r.loc[start:], spy.loc[start:]
    h = len(r) // 2
    mF, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    sF, s1, s2 = metrics(spy), metrics(spy.iloc[:h]), metrics(spy.iloc[h:])
    rI, rO = r.loc[:IS_END], r.loc[OOS_START:]
    yI, yO = spy.loc[:IS_END], spy.loc[OOS_START:]
    mI, mO, sI, sO = metrics(rI), metrics(rO), metrics(yI), metrics(yO)
    d = dict(
        CAGR=mF["CAGR"], Sharpe=mF["Sharpe"], MaxDD=mF["MaxDD"], H1=m1["Sharpe"], H2=m2["Sharpe"],
        isCAGR=mI["CAGR"], isSharpe=mI["Sharpe"], isMaxDD=mI["MaxDD"],
        oCAGR=mO["CAGR"], oSharpe=mO["Sharpe"], oMaxDD=mO["MaxDD"],
        spyCAGR=sF["CAGR"], spySharpe=sF["Sharpe"], spyMaxDD=sF["MaxDD"], spyH1=s1["Sharpe"],
        spyH2=s2["Sharpe"], spyoCAGR=sO["CAGR"], spyoSharpe=sO["Sharpe"], spyoMaxDD=sO["MaxDD"],
        spyisSharpe=sI["Sharpe"],
    )
    d["L1_H1"] = d["H1"] > d["spyH1"]
    d["L2_H2"] = d["H2"] > d["spyH2"]
    d["L3_OOS"] = d["oSharpe"] > d["spyoSharpe"]
    d["L4_DDfull"] = abs(d["MaxDD"]) <= 0.60 * abs(d["spyMaxDD"])
    d["L5_CAGRfull"] = d["CAGR"] >= 0.70 * d["spyCAGR"]
    d["L4_DDoos"] = abs(d["oMaxDD"]) <= 0.60 * abs(d["spyoMaxDD"])
    d["L5_CAGRoos"] = d["oCAGR"] >= 0.70 * d["spyoCAGR"]
    d["pass4b_FULL"] = d["L1_H1"] and d["L2_H2"] and d["L4_DDfull"] and d["L5_CAGRfull"]
    d["pass4b_OOS"] = d["L3_OOS"] and d["L4_DDoos"] and d["L5_CAGRoos"]
    d["pass4b"] = d["pass4b_FULL"] and d["pass4b_OOS"]
    return d


def add4a(d, base):
    d["L_4a_H1"] = d["H1"] > base["H1"]
    d["L_4a_H2"] = d["H2"] > base["H2"]
    d["L_4a_DD"] = d["MaxDD"] >= base["MaxDD"]      # "no worse" = less negative or equal
    d["pass4a"] = d["L_4a_H1"] and d["L_4a_H2"] and d["L_4a_DD"]
    return d


# ---------------------------------------------------------------- main
def main():
    P("=" * 100)
    P("IDEA 941 / lane B / 2026-09-22 — can ANY U56 book clear 4b on the 36-name NOMEGA panel?")
    P("=" * 100)

    px = load_universe()
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    mega = [t for t in U["megacap"] if t in px.columns]
    nomega_cols = [c for c in px.columns if c not in set(mega)]
    panels = {"NOMEGA": px[nomega_cols].copy(), "FULL": px.copy()}
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0)

    P(f"tape {px.index[0].date()} -> {px.index[-1].date()}, {len(px)} rows; scoring window starts {start.date()}")
    P(f"FULL  panel: {px.shape[1]} tradables (U56)")
    P(f"NOMEGA panel: {panels['NOMEGA'].shape[1]} tradables = U56 minus the {len(mega)}-name megacap sleeve")
    P(f"  removed: {', '.join(mega)}")
    P(f"  kept   : {', '.join(nomega_cols)}")
    P(f"IS window 2009..{IS_END} | OOS window {OOS_START}..{px.index[-1].date()} (read ONCE, rule 8)")
    P("")

    # ---- 4a comparand: LIVE RULES v2 on U56, at every cost x freq -------------------------
    P("-" * 100)
    P("STEP 0 — comparands.  LIVE RULES v2 (band 0.03 / gross 0.75) on its own U56 panel, and SPY.")
    P("-" * 100)
    base_l: dict[tuple, dict] = {}
    for fq in FREQS:
        r0, tn = run(px, rules_v2_weights(px), fq)
        for c in COSTS:
            base_l[(fq, c)] = legs(at_cost(r0, tn, c), spy, start)
    b = base_l[("W", 10.0)]
    P(f"RULES v2 live (W, 10bps): FULL {b['CAGR']:.2%} / {b['Sharpe']:.4f} / {b['MaxDD']:.2%} "
      f"(H1 {b['H1']:.3f} H2 {b['H2']:.3f}) | OOS {b['oCAGR']:.2%} / {b['oSharpe']:.4f} / {b['oMaxDD']:.2%}")
    P(f"SPY                     : FULL {b['spyCAGR']:.2%} / {b['spySharpe']:.4f} / {b['spyMaxDD']:.2%} "
      f"(H1 {b['spyH1']:.3f} H2 {b['spyH2']:.3f}) | OOS {b['spyoCAGR']:.2%} / {b['spyoSharpe']:.4f} / {b['spyoMaxDD']:.2%}")
    P(f"4b bars: FULL DD cap {0.60*abs(b['spyMaxDD']):.2%}, CAGR floor {0.70*b['spyCAGR']:.2%}; "
      f"OOS DD cap {0.60*abs(b['spyoMaxDD']):.2%}, CAGR floor {0.70*b['spyoCAGR']:.2%}")
    P("")

    # ---- the grid -------------------------------------------------------------------------
    P("-" * 100)
    P(f"STEP 1 — THE GRID.  {len(panels)} panels x {len(NS)} n x {len(BANDS)} band x {len(GROSSES)} gross "
      f"x {len(FREQS)} freq x {len(COSTS)} cost = "
      f"{len(panels)*len(NS)*len(BANDS)*len(GROSSES)*len(FREQS)*len(COSTS)} cells.  ALL reported.")
    P("-" * 100)
    rows = []
    for pname, ppx in panels.items():
        for n in NS:
            k = ppx.shape[1] if n == "ALL" else n
            if k > ppx.shape[1]:
                continue
            for band in BANDS:
                for g in GROSSES:
                    w = topn_band_weights(ppx, n, band, g)
                    for fq in FREQS:
                        r0, tn = run(ppx, w, fq)
                        for c in COSTS:
                            d = legs(at_cost(r0, tn, c), spy, start)
                            d = add4a(d, base_l[(fq, c)])
                            d.update(panel=pname, n=str(n), k=k, band=band, gross=g, freq=fq,
                                     cost_bps=c, turnover=float(tn.loc[start:].sum() / (len(tn.loc[start:]) / 252)))
                            rows.append(d)
    grid = pd.DataFrame(rows)
    front = ["panel", "n", "k", "band", "gross", "freq", "cost_bps"]
    grid = grid[front + [c for c in grid.columns if c not in front]]
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    P(f"wrote {Path(str(STEM) + '.grid.csv').name}  ({len(grid)} rows)")
    P("")

    # ---- headline: is NOMEGA 4b-empty? ----------------------------------------------------
    P("-" * 100)
    P("STEP 2 — THE ANSWER.  4b pass counts by panel x cost (all n, band, gross, freq pooled).")
    P("-" * 100)
    P(f"{'panel':<8}{'cost':>6}{'cells':>8}{'4b FULL':>10}{'4b OOS':>9}{'4b BOTH':>10}{'4a':>6}   binding-leg failure counts (4b BOTH)")
    for pname in panels:
        for c in COSTS:
            s = grid[(grid.panel == pname) & (grid.cost_bps == c)]
            fails = {L: int((~s[L]).sum()) for L in
                     ["L1_H1", "L2_H2", "L3_OOS", "L4_DDfull", "L5_CAGRfull", "L4_DDoos", "L5_CAGRoos"]}
            P(f"{pname:<8}{c:>6.0f}{len(s):>8}{int(s.pass4b_FULL.sum()):>10}{int(s.pass4b_OOS.sum()):>9}"
              f"{int(s.pass4b.sum()):>10}{int(s.pass4a.sum()):>6}   " +
              " ".join(f"{k}={v}" for k, v in fails.items()))
    P("")

    P("4b pass counts on NOMEGA by (freq, gross), 10 bps — the cell-level read:")
    for fq in FREQS:
        for g in GROSSES:
            s = grid[(grid.panel == "NOMEGA") & (grid.cost_bps == 10.0) & (grid.freq == fq) & (grid.gross == g)]
            P(f"  freq={fq} gross={g:.2f}: {int(s.pass4b.sum())} of {len(s)} cells pass 4b "
              f"(4b FULL {int(s.pass4b_FULL.sum())}, 4b OOS {int(s.pass4b_OOS.sum())}, 4a {int(s.pass4a.sum())})")
    P("")

    # full n x band table at the binding convention
    for pname in panels:
        P(f"FULL GRID READ — {pname}, W, gross 1.00, 10 bps.  Sharpe / OOS Sharpe / OOS CAGR / OOS MaxDD | 4b legs")
        s = grid[(grid.panel == pname) & (grid.freq == "W") & (grid.gross == 1.00) & (grid.cost_bps == 10.0)]
        P(f"  {'n':>4} {'band':>6} {'Sharpe':>8} {'H1':>7} {'H2':>7} {'oSharpe':>8} {'oCAGR':>8} {'oMaxDD':>8} "
          f"{'4bF':>4} {'4bO':>4} {'4b':>3} {'4a':>3}")
        for _, r in s.sort_values(["k", "band"]).iterrows():
            P(f"  {r['n']:>4} {r['band']:>6.2f} {r['Sharpe']:>8.4f} {r['H1']:>7.3f} {r['H2']:>7.3f} "
              f"{r['oSharpe']:>8.4f} {r['oCAGR']:>8.2%} {r['oMaxDD']:>8.2%} "
              f"{str(bool(r['pass4b_FULL'])):>4.4} {str(bool(r['pass4b_OOS'])):>4.4} "
              f"{str(bool(r['pass4b'])):>3.3} {str(bool(r['pass4a'])):>3.3}")
        P("")

    # ---- how far is NOMEGA from the bar? --------------------------------------------------
    P("-" * 100)
    P("STEP 3 — HOW FAR FROM THE BAR (NOMEGA, 10 bps).  Best cell on each leg, over the WHOLE grid.")
    P("-" * 100)
    s = grid[(grid.panel == "NOMEGA") & (grid.cost_bps == 10.0)]
    f = grid[(grid.panel == "FULL") & (grid.cost_bps == 10.0)]
    for lab, sub in (("NOMEGA", s), ("FULL", f)):
        best_o = sub.loc[sub.oSharpe.idxmax()]
        best_c = sub.loc[sub.oCAGR.idxmax()]
        best_d = sub.loc[sub.oMaxDD.idxmax()]
        P(f"{lab}: max OOS Sharpe {best_o.oSharpe:.4f} at n={best_o['n']} band={best_o.band} g={best_o.gross} "
          f"{best_o.freq} (SPY OOS {best_o.spyoSharpe:.4f}; margin {best_o.oSharpe - best_o.spyoSharpe:+.4f})")
        P(f"{lab}: max OOS CAGR  {best_c.oCAGR:.2%} at n={best_c['n']} band={best_c.band} g={best_c.gross} "
          f"{best_c.freq} (floor {0.70*best_c.spyoCAGR:.2%}; margin {best_c.oCAGR - 0.70*best_c.spyoCAGR:+.2%})")
        P(f"{lab}: best OOS MaxDD {best_d.oMaxDD:.2%} at n={best_d['n']} band={best_d.band} g={best_d.gross} "
          f"{best_d.freq} (cap {-0.60*abs(best_d.spyoMaxDD):.2%})")
    P("")
    P("NOMEGA cells that clear EACH 4b leg on its own, 10 bps (of "
      f"{len(s)}): " + ", ".join(f"{L}={int(s[L].sum())}" for L in
      ["L1_H1", "L2_H2", "L3_OOS", "L4_DDfull", "L5_CAGRfull", "L4_DDoos", "L5_CAGRoos"]))
    P("Same on FULL (of " f"{len(f)}): " + ", ".join(f"{L}={int(f[L].sum())}" for L in
      ["L1_H1", "L2_H2", "L3_OOS", "L4_DDfull", "L5_CAGRfull", "L4_DDoos", "L5_CAGRoos"]))
    P("")

    # ---- controls -------------------------------------------------------------------------
    P("-" * 100)
    P("STEP 4 — CONTROLS on NOMEGA (base rate a fitted cell has to beat).")
    P("-" * 100)
    npx = panels["NOMEGA"]
    ctl = []
    for nm, w in (("EW36 (all 36, g1.00, no band, 0 params)", ew_weights(npx, 1.00)),
                  ("RULESv2 re-run on NOMEGA (b0.03 g0.75)", rules_v2_weights(npx, 0.03, 0.75))):
        r0, tn = run(npx, w, "W")
        d = add4a(legs(at_cost(r0, tn, 10.0), spy, start), base_l[("W", 10.0)])
        d.update(name=nm); ctl.append(d)
    for seed in range(10):
        r0, tn = run(npx, rand_weights(npx, 8, 0.03, 1.00, seed), "W")
        d = add4a(legs(at_cost(r0, tn, 10.0), spy, start), base_l[("W", 10.0)])
        d.update(name=f"RAND8 seed{seed} (b0.03 g1.00)"); ctl.append(d)
    ctlf = pd.DataFrame(ctl)
    ctlf.to_csv(f"{STEM}.controls.csv", index=False)
    for _, r in ctlf.iterrows():
        P(f"  {r['name']:<42} FULL {r.CAGR:>7.2%} / {r.Sharpe:>7.4f} / {r.MaxDD:>7.2%} | "
          f"OOS {r.oCAGR:>7.2%} / {r.oSharpe:>7.4f} / {r.oMaxDD:>7.2%} | 4b {str(bool(r.pass4b)):<5} 4a {str(bool(r.pass4a))}")
    rnd = ctlf[ctlf.name.str.startswith("RAND8")]
    P(f"  RAND8 base rate: 4b {int(rnd.pass4b.sum())} of 10, mean OOS Sharpe {rnd.oSharpe.mean():.4f} "
      f"(sd {rnd.oSharpe.std():.4f}), mean OOS CAGR {rnd.oCAGR.mean():.2%}")
    P("")

    # ---- rule 8 ---------------------------------------------------------------------------
    P("-" * 100)
    P("STEP 5 — RULE 8 WALK-FORWARD.  (n, band) chosen by IS Sharpe on 2009-2016 ONLY, inside each")
    P("(panel, gross, freq, cost) instance; 2017-2026 read ONCE.")
    P("-" * 100)
    wf = []
    for pname in panels:
        for g in GROSSES:
            for fq in FREQS:
                for c in COSTS:
                    sub = grid[(grid.panel == pname) & (grid.gross == g) & (grid.freq == fq) & (grid.cost_bps == c)]
                    pick = sub.loc[sub.isSharpe.idxmax()]
                    bl = base_l[(fq, c)]
                    wf.append(dict(panel=pname, gross=g, freq=fq, cost_bps=c,
                                   pick_n=pick["n"], pick_band=pick["band"], isSharpe=pick["isSharpe"],
                                   oCAGR=pick["oCAGR"], oSharpe=pick["oSharpe"], oMaxDD=pick["oMaxDD"],
                                   base_oCAGR=bl["oCAGR"], base_oSharpe=bl["oSharpe"], base_oMaxDD=bl["oMaxDD"],
                                   spy_oCAGR=pick["spyoCAGR"], spy_oSharpe=pick["spyoSharpe"],
                                   spy_oMaxDD=pick["spyoMaxDD"],
                                   pass4b=bool(pick["pass4b"]), pass4b_OOS=bool(pick["pass4b_OOS"]),
                                   pass4b_FULL=bool(pick["pass4b_FULL"]), pass4a=bool(pick["pass4a"]),
                                   rank_oSharpe_of=int((sub.oSharpe > pick["oSharpe"]).sum() + 1), cells=len(sub)))
    wfd = pd.DataFrame(wf)
    wfd.to_csv(f"{STEM}.walkforward.csv", index=False)
    P(f"{'panel':<8}{'g':>6}{'fq':>4}{'cost':>6}  {'pick':>12}  {'OOS CAGR':>9}{'OOS Shp':>9}{'OOS DD':>9}  "
      f"{'base Shp':>9}{'SPY Shp':>8}  {'4b':>4}{'4a':>4}{'OOSrank':>8}")
    for _, r in wfd.iterrows():
        P(f"{r.panel:<8}{r.gross:>6.2f}{r.freq:>4}{r.cost_bps:>6.0f}  "
          f"{'n'+str(r.pick_n)+'_b'+format(r.pick_band,'.2f'):>12}  "
          f"{r.oCAGR:>9.2%}{r.oSharpe:>9.4f}{r.oMaxDD:>9.2%}  {r.base_oSharpe:>9.4f}{r.spy_oSharpe:>8.4f}  "
          f"{str(r.pass4b):>4.4}{str(r.pass4a):>4.4}{str(r.rank_oSharpe_of)+'/'+str(r.cells):>8}")
    P("")

    # ---- verdict --------------------------------------------------------------------------
    P("=" * 100)
    P("VERDICT")
    P("=" * 100)
    nm = grid[grid.panel == "NOMEGA"]; fl = grid[grid.panel == "FULL"]
    n4b, f4b = int(nm.pass4b.sum()), int(fl.pass4b.sum())
    P(f"NOMEGA: {n4b} of {len(nm)} cells clear 4b (FULL+OOS) at any n, band, gross, cadence or cost rung.")
    P(f"FULL  : {f4b} of {len(fl)} cells clear 4b — the SAME sweep, the SAME code, the SAME windows.")
    wfn = wfd[(wfd.panel == 'NOMEGA')]
    P(f"RULE 8 on NOMEGA: {int(wfn.pass4b.sum())} of {len(wfn)} instances clear 4b out of sample; "
      f"best OOS Sharpe reached by a legal IS-only chooser {wfn.oSharpe.max():.4f} against SPY {wfn.spy_oSharpe.iloc[0]:.4f}.")
    wff = wfd[(wfd.panel == 'FULL')]
    P(f"RULE 8 on FULL  : {int(wff.pass4b.sum())} of {len(wff)} instances clear 4b out of sample; "
      f"best OOS Sharpe {wff.oSharpe.max():.4f}.")
    if n4b == 0:
        P("")
        P("ANSWER: the 36-name NOMEGA panel is 4b-EMPTY, not merely unsearched.  Idea 933's 12 cells")
        P("were not the wrong place to look — the whole (n x band x gross x cadence x cost) grid is empty")
        P("while the identical sweep on U56 is not.  KILL of the hypothesis that 933 under-searched.")
    else:
        P("")
        P("ANSWER: the panel is NOT 4b-empty — 933 under-searched.  Surviving cells are listed above;")
        P("each is sent to rule 8 before it is called anything.")
    P("=" * 100)

    grid[["panel", "n", "band", "gross", "freq", "cost_bps", "L1_H1", "L2_H2", "L3_OOS", "L4_DDfull",
          "L5_CAGRfull", "L4_DDoos", "L5_CAGRoos", "pass4b_FULL", "pass4b_OOS", "pass4b",
          "pass4a"]].to_csv(f"{STEM}.legs.csv", index=False)
    Path(f"{STEM}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
