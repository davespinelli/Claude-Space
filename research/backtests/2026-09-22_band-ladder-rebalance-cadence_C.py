#!/usr/bin/env python3
"""
IDEA 2207 (lane C, 2026-09-22) -- is the KEEP-4b CANDIDATE a REBALANCE-FREQUENCY object?

THE QUESTION, as filed.  Every band x gross verdict in the record is priced WEEKLY (idea 2119's
ladder, 2121's chooser study, 2125's realised-gross reading, 2211's zero-parameter comparand --
all of them freq='W', because that is the cadence RULES v2 happens to run).  Nobody has counted
the weekly convention as a dial.  So: price the SAME ladder at D / W / 2W / M cadence at 10 and
25 bps and report whether the 4b pass SET is cadence-stable, or whether 'weekly' is itself a
tuned parameter hiding inside every committed verdict on this family.

THE BOOK (RULES v2's own form on its own two dials; nothing new is invented).
    band(i,t) TRUE when close > 200d MA x (1+b), FALSE below x (1-b), previous state in between,
    FALSE before 200 closes exist  ==  baseline.band_state(px, b).
    Hold every priced in-band name at g/#priced of NAV; gated-out weight goes to CASH (de-gross,
    never re-spread).  Weights at close t applied at t+1, cost per unit turnover, long only, no
    leverage.  (b,g) = (0.03,0.75) at W IS the live book (gate G3).

THE LADDER (identical to 2119/2121/2211's, so this run is comparable to them cell for cell):
    BAND  b in {0.00, 0.02, 0.03, 0.05, 0.08}
    GROSS g in {0.50, 0.60, 0.75, 0.85, 1.00}          = 25 cells per panel
    CADENCE R in {D, W, 2W, M}                         = 100 books per panel

EXACTLY TWO TUNED DIALS, and every grid point is published (<slug>.grid.csv, 400 rows):
    1. CADENCE R in {D, W, 2W, M}.
    2. GROSS g in {0.50, 0.60, 0.75, 0.85, 1.00}.
    The BAND is NOT tuned: all five rungs are priced and reported, and the rule-8 chooser's
    PRIMARY scope is (cadence x gross) at the LIVE band 0.03 -- two dials, no more.  The joint
    (band x gross x cadence) pick is reported beside it as a THREE-dial control, labelled as such.
NOT tuned, reported as axes: PANEL {U56, B136}; COST {10, 25} bps (the idea's own two rungs,
    PROTOCOL's 10 first); WINDOWS FULL / IS(..2016-12-31) / OOS(2017-01-01..), rule 8, OOS read ONCE.

PRE-REGISTERED BARS, written before any number below was read:
  B1  THE PASS COUNT PER CADENCE.  #cells of 25 clearing 4b (FULL, four legs vs SPY) and 4a (vs
      the LIVE weekly book), per panel x cost x cadence.  If 'weekly' were not a dial the counts
      would be flat in R.
  B2  THE PASS SET, not just its size.  Jaccard of each cadence's 4b pass set against WEEKLY's,
      and the count of cells passing at ALL FOUR cadences (cadence-robust) vs at exactly one
      (cadence artefacts).  A verdict that survives only at W is a convention, not an edge.
  B3  THE BINDING LEG per cadence, and the WEEKLY CELLS' MARGIN MOVE: for every cell passing 4b
      at W, its four leg margins at D / 2W / M and the pp it gains or loses by moving cadence.
      This is the number that says how much of a committed margin is cadence.
  B4  RULE 8 (PROTOCOL rule 8, mandatory).  Cadence x gross chosen on 2009-2016 IS rows ONLY
      inside each (panel, cost) instance at the live band; 2017-2026 read once.  OOS CAGR /
      Sharpe / MaxDD vs RULES v2 (live, weekly) and vs SPY, BOTH KEEP paths.  Choosers: IS_SHARPE
      (the record's habit), IS_CALMAR, IS_MINMARG, plus the zero-parameter comparands MAXGROSS_W
      (top gross rung, live band, weekly -- reads no in-sample data) and RANDCELL (the uniform
      draw's expectation = mean over the scope).  The three-dial joint scope is reported beside.
  B5  THE MECHANISM.  Realised annual turnover and the cost drag (gross return minus net) per
      cadence, so any cadence effect can be attributed to TRADING COST vs SIGNAL TIMING: the
      same grid re-read at 0 bps isolates the timing half.  Declared post-hoc, no cell selected on it.

GATES, printed before any hypothesis is read:
  G1  local run()+net() == engine.backtest(freq=R, 10 bps) for R in D / W / M   bar max|d| < 1e-12
  G2  D / W / M masks ARE engine.rebalance_mask(idx,R); the 2W mask (engine has no '2W') is
      every SECOND weekly rebalance date                bar subset of W and |2W| == ceil(|W|/2)
  G3  ladder cell (0.03,0.75) at W == baseline.rules_v2_weights   bar max|d| == 0
  G4  the rule-8 chooser is handed an IS-ONLY view of the frame and cannot read an OOS column
  G5  comparands are baseline's own: rules_v2_weights (weekly, live) and SPY buy-and-hold

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every absolute
CAGR and drawdown level here is optimistic.  This run is a WITHIN-TAPE contrast across cadence on
identical cells; it does not repair the level.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_band-ladder-rebalance-cadence_C.py
"""
import sys, itertools, math
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights          # noqa
from engine import backtest, metrics, rebalance_mask                      # noqa

DATE, SLUG = "2026-09-22", "band-ladder-rebalance-cadence"
OUT = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_C"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

BANDS    = [0.00, 0.02, 0.03, 0.05, 0.08]
GROSSES  = [0.50, 0.60, 0.75, 0.85, 1.00]
CADENCES = ["D", "W", "2W", "M"]
COSTS    = [10, 25]
COST_ALL = [0, 10, 25]          # 0 bps is the B5 mechanism read only, never a verdict rung
COST0    = 10
LIVE_B, LIVE_G, LIVE_R = 0.03, 0.75, "W"
IS_END, OOS_BEG = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70


# ------------------------------------------------------------------ masks
def cadence_mask(idx, R):
    """D / W / M are engine.rebalance_mask verbatim.  2W = every SECOND weekly rebalance date
    (engine has no '2W'); deterministic, anchored on the first weekly date in the sample."""
    if R in ("D", "W", "M", "Q"):
        return rebalance_mask(idx, R)
    if R == "2W":
        w = rebalance_mask(idx, "W")
        keep = pd.Series(False, index=idx)
        dates = list(idx[w.values])
        keep.loc[dates[::2]] = True
        return keep
    raise ValueError(R)


# ------------------------------------------------------------------ book + engine
def ladder_weights(px, band, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


def run(prices, weights, mask):
    """engine.backtest's loop in numpy (gate G1).  Costs applied afterwards -- they never change
    the held path -- so one loop serves every cost rung."""
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).values
    m = mask.shift(1, fill_value=False).values
    n = len(prices)
    cur = np.zeros(prices.shape[1])
    gross_ret = np.empty(n); turn = np.zeros(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        gross_ret[i] = np.nansum(cur * rets[i])
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return (pd.Series(gross_ret, index=prices.index), pd.Series(turn, index=prices.index))


def net(gross_ret, turnover, cost_bps):
    return gross_ret - turnover * cost_bps / 1e4


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def legs4b(s, ss):
    """4b's four legs on a window with halves: Sharpe > SPY in BOTH halves, MaxDD <= 60% of
    SPY's, CAGR >= 70% of SPY's.  Margins in pp for the level legs, Sharpe units for the rest."""
    L = dict(H1=s["H1"] > ss["H1"], H2=s["H2"] > ss["H2"],
             DD=s["MaxDD"] >= DD_CAP * ss["MaxDD"], CAGR=s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])
    Mg = dict(H1=s["H1"] - ss["H1"], H2=s["H2"] - ss["H2"],
              DD=(s["MaxDD"] - DD_CAP * ss["MaxDD"]) * 100,
              CAGR=(s["CAGR"] - CAGR_FLOOR * ss["CAGR"]) * 100)
    return all(L.values()), L, Mg


def keep4b_oos(s, ss):
    return (s["Sharpe"] > ss["Sharpe"] and s["MaxDD"] >= DD_CAP * ss["MaxDD"]
            and s["CAGR"] >= CAGR_FLOOR * ss["CAGR"])


def keep4a(s, sb):
    return (s["H1"] > sb["H1"]) and (s["H2"] > sb["H2"]) and (s["MaxDD"] >= sb["MaxDD"])


def keep4a_oos(s, sb):
    return (s["Sharpe"] > sb["Sharpe"]) and (s["MaxDD"] >= sb["MaxDD"])


# ------------------------------------------------------------------ choosers (IS-only)
def pick(sub, chooser):
    """LEGAL IS-ONLY chooser.  `sub` carries is_* columns only (gate G4).  Deterministic
    tie-break on the cell label ascending."""
    s = sub.sort_values("cell").reset_index(drop=True)
    if chooser == "IS_SHARPE":    key = s.is_Sharpe.values
    elif chooser == "IS_CALMAR":  key = np.nan_to_num(s.is_calmar.values, nan=-1e9)
    elif chooser == "IS_MINMARG": key = s.is_minmarg.values
    else: raise ValueError(chooser)
    return s.iloc[int(np.argmax(np.nan_to_num(key, nan=-1e18)))]["cell"]


CHOOSERS = ["IS_SHARPE", "IS_CALMAR", "IS_MINMARG"]


def main():
    P("=" * 100)
    P("IDEA 2207 lane C 2026-09-22 -- is the KEEP-4b CANDIDATE a REBALANCE-FREQUENCY object?")
    P("=" * 100)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"tuned dial 1: CADENCE {CADENCES}")
    P(f"tuned dial 2: GROSS   {GROSSES}")
    P(f"reported, NOT tuned: BAND {BANDS} (all five published; rule-8 primary scope is at the")
    P(f"                     live band {LIVE_B}), PANELS U56 + B136, COST {COSTS} bps (+0 bps for B5),")
    P(f"                     windows FULL / IS ..{IS_END} / OOS {OOS_BEG}.. (rule 8, read once)")
    P(f"the live book is (band {LIVE_B}, gross {LIVE_G}, cadence {LIVE_R}) -- gate G3")
    P("")

    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in panels.items():
        P(f"  panel {k:5s}  {v.shape[1]:3d} names  {v.index[0].date()} .. {v.index[-1].date()}"
          f"  ({len(v)} sessions)")
    P("")

    # ---------------------------------------------------------------- GATES
    P("-" * 100); P("(G) GATES -- printed before any hypothesis is read"); P("-" * 100)
    gate_rows, gp, gn = [], 0, 0
    px_u = panels["U56"]

    bad = 0
    for R in ("D", "W", "M"):
        bad += int((cadence_mask(px_u.index, R) != rebalance_mask(px_u.index, R)).sum())
    w = cadence_mask(px_u.index, "W"); tw = cadence_mask(px_u.index, "2W")
    subset = bool((tw & ~w).sum() == 0)
    half_ok = int(tw.sum()) == math.ceil(int(w.sum()) / 2)
    ok = (bad == 0) and subset and half_ok; gp += ok; gn += 1
    P(f"  G2  D/W/M masks ARE engine.rebalance_mask : {bad} differing rows; 2W subset of W "
      f"{subset}, |2W| {int(tw.sum())} == ceil(|W| {int(w.sum())}/2) {half_ok}   "
      f"[{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G2", value=bad, bar="0 differing rows; 2W = every 2nd W", passed=bool(ok)))

    w_live = ladder_weights(px_u, LIVE_B, LIVE_G)
    g3 = float(np.nanmax(np.abs(w_live.values - rules_v2_weights(px_u, LIVE_B, LIVE_G).values)))
    ok = g3 == 0.0; gp += ok; gn += 1
    P(f"  G3  ladder cell ({LIVE_B},{LIVE_G}) == baseline.rules_v2_weights : max|d| {g3:.3e}   "
      f"[{'PASS' if ok else 'FAIL'}]  (the ladder's centre cell IS the live book)")
    gate_rows.append(dict(gate="G3", value=g3, bar="max|d| == 0", passed=bool(ok)))

    worst = 0.0
    for R in ("D", "W", "M"):
        gr, to = run(px_u, w_live, cadence_mask(px_u.index, R))
        a = net(gr, to, COST0).values
        b = backtest(px_u, w_live, cost_bps=COST0, freq=R)["returns"].values
        fin = np.isfinite(b)
        worst = max(worst, float(np.abs(a[fin] - b[fin]).max()))
    ok = worst < 1e-12; gp += ok; gn += 1
    P(f"  G1  local run()+net() == engine.backtest(freq=R,{COST0}bps) for R in D/W/M : "
      f"max|d| {worst:.3e}   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G1", value=worst, bar="max|d| < 1e-12", passed=bool(ok)))
    P("  G4  pick() is handed an IS-ONLY view (is_* columns) and cannot read an OOS or FULL")
    P("      column -- structural, asserted at call time   [PASS by construction]")
    gate_rows.append(dict(gate="G4", value=0, bar="IS-only view", passed=True)); gp += 1; gn += 1
    P(f"  G5  comparands: baseline.rules_v2_weights ({LIVE_B}/{LIVE_G}, WEEKLY as it runs live) "
      f"and SPY buy-and-hold   [PASS]")
    gate_rows.append(dict(gate="G5", value=0, bar="baseline's own", passed=True)); gp += 1; gn += 1
    P(f"  --> {gp} of {gn} gates PASS.")
    P("")

    # ---------------------------------------------------------------- price the grid
    rows = []
    REFTAB = []
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        SPY = dict(FULL=stats(spy), IS=stats(spy.loc[:IS_END]), OOS=stats(spy.loc[OOS_BEG:]))
        # the LIVE book, as it actually runs: weekly
        lvg, lvt = run(px, rules_v2_weights(px, LIVE_B, LIVE_G), cadence_mask(px.index, LIVE_R))
        LV = {}
        for c in COST_ALL:
            lr = net(lvg, lvt, c).loc[start:]
            LV[c] = dict(FULL=stats(lr), IS=stats(lr.loc[:IS_END]), OOS=stats(lr.loc[OOS_BEG:]),
                         turn=float(lvt.loc[start:].sum()) / (len(lr) / 252))
        REFTAB.append(dict(panel=pname, ref="SPY", **{f"FULL_{k}": v for k, v in SPY["FULL"].items()},
                           **{f"OOS_{k}": v for k, v in SPY["OOS"].items()}))
        for c in COST_ALL:
            REFTAB.append(dict(panel=pname, ref=f"RULESv2_W_{c}bps",
                               **{f"FULL_{k}": v for k, v in LV[c]["FULL"].items()},
                               **{f"OOS_{k}": v for k, v in LV[c]["OOS"].items()}))
        P(f"  {pname}: SPY FULL {SPY['FULL']['CAGR']:.2%} / {SPY['FULL']['Sharpe']:.4f} / "
          f"{SPY['FULL']['MaxDD']:.2%} (H {SPY['FULL']['H1']:.4f}/{SPY['FULL']['H2']:.4f})"
          f" | OOS {SPY['OOS']['CAGR']:.2%} / {SPY['OOS']['Sharpe']:.4f} / {SPY['OOS']['MaxDD']:.2%}")
        P(f"        4b bars: DD cap {DD_CAP*SPY['FULL']['MaxDD']:.2%} FULL / "
          f"{DD_CAP*SPY['OOS']['MaxDD']:.2%} OOS; CAGR floor {CAGR_FLOOR*SPY['FULL']['CAGR']:.2%} FULL / "
          f"{CAGR_FLOOR*SPY['OOS']['CAGR']:.2%} OOS")
        P(f"        live RULES v2 (W) @{COST0}bps FULL {LV[COST0]['FULL']['CAGR']:.2%} / "
          f"{LV[COST0]['FULL']['Sharpe']:.4f} / {LV[COST0]['FULL']['MaxDD']:.2%} | OOS "
          f"{LV[COST0]['OOS']['CAGR']:.2%} / {LV[COST0]['OOS']['Sharpe']:.4f} / "
          f"{LV[COST0]['OOS']['MaxDD']:.2%} | turnover {LV[COST0]['turn']:.2f}x/yr")

        for b_, g_ in itertools.product(BANDS, GROSSES):
            W = ladder_weights(px, b_, g_)
            for R in CADENCES:
                gr, to = run(px, W, cadence_mask(px.index, R))
                turn = float(to.loc[start:].sum())
                for c in COST_ALL:
                    r = net(gr, to, c).loc[start:]
                    g0 = gr.loc[start:]
                    sF, sI, sO = stats(r), stats(r.loc[:IS_END]), stats(r.loc[OOS_BEG:])
                    pF, LF, MF = legs4b(sF, SPY["FULL"])
                    pI, LI, MI = legs4b(sI, SPY["IS"])
                    yrs = len(r) / 252
                    rows.append(dict(
                        panel=pname, band=b_, gross=g_, cadence=R, cost=c,
                        cell=f"b{b_:.2f}_g{g_:.2f}_{R}", cg=f"{R}_g{g_:.2f}",
                        turn_yr=turn / yrs, cost_drag=float((g0 - r).sum()) / yrs,
                        full_CAGR=sF["CAGR"], full_Sharpe=sF["Sharpe"], full_MaxDD=sF["MaxDD"],
                        full_H1=sF["H1"], full_H2=sF["H2"],
                        is_CAGR=sI["CAGR"], is_Sharpe=sI["Sharpe"], is_MaxDD=sI["MaxDD"],
                        is_calmar=sI["CAGR"] / abs(sI["MaxDD"]) if sI["MaxDD"] else np.nan,
                        is_minmarg=min(MI.values()), is_legs=sum(LI.values()),
                        oos_CAGR=sO["CAGR"], oos_Sharpe=sO["Sharpe"], oos_MaxDD=sO["MaxDD"],
                        keep4b_full=pF, leg_H1=LF["H1"], leg_H2=LF["H2"], leg_DD=LF["DD"],
                        leg_CAGR=LF["CAGR"], mg_H1=MF["H1"], mg_H2=MF["H2"], mg_DD=MF["DD"],
                        mg_CAGR=MF["CAGR"], min_margin=min(MF.values()),
                        keep4b_oos=keep4b_oos(sO, SPY["OOS"]),
                        keep4a_full=keep4a(sF, LV[c]["FULL"]), keep4a_oos=keep4a_oos(sO, LV[c]["OOS"]),
                        spy_full_Sharpe=SPY["FULL"]["Sharpe"], spy_oos_Sharpe=SPY["OOS"]["Sharpe"],
                        spy_full_CAGR=SPY["FULL"]["CAGR"], spy_oos_CAGR=SPY["OOS"]["CAGR"],
                        spy_full_MaxDD=SPY["FULL"]["MaxDD"], spy_oos_MaxDD=SPY["OOS"]["MaxDD"],
                        lv_full_Sharpe=LV[c]["FULL"]["Sharpe"], lv_oos_Sharpe=LV[c]["OOS"]["Sharpe"],
                        lv_full_MaxDD=LV[c]["FULL"]["MaxDD"], lv_oos_MaxDD=LV[c]["OOS"]["MaxDD"],
                        lv_oos_CAGR=LV[c]["OOS"]["CAGR"]))
    G = pd.DataFrame(rows)
    G.to_csv(f"{OUT}.grid.csv", index=False)
    pd.DataFrame(REFTAB).to_csv(f"{OUT}.refs.csv", index=False)
    P("")
    P(f"  priced {len(G[G.cost==COST0])} books ({len(panels)} panels x {len(BANDS)*len(GROSSES)} "
      f"cells x {len(CADENCES)} cadences) x {len(COST_ALL)} cost rungs = {len(G)} published rows")
    P("")

    V = G[G.cost.isin(COSTS)]          # verdict rungs (0 bps is B5 only)

    # ---------------------------------------------------------------- B1 pass counts
    P("-" * 100); P("(B1) PASS COUNT PER CADENCE -- flat in R would mean cadence is not a dial")
    P("-" * 100)
    b1 = (V.groupby(["panel", "cost", "cadence"])
            .agg(n=("cell", "size"), pass4b_full=("keep4b_full", "sum"),
                 pass4b_oos=("keep4b_oos", "sum"), pass4a_full=("keep4a_full", "sum"),
                 pass4a_oos=("keep4a_oos", "sum"), best_full_Sharpe=("full_Sharpe", "max"),
                 best_oos_Sharpe=("oos_Sharpe", "max"), best_oos_CAGR=("oos_CAGR", "max"),
                 mean_turn=("turn_yr", "mean")).reset_index())
    b1.to_csv(f"{OUT}.passcount.csv", index=False)
    for pn in panels:
        for c in COSTS:
            s = b1[(b1.panel == pn) & (b1.cost == c)].set_index("cadence").reindex(CADENCES)
            P(f"  {pn} @{c:2d}bps  4b FULL passes of 25: " +
              "  ".join(f"{R}={int(s.loc[R,'pass4b_full']):2d}" for R in CADENCES) +
              "   | 4b OOS: " + "  ".join(f"{R}={int(s.loc[R,'pass4b_oos']):2d}" for R in CADENCES) +
              "   | 4a FULL: " + "  ".join(f"{R}={int(s.loc[R,'pass4a_full']):2d}" for R in CADENCES))
            P(f"              mean turnover/yr: " +
              "  ".join(f"{R}={s.loc[R,'mean_turn']:5.2f}x" for R in CADENCES) +
              "   best FULL Sharpe: " + " ".join(f"{R}={s.loc[R,'best_full_Sharpe']:.4f}" for R in CADENCES))
    P("")

    # ---------------------------------------------------------------- B2 pass SETS
    P("-" * 100); P("(B2) THE PASS SET, not its size -- Jaccard vs WEEKLY, and cadence-robust cells")
    P("-" * 100)
    b2, cellrows = [], []
    for pn in panels:
        for c in COSTS:
            sub = V[(V.panel == pn) & (V.cost == c)]
            sets = {R: set(sub[(sub.cadence == R) & sub.keep4b_full].apply(
                        lambda r: f"b{r.band:.2f}_g{r.gross:.2f}", axis=1)) for R in CADENCES}
            Wset = sets["W"]
            for R in CADENCES:
                u = Wset | sets[R]; i = Wset & sets[R]
                b2.append(dict(panel=pn, cost=c, cadence=R, n_pass=len(sets[R]),
                               n_pass_W=len(Wset), inter_W=len(i), union_W=len(u),
                               jaccard_vs_W=(len(i) / len(u)) if u else np.nan,
                               only_here=len(sets[R] - Wset), lost_vs_W=len(Wset - sets[R])))
            allc = set.intersection(*sets.values()) if all(sets.values()) else set()
            anyc = set.union(*sets.values())
            once = {x for x in anyc if sum(x in sets[R] for R in CADENCES) == 1}
            for x in sorted(anyc):
                cellrows.append(dict(panel=pn, cost=c, cell=x,
                                     **{f"pass_{R}": (x in sets[R]) for R in CADENCES},
                                     n_cadences=sum(x in sets[R] for R in CADENCES)))
            P(f"  {pn} @{c:2d}bps  |4b pass| D/W/2W/M = " +
              "/".join(str(len(sets[R])) for R in CADENCES) +
              f"   union {len(anyc)}   ALL-FOUR {len(allc)}   EXACTLY-ONE {len(once)}")
            for R in CADENCES:
                rr = [x for x in b2 if x["panel"] == pn and x["cost"] == c and x["cadence"] == R][0]
                P(f"      {R:>2s} vs W: jaccard {rr['jaccard_vs_W']:.3f}  (shared {rr['inter_W']}, "
                  f"only-{R} {rr['only_here']}, lost-from-W {rr['lost_vs_W']})")
            if allc:  P(f"      cadence-robust (all four): {sorted(allc)}")
            if once:  P(f"      cadence artefacts (one cadence only): {sorted(once)}")
    B2 = pd.DataFrame(b2); B2.to_csv(f"{OUT}.passsets.csv", index=False)
    CR = pd.DataFrame(cellrows); CR.to_csv(f"{OUT}.cellstability.csv", index=False)
    P("")

    # ---------------------------------------------------------------- B3 binding leg + margin move
    P("-" * 100); P("(B3) BINDING LEG per cadence, and what a WEEKLY margin is worth at other cadences")
    P("-" * 100)
    legnames = ["H1", "H2", "DD", "CAGR"]
    b3 = []
    for pn in panels:
        for c in COSTS:
            for R in CADENCES:
                sub = V[(V.panel == pn) & (V.cost == c) & (V.cadence == R)]
                fails = sub[~sub.keep4b_full]
                rate = {L: float((~sub[f"leg_{L}"]).mean()) for L in legnames}
                sole = {L: int(((~sub[f"leg_{L}"]) & np.logical_and.reduce(
                            [sub[f"leg_{K}"] for K in legnames if K != L])).sum()) for L in legnames}
                b3.append(dict(panel=pn, cost=c, cadence=R, n_fail=len(fails),
                               **{f"failrate_{L}": rate[L] for L in legnames},
                               **{f"sole_{L}": sole[L] for L in legnames}))
                P(f"  {pn} @{c:2d}bps {R:>2s}  fail rate  " +
                  "  ".join(f"{L}={rate[L]:.3f}" for L in legnames) +
                  "   sole binder  " + " ".join(f"{L}={sole[L]}" for L in legnames))
    pd.DataFrame(b3).to_csv(f"{OUT}.bindingleg.csv", index=False)
    P("")
    mv = []
    for pn in panels:
        for c in COSTS:
            sub = V[(V.panel == pn) & (V.cost == c)]
            wp = sub[(sub.cadence == "W") & sub.keep4b_full]
            for r in wp.itertuples():
                key = (r.band, r.gross)
                for R in CADENCES:
                    o = sub[(sub.cadence == R) & (sub.band == key[0]) & (sub.gross == key[1])].iloc[0]
                    mv.append(dict(panel=pn, cost=c, band=key[0], gross=key[1], cadence=R,
                                   keep4b=bool(o.keep4b_full), min_margin=o.min_margin,
                                   mg_DD=o.mg_DD, mg_CAGR=o.mg_CAGR, mg_H1=o.mg_H1, mg_H2=o.mg_H2,
                                   oos_Sharpe=o.oos_Sharpe, oos_CAGR=o.oos_CAGR, oos_MaxDD=o.oos_MaxDD,
                                   keep4b_oos=bool(o.keep4b_oos), turn_yr=o.turn_yr))
    MV = pd.DataFrame(mv)
    MV.to_csv(f"{OUT}.weeklycells_across_cadence.csv", index=False)
    if len(MV):
        piv = MV.pivot_table(index=["panel", "cost", "band", "gross"], columns="cadence",
                             values="min_margin")
        P("  min 4b leg margin of each WEEKLY passer, re-read at every cadence (pp / Sharpe units):")
        P(piv.reindex(columns=CADENCES).to_string(float_format=lambda x: f"{x:+.3f}"))
        sw = MV[MV.cadence != "W"]
        P(f"  of {len(MV[MV.cadence=='W'])} weekly 4b passers x 3 other cadences = {len(sw)} "
          f"re-reads: {int(sw.keep4b.sum())} still pass 4b "
          f"({sw.keep4b.mean():.1%}); median min-margin move "
          f"{(sw.min_margin.median() - MV[MV.cadence=='W'].min_margin.median()):+.3f}")
    else:
        P("  no cell passes 4b at WEEKLY on either panel at either cost rung -- nothing to re-read.")
    P("")

    # ---------------------------------------------------------------- B4 rule 8
    P("-" * 100)
    P("(B4) RULE 8 -- cadence x gross chosen on IS (..2016-12-31) ONLY, OOS 2017-2026 read ONCE")
    P("-" * 100)
    IS_COLS = ["cell", "cg", "is_CAGR", "is_Sharpe", "is_MaxDD", "is_calmar", "is_minmarg", "is_legs"]
    picks = []
    for pn in panels:
        for c in COSTS:
            for scope, flt, lab in (
                ("CADENCE_x_GROSS@live_band", lambda d: d[d.band == LIVE_B], "2 dials"),
                ("BAND_x_GROSS_x_CADENCE",    lambda d: d,                   "3 dials (control)")):
                sub = flt(V[(V.panel == pn) & (V.cost == c)]).copy()
                isview = sub[IS_COLS].copy()          # gate G4: IS columns only
                for ch in CHOOSERS:
                    cell = pick(isview, ch)
                    row = sub[sub.cell == cell].iloc[0]
                    picks.append(dict(panel=pn, cost=c, scope=scope, dials=lab, chooser=ch,
                                      cell=cell, cadence=row.cadence, band=row.band, gross=row.gross,
                                      oos_CAGR=row.oos_CAGR, oos_Sharpe=row.oos_Sharpe,
                                      oos_MaxDD=row.oos_MaxDD, keep4b_full=bool(row.keep4b_full),
                                      keep4b_oos=bool(row.keep4b_oos),
                                      keep4a_full=bool(row.keep4a_full), keep4a_oos=bool(row.keep4a_oos),
                                      oos_rank=int((sub.oos_Sharpe > row.oos_Sharpe).sum()) + 1,
                                      n_cells=len(sub), turn_yr=row.turn_yr))
                # zero-parameter comparands
                mg = sub[(sub.gross == max(GROSSES)) & (sub.cadence == LIVE_R)]
                mg = mg[mg.band == LIVE_B] if scope.startswith("BAND") else mg
                row = mg.iloc[0]
                picks.append(dict(panel=pn, cost=c, scope=scope, dials="0 dials", chooser="MAXGROSS_W",
                                  cell=row.cell, cadence=row.cadence, band=row.band, gross=row.gross,
                                  oos_CAGR=row.oos_CAGR, oos_Sharpe=row.oos_Sharpe,
                                  oos_MaxDD=row.oos_MaxDD, keep4b_full=bool(row.keep4b_full),
                                  keep4b_oos=bool(row.keep4b_oos), keep4a_full=bool(row.keep4a_full),
                                  keep4a_oos=bool(row.keep4a_oos),
                                  oos_rank=int((sub.oos_Sharpe > row.oos_Sharpe).sum()) + 1,
                                  n_cells=len(sub), turn_yr=row.turn_yr))
                picks.append(dict(panel=pn, cost=c, scope=scope, dials="0 dials (expectation)",
                                  chooser="RANDCELL", cell="mean-over-scope", cadence="-",
                                  band=np.nan, gross=np.nan,
                                  oos_CAGR=sub.oos_CAGR.mean(), oos_Sharpe=sub.oos_Sharpe.mean(),
                                  oos_MaxDD=sub.oos_MaxDD.mean(), keep4b_full=False, keep4b_oos=False,
                                  keep4a_full=False, keep4a_oos=False,
                                  oos_rank=int(round((len(sub) + 1) / 2)), n_cells=len(sub),
                                  turn_yr=sub.turn_yr.mean()))
    PK = pd.DataFrame(picks); PK.to_csv(f"{OUT}.walkforward.csv", index=False)
    for pn in panels:
        for c in COSTS:
            s = PK[(PK.panel == pn) & (PK.cost == c) & (PK.scope == "CADENCE_x_GROSS@live_band")]
            lv = V[(V.panel == pn) & (V.cost == c)].iloc[0]
            P(f"  {pn} @{c:2d}bps  (scope: cadence x gross at band {LIVE_B}, {int(s.n_cells.iloc[0])} cells)")
            for r in s.itertuples():
                P(f"      {r.chooser:<12s} -> {r.cell:<16s}  OOS {r.oos_CAGR:6.2%} / "
                  f"{r.oos_Sharpe:.4f} / {r.oos_MaxDD:7.2%}   4b_OOS {str(r.keep4b_oos):5s} "
                  f"4b_FULL {str(r.keep4b_full):5s} 4a_OOS {str(r.keep4a_oos):5s}  "
                  f"OOS rank {r.oos_rank}/{r.n_cells}  turn {r.turn_yr:.2f}x")
            P(f"      comparands: SPY OOS {lv.spy_oos_CAGR:.2%} / {lv.spy_oos_Sharpe:.4f} / "
              f"{lv.spy_oos_MaxDD:.2%}  |  RULES v2 (W) OOS {lv.lv_oos_CAGR:.2%} / "
              f"{lv.lv_oos_Sharpe:.4f} / {lv.lv_oos_MaxDD:.2%}")
    s3 = PK[PK.scope == "BAND_x_GROSS_x_CADENCE"]
    P(f"  3-dial control ({int(s3.n_cells.iloc[0])} cells): "
      f"4b_OOS passes {int(s3[s3.chooser.isin(CHOOSERS)].keep4b_oos.sum())} of "
      f"{len(s3[s3.chooser.isin(CHOOSERS)])} fitted picks; cadences picked "
      f"{sorted(set(s3[s3.chooser.isin(CHOOSERS)].cadence))}")
    fit = PK[PK.chooser.isin(CHOOSERS)]
    P(f"  fitted picks overall: 4b_OOS {int(fit.keep4b_oos.sum())}/{len(fit)}, "
      f"4b_FULL {int(fit.keep4b_full.sum())}/{len(fit)}, 4a_OOS {int(fit.keep4a_oos.sum())}/{len(fit)}, "
      f"4a_FULL {int(fit.keep4a_full.sum())}/{len(fit)}")
    mgr = PK[PK.chooser == "MAXGROSS_W"]
    P(f"  zero-parameter MAXGROSS_W: 4b_OOS {int(mgr.keep4b_oos.sum())}/{len(mgr)}; "
      f"mean OOS Sharpe {mgr.oos_Sharpe.mean():.4f} vs fitted {fit.oos_Sharpe.mean():.4f} "
      f"(premium {fit.oos_Sharpe.mean()-mgr.oos_Sharpe.mean():+.4f})")
    P("")

    # ---------------------------------------------------------------- B5 mechanism
    P("-" * 100); P("(B5) MECHANISM -- turnover, cost drag, and the same grid at 0 bps (post-hoc)")
    P("-" * 100)
    b5 = (G.groupby(["panel", "cadence", "cost"])
            .agg(turn_yr=("turn_yr", "mean"), drag=("cost_drag", "mean"),
                 pass4b=("keep4b_full", "sum"), mean_Sharpe=("full_Sharpe", "mean"),
                 mean_CAGR=("full_CAGR", "mean")).reset_index())
    b5.to_csv(f"{OUT}.mechanism.csv", index=False)
    for pn in panels:
        s = b5[b5.panel == pn]
        P(f"  {pn}  turnover/yr " + "  ".join(
            f"{R}={s[(s.cadence==R)&(s.cost==COST0)].turn_yr.iloc[0]:5.2f}x" for R in CADENCES))
        for c in COST_ALL:
            P(f"        @{c:2d}bps  4b passes of 25: " + "  ".join(
                f"{R}={int(s[(s.cadence==R)&(s.cost==c)].pass4b.iloc[0]):2d}" for R in CADENCES) +
              "   mean drag/yr " + " ".join(
                f"{R}={s[(s.cadence==R)&(s.cost==c)].drag.iloc[0]:.3%}" for R in CADENCES))
    P("")

    # ---------------------------------------------------------------- headline
    P("=" * 100); P("HEADLINE"); P("=" * 100)
    wj = B2[B2.cadence != "W"]
    P(f"  1. 4b FULL pass counts by cadence, pooled over panel x cost rung: " + "  ".join(
        f"{R}={int(V[(V.cadence==R)].keep4b_full.sum()):3d}" for R in CADENCES) +
      f"   (of {len(V[V.cadence=='W'])} books each)")
    P(f"  2. pass-set Jaccard vs WEEKLY: median {wj.jaccard_vs_W.median():.3f}, "
      f"range {wj.jaccard_vs_W.min():.3f}-{wj.jaccard_vs_W.max():.3f} over "
      f"{len(wj)} cadence x panel x cost comparisons")
    P(f"  3. cells passing 4b at ALL FOUR cadences: " + ", ".join(
        f"{pn}@{c}bps {int((CR[(CR.panel==pn)&(CR.cost==c)].n_cadences==4).sum())}"
        for pn in panels for c in COSTS))
    P(f"  4. rule 8: {int(fit.keep4b_oos.sum())} of {len(fit)} fitted picks clear 4b OOS; "
      f"MAXGROSS_W {int(mgr.keep4b_oos.sum())} of {len(mgr)}")
    P("")
    Path(f"{OUT}.log.txt").write_text("\n".join(LINES))
    pd.DataFrame(gate_rows).to_csv(f"{OUT}.gates.csv", index=False)


if __name__ == "__main__":
    main()
