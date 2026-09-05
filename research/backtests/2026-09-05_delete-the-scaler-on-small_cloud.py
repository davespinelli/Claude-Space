#!/usr/bin/env python3
"""QUEUE idea 120 — delete-the-scaler-on-small (cloud, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 119 found that turning off /sqrt(vol20) at n=5 on the 439-name panel is worth +11.7 pp
of CAGR and +0.15 Sharpe at LOWER turnover (18.72%/0.690/-39.8% vs 7.05%/0.537/-34.0%,
21.5x vs 33.3x), the largest single-component effect measured on any panel in this project.
Sweep n and gross for the unscaled book against 4b's bars with a liquidity screen applied
FIRST, since idea 119's test F shows the top-5 small-cap book is uninvestable above ~$1M.
Max 2 params."

The thing on trial is whether idea 119's +11.7 pp survives being made TRADEABLE, and whether
anything on the far side of the screen clears PROTOCOL 4b.  The order matters and is the whole
point: the screen is applied to the SELECTABLE SET, point-in-time, before the composite ranks
anything, so the book never holds a name it could not have bought.  A premium that only exists
in names the book cannot buy is not a premium.

The book.  `V1u-noscale`: composite = mean(pct-rank of 12-1, 6m, 3m), NO /sqrt(vol20), NO
200d/vol20 eligibility gate (idea 119's control convention), top-n names, equal weight g/n,
weekly rebalance, next-day execution, 10 bps per unit turnover, long-only.  SPY is the
benchmark column and is never selectable.  Panel = data/prices_small.csv.gz, 439 names after
dropping the 44 with max_1d_move >= 1.0 per data/small_meta.csv.

Liquidity screen (applied FIRST, point-in-time).  L = 20-day rolling MEDIAN dollar volume
(close x share volume, data/volume_small.csv.gz) at the decision date.  A name is selectable
on day t only if L_t >= floor.  Floors reported: $0 (idea 119's convention), $1M, $5M, $20M.
$5M is the PRE-REGISTERED headline floor (fixed before any result below was read; chosen as
the smallest floor at which the thinnest year, 2012, still offers >= 40 names so that every
n in the sweep can be filled).  The other three floors are a REPORTED ladder, not a choice.

Tuned parameters (PROTOCOL rule 4): TWO — position count n in {3,5,10,20,40} and gross
g in {0.25,0.50,0.75,1.00}.  Everything else is either inherited (cadence, cost, composite,
next-day execution, the 2016/2017 walk-forward split) or reported at every value without
selection (floor, scaler on/off, gate on/off, gross convention).

Gross convention (idea 81).  `lit` = literal g/n per name, so the book de-grosses whenever
fewer than n names are selectable — which the $20M floor forces in the early years.  `mat` =
gross-matched, weights renormalised to sum to g whenever >= 1 name is selectable.  Both are
reported for every cell, with realised mean invested gross, because idea 81 showed a whole
apparent premium can be a de-grossing in disguise.

Tests (all reported whatever they say)
    A  HARNESS + REPRODUCTION.  A numpy simulator checked against engine.backtest
       (max|diff| printed) and idea 119's unscreened n=5 scaler on/off pair reproduced.
    B  DOES THE PREMIUM SURVIVE THE SCREEN.  dCAGR / dSharpe / dTurnover of scaler-off vs
       scaler-on at every (floor, n, g), i.e. idea 119's headline effect as a function of
       tradeability.
    C  MAIN GRID.  5 n x 4 g x 4 floors x 2 scaler x 2 gate x 2 gross conventions = 640
       points, every one written to .grid.csv with full-sample / H1 / H2 / OOS statistics,
       turnover, realised gross, and its 4a and 4b verdicts.
    D  PROTOCOL RULE 8 WALK-FORWARD.  (n,g) chosen on 2010-2016 ONLY at the pre-registered
       floor, on the unscaled ungated matched-gross family, under two selectors fixed in
       advance: S1 = argmax IS Sharpe (plain rule 8); S2 = argmax IS Sharpe among cells whose
       IS MaxDD clears 4b's cap (<= 60% of SPY's IS MaxDD).  2017-2026 read once, untouched.
    E  COST LADDER.  0 / 10 / 25 / 50 bps on the walk-forward picks and on the n=5, g=0.75
       anchor, at the headline floor.
    F  CAPACITY.  Dollar ADV of the names actually held, and the fraction of a held name's
       ADV the book must trade at $1M / $10M / $100M of capital given its realised turnover.
       This is what idea 119's test F left open and is a hard constraint, not a statistic.
    G  YEAR TABLE for the picks and the anchor.

Pre-registered predictions (written before any number from tests B-G was read)
    P1  The screen eats most of the premium: at the $5M floor the scaler-off minus scaler-on
        dCAGR at n=5 is less than half of idea 119's +11.7 pp.
    P2  No cell passes 4b at the $5M floor: the small-cap book buys its CAGR with drawdown,
        so the cells that clear 4b's CAGR floor (>= 70% of SPY) breach its MaxDD cap
        (<= 60% of SPY's) and vice versa.
    P3  The walk-forward pick's OOS Sharpe is below SPY's OOS Sharpe.
    P4  Capacity binds early: at $10M of capital the n=5 book at the $5M floor trades > 10%
        of the median held name's dollar ADV on a rebalance.

SURVIVORSHIP (stated, not fixed).  data/prices_small.csv.gz is the CURRENT constituent list of
a sub-$2B screen: every name in it survived to 2026, so the 2010-2025 small caps that were
delisted, bankrupted or acquired are absent.  The direction of the bias is one-directional and
large on this panel — the missing cohort is the beaten-down one — so every CAGR and Sharpe
level below is an overstatement of what was achievable, and no number here is quoted as an
achievable return.  The liquidity screen does not fix this; if anything it correlates with it,
since the names that died were also the thin ones.  Comparisons WITHIN the panel (scaler on
vs off, floor vs floor, n vs n) are what this run is for.

Deterministic, standalone.  Imports research/baseline.py; modifies nothing.  Writes
.console.txt and five .csv companions next to itself.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, load_volume, rules_v1_weights, score  # noqa: E402
from engine import backtest, metrics, rebalance_mask  # noqa: E402

STEM = "2026-09-05_delete-the-scaler-on-small_cloud"
OUT = ROOT / "research" / "backtests"

FREQ, COST, MAX_VOL = "W", 10.0, 0.60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
NS = [3, 5, 10, 20, 40]
GS = [0.25, 0.50, 0.75, 1.00]
FLOORS = [0.0, 1e6, 5e6, 20e6]          # $0 / $1M / $5M / $20M
HEADLINE_FLOOR = 5e6                     # pre-registered
BAD_MOVE = 1.0
WARMUP = 260

_tee = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _tee.append(s)


# ---------------------------------------------------------------- data ----
def panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= BAD_MOVE, "ticker"])
    px = px[[c for c in px.columns if c not in bad]]
    sel = px.drop(columns=["SPY"])                       # SPY is benchmark only
    vol = load_volume(small=True).reindex(index=px.index, columns=sel.columns)
    dv20 = (sel * vol).rolling(20).median()              # point-in-time dollar ADV
    return px, sel, dv20, sorted(bad)


# ------------------------------------------------------------ simulator ----
def fast_bt(px, w, cost_bps=COST, freq=FREQ):
    """Vectorised equivalent of engine.backtest (checked in test A)."""
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    n = len(px)
    held = np.zeros_like(rets)
    turn = np.zeros(n)
    cur = np.zeros(rets.shape[1])
    for i in range(n):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new
        held[i] = cur
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        if tot > 0:
            cur = growth / tot
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return (pd.Series(port, index=px.index), pd.Series(turn, index=px.index),
            pd.DataFrame(held, index=px.index, columns=px.columns))


def weights(sel, cols, dv20, floor, n, g, vol_scale, gate, matched):
    s, above, vol20 = score(sel, vol_scale)
    e = s.where(above & (vol20 < MAX_VOL)) if gate else s
    if floor > 0:
        e = e.where(dv20 >= floor)
    rank = e.rank(axis=1, ascending=False)
    hold = (rank <= n) & e.notna()
    w = hold.astype(float) * (g / n)
    if matched:
        cnt = hold.sum(axis=1)
        w = hold.astype(float).div(cnt.replace(0, np.nan), axis=0).fillna(0.0) * g
    return w.reindex(columns=cols).fillna(0.0), hold


def stats(r, start):
    r = r.loc[start:]
    h = len(r) // 2
    m, m1, m2 = metrics(r), metrics(r.iloc[:h]), metrics(r.iloc[h:])
    o, i = metrics(r.loc[OOS_START:]), metrics(r.loc[:IS_END])
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=m1["Sharpe"], H2=m2["Sharpe"],
                IS_Sharpe=i["Sharpe"], IS_CAGR=i["CAGR"], IS_MaxDD=i["MaxDD"],
                OOS_CAGR=o["CAGR"], OOS_Sharpe=o["Sharpe"], OOS_MaxDD=o["MaxDD"])


def verdicts(d, base, spy):
    """PROTOCOL 4a (beat the live book) and 4b (capital-worthy vs SPY)."""
    p4a = d["H1"] > base["H1"] and d["H2"] > base["H2"] and d["MaxDD"] >= base["MaxDD"]
    p4b = (d["H1"] > spy["H1"] and d["H2"] > spy["H2"] and d["OOS_Sharpe"] > spy["OOS_Sharpe"]
           and d["MaxDD"] >= 0.60 * spy["MaxDD"] and d["CAGR"] >= 0.70 * spy["CAGR"])
    return p4a, p4b


def main():
    px, sel, dv20, dropped = panel()
    start = px.index[WARMUP]
    spy_r = px["SPY"].pct_change().fillna(0.0)
    spy = stats(spy_r, start)
    say(f"[panel] {sel.shape[1]} selectable names + SPY benchmark | "
        f"{px.index[0].date()} -> {px.index[-1].date()} | {len(dropped)} dropped for "
        f"max_1d_move >= {BAD_MOVE} | eval from {start.date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    say(f"[SPY] CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.3f} MaxDD {spy['MaxDD']:.1%} "
        f"halves {spy['H1']:.3f}/{spy['H2']:.3f} OOS Sharpe {spy['OOS_Sharpe']:.3f} "
        f"| 4b bars: MaxDD >= {0.60*spy['MaxDD']:.1%}, CAGR >= {0.70*spy['CAGR']:.2%}")

    # ---- A: harness equivalence + live-rules baseline + idea 119 reproduction ----
    wv1 = rules_v1_weights(sel).reindex(columns=px.columns).fillna(0.0)
    r_eng = backtest(px, wv1, cost_bps=COST, freq=FREQ)["returns"]
    r_fast, t_v1, _ = fast_bt(px, wv1)
    say(f"\n[A] engine-equivalence max|diff| = {float((r_fast - r_eng).abs().max()):.3e}")
    base = stats(r_fast, start)
    base["turnover"] = t_v1.loc[start:].sum() / (len(t_v1.loc[start:]) / 252)
    say(f"[A] live RULES v1 on this panel: CAGR {base['CAGR']:.2%} Sharpe {base['Sharpe']:.3f} "
        f"MaxDD {base['MaxDD']:.1%} halves {base['H1']:.3f}/{base['H2']:.3f} "
        f"OOS {base['OOS_Sharpe']:.3f} turnover {base['turnover']:.1f}x/yr")
    say("[A] idea 119 reproduction — ungated n=5 g=0.75, unscreened, scaler on vs off:")
    repro = []
    for vs in (True, False):
        w, _ = weights(sel, px.columns, dv20, 0.0, 5, 0.75, vs, False, False)
        r, t, _ = fast_bt(px, w)
        d = stats(r, start)
        d["turnover"] = t.loc[start:].sum() / (len(t.loc[start:]) / 252)
        repro.append(d)
        say(f"    scaler={'on ' if vs else 'off'}: CAGR {d['CAGR']:.2%} Sharpe {d['Sharpe']:.3f} "
            f"MaxDD {d['MaxDD']:.1%} turnover {d['turnover']:.1f}x/yr")
    say(f"    delta (off - on): dCAGR {100*(repro[1]['CAGR']-repro[0]['CAGR']):+.2f} pp  "
        f"dSharpe {repro[1]['Sharpe']-repro[0]['Sharpe']:+.3f}  "
        f"dTurnover {repro[1]['turnover']-repro[0]['turnover']:+.1f}x  "
        f"[idea 119 published +11.7 pp / +0.15 / -11.8x on its own start convention]")

    # ---- C: main grid ----
    say(f"\n[C] main grid: {len(NS)}n x {len(GS)}g x {len(FLOORS)} floors x 2 scaler x 2 gate "
        f"x 2 gross conventions = {len(NS)*len(GS)*len(FLOORS)*8} points")
    rows, rets = [], {}
    for floor in FLOORS:
        for gate in (False, True):
            for vs in (False, True):
                for matched in (True, False):
                    for n in NS:
                        for g in GS:
                            w, hold = weights(sel, px.columns, dv20, floor, n, g, vs, gate, matched)
                            r, t, held = fast_bt(px, w)
                            d = stats(r, start)
                            key = (floor, gate, vs, matched, n, g)
                            rets[key] = r
                            yrs = len(t.loc[start:]) / 252
                            d.update(floor_musd=floor / 1e6, gate=gate, scaler=vs,
                                     gross_conv="mat" if matched else "lit", n=n, g=g,
                                     turnover=t.loc[start:].sum() / yrs,
                                     mean_gross=float(held.loc[start:].sum(axis=1).mean()),
                                     mean_held=float(hold.loc[start:].sum(axis=1).mean()))
                            d["pass4a"], d["pass4b"] = verdicts(d, base, spy)
                            rows.append(d)
    grid = pd.DataFrame(rows)
    cols = ["floor_musd", "gate", "scaler", "gross_conv", "n", "g", "CAGR", "Sharpe", "MaxDD",
            "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "IS_Sharpe", "IS_MaxDD",
            "turnover", "mean_gross", "mean_held", "pass4a", "pass4b"]
    grid[cols].to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"[C] wrote {len(grid)} rows -> {STEM}.grid.csv | 4a passes {int(grid.pass4a.sum())} "
        f"| 4b passes {int(grid.pass4b.sum())}")
    if grid.pass4b.any():
        say("[C] ALL 4b passes:")
        for _, x in grid[grid.pass4b].iterrows():
            say(f"    floor ${x.floor_musd:.0f}M gate={x.gate} scaler={x.scaler} {x.gross_conv} "
                f"n={x.n} g={x.g:.2f}: {x.CAGR:.2%}/{x.Sharpe:.3f}/{x.MaxDD:.1%} "
                f"halves {x.H1:.3f}/{x.H2:.3f} OOS {x.OOS_Sharpe:.3f} turn {x.turnover:.1f}x")

    # headline slice printed in full (the idea as worded: unscaled, ungated, matched gross)
    say(f"\n[C] headline family (floor ${HEADLINE_FLOOR/1e6:.0f}M, ungated, scaler OFF, matched gross) "
        f"— every grid point:")
    say(f"    {'n':>3} {'g':>5} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1':>6} {'H2':>6} "
        f"{'OOSs':>6} {'turn':>6} {'gross':>6} {'4a':>3} {'4b':>3}")
    hf = grid[(grid.floor_musd == HEADLINE_FLOOR / 1e6) & (~grid.gate) & (~grid.scaler)
              & (grid.gross_conv == "mat")].sort_values(["n", "g"])
    for _, x in hf.iterrows():
        say(f"    {x.n:>3.0f} {x.g:>5.2f} {x.CAGR:>7.2%} {x.Sharpe:>6.3f} {x.MaxDD:>7.1%} "
            f"{x.H1:>6.3f} {x.H2:>6.3f} {x.OOS_Sharpe:>6.3f} {x.turnover:>5.1f}x "
            f"{x.mean_gross:>6.2f} {str(x.pass4a):>3} {str(x.pass4b):>3}")

    # ---- B: does idea 119's premium survive the screen ----
    say("\n[B] scaler premium (OFF minus ON) by floor, ungated matched-gross:")
    say(f"    {'floor':>7} {'n':>3} {'g':>5} {'dCAGR pp':>9} {'dSharpe':>8} {'dMaxDD pp':>10} {'dTurn':>7}")
    brows = []
    for floor in FLOORS:
        for n in NS:
            for g in GS:
                on = grid[(grid.floor_musd == floor / 1e6) & (~grid.gate) & (grid.scaler)
                          & (grid.gross_conv == "mat") & (grid.n == n) & (grid.g == g)].iloc[0]
                off = grid[(grid.floor_musd == floor / 1e6) & (~grid.gate) & (~grid.scaler)
                           & (grid.gross_conv == "mat") & (grid.n == n) & (grid.g == g)].iloc[0]
                b = dict(floor_musd=floor / 1e6, n=n, g=g,
                         dCAGR_pp=100 * (off.CAGR - on.CAGR), dSharpe=off.Sharpe - on.Sharpe,
                         dMaxDD_pp=100 * (off.MaxDD - on.MaxDD), dTurnover=off.turnover - on.turnover,
                         CAGR_off=off.CAGR, CAGR_on=on.CAGR)
                brows.append(b)
                if g == 0.75:
                    say(f"    ${floor/1e6:>5.0f}M {n:>3} {g:>5.2f} {b['dCAGR_pp']:>9.2f} "
                        f"{b['dSharpe']:>8.3f} {b['dMaxDD_pp']:>10.2f} {b['dTurnover']:>6.1f}x")
    prem = pd.DataFrame(brows)
    prem.to_csv(OUT / f"{STEM}.scalerpremium.csv", index=False)
    for floor in FLOORS:
        s = prem[prem.floor_musd == floor / 1e6]
        say(f"    ${floor/1e6:>5.0f}M summary: median dCAGR {s.dCAGR_pp.median():+.2f} pp, "
            f"median dSharpe {s.dSharpe.median():+.3f}, positive dCAGR in {int((s.dCAGR_pp>0).sum())}/{len(s)} cells")

    # ---- D: rule 8 walk-forward ----
    say(f"\n[D] PROTOCOL rule 8 walk-forward — (n,g) chosen on {px.index[WARMUP].date()}..{IS_END} "
        f"only, at the pre-registered ${HEADLINE_FLOOR/1e6:.0f}M floor, ungated / scaler OFF / matched gross; "
        f"{OOS_START}..{px.index[-1].date()} read once")
    fam = grid[(grid.floor_musd == HEADLINE_FLOOR / 1e6) & (~grid.gate) & (~grid.scaler)
               & (grid.gross_conv == "mat")].copy()
    spy_is = metrics(spy_r.loc[start:IS_END])
    picks = []
    s1 = fam.loc[fam.IS_Sharpe.idxmax()]
    picks.append(("S1 argmax IS Sharpe", s1))
    cap = fam[fam.IS_MaxDD >= 0.60 * spy_is["MaxDD"]]
    if len(cap):
        picks.append(("S2 argmax IS Sharpe | IS MaxDD <= 60% SPY", cap.loc[cap.IS_Sharpe.idxmax()]))
    else:
        say("    S2: no cell clears 4b's drawdown cap in-sample — selector empty.")
    wf = []
    for label, p in picks:
        say(f"    {label}: pick n={p.n:.0f} g={p.g:.2f} | IS Sharpe {p.IS_Sharpe:.3f} "
            f"(SPY IS {spy_is['Sharpe']:.3f}) IS MaxDD {p.IS_MaxDD:.1%} (SPY IS {spy_is['MaxDD']:.1%})")
        say(f"        OOS: CAGR {p.OOS_CAGR:.2%} Sharpe {p.OOS_Sharpe:.3f} MaxDD {p.OOS_MaxDD:.1%} "
            f"| SPY OOS {spy['OOS_CAGR']:.2%}/{spy['OOS_Sharpe']:.3f}/{spy['OOS_MaxDD']:.1%} "
            f"| v1 OOS {base['OOS_CAGR']:.2%}/{base['OOS_Sharpe']:.3f}/{base['OOS_MaxDD']:.1%}")
        say(f"        full {p.CAGR:.2%}/{p.Sharpe:.3f}/{p.MaxDD:.1%} halves {p.H1:.3f}/{p.H2:.3f} "
            f"| 4a {p.pass4a} 4b {p.pass4b}")
        wf.append(dict(selector=label, n=p.n, g=p.g, IS_Sharpe=p.IS_Sharpe, IS_MaxDD=p.IS_MaxDD,
                       OOS_CAGR=p.OOS_CAGR, OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                       SPY_OOS_Sharpe=spy["OOS_Sharpe"], v1_OOS_Sharpe=base["OOS_Sharpe"],
                       pass4a=p.pass4a, pass4b=p.pass4b))
    pd.DataFrame(wf).to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ---- E: cost ladder ----
    say("\n[E] cost ladder (headline floor, ungated, scaler OFF, matched gross):")
    anchors = {(int(p.n), float(p.g)) for _, p in picks} | {(5, 0.75)}
    crows = []
    for (n, g) in sorted(anchors):
        w, _ = weights(sel, px.columns, dv20, HEADLINE_FLOOR, n, g, False, False, True)
        line = []
        for c in (0.0, 10.0, 25.0, 50.0):
            r, _, _ = fast_bt(px, w, cost_bps=c)
            d = stats(r, start)
            crows.append(dict(n=n, g=g, cost_bps=c, **{k: d[k] for k in
                              ("CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe")}))
            line.append(f"{c:>4.0f}bp {d['CAGR']:>7.2%}/{d['Sharpe']:.3f}")
        say(f"    n={n} g={g:.2f}: " + " | ".join(line))
    pd.DataFrame(crows).to_csv(OUT / f"{STEM}.costladder.csv", index=False)

    # ---- F: capacity ----
    say("\n[F] capacity — dollar ADV of names actually held, and % of a held name's ADV traded")
    say(f"    {'floor':>7} {'n':>3} {'p25 ADV':>9} {'med ADV':>9} {'%ADV @$1M':>10} "
        f"{'@$10M':>8} {'@$100M':>8}")
    frows = []
    for floor in (0.0, HEADLINE_FLOOR):
        for n in NS:
            w, hold = weights(sel, px.columns, dv20, floor, n, 0.75, False, False, True)
            r, t, _ = fast_bt(px, w)
            h = hold.loc[start:]
            adv = dv20.loc[start:].where(h)
            flat = adv.stack().dropna()
            p25, p50 = flat.quantile(0.25), flat.quantile(0.50)
            yrs = len(t.loc[start:]) / 252
            turn = t.loc[start:].sum() / yrs                       # gross turnover per year
            nheld = h.sum(axis=1).replace(0, np.nan).mean()
            # per-rebalance trade per name, as a fraction of that name's daily ADV
            nreb = float((t.loc[start:] > 0).sum()) / yrs
            per_trade_frac = (turn / nreb) / nheld                 # fraction of capital per name per rebalance
            row = dict(floor_musd=floor / 1e6, n=n, adv_p25=p25, adv_p50=p50,
                       turnover=turn, rebals_per_yr=nreb, mean_names=nheld)
            for cap in (1e6, 1e7, 1e8):
                row[f"pct_adv_{int(cap/1e6)}M"] = 100 * per_trade_frac * cap / p50
            frows.append(row)
            say(f"    ${floor/1e6:>5.0f}M {n:>3} {p25/1e6:>8.2f}M {p50/1e6:>8.2f}M "
                f"{row['pct_adv_1M']:>9.2f}% {row['pct_adv_10M']:>7.1f}% {row['pct_adv_100M']:>7.0f}%")
    pd.DataFrame(frows).to_csv(OUT / f"{STEM}.capacity.csv", index=False)

    # ---- H: no-ranking control (added after test C: is the SCREENED UNIVERSE bad, or the RANKING?) ----
    say("\n[H] control — equal-weight EVERY name passing the screen (no composite, no ranking, "
        "no scaler, no gate), so the grid's result can be attributed:")
    say(f"    {'floor':>7} {'g':>5} {'CAGR':>7} {'Shrp':>6} {'MaxDD':>7} {'H1':>6} {'H2':>6} "
        f"{'OOSs':>6} {'turn':>6} {'names':>6} {'4a':>5} {'4b':>5}")
    hrows = []
    for floor in FLOORS:
        elig = (dv20 >= floor) if floor > 0 else sel.notna()
        elig = elig & sel.notna()
        for g in GS:
            w = elig.astype(float).div(elig.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * g
            w = w.reindex(columns=px.columns).fillna(0.0)
            r, t, _ = fast_bt(px, w)
            d = stats(r, start)
            d["turnover"] = t.loc[start:].sum() / (len(t.loc[start:]) / 252)
            d["names"] = float(elig.loc[start:].sum(axis=1).mean())
            d["floor_musd"], d["g"] = floor / 1e6, g
            d["pass4a"], d["pass4b"] = verdicts(d, base, spy)
            hrows.append(d)
            say(f"    ${floor/1e6:>5.0f}M {g:>5.2f} {d['CAGR']:>7.2%} {d['Sharpe']:>6.3f} "
                f"{d['MaxDD']:>7.1%} {d['H1']:>6.3f} {d['H2']:>6.3f} {d['OOS_Sharpe']:>6.3f} "
                f"{d['turnover']:>5.1f}x {d['names']:>6.0f} {str(d['pass4a']):>5} {str(d['pass4b']):>5}")
    pd.DataFrame(hrows).to_csv(OUT / f"{STEM}.norankcontrol.csv", index=False)
    ctl5 = [x for x in hrows if x["floor_musd"] == HEADLINE_FLOOR / 1e6 and x["g"] == 0.75][0]
    rk5 = hf[(hf.n == 5) & (hf.g == 0.75)].iloc[0]
    say(f"    attribution at the ${HEADLINE_FLOOR/1e6:.0f}M floor, g=0.75: no-ranking control "
        f"{ctl5['CAGR']:.2%}/{ctl5['Sharpe']:.3f}/{ctl5['MaxDD']:.1%} vs unscaled ranked n=5 "
        f"{rk5.CAGR:.2%}/{rk5.Sharpe:.3f}/{rk5.MaxDD:.1%} -> the ranking is worth "
        f"{100*(rk5.CAGR-ctl5['CAGR']):+.2f} pp of CAGR and {rk5.Sharpe-ctl5['Sharpe']:+.3f} of Sharpe")

    # ---- G: year table ----
    say("\n[G] calendar-year returns (headline floor, ungated, scaler OFF, matched gross):")
    yrows = {}
    for (n, g) in sorted(anchors):
        r = rets[(HEADLINE_FLOOR, False, False, True, n, g)].loc[start:]
        yrows[f"n{n}g{g:.2f}"] = r.groupby(r.index.year).apply(lambda x: (1 + x).prod() - 1)
    yrows["SPY"] = spy_r.loc[start:].groupby(spy_r.loc[start:].index.year).apply(lambda x: (1 + x).prod() - 1)
    yrows["v1"] = r_fast.loc[start:].groupby(r_fast.loc[start:].index.year).apply(lambda x: (1 + x).prod() - 1)
    yt = pd.DataFrame(yrows)
    yt.to_csv(OUT / f"{STEM}.years.csv")
    say(yt.to_string(float_format=lambda x: f"{x:>7.1%}"))

    # ---- predictions ----
    say("\n[P] pre-registered predictions vs outcome")
    d5 = prem[(prem.floor_musd == HEADLINE_FLOOR / 1e6) & (prem.n == 5) & (prem.g == 0.75)].iloc[0]
    say(f"    P1 screen eats >half the premium: n=5 g=0.75 dCAGR at $5M floor = {d5.dCAGR_pp:+.2f} pp "
        f"vs unscreened {prem[(prem.floor_musd==0)&(prem.n==5)&(prem.g==0.75)].iloc[0].dCAGR_pp:+.2f} pp "
        f"-> {'CONFIRMED' if d5.dCAGR_pp < 0.5*prem[(prem.floor_musd==0)&(prem.n==5)&(prem.g==0.75)].iloc[0].dCAGR_pp else 'REFUTED'}")
    n4b = int(grid[(grid.floor_musd == HEADLINE_FLOOR / 1e6)].pass4b.sum())
    say(f"    P2 no 4b pass at the $5M floor: {n4b} passes -> {'CONFIRMED' if n4b == 0 else 'REFUTED'}")
    p1 = picks[0][1]
    say(f"    P3 pick OOS Sharpe < SPY OOS: {p1.OOS_Sharpe:.3f} vs {spy['OOS_Sharpe']:.3f} -> "
        f"{'CONFIRMED' if p1.OOS_Sharpe < spy['OOS_Sharpe'] else 'REFUTED'}")
    cf = pd.DataFrame(frows)
    c5 = cf[(cf.floor_musd == HEADLINE_FLOOR / 1e6) & (cf.n == 5)].iloc[0]
    say(f"    P4 >10% of median held ADV at $10M: {c5.pct_adv_10M:.1f}% -> "
        f"{'CONFIRMED' if c5.pct_adv_10M > 10 else 'REFUTED'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
