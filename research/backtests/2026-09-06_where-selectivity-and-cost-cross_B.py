#!/usr/bin/env python3
"""Idea 155 - "where-selectivity-and-cost-cross": at what selectivity q does the ranking
stop paying for its own turnover, and how does that q move with the cost rung?

The question
------------
Idea 78 left two curves pointing opposite ways:

    gross selection spread   rises monotonically as the book gets MORE selective
    net Sharpe premium       falls monotonically as the pool gets BIGGER
                             (Spearman(k, premium) -0.358 at n=5, -0.601 at n=20)

Two monotone curves of opposite sign cross somewhere.  This run locates the crossing on
the one axis that idea 78's Test A3 showed actually governs the payoff - SELECTIVITY
q = n / n_elig, not the candidate count - and reads it against the cost ladder idea 82
used (0 to 30 bps).  The pre-registered payoff is a number: the q that maximises the net
Sharpe premium at each rung.  If that argmax sits at or near q = 1.0 by 10 bps, it is a
third independent derivation of idea 82's "drop the ranking", arrived at from a
different direction (a continuous selectivity ladder rather than a book-vs-book test).

Design
------
One family of books, indexed by a single number.

    CANDq:  each rebalance week, take the eligible set (200d MA and vol20 < 0.60 gate,
            tradable names only), rank it by RULES v1's composite WITHOUT the /sqrt(vol20)
            tilt (idea 78's convention), and hold the top
                n_t = clip(round(q * n_elig_t), 1, n_elig_t)
            equally weighted at 75% gross.

    q = 1.00 is EWall EXACTLY (every eligible name, equal weight), so the ladder carries
    its own control: the net premium at q is Sharpe(CANDq) - Sharpe(CAND(q=1)) at the
    same rung, on the same days, with the same gate and the same gross.  Nothing is being
    compared across constructions.

    Deployed gross is 75% at EVERY q, so idea 157's finding - that a count rule can win
    or lose purely by holding cash - cannot contaminate this ladder.  Cash is held equal
    by construction; only WHICH names are held changes.

Tuned parameters (PROTOCOL rule 4: at most two)
    1. q in {0.05, 0.10, ..., 1.00}     selectivity (20 points, the swept axis)
    2. c in {0, 5, 10, 15, 20, 25, 30}  cost rung in bps (7 points, idea 82's ladder)
Everything else - the gate, 75% gross, weekly rebalancing, t+1 execution, the composite -
is RULES v1's own and is held fixed.  Panels are REPORTED, not tuned: every number is
shown on all three, and the verdict is required to hold on the large-cap panels.

Grid = 3 panels x 20 q x 7 rungs = 420 points; ALL of them are printed and written to
the .grid.csv beside this script.

The cost ladder is exact, not re-simulated: turnover does not depend on the rung, so
    net(c) = gross_returns - turnover * c / 1e4
is an identity of the engine.  Pre-check [c] verifies it against a direct backtest at
10 bps and requires max|d| < 1e-12 before any ladder number is read.

Pre-checks run BEFORE any new number is read
    [a] harness: idea 2's U56/CAND20 row and the live RULES v1 row.
    [b] premise: idea 78's published full-panel B136 trio at 10 bps
        (EWall 1.026 > CAND20 0.957 > CAND5 0.880).  If it does not reproduce, this
        idea has no premise.
    [c] the cost identity above.

Secondary view (a construction check, NOT a third tuned parameter)
    FIXn: the same ladder with a CONSTANT count n = round(q * mean n_elig) instead of a
    time-varying one, on the primary panel.  If the crossing moves, the crossing is a
    property of the count rule rather than of selectivity.

Walk-forward (PROTOCOL rule 8) - selectors fixed before any OOS number was read
    S0  do-nothing control: q = 1.00 (EWall).  Idea 82's recommendation, taken as given.
    S1  IS-argmax: the q with the highest 2009-2016 net Sharpe premium at 10 bps.
    S2  IS-argmax-GROSS: the q chosen the same way but at 0 bps - the cost-blind chooser,
        which is what a researcher reading only idea 78's Test A would have picked.
    S3  random q, seed fixed in advance: the size-matched null.
    Parameters chosen on 2009-2016 only; 2017-2026 read once, untouched.

Verdicts (both KEEP paths, every one of the 420 points)
    4a  Sharpe > RULES v1 in BOTH halves AND MaxDD no worse than RULES v1.
    4b  Sharpe > SPY in BOTH halves AND out-of-sample, MaxDD <= 60% of SPY's,
        CAGR >= 70% of SPY's.

Survivorship: universe_broad.json and the small panel are current constituents,
one-directional; the ladder inherits that in full and nothing here corrects it.

Deterministic, standalone.  Reads baseline.py and engine.py; modifies nothing.
"""
import sys, json, time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore", category=RuntimeWarning)
from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics, rebalance_mask

FREQ = "W"
MAX_VOL = 0.60
GROSS = 0.75
QS = [round(0.05 * i, 2) for i in range(1, 21)]      # 0.05 .. 1.00
RUNGS = [0, 5, 10, 15, 20, 25, 30]                   # idea 82's ladder
COST_MAIN = 10                                       # PROTOCOL rule 2
WARMUP = 260
IS_END = "2016-12-31"
OOS_START = "2017-01-01"
SEED_S3 = 155_000
SCRIPT = Path(__file__).name
STEM = SCRIPT[:-3]
OUT = REPO / "research" / "backtests"

pd.set_option("display.width", 260)
pd.set_option("display.max_columns", 80)
pd.set_option("display.max_rows", 600)

_lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


def fmt(df, p=4):
    return df.to_string(float_format=lambda x: f"{x:.{p}f}")


def spearman(a, b):
    a, b = pd.Series(np.asarray(a, dtype=float)), pd.Series(np.asarray(b, dtype=float))
    ok = a.notna() & b.notna()
    if ok.sum() < 3:
        return np.nan
    return float(np.corrcoef(a[ok].rank(), b[ok].rank())[0, 1])


def half_sharpes(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def fail_4a(r, base):
    h1, h2 = half_sharpes(r); b1, b2 = half_sharpes(base)
    f = []
    if not h1 > b1: f.append("H1")
    if not h2 > b2: f.append("H2")
    if not metrics(r)["MaxDD"] >= metrics(base)["MaxDD"]: f.append("DD")
    return ",".join(f) if f else "-"


def fail_4b(r, spy, r_oos, spy_oos):
    h1, h2 = half_sharpes(r); s1, s2 = half_sharpes(spy)
    m, ms = metrics(r), metrics(spy)
    f = []
    if not h1 > s1: f.append("H1")
    if not h2 > s2: f.append("H2")
    if not metrics(r_oos)["Sharpe"] > metrics(spy_oos)["Sharpe"]: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return ",".join(f) if f else "-"


# ---------------------------------------------------------------- panels (idea 78's)
def build_panels():
    U = json.loads((REPO / "research" / "universe.json").read_text())
    crypto = {"BTC-USD", "ETH-USD"}
    etf36 = [t for t in U["broad"] + U["sectors"] + U["bonds_fx_commod"] if t not in crypto]

    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)

    def sub(px, cols, tradable=None):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + (["SPY"] if "SPY" in px.columns else [])))
        p = px[keep].dropna(how="all").ffill()
        return p, set(tradable if tradable is not None else cols)

    s_stk = [c for c in pxs.columns if c != "SPY"]
    return {
        "U56":      sub(px56, list(px56.columns)),
        "B136":     sub(px136, list(px136.columns)),
        "SMALL484": sub(pxs, s_stk, tradable=s_stk),
    }


def eligible_mask(px, tradable):
    _, above, vol20 = score(px)
    m = (above & (vol20 < MAX_VOL)).copy()
    drop = [c for c in px.columns if c not in tradable]
    if drop:
        m[drop] = False
    return m


def rank_key(px, tradable):
    """Composite WITHOUT the /sqrt(vol20) tilt (idea 78's convention), masked to the
    eligible set.  A name that passes the gate but has no defined composite (200-251 bars
    of history: `above` exists, 12-1 momentum does not) cannot be ranked, so it cannot be
    selected at ANY q; it is therefore dropped from the eligible set here as well, which
    is what makes q=1.00 the ladder's own exact EWall endpoint.  713 such cells exist on
    B136 across 426 of 4699 days; the reconciliation against plain EWall is printed."""
    elig = eligible_mask(px, tradable)
    s = score(px, vol_scale=False)[0].where(elig)
    elig_r = elig & s.notna()
    return elig_r, s.rank(axis=1, ascending=False)


def weights_q(px, tradable, q, cache):
    """Top round(q * n_elig) eligible names, equal weight, 75% gross.  q=1 == EWall."""
    elig, rank = cache
    n_elig = elig.sum(axis=1)
    n_t = np.clip(np.round(q * n_elig.values), 1, np.maximum(n_elig.values, 1))
    n_t = pd.Series(n_t, index=px.index)
    sel = rank.le(n_t, axis=0) & elig
    cnt = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)


def weights_fixed_n(px, tradable, n, cache, norm=True):
    """Constant count n.  norm=True spreads 75% over however many names were actually
    selected (cash held equal to the CANDq ladder); norm=False is idea 78's raw
    `gross/n`, which silently holds cash in weeks with fewer than n eligible names -
    the channel idea 157 isolated.  Pre-checks use norm=False to reproduce published
    rows; the secondary view reports both."""
    elig, rank = cache
    sel = (rank <= n) & elig
    if not norm:
        return sel.astype(float) * (GROSS / n)
    cnt = sel.sum(axis=1).replace(0, np.nan)
    return sel.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)


def weights_ewall_plain(px, tradable):
    """baseline-style EWall over the FULL eligible set (unrankable names included)."""
    elig = eligible_mask(px, tradable)
    cnt = elig.sum(axis=1).replace(0, np.nan)
    return elig.astype(float).div(cnt, axis=0).mul(GROSS).fillna(0.0)


def run_book(px, w, start):
    """One 0-bps backtest; returns (gross returns, turnover) sliced past warm-up."""
    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
    return res["returns"].loc[start:], res["turnover"].loc[start:]


def net(r0, tno, c):
    return r0 - tno * c / 1e4


def main():
    t0 = time.time()
    P("=" * 210)
    P(f"Idea 155 where-selectivity-and-cost-cross (lane B) | {SCRIPT} | weekly, next-day execution, {GROSS:.0%} gross")
    P("=" * 210)

    panels = build_panels()
    px56, tr56 = panels["U56"]
    px136, tr136 = panels["B136"]

    yrs = px56.index.to_series().groupby(px56.index.year).count()
    P(f"Index sanity (must be ~252 rows/yr): 2013 {yrs.get(2013)}, 2018 {yrs.get(2018)}, 2024 {yrs.get(2024)}")
    if yrs.loc[2015:2024].max() > 300:
        P("!! CALENDAR-DAY INDEX DETECTED - aborting."); sys.exit(1)

    # ------------------------------------------------ pre-check [a]: harness
    P("\n--- pre-check [a] harness on universe.json's own window (must match published rows) ---")
    start56 = px56.index[WARMUP]
    c56 = rank_key(px56, tr56)
    for lbl, w, want in [("U56/CAND20", weights_fixed_n(px56, tr56, 20, c56, norm=False),
                          "idea 2 KEEP: 12.7% / 1.093 / -18.3%, halves 1.088/1.103"),
                         ("U56/v1", rules_v1_weights(px56), "live v1: 6.5% / 0.666 / -13.8%")]:
        r = backtest(px56, w, cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start56:]
        m = metrics(r); h1, h2 = half_sharpes(r)
        P(f"  {lbl:<11} {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}  halves {h1:.3f}/{h2:.3f}   [{want}]")

    # ------------------------------------------------ pre-check [b]: idea 78's premise
    P("\n--- pre-check [b] idea 78's published full-panel B136 trio at 10 bps (EWall 1.026 > CAND20 0.957 > CAND5 0.880) ---")
    start136 = px136.index[WARMUP]
    c136 = rank_key(px136, tr136)
    prem_b = {}
    for lbl, w in [("EWall", weights_ewall_plain(px136, tr136)),
                   ("CAND20", weights_fixed_n(px136, tr136, 20, c136, norm=False)),
                   ("CAND5", weights_fixed_n(px136, tr136, 5, c136, norm=False)),
                   ("q=1.00", weights_q(px136, tr136, 1.0, c136))]:
        r = backtest(px136, w, cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start136:]
        m = metrics(r); prem_b[lbl] = m["Sharpe"]
        P(f"  B136/{lbl:<7} {m['CAGR']:.1%} / {m['Sharpe']:.3f} / {m['MaxDD']:.1%}")
    P(f"  reproduction |d| vs published: EWall {abs(prem_b['EWall']-1.026):.4f}, "
      f"CAND20 {abs(prem_b['CAND20']-0.957):.4f}, CAND5 {abs(prem_b['CAND5']-0.880):.4f}"
      f"   ordering EWall>CAND20>CAND5: {prem_b['EWall']>prem_b['CAND20']>prem_b['CAND5']}")
    P(f"  reconciliation: the ladder's own q=1.00 endpoint is {prem_b['q=1.00']:.4f} vs plain EWall "
      f"{prem_b['EWall']:.4f} (d {prem_b['q=1.00']-prem_b['EWall']:+.4f}) - the unrankable-name gap "
      f"documented in rank_key(); every premium below is measured against the q=1.00 endpoint.")

    # ------------------------------------------------ pre-check [c]: the cost identity
    P("\n--- pre-check [c] cost identity  net(c) = gross - turnover*c/1e4  (must be < 1e-12) ---")
    w_test = weights_q(px136, tr136, 0.25, c136)
    r0, tno = run_book(px136, w_test, start136)
    direct = backtest(px136, w_test, cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start136:]
    dmax = float((net(r0, tno, COST_MAIN) - direct).abs().max())
    P(f"  B136 q=0.25 at 10 bps: max|identity - direct| = {dmax:.3e}")
    if not dmax < 1e-12:
        P("!! cost identity broken - aborting."); sys.exit(1)

    # ------------------------------------------------ the ladder
    P("\n" + "=" * 210)
    P(f"THE LADDER - {len(panels)} panels x {len(QS)} q x {len(RUNGS)} rungs = {len(panels)*len(QS)*len(RUNGS)} points, all reported")
    P("=" * 210)

    books, rows, spy_by_panel, base_by_panel = {}, [], {}, {}
    for pk, (px, tr) in panels.items():
        start = px.index[WARMUP]
        cache = rank_key(px, tr)
        elig = cache[0]
        mask = rebalance_mask(px.index, FREQ)
        n_elig_reb = elig.loc[px.index[mask.values]].sum(axis=1).loc[start:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
        base = backtest(px, rules_v1_weights(px), cost_bps=COST_MAIN, freq=FREQ)["returns"].loc[start:]
        spy_by_panel[pk] = spy; base_by_panel[pk] = base
        oos_m = spy.index >= OOS_START
        spy_oos = spy[oos_m]
        P(f"\n[{pk}] {px.shape[1]-1 if 'SPY' in px.columns else px.shape[1]} tradables, "
          f"{start.date()} -> {px.index[-1].date()}, mean n_elig on rebalance weeks {n_elig_reb.mean():.1f} "
          f"(min {int(n_elig_reb.min())}, max {int(n_elig_reb.max())})")
        for q in QS:
            w = weights_q(px, tr, q, cache)
            r0, tno = run_book(px, w, start)
            books[(pk, q)] = (r0, tno)
            nheld = (w.loc[px.index[mask.values]].loc[start:] > 0).sum(axis=1)
            for c in RUNGS:
                r = net(r0, tno, c)
                rr = r[oos_m]
                m = metrics(r); h1, h2 = half_sharpes(r)
                rows.append(dict(panel=pk, q=q, bps=c, n_mean=nheld.mean(),
                                 turn_yr=tno.sum() / metrics(r)["Years"],
                                 CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                 H1=h1, H2=h2,
                                 OOS_Sharpe=metrics(rr)["Sharpe"], OOS_CAGR=metrics(rr)["CAGR"],
                                 OOS_MaxDD=metrics(rr)["MaxDD"],
                                 fail4a=fail_4a(r, base), fail4b=fail_4b(r, spy, rr, spy_oos)))

    grid = pd.DataFrame(rows)
    # premium against the same panel's own q=1.00 book at the same rung
    ref = grid[grid["q"] == 1.00].set_index(["panel", "bps"])[["Sharpe", "CAGR"]]
    grid["prem_Sharpe"] = grid.apply(lambda x: x["Sharpe"] - ref.loc[(x["panel"], x["bps"]), "Sharpe"], axis=1)
    grid["prem_CAGR"] = grid.apply(lambda x: x["CAGR"] - ref.loc[(x["panel"], x["bps"]), "CAGR"], axis=1)
    grid["4a"] = grid["fail4a"] == "-"
    grid["4b"] = grid["fail4b"] == "-"
    grid.to_csv(OUT / f"{STEM}.grid.csv", index=False)

    for pk in panels:
        g = grid[grid["panel"] == pk]
        P(f"\n--- [{pk}] net Sharpe premium vs its own q=1.00 (EWall), by q x rung (ALL points) ---")
        P(fmt(g.pivot(index="q", columns="bps", values="prem_Sharpe")))
        P(f"  turnover x/yr and mean names held by q:")
        t = g[g["bps"] == 0].set_index("q")[["turn_yr", "n_mean"]]
        P(fmt(t.T, 2))

    # ------------------------------------------------ THE CROSSING
    P("\n" + "=" * 210)
    P("THE CROSSING - argmax_q net Sharpe premium at each rung")
    P("=" * 210)
    cross = []
    for pk in panels:
        g = grid[grid["panel"] == pk]
        for c in RUNGS:
            gc = g[g["bps"] == c]
            i = gc["prem_Sharpe"].idxmax()
            cross.append(dict(panel=pk, bps=c, argmax_q=gc.loc[i, "q"],
                              best_prem=gc.loc[i, "prem_Sharpe"],
                              prem_at_q05=float(gc[gc["q"] == 0.05]["prem_Sharpe"].iloc[0]),
                              prem_at_q25=float(gc[gc["q"] == 0.25]["prem_Sharpe"].iloc[0]),
                              sp_q_prem=spearman(gc["q"], gc["prem_Sharpe"]),
                              n_q_positive=int((gc["prem_Sharpe"] > 0).sum())))
    crossdf = pd.DataFrame(cross)
    for pk in panels:
        P(f"\n[{pk}]")
        P(fmt(crossdf[crossdf["panel"] == pk].drop(columns=["panel"]).set_index("bps")))
    P("\n  argmax_q by rung, all panels:")
    P(fmt(crossdf.pivot(index="bps", columns="panel", values="argmax_q"), 2))
    P("  Spearman(q, net premium) by rung, all panels  [negative = selectivity pays, positive = breadth pays]:")
    P(fmt(crossdf.pivot(index="bps", columns="panel", values="sp_q_prem")))

    P("\n  --- the pre-registered read: is argmax_q at or near 1.00 by 10 bps? ---")
    for pk in panels:
        row = crossdf[(crossdf["panel"] == pk) & (crossdf["bps"] == COST_MAIN)].iloc[0]
        P(f"    [{pk}] argmax q at 10 bps = {row['argmax_q']:.2f}  (premium {row['best_prem']:+.4f}; "
          f"{row['n_q_positive']} of {len(QS)} q beat EWall; Spearman(q, premium) {row['sp_q_prem']:+.3f})")

    # breakeven rung per q: the lowest rung at which the premium turns negative
    P("\n  --- breakeven rung per q (lowest rung in the 0-30 ladder where the premium goes negative; '>30' = never) ---")
    be = []
    for pk in panels:
        for q in QS:
            g = grid[(grid["panel"] == pk) & (grid["q"] == q)].sort_values("bps")
            neg = g[g["prem_Sharpe"] <= 0]
            be.append(dict(panel=pk, q=q, breakeven=(int(neg["bps"].iloc[0]) if len(neg) else 99)))
    bedf = pd.DataFrame(be).pivot(index="q", columns="panel", values="breakeven").replace(99, np.nan)
    P(fmt(bedf, 0).replace("NaN", ">30"))

    # ------------------------------------------------ gross vs net, the two curves
    P("\n" + "=" * 210)
    P("THE TWO CURVES - gross (0 bps) and net (10 bps) premium side by side")
    P("=" * 210)
    for pk in panels:
        g = grid[grid["panel"] == pk]
        tab = pd.DataFrame({
            "gross_prem(0bps)": g[g["bps"] == 0].set_index("q")["prem_Sharpe"],
            "net_prem(10bps)": g[g["bps"] == COST_MAIN].set_index("q")["prem_Sharpe"],
            "net_prem(30bps)": g[g["bps"] == 30].set_index("q")["prem_Sharpe"],
            "turn_yr": g[g["bps"] == 0].set_index("q")["turn_yr"],
        })
        P(f"\n[{pk}]"); P(fmt(tab, 4))
        P(f"  Spearman(q, gross premium) {spearman(tab.index, tab['gross_prem(0bps)']):+.3f}  |  "
          f"Spearman(q, net premium @10) {spearman(tab.index, tab['net_prem(10bps)']):+.3f}  |  "
          f"Spearman(q, turnover) {spearman(tab.index, tab['turn_yr']):+.3f}")

    # ------------------------------------------------ KEEP paths on every point
    P("\n" + "=" * 210)
    P("KEEP PATHS on all 420 points (4a vs live RULES v1, 4b vs SPY; full detail in the .grid.csv)")
    P("=" * 210)
    P(fmt(grid.pivot_table(index="panel", columns="bps", values="4a", aggfunc="sum"), 0))
    P("  ^ 4a passes out of 20 q per cell")
    P(fmt(grid.pivot_table(index="panel", columns="bps", values="4b", aggfunc="sum"), 0))
    P("  ^ 4b passes out of 20 q per cell")
    P(f"\n  totals: 4a {int(grid['4a'].sum())} of {len(grid)}, 4b {int(grid['4b'].sum())} of {len(grid)}")
    for pk in panels:
        g = grid[(grid["panel"] == pk) & (grid["bps"] == COST_MAIN)]
        P(f"\n  [{pk}] at the protocol's own 10 bps, every q (CAGR / Sharpe / MaxDD / halves / 4a-fail / 4b-fail):")
        P(fmt(g.set_index("q")[["CAGR", "Sharpe", "MaxDD", "H1", "H2", "prem_Sharpe", "fail4a", "fail4b"]]))
        b, s = base_by_panel[pk], spy_by_panel[pk]
        mb, ms = metrics(b), metrics(s)
        P(f"     RULES v1 {mb['CAGR']:.1%}/{mb['Sharpe']:.3f}/{mb['MaxDD']:.1%} halves "
          f"{half_sharpes(b)[0]:.3f}/{half_sharpes(b)[1]:.3f}   |   SPY {ms['CAGR']:.1%}/{ms['Sharpe']:.3f}/{ms['MaxDD']:.1%} "
          f"halves {half_sharpes(s)[0]:.3f}/{half_sharpes(s)[1]:.3f}")

    # ------------------------------------------------ secondary: fixed-count construction
    P("\n" + "=" * 210)
    P("SECONDARY VIEW (construction check, not a tuned parameter) - the same ladder with a CONSTANT count")
    P("=" * 210)
    for pk in ["U56", "B136"]:
        px, tr = panels[pk]
        start = px.index[WARMUP]
        cache = rank_key(px, tr)
        mask = rebalance_mask(px.index, FREQ)
        nbar = cache[0].loc[px.index[mask.values]].sum(axis=1).loc[start:].mean()
        ref0 = {c: metrics(net(*books[(pk, 1.00)], c))["Sharpe"] for c in RUNGS}
        for nm in (True, False):
            fx = {}
            for q in QS:
                n = int(max(1, round(q * nbar)))
                w = weights_fixed_n(px, tr, n, cache, norm=nm)
                r0, tno = run_book(px, w, start)
                fx[q] = (n, r0, tno)
            tab = pd.DataFrame({c: {q: metrics(net(fx[q][1], fx[q][2], c))["Sharpe"] - ref0[c] for q in QS}
                                for c in RUNGS})
            tab.insert(0, "n", {q: fx[q][0] for q in QS})
            conv = "norm (cash held equal to CANDq)" if nm else "raw gross/n (idea 78's / idea 157's cash channel)"
            P(f"\n[{pk}]  FIXn premium vs the SAME q=1.00 EWall reference, {conv}; n = round(q * mean n_elig {nbar:.1f})")
            P(fmt(tab))
            am = {c: float(tab[c].idxmax()) for c in RUNGS}
            P(f"  FIXn argmax q by rung: {am}")
            if nm:
                P(f"  CANDq argmax q by rung: "
                  f"{ {c: float(crossdf[(crossdf.panel==pk)&(crossdf.bps==c)]['argmax_q'].iloc[0]) for c in RUNGS} }")

    # ------------------------------------------------ rule 8 walk-forward
    P("\n" + "=" * 210)
    P(f"RULE 8 WALK-FORWARD - q chosen on <= {IS_END}, {OOS_START}+ read once")
    P("=" * 210)
    rng = np.random.default_rng(SEED_S3)
    wf = []
    for pk in panels:
        px = panels[pk][0]; start = px.index[WARMUP]
        idx = books[(pk, 1.00)][0].index
        is_m, oos_m = idx <= IS_END, idx >= OOS_START

        def prem_is(q, c):
            r = net(*books[(pk, q)], c)
            r1 = net(*books[(pk, 1.00)], c)
            return metrics(r[is_m])["Sharpe"] - metrics(r1[is_m])["Sharpe"]

        q_s1 = max(QS, key=lambda q: prem_is(q, COST_MAIN))
        q_s2 = max(QS, key=lambda q: prem_is(q, 0))
        q_s3 = float(rng.choice(QS))
        sel = [("S0 do-nothing q=1.00", 1.00), ("S1 IS-argmax @10bps", q_s1),
               ("S2 IS-argmax GROSS", q_s2), ("S3 random q (null)", q_s3)]
        spy = spy_by_panel[pk]; base = base_by_panel[pk]
        P(f"\n[{pk}] IS picks: S1 q={q_s1:.2f} (IS premium {prem_is(q_s1, COST_MAIN):+.4f}), "
          f"S2 q={q_s2:.2f} (IS gross premium {prem_is(q_s2, 0):+.4f}), S3 q={q_s3:.2f}")
        out = []
        for lbl, q in sel:
            r = net(*books[(pk, q)], COST_MAIN)
            ro = r[oos_m]; m = metrics(ro)
            out.append(dict(selector=lbl, q=q, OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
            wf.append(dict(panel=pk, **out[-1]))
        for lbl, r in [("RULES v1 baseline", base), ("SPY buy-and-hold", spy)]:
            ro = r[r.index >= OOS_START]; m = metrics(ro)
            out.append(dict(selector=lbl, q=np.nan, OOS_CAGR=m["CAGR"], OOS_Sharpe=m["Sharpe"], OOS_MaxDD=m["MaxDD"]))
        # the oracle: best OOS q, never selectable, printed to size the loss
        qo = max(QS, key=lambda q: metrics(net(*books[(pk, q)], COST_MAIN)[oos_m])["Sharpe"])
        mo = metrics(net(*books[(pk, qo)], COST_MAIN)[oos_m])
        out.append(dict(selector="ORACLE (not selectable)", q=qo, OOS_CAGR=mo["CAGR"],
                        OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"]))
        P(fmt(pd.DataFrame(out).set_index("selector")))
        s0 = [o for o in out if o["selector"].startswith("S0")][0]["OOS_Sharpe"]
        for lbl in ("S1", "S2", "S3"):
            o = [x for x in out if x["selector"].startswith(lbl)][0]
            P(f"    {lbl} minus do-nothing: {o['OOS_Sharpe'] - s0:+.4f} OOS Sharpe")

    wfdf = pd.DataFrame(wf)
    P("\n  OOS Sharpe minus do-nothing, averaged over the 3 panels:")
    piv = wfdf.pivot(index="selector", columns="panel", values="OOS_Sharpe")
    d = piv.sub(piv.loc["S0 do-nothing q=1.00"], axis=1)
    P(fmt(d.assign(mean=d.mean(axis=1))))

    P("\n" + "=" * 210)
    P(f"done in {time.time()-t0:.0f}s")
    P("=" * 210)
    (OUT / f"{STEM}.log.txt").write_text("\n".join(_lines) + "\n")


if __name__ == "__main__":
    main()
