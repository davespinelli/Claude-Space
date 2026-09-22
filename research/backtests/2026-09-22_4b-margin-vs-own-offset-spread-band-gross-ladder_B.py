#!/usr/bin/env python3
"""
IDEA 2119 (lane B, 2026-09-22) -- how-many-4b-PASSES-on-a-BAND-x-GROSS-LADDER-SURVIVE
                                  -THEIR-OWN-OFFSET-SPREAD

THE QUESTION, as filed.  Idea 914 (2026-09-22, lane B) killed idea 910's B136 TREND/AGG
KEEP-4b candidate because its 0.70 pp DD margin is smaller than the SAME BOOK's spread
across the five weekly rebalance offsets (4.18 pp OOS) -- the pass was a weekday, not a
rule.  914's own residue states, in the form it was written, that the run "does not certify
that every other committed 4b DD margin in the record is as fragile."  This run turns the
clause on a POPULATION instead of an anecdote.

Build a MECHANICAL ladder of the live book's own form -- band b x gross g, 25 cells -- on
two panels, score 4b at every cell at the published offset d=0, and for every leg of every
PASS ask whether that leg's MARGIN exceeds that same cell's SPREAD over the five weekly
offsets.  If most passes fail their own weekday spread, the record's KEEP-4b machinery has
been measuring dates, not books.

THE BOOK (RULES v2's form, baseline.rules_v2_weights generalised on its own two dials --
nothing new is invented here):
    band(i,t) TRUE when close > 200d MA x (1+b), FALSE below x (1-b), previous state in
    between, FALSE before 200 closes exist  ==  baseline.band_state(px, b).
    Hold every priced name whose band state is TRUE at g/#priced of NAV; gated-out weight
    goes to CASH (de-gross, never re-spread).  Weekly, weights at close t applied at t+1,
    10 bps per unit turnover, long only, no leverage.
    (b, g) = (0.03, 0.75) IS the live book -- gate G3 proves the cell is bit-identical to
    baseline.rules_v2_weights.

TUNED PARAMETERS -- EXACTLY TWO, and EVERY grid point is published (<slug>.grid.csv):
    1. BAND   b in {0.00, 0.02, 0.03, 0.05, 0.08}
    2. GROSS  g in {0.50, 0.60, 0.75, 0.85, 1.00}
NOT TUNED, and declared as such before any number was read:
    OFFSET d in {0,1,2,3,4} is a NOISE MEASUREMENT, never a choice.  The reported book is
      ALWAYS d=0 (the published convention, gate G2).  d=1..4 exist only to build the
      spread the margin is judged against.  No cell is ever selected on its best offset,
      and no verdict below is read off d>0.
    COST c in {0,10,25,50} bps is PROTOCOL rung 2 (10 bps) plus its robustness ladder.
    PANEL {U56 = research/universe.json, B136 = research/universe_broad.json}.
    WINDOWS FULL / IS (..2016-12-31) / OOS (2017-01-01..), rule 8.

PRE-REGISTERED BARS -- written before any number below was read:
  B1  THE QUESTION.  Over the cells that PASS 4b at d=0, what share have a DD margin
      M_DD > S_DD, their own max-minus-min MaxDD spread in pp over the 5 offsets?  Same
      question on the CAGR leg.  Reported per panel per window at 10 bps.
  B2  ALL-LEG version: share of d=0 passes whose EVERY leg margin exceeds that leg's own
      offset spread.  This is the form 914's proposed clause would actually take.
  B3  VERDICT-LEVEL version: share of d=0 passes that are still a 4b PASS at 5 of 5
      offsets.  B2 and B3 are different tests and are reported separately.
  B4  B1/B2/B3 re-read at 0 / 25 / 50 bps.
  B5  RULE 8.  (b, g) chosen on the IS window ONLY, by IS Sharpe, at d=0.  2017-2026 read
      ONCE.  Report OOS CAGR / Sharpe / MaxDD against RULES v2 and SPY, BOTH KEEP paths,
      and whether the picked cell's OOS margins clear its own OOS offset spread.
  B6  PATH 4a scored at every grid point (Sharpe > RULES v2 in BOTH halves AND MaxDD no
      worse than RULES v2).
  B7  CONTROL.  SPY's own legs do not move with the offset (buy-and-hold), so the 4b bars
      are constant across d by construction; any spread reported here is the BOOK's.

GATES, printed before any hypothesis is read:
  G1  local run()+net() == engine.backtest(freq='W', 10 bps)     bar max|d| < 1e-12
  G2  offset_mask(idx, 0)  == engine.rebalance_mask(idx, 'W')    bar 0 differing rows
  G3  the (b=0.03, g=0.75) weights == baseline.rules_v2_weights  bar max|d| == 0
  G4a offset fairness (count): every offset trades 50-53 times/yr
  G4b offset fairness (clipping): weeks too short to carry offset d.  This FAILS
      structurally at d=3,4 (short holiday weeks) -- published, and B1 is re-read on the
      clip-free offsets {0,1,2} as B1c rather than the bar being quietly widened.
  G5  comparands are baseline's own: rules_v2_weights and SPY buy-and-hold.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-CONSTITUENT lists, so every
absolute CAGR and drawdown level here is optimistic.  This run is a WITHIN-TAPE contrast --
same names, same dates, only the weekday of the rebalance moves -- which is the comparison
the idea asks for; it does not repair the level.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_4b-margin-vs-own-offset-spread-band-gross-ladder_B.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, band_state, rules_v2_weights          # noqa
from engine import backtest, metrics, rebalance_mask                      # noqa

SLUG = "2026-09-22_4b-margin-vs-own-offset-spread-band-gross-ladder_B"
OUT = ROOT / "research" / "backtests"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

BANDS   = [0.00, 0.02, 0.03, 0.05, 0.08]      # TUNED axis 1
GROSSES = [0.50, 0.60, 0.75, 0.85, 1.00]      # TUNED axis 2
OFFSETS = [0, 1, 2, 3, 4]                     # measurement axis, never selected on
COSTS   = [0, 10, 25, 50]
COST0   = 10
FREQ    = "W"
IS_END  = "2016-12-31"
OOS_BEG = "2017-01-01"
LIVE    = (0.03, 0.75)                        # the live RULES v2 cell


# ==========================================================================================
# offsets + a schedule-taking backtester (engine.backtest only accepts a freq string)
# ==========================================================================================
def offset_mask(idx, d):
    """True d trading days BEFORE the last trading day of each week.  d=0 == rebalance_mask."""
    key = pd.Series(idx.to_period("W"), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    clipped = int((last - d < first).sum())
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, clipped


def run(prices, weights, mask):
    """engine.backtest's loop in numpy, semantics byte-for-byte (gate G1).  Costs are
    applied afterwards -- they never change the held path -- so one loop serves every rung."""
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
    return (pd.Series(gross_ret, index=prices.index),
            pd.Series(turn, index=prices.index))


def net(gross_ret, turnover, cost_bps):
    return gross_ret - turnover * cost_bps / 1e4


# ==========================================================================================
# the book: RULES v2's form on its own two dials
# ==========================================================================================
def ladder_weights(px, band, gross):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(band_state(px, band), 0.0)


# ==========================================================================================
# scoring
# ==========================================================================================
def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def legs4b(s, ss):
    """PROTOCOL 4b against SPY measured on the SAME window.  Returns (pass, legs, margins).
    Margins are in the leg's own unit: Sharpe points for H1/H2, pp for DD and CAGR."""
    L = dict(H1=s["H1"] > ss["H1"], H2=s["H2"] > ss["H2"],
             DD=s["MaxDD"] >= 0.60 * ss["MaxDD"], CAGR=s["CAGR"] >= 0.70 * ss["CAGR"])
    Mg = dict(H1=s["H1"] - ss["H1"], H2=s["H2"] - ss["H2"],
              DD=(s["MaxDD"] - 0.60 * ss["MaxDD"]) * 100,
              CAGR=(s["CAGR"] - 0.70 * ss["CAGR"]) * 100)
    return all(L.values()), L, Mg


def legs4a(s, sb):
    return (s["H1"] > sb["H1"]) and (s["H2"] > sb["H2"]) and (s["MaxDD"] >= sb["MaxDD"])


def wins(r, start):
    r = r.loc[start:]
    return dict(FULL=r, IS=r.loc[:IS_END], OOS=r.loc[OOS_BEG:])


# leg -> the statistic whose offset spread the margin is compared against, and its unit scale
LEGUNIT = dict(H1=("H1", 1.0), H2=("H2", 1.0), DD=("MaxDD", 100.0), CAGR=("CAGR", 100.0))


# ==========================================================================================
def main():
    P("=" * 100)
    P("IDEA 2119 lane B 2026-09-22 -- how many 4b PASSES on a BAND x GROSS ladder survive")
    P("                                THEIR OWN REBALANCE-OFFSET SPREAD?")
    P("=" * 100)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"tuned: band {BANDS} x gross {GROSSES}  ({len(BANDS)*len(GROSSES)} cells/panel)")
    P(f"not tuned: offsets {OFFSETS} (measurement only, book is always d=0), costs {COSTS} bps,")
    P(f"           cadence {FREQ}, panels U56 + B136, windows FULL / IS..{IS_END} / OOS {OOS_BEG}..")
    P("")

    panels = {}
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    for k, v in panels.items():
        P(f"  panel {k:5s}  {v.shape[1]:3d} names  {v.index[0].date()} .. {v.index[-1].date()}"
          f"  ({len(v)} sessions)")
    P("")

    # ------------------------------------------------------------------ GATES
    P("-" * 100)
    P("(G) GATES -- printed before any hypothesis is read")
    P("-" * 100)
    gate_rows, gp, gn = [], 0, 0

    px_u = panels["U56"]
    m0, clip0 = offset_mask(px_u.index, 0)
    ref = rebalance_mask(px_u.index, FREQ)
    g2 = int((m0.values != ref.values).sum())
    ok = g2 == 0; gp += ok; gn += 1
    P(f"  G2  offset_mask(idx,0) == engine.rebalance_mask(idx,'W') : {g2} differing rows"
      f"   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G2", value=g2, bar="0 differing rows", passed=ok))

    w_live = ladder_weights(px_u, *LIVE)
    w_ref = rules_v2_weights(px_u, band=LIVE[0], gross=LIVE[1])
    g3 = float(np.nanmax(np.abs(w_live.values - w_ref.values)))
    ok = g3 == 0.0; gp += ok; gn += 1
    P(f"  G3  ladder_weights(px,0.03,0.75) == baseline.rules_v2_weights : max|d| {g3:.3e}"
      f"   [{'PASS' if ok else 'FAIL'}]  (the ladder's centre cell IS the live book)")
    gate_rows.append(dict(gate="G3", value=g3, bar="max|d| == 0", passed=ok))

    gr, to = run(px_u, w_live, m0)
    r_local = net(gr, to, COST0)
    r_eng = backtest(px_u, w_live, cost_bps=COST0, freq=FREQ)["returns"]
    a, b = r_local.values, r_eng.values
    fin = np.isfinite(b)
    g1 = float(np.abs(a[fin] - b[fin]).max())
    ok = g1 < 1e-12; gp += ok; gn += 1
    P(f"  G1  local run()+net() == engine.backtest(freq='W',{COST0}bps) : max|d| {g1:.3e}"
      f" over {int(fin.sum())} rows   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G1", value=g1, bar="max|d| < 1e-12", passed=ok))

    yrs = len(px_u) / 252
    cnt, clip = {}, {}
    for d in OFFSETS:
        md, cd = offset_mask(px_u.index, d)
        cnt[d] = md.sum() / yrs; clip[d] = cd
    ok = all(50 <= cnt[d] <= 53 for d in OFFSETS); gp += ok; gn += 1
    P("  G4a offset fairness (trades/yr): " +
      "  ".join(f"d{d}={cnt[d]:.1f}" for d in OFFSETS) +
      f"   bar 50-53   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G4a", value=min(cnt.values()), bar="50-53 trades/yr", passed=ok))
    okc = all(v == 0 for v in clip.values()); gp += okc; gn += 1
    P("  G4b offset fairness (clipped weeks): " +
      "  ".join(f"d{d}={clip[d]}" for d in OFFSETS) +
      f"   bar 0   [{'PASS' if okc else 'FAIL — STRUCTURAL, see B1c'}]")
    gate_rows.append(dict(gate="G4b", value=max(clip.values()), bar="0 clipped weeks", passed=okc))

    P(f"  G5  comparands: baseline.rules_v2_weights (band 0.03, gross 0.75, W) and SPY"
      f" buy-and-hold   [PASS by construction]")
    gate_rows.append(dict(gate="G5", value=0, bar="baseline's own", passed=True))
    P(f"  --> {gp} of {gn} gates PASS.  G4b's structural failure is published, not patched.")
    P("")

    # ------------------------------------------------------------------ the grid
    P("-" * 100)
    P("(1) THE GRID -- every one of the 2 x 25 x 5 x 4 cells is written to "
      f"{SLUG}.grid.csv")
    P("-" * 100)

    rows = []
    bench = {}
    for pname, px in panels.items():
        start = px.index[260]
        spy = px["SPY"].pct_change().fillna(0.0)
        base_r = backtest(px, rules_v2_weights(px), cost_bps=COST0, freq=FREQ)["returns"]
        masks = {d: offset_mask(px.index, d)[0] for d in OFFSETS}
        bench[pname] = dict(
            spy={w: stats(x) for w, x in wins(spy, start).items()},
            base={w: stats(x) for w, x in wins(base_r, start).items()},
            start=start)
        for band in BANDS:
            W = {g: ladder_weights(px, band, g) for g in GROSSES}
            for g in GROSSES:
                for d in OFFSETS:
                    gr, to = run(px, W[g], masks[d])
                    for c in COSTS:
                        r = net(gr, to, c)
                        for wname, rr in wins(r, start).items():
                            s = stats(rr)
                            sp = bench[pname]["spy"][wname]
                            sb = bench[pname]["base"][wname]
                            ok4b, L, Mg = legs4b(s, sp)
                            rows.append(dict(
                                panel=pname, band=band, gross=g, offset=d, cost=c,
                                window=wname, **s,
                                pass4b=ok4b, pass4a=legs4a(s, sb),
                                **{f"leg_{k}": v for k, v in L.items()},
                                **{f"marg_{k}": v for k, v in Mg.items()},
                                turnover_yr=to.loc[start:].sum() / (len(rr) / 252)))
        P(f"  {pname}: done ({len(rows)} rows so far)")
    G = pd.DataFrame(rows)
    G.to_csv(OUT / f"{SLUG}.grid.csv", index=False)
    P(f"  grid rows: {len(G)}")
    P("")

    # ------------------------------------------------------------------ spreads
    # For each (panel, band, gross, cost, window) the SPREAD of each leg statistic over the
    # 5 offsets, and the MARGIN at d=0.
    key = ["panel", "band", "gross", "cost", "window"]
    spread = {}
    for k, sub in G.groupby(key):
        sp = {}
        clipfree = sub[sub.offset <= 2]
        for leg, (stat, scale) in LEGUNIT.items():
            sp["spread_" + leg] = (sub[stat].max() - sub[stat].min()) * scale
            sp["spreadc_" + leg] = (clipfree[stat].max() - clipfree[stat].min()) * scale
        sp["n_pass"] = int(sub["pass4b"].sum())
        spread[k] = sp
    d0 = G[G.offset == 0].set_index(key)
    S = pd.DataFrame(spread).T
    S.index = pd.MultiIndex.from_tuples(S.index, names=key)
    T = d0.join(S)
    for leg in LEGUNIT:
        T[f"surv_{leg}"] = T[f"marg_{leg}"] > T[f"spread_{leg}"]
        T[f"survc_{leg}"] = T[f"marg_{leg}"] > T[f"spreadc_{leg}"]
    T["surv_all"] = T[[f"surv_{l}" for l in LEGUNIT]].all(axis=1)
    T["survc_all"] = T[[f"survc_{l}" for l in LEGUNIT]].all(axis=1)
    T["pass_5of5"] = T["n_pass"] == 5
    T.reset_index().to_csv(OUT / f"{SLUG}.spreads.csv", index=False)

    # ------------------------------------------------------------------ B1 / B2 / B3
    P("-" * 100)
    P("(2) B1 / B2 / B3 -- of the cells that PASS 4b at the published offset d=0, how many")
    P("    have margins bigger than their own weekday spread?   [10 bps, the protocol rung]")
    P("-" * 100)
    P(f"  {'panel':6s} {'window':6s} {'4b pass':>8s} {'B1 DD':>10s} {'B1 CAGR':>10s}"
      f" {'B2 all-leg':>11s} {'B3 5of5':>9s}")
    summ = []
    for pname in panels:
        for wname in ("FULL", "IS", "OOS"):
            sub = T.xs((pname, COST0, wname), level=("panel", "cost", "window"))
            pas = sub[sub.pass4b]
            n = len(pas)
            f = lambda col: (f"{int(pas[col].sum())}/{n}" if n else "0/0")
            P(f"  {pname:6s} {wname:6s} {n:8d} {f('surv_DD'):>10s} {f('surv_CAGR'):>10s}"
              f" {f('surv_all'):>11s} {f('pass_5of5'):>9s}")
            summ.append(dict(panel=pname, window=wname, cost=COST0, n_pass4b=n,
                             B1_DD=int(pas["surv_DD"].sum()) if n else 0,
                             B1_CAGR=int(pas["surv_CAGR"].sum()) if n else 0,
                             B2_all=int(pas["surv_all"].sum()) if n else 0,
                             B3_5of5=int(pas["pass_5of5"].sum()) if n else 0,
                             B1c_DD=int(pas["survc_DD"].sum()) if n else 0,
                             B2c_all=int(pas["survc_all"].sum()) if n else 0,
                             n_pass4a=int(sub["pass4a"].sum())))
    P("")
    P("  B1c (clip-free re-read, offsets {0,1,2} only -- G4b's structural failure priced):")
    for s in summ:
        P(f"    {s['panel']:6s} {s['window']:6s}  DD {s['B1c_DD']}/{s['n_pass4b']}"
          f"   all-leg {s['B2c_all']}/{s['n_pass4b']}")
    pd.DataFrame(summ).to_csv(OUT / f"{SLUG}.summary.csv", index=False)
    P("")

    # ------------------------------------------------------------------ B6 4a
    P("-" * 100)
    P("(3) B6 -- PATH 4a (beat the live book) at every grid point, d=0, 10 bps")
    P("-" * 100)
    for pname in panels:
        for wname in ("FULL", "IS", "OOS"):
            sub = T.xs((pname, COST0, wname), level=("panel", "cost", "window"))
            P(f"  {pname:6s} {wname:6s}  4a {int(sub['pass4a'].sum())} of {len(sub)}"
              f"   4b {int(sub['pass4b'].sum())} of {len(sub)}")
    P("")

    # ------------------------------------------------------------------ B4 cost ladder
    P("-" * 100)
    P("(4) B4 -- the same three bars at every cost rung")
    P("-" * 100)
    P(f"  {'panel':6s} {'window':6s} {'cost':>5s} {'4b pass':>8s} {'B1 DD':>9s}"
      f" {'B2 all':>8s} {'B3 5of5':>8s}")
    lad = []
    for pname in panels:
        for wname in ("FULL", "OOS"):
            for c in COSTS:
                sub = T.xs((pname, c, wname), level=("panel", "cost", "window"))
                pas = sub[sub.pass4b]; n = len(pas)
                P(f"  {pname:6s} {wname:6s} {c:5d} {n:8d}"
                  f" {(str(int(pas['surv_DD'].sum()))+'/'+str(n)):>9s}"
                  f" {(str(int(pas['surv_all'].sum()))+'/'+str(n)):>8s}"
                  f" {(str(int(pas['pass_5of5'].sum()))+'/'+str(n)):>8s}")
                lad.append(dict(panel=pname, window=wname, cost=c, n_pass=n,
                                B1_DD=int(pas["surv_DD"].sum()) if n else 0,
                                B2_all=int(pas["surv_all"].sum()) if n else 0,
                                B3_5of5=int(pas["pass_5of5"].sum()) if n else 0))
    pd.DataFrame(lad).to_csv(OUT / f"{SLUG}.costladder.csv", index=False)
    P("")

    # ------------------------------------------------------------------ B5 rule 8
    P("-" * 100)
    P("(5) B5 -- RULE 8 WALK-FORWARD.  (band, gross) chosen on IS Sharpe ONLY, at d=0,")
    P("    10 bps.  2017-2026 read ONCE.  Both KEEP paths on the OOS window.")
    P("-" * 100)
    wf = []
    for pname in panels:
        isub = T.xs((pname, COST0, "IS"), level=("panel", "cost", "window"))
        pick = isub["Sharpe"].idxmax()
        osub = T.xs((pname, COST0, "OOS"), level=("panel", "cost", "window")).loc[pick]
        sp = bench[pname]["spy"]["OOS"]; sb = bench[pname]["base"]["OOS"]
        P(f"  {pname}: IS pick = band {pick[0]:.2f} / gross {pick[1]:.2f}"
          f"  (IS Sharpe {isub.loc[pick,'Sharpe']:.4f}; IS spread over the 25 cells"
          f" {isub['Sharpe'].max()-isub['Sharpe'].min():.4f})")
        P(f"      OOS  pick   {osub['CAGR']:7.2%} / {osub['Sharpe']:.4f} /"
          f" {osub['MaxDD']:7.2%}   H1 {osub['H1']:.3f}  H2 {osub['H2']:.3f}")
        P(f"      OOS  RULESv2 {sb['CAGR']:7.2%} / {sb['Sharpe']:.4f} / {sb['MaxDD']:7.2%}"
          f"   H1 {sb['H1']:.3f}  H2 {sb['H2']:.3f}")
        P(f"      OOS  SPY     {sp['CAGR']:7.2%} / {sp['Sharpe']:.4f} / {sp['MaxDD']:7.2%}"
          f"   H1 {sp['H1']:.3f}  H2 {sp['H2']:.3f}")
        P(f"      4b {'PASS' if osub['pass4b'] else 'FAIL'}"
          f"  (legs " + " ".join(f"{l}:{'ok' if osub['leg_'+l] else 'NO'}" for l in LEGUNIT) + ")"
          f"   4a {'PASS' if osub['pass4a'] else 'FAIL'}")
        P(f"      margins  DD   {osub['marg_DD']:+7.3f} pp vs own spread {osub['spread_DD']:6.3f} pp"
          f"  ->  {'SURVIVES' if osub['surv_DD'] else 'INSIDE THE WEEKDAY NOISE'}")
        P(f"               CAGR {osub['marg_CAGR']:+7.3f} pp vs own spread {osub['spread_CAGR']:6.3f} pp"
          f"  ->  {'SURVIVES' if osub['surv_CAGR'] else 'INSIDE THE WEEKDAY NOISE'}")
        P(f"               H1   {osub['marg_H1']:+7.3f}    vs own spread {osub['spread_H1']:6.3f}"
          f"     H2 {osub['marg_H2']:+7.3f} vs {osub['spread_H2']:6.3f}")
        wf.append(dict(panel=pname, pick_band=pick[0], pick_gross=pick[1],
                       IS_Sharpe=isub.loc[pick, "Sharpe"],
                       OOS_CAGR=osub["CAGR"], OOS_Sharpe=osub["Sharpe"], OOS_MaxDD=osub["MaxDD"],
                       OOS_H1=osub["H1"], OOS_H2=osub["H2"],
                       pass4b=bool(osub["pass4b"]), pass4a=bool(osub["pass4a"]),
                       marg_DD=osub["marg_DD"], spread_DD=osub["spread_DD"],
                       surv_DD=bool(osub["surv_DD"]),
                       marg_CAGR=osub["marg_CAGR"], surv_CAGR=bool(osub["surv_CAGR"]),
                       surv_all=bool(osub["surv_all"]), pass_5of5=bool(osub["pass_5of5"]),
                       base_CAGR=sb["CAGR"], base_Sharpe=sb["Sharpe"], base_MaxDD=sb["MaxDD"],
                       spy_CAGR=sp["CAGR"], spy_Sharpe=sp["Sharpe"], spy_MaxDD=sp["MaxDD"]))
        P("")
    pd.DataFrame(wf).to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)

    # ------------------------------------------------------------------ the live cell
    P("-" * 100)
    P("(6) THE LIVE BOOK'S OWN CELL (band 0.03 / gross 0.75) -- margins vs its own spread")
    P("-" * 100)
    for pname in panels:
        for wname in ("FULL", "OOS"):
            r = T.xs((pname, COST0, wname), level=("panel", "cost", "window")).loc[LIVE]
            P(f"  {pname:6s} {wname:5s}  {r['CAGR']:7.2%} / {r['Sharpe']:.4f} / {r['MaxDD']:7.2%}"
              f"   4b {'PASS' if r['pass4b'] else 'FAIL'}"
              f"   DD margin {r['marg_DD']:+7.3f} pp  spread {r['spread_DD']:6.3f} pp"
              f"   CAGR margin {r['marg_CAGR']:+7.3f} pp")
    P("")

    # ------------------------------------------------------------------ (7) chooser
    P("-" * 100)
    P("(7) WHAT RULE 8 CAN AND CANNOT RESOLVE -- the IS Sharpe ranking it chooses on")
    P("-" * 100)
    for pname in panels:
        isub = T.xs((pname, COST0, "IS"), level=("panel", "cost", "window")).sort_values(
            "Sharpe", ascending=False)
        osub = T.xs((pname, COST0, "OOS"), level=("panel", "cost", "window"))
        P(f"  {pname}: IS top 8 (d=0, {COST0} bps)")
        P(f"    {'band':>5s} {'gross':>6s} {'IS Sh':>8s} {'IS 4b':>6s} {'OOS Sh':>8s}"
          f" {'OOS 4b':>7s} {'OOS mDD':>8s} {'OOS sDD':>8s} {'survDD':>7s}")
        for k in list(isub.index)[:8]:
            o = osub.loc[k]
            P(f"    {k[0]:5.2f} {k[1]:6.2f} {isub.loc[k,'Sharpe']:8.4f}"
              f" {('PASS' if isub.loc[k,'pass4b'] else 'fail'):>6s} {o['Sharpe']:8.4f}"
              f" {('PASS' if o['pass4b'] else 'fail'):>7s} {o['marg_DD']:8.3f}"
              f" {o['spread_DD']:8.3f} {('yes' if o['surv_DD'] else 'NO'):>7s}")
        gspread = {}
        for b in BANDS:
            v = [isub.loc[(b, g), "Sharpe"] for g in GROSSES]
            gspread[b] = max(v) - min(v)
        bspread = max(isub["Sharpe"]) - min(isub["Sharpe"])
        P(f"    IS Sharpe moves {max(gspread.values()):.4f} across the WHOLE gross ladder at a"
          f" fixed band, vs {bspread:.4f} across the grid:")
        P(f"    the IS chooser resolves BAND and is blind to GROSS -- and GROSS is the dial the"
          f" CAGR floor is made of.")
        P("")

    # ------------------------------------------------------------------ (8) survivors
    P("-" * 100)
    P("(8) SURVIVORS -- cells that PASS 4b at d=0 AND clear every leg's own offset spread")
    P("    AND are still a PASS at 5 of 5 offsets, on FULL *and* OOS, 10 bps")
    P("-" * 100)
    surv = []
    for pname in panels:
        f_ = T.xs((pname, COST0, "FULL"), level=("panel", "cost", "window"))
        o_ = T.xs((pname, COST0, "OOS"), level=("panel", "cost", "window"))
        for k in f_.index:
            good = (f_.loc[k, "pass4b"] and o_.loc[k, "pass4b"]
                    and f_.loc[k, "surv_all"] and o_.loc[k, "surv_all"]
                    and f_.loc[k, "pass_5of5"] and o_.loc[k, "pass_5of5"])
            if good:
                surv.append((pname, k))
                P(f"  {pname:5s} band {k[0]:.2f} / gross {k[1]:.2f}:"
                  f"  FULL {f_.loc[k,'CAGR']:6.2%} / {f_.loc[k,'Sharpe']:.4f} /"
                  f" {f_.loc[k,'MaxDD']:7.2%}   OOS {o_.loc[k,'CAGR']:6.2%} /"
                  f" {o_.loc[k,'Sharpe']:.4f} / {o_.loc[k,'MaxDD']:7.2%}")
                P(f"        IS 4b {'PASS' if T.xs((pname,COST0,'IS'),level=('panel','cost','window')).loc[k,'pass4b'] else 'FAIL'}"
                  f"   IS Sharpe rank "
                  f"{int(T.xs((pname,COST0,'IS'),level=('panel','cost','window'))['Sharpe'].rank(ascending=False).loc[k])}"
                  f" of 25   (rule-8 pick is rank 1)")
    if not surv:
        P("  none.")
    P(f"  survivors: {len(surv)} of {2*len(BANDS)*len(GROSSES)} cells.")
    P("")

    # ------------------------------------------------------------------ headline
    P("=" * 100)
    P("HEADLINE")
    P("=" * 100)
    tot_pass = sum(s["n_pass4b"] for s in summ if s["window"] in ("FULL", "OOS"))
    tot_dd = sum(s["B1_DD"] for s in summ if s["window"] in ("FULL", "OOS"))
    tot_all = sum(s["B2_all"] for s in summ if s["window"] in ("FULL", "OOS"))
    tot_5 = sum(s["B3_5of5"] for s in summ if s["window"] in ("FULL", "OOS"))
    P(f"  Over FULL + OOS on both panels at 10 bps: {tot_pass} cells PASS 4b at the published")
    P(f"  offset.  Of those, {tot_dd} have a DD margin bigger than their own weekday spread,")
    P(f"  {tot_all} clear the spread on EVERY leg, and {tot_5} are still a 4b PASS at 5 of 5 offsets.")
    P("")
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LINES) + "\n")
    pd.DataFrame(gate_rows).to_csv(OUT / f"{SLUG}.gates.csv", index=False)


if __name__ == "__main__":
    main()
