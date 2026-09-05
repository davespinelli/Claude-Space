#!/usr/bin/env python3
"""QUEUE idea 121 — liquidity-screened-small-panel (cloud, 2026-09-05).

Question (pre-registered, verbatim from QUEUE)
----------------------------------------------
"idea 119 measured the held-name 20d median dollar volume of the small-panel books at
p25 $0.87M / p50 $4.33M, i.e. every small-panel row in this project (ideas 31, 38, 49, 50,
51, 54, 97, 119) is computed on names that cannot absorb the trades. Propose an ADV floor
as a PROTOCOL clause for `load_universe(small=True)` callers and re-run the rows whose
verdicts could move."

What is on trial.  Not a new book.  The claim under test is that the project's PUBLISHED
small-panel FINDINGS — not just their return levels, which everyone already discounts for
survivorship, but the signed comparisons they are quoted for — are artefacts of names the
books could not have bought.  Idea 120 established this for ONE finding (the /sqrt(vol20)
scaler premium, which sign-flips between a $1M and a $5M floor).  This run asks whether the
same is true of the two small-panel findings the project actually cites in argument:

    Claim A (ideas 49/51/39, quoted in the QUEUE five times):  the RULES v1 eligibility gate
            (above 200d AND vol20 < 0.60) *destroys* ~5.4 pp/yr of CAGR at zero cost on the
            sub-$2B panel, i.e. trend-following is inverted on small caps.
    Claim B (idea 38/56, quoted as the vol20-gate indictment):  at n=40 the four-way gate
            decomposition orders no-gate 0.797 > 200d 0.693 > vol20 0.524 > both 0.441 on
            Sharpe, so the vol20 half is the larger destroyer.

Both are DIFFERENCES between two books on the same panel, so survivorship does not obviously
cancel them — but a liquidity floor might, because the floor changes WHICH names are in the
difference.  The output is (1) a floor proposed as a PROTOCOL clause on a capacity criterion
fixed before any return was read, and (2) a table of every re-runnable small-panel row with
its verdict at each floor and a flag where the verdict moves.

The panel.  data/prices_small.csv.gz, 483 names, minus the 44 with max_1d_move >= 1.0 per
data/small_meta.csv (mandatory), = 439 selectable names + SPY as a benchmark column that is
never selectable.  2010-01-04 .. 2026-09-04, 4194 trading-day rows.

Liquidity screen, applied FIRST and point-in-time (idea 120's convention, reused unchanged so
the two runs are comparable).  L_t = 20-day rolling MEDIAN of close x share volume from
data/volume_small.csv.gz.  A name is selectable on day t only if L_t >= floor.  Ladder:
$0 / $1M / $5M / $20M, every value reported for every book.  The floor is NOT tuned: it is
reported at all four values and the PROPOSED clause is picked by the capacity rule below.

PRE-REGISTERED capacity criterion for the proposed clause (fixed before any result below was
read, and a function of ADV only — no return, Sharpe or drawdown enters it):

    Propose the smallest floor on the ladder at which a $10M book trades <= 10% of the
    p25 (not median) held name's 20-day median dollar volume on a rebalance, for the
    NARROWEST book the project publishes on this panel (the ranked n=20 book).

p25 rather than median because the binding constraint is the thinnest name held, and idea 119
reported both.  If no ladder floor satisfies it, the honest answer is that the panel has no
tradeable floor and the clause must say so.

Books re-run (every published small-panel construction that can be rebuilt from baseline.py
primitives, so nothing is re-implemented by guesswork):
    v1        RULES v1 live: composite /sqrt(vol20), gate on, top-5, w=0.15  (ideas 31, 38)
    EWall     equal-weight EVERY selectable name, no gate                     (idea 49 control)
    EWgate    equal-weight every name with px>200d AND vol20<0.60             (idea 49 treatment)
    EW200d    equal-weight every name with px>200d only                       (idea 38/56)
    EWvol60   equal-weight every name with vol20<0.60 only                    (idea 38/56)
    R{n}      composite ranked top-n, gate ON, scaler ON, equal weight        (idea 2 shape)
    R{n}u     composite ranked top-n, gate OFF, scaler OFF, equal weight      (idea 119/120)
    R40g*     the four-way gate decomposition at n=40 with the scaler on      (idea 38/56 exact)
All equal-weight books use gross-matched weights (idea 81): weights renormalise to g whenever
>= 1 name is selectable, so a floor cannot manufacture a premium by silently de-grossing.
Realised mean invested gross is reported for every cell so the reader can check.

Tuned parameters (PROTOCOL rule 4): TWO — position count n in {5,10,20,40} and gross
g in {0.50,0.75,1.00}.  Floor, book family, gate composition and cost rung are reported at
every value with no selection.

Tests (all reported whatever they say)
    A  HARNESS.  numpy simulator vs engine.backtest (max|diff| printed); RULES v1 on this
       panel; the held-name ADV percentiles idea 119 published, recomputed.
    B  CAPACITY LADDER -> the proposed floor.  Held-name ADV p25/p50 and %-of-ADV traded at
       $1M/$10M/$100M for every book at every floor.  The clause is read off this table only.
    C  MAIN GRID.  Every book x floor x g (x n) with full/H1/H2/IS/OOS statistics, turnover,
       realised gross, mean names held, and 4a / 4b verdicts.  Written to .grid.csv.
    D  CLAIM A RE-RUN.  dCAGR and dSharpe of EWgate minus EWall at every floor and g.  Does
       the published -5.4 pp/yr survive being made tradeable, and does its SIGN survive?
    E  CLAIM B RE-RUN.  The four-way n=40 ordering at every floor; report Kendall agreement
       with the published ordering and name every adjacent inversion.
    F  PROTOCOL RULE 8 WALK-FORWARD.  (n,g) chosen on 2010..2016 ONLY, evaluated on
       2017..2026 read once, at EVERY floor, under two selectors fixed in advance:
       S1 = argmax IS Sharpe over the ranked family; S2 = argmax IS Sharpe among cells whose
       IS MaxDD clears 4b's cap.  OOS CAGR/Sharpe/MaxDD vs RULES v1 and vs SPY.
    G  COST ROBUSTNESS.  0 / 10 / 25 bps on the walk-forward picks and on EWall/EWgate, so
       Claim A's "at zero cost" wording can be checked at its own cost rung.
    H  VERDICT-MOVEMENT TABLE.  For every book/g, the 4a and 4b verdict at $0 vs at the
       proposed floor, with the rows whose verdict moves listed explicitly.

Pre-registered predictions (written before any number from tests B-H was read)
    P1  Claim A is a thin-name artefact: |dCAGR(EWgate - EWall)| at the proposed floor is
        less than half its value at floor $0.
    P2  Claim B's four-way ordering does not survive: at the proposed floor at least one
        adjacent pair of the published ordering (none > 200d > vol20 > both) inverts.
    P3  No arm passes 4b at any floor >= $1M.
    P4  The rule-8 pick's OOS Sharpe is below SPY's OOS Sharpe at every floor.

SURVIVORSHIP (stated, not fixed).  data/prices_small.csv.gz is the CURRENT constituent list of
a sub-$2B screen: every name in it survived to 2026, so the small caps that were delisted,
bankrupted or acquired between 2010 and 2025 are absent.  The bias is one-directional and
falls hardest on the beaten-down, thin cohort — which is exactly the cohort a liquidity floor
also removes, so the floor and the bias are CORRELATED and the floor does not correct it.
No level (CAGR, Sharpe) below is an achievable return.  What this run is for is the SIGN and
SIZE of within-panel differences as a function of tradeability, and even those inherit the
bias whenever the floor and the missing cohort overlap; that limitation is restated in the
memo and is the reason the proposed clause is a reporting requirement, not a fix.

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

STEM = "2026-09-05_liquidity-screened-small-panel_cloud"
OUT = ROOT / "research" / "backtests"

FREQ, COST, MAX_VOL = "W", 10.0, 0.60
IS_END, OOS_START = "2016-12-31", "2017-01-01"
FLOORS = [0.0, 1e6, 5e6, 20e6]
NS = [5, 10, 20, 40]
GS = [0.50, 0.75, 1.00]
NARROW_N = 20            # the "narrowest published book" in the capacity criterion
CAP_CAPITAL = 10e6       # $10M
CAP_MAX_FRAC = 0.10      # <= 10% of p25 held-name ADV per rebalance
BAD_MOVE, WARMUP = 1.0, 260

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
    sel = px.drop(columns=["SPY"])
    vol = load_volume(small=True).reindex(index=px.index, columns=sel.columns)
    dv20 = (sel * vol).rolling(20).median()
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


_SC = {}


def prep(sel):
    """Compute baseline.score() once for each scaler setting; everything else reuses it."""
    if not _SC:
        s_on, above, vol20 = score(sel, True)
        s_off, _, _ = score(sel, False)
        _SC.update(on=s_on, off=s_off, above=above, vol20=vol20)
    return _SC


def eligible(sel, dv20, floor, gate):
    """Point-in-time selectable set. gate in {'none','200d','vol60','both'}."""
    c = prep(sel)
    ok = sel.notna()
    if gate in ("200d", "both"):
        ok &= c["above"]
    if gate in ("vol60", "both"):
        ok &= (c["vol20"] < MAX_VOL)
    if floor > 0:
        ok &= (dv20 >= floor)
    return ok


def w_equal(sel, cols, dv20, floor, gate, g):
    ok = eligible(sel, dv20, floor, gate)
    w = ok.astype(float).div(ok.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * g
    return w.reindex(columns=cols).fillna(0.0), ok


def w_ranked(sel, cols, dv20, floor, gate, g, n, vol_scale):
    s = prep(sel)["on" if vol_scale else "off"]
    e = s.where(eligible(sel, dv20, floor, gate))
    rank = e.rank(axis=1, ascending=False)
    hold = (rank <= n) & e.notna()
    w = hold.astype(float).div(hold.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * g
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
    p4a = d["H1"] > base["H1"] and d["H2"] > base["H2"] and d["MaxDD"] >= base["MaxDD"]
    p4b = (d["H1"] > spy["H1"] and d["H2"] > spy["H2"] and d["OOS_Sharpe"] > spy["OOS_Sharpe"]
           and d["MaxDD"] >= 0.60 * spy["MaxDD"] and d["CAGR"] >= 0.70 * spy["CAGR"])
    return p4a, p4b


def capacity(dv20, hold, turn, start):
    """p25/p50 dollar ADV of names actually held, and % of the p25 name's ADV traded."""
    h = hold.loc[start:]
    flat = dv20.loc[start:].where(h).stack().dropna()
    if not len(flat):
        return dict(adv_p25=np.nan, adv_p50=np.nan, pct_adv_p25_10M=np.nan,
                    pct_adv_p50_10M=np.nan, pct_adv_p25_1M=np.nan, pct_adv_p25_100M=np.nan,
                    turnover=np.nan, mean_names=np.nan)
    p25, p50 = float(flat.quantile(0.25)), float(flat.quantile(0.50))
    t = turn.loc[start:]
    yrs = len(t) / 252
    turnover = t.sum() / yrs
    nreb = float((t > 0).sum()) / yrs
    nheld = float(h.sum(axis=1).replace(0, np.nan).mean())
    per_trade_frac = (turnover / nreb) / nheld     # fraction of capital traded per name per rebalance
    out = dict(adv_p25=p25, adv_p50=p50, turnover=turnover, mean_names=nheld)
    for cap in (1e6, 1e7, 1e8):
        out[f"pct_adv_p25_{int(cap/1e6)}M"] = 100 * per_trade_frac * cap / p25
    out["pct_adv_p50_10M"] = 100 * per_trade_frac * 1e7 / p50
    return out


# ------------------------------------------------------------------ main ----
def main():
    px, sel, dv20, dropped = panel()
    cols = px.columns
    start = px.index[WARMUP]
    spy_r = px["SPY"].pct_change().fillna(0.0)
    spy = stats(spy_r, start)
    say(f"[panel] {sel.shape[1]} selectable names + SPY benchmark | {px.index[0].date()} -> "
        f"{px.index[-1].date()} | {len(dropped)} dropped for max_1d_move >= {BAD_MOVE} | "
        f"eval from {start.date()} | IS <= {IS_END} | OOS >= {OOS_START}")
    say(f"[SPY] CAGR {spy['CAGR']:.2%} Sharpe {spy['Sharpe']:.3f} MaxDD {spy['MaxDD']:.1%} "
        f"halves {spy['H1']:.3f}/{spy['H2']:.3f} OOS {spy['OOS_CAGR']:.2%}/{spy['OOS_Sharpe']:.3f}/"
        f"{spy['OOS_MaxDD']:.1%} | 4b bars: MaxDD >= {0.60*spy['MaxDD']:.1%}, "
        f"CAGR >= {0.70*spy['CAGR']:.2%}")

    # ---- A: harness ----
    wv1 = rules_v1_weights(sel).reindex(columns=cols).fillna(0.0)
    r_eng = backtest(px, wv1, cost_bps=COST, freq=FREQ)["returns"]
    r_v1, t_v1, h_v1 = fast_bt(px, wv1)
    say(f"\n[A] engine-equivalence max|diff| = {float((r_v1 - r_eng).abs().max()):.3e}")
    base = stats(r_v1, start)
    base["turnover"] = t_v1.loc[start:].sum() / (len(t_v1.loc[start:]) / 252)
    say(f"[A] live RULES v1 on this panel: CAGR {base['CAGR']:.2%} Sharpe {base['Sharpe']:.3f} "
        f"MaxDD {base['MaxDD']:.1%} halves {base['H1']:.3f}/{base['H2']:.3f} "
        f"OOS {base['OOS_CAGR']:.2%}/{base['OOS_Sharpe']:.3f}/{base['OOS_MaxDD']:.1%} "
        f"turnover {base['turnover']:.1f}x/yr")
    w20, h20 = w_ranked(sel, cols, dv20, 0.0, "both", 0.75, 20, True)
    _r20, t20, _h = fast_bt(px, w20)
    c119 = capacity(dv20, h20, t20, start)
    say(f"[A] idea 119 reproduction — held-name 20d median dollar volume, unscreened ranked "
        f"n=20 book: p25 ${c119['adv_p25']/1e6:.2f}M p50 ${c119['adv_p50']/1e6:.2f}M "
        f"[idea 119 published p25 $0.87M / p50 $4.33M on its own book convention]")

    # ---- book catalogue ----
    def books(floor, g):
        out = {}
        w, ok = w_equal(sel, cols, dv20, floor, "none", g)
        out["EWall"] = (w, ok)
        w, ok = w_equal(sel, cols, dv20, floor, "both", g)
        out["EWgate"] = (w, ok)
        w, ok = w_equal(sel, cols, dv20, floor, "200d", g)
        out["EW200d"] = (w, ok)
        w, ok = w_equal(sel, cols, dv20, floor, "vol60", g)
        out["EWvol60"] = (w, ok)
        for n in NS:
            out[f"R{n}"] = w_ranked(sel, cols, dv20, floor, "both", g, n, True)
            out[f"R{n}u"] = w_ranked(sel, cols, dv20, floor, "none", g, n, False)
        for gt in ("none", "200d", "vol60", "both"):
            out[f"R40-{gt}"] = w_ranked(sel, cols, dv20, floor, gt, g, 40, True)
        return out

    # ---- C: main grid (+ B capacity for every cell) ----
    say(f"\n[C] main grid: {len(FLOORS)} floors x {len(GS)} gross x "
        f"{4 + 2*len(NS) + 4} books = {len(FLOORS)*len(GS)*(4+2*len(NS)+4)} points")
    rows, keep_r = [], {}
    for floor in FLOORS:
        for g in GS:
            for name, (w, ok) in books(floor, g).items():
                r, t, held = fast_bt(px, w)
                d = stats(r, start)
                d.update(book=name, floor_musd=floor / 1e6, g=g,
                         mean_gross=float(held.loc[start:].sum(axis=1).mean()))
                d.update(capacity(dv20, ok, t, start))
                d["pass4a"], d["pass4b"] = verdicts(d, base, spy)
                rows.append(d)
                keep_r[(name, floor, g)] = r
    grid = pd.DataFrame(rows)
    gcols = ["book", "floor_musd", "g", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
             "IS_Sharpe", "IS_MaxDD", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD",
             "turnover", "mean_gross", "mean_names", "adv_p25", "adv_p50",
             "pct_adv_p25_1M", "pct_adv_p25_10M", "pct_adv_p25_100M", "pass4a", "pass4b"]
    grid[gcols].to_csv(OUT / f"{STEM}.grid.csv", index=False)
    say(f"[C] wrote {len(grid)} rows -> {STEM}.grid.csv | 4a passes {int(grid.pass4a.sum())} "
        f"| 4b passes {int(grid.pass4b.sum())}")
    if grid.pass4b.any():
        say("[C] ALL 4b passes:")
        for _, x in grid[grid.pass4b].iterrows():
            say(f"    {x.book} floor ${x.floor_musd:.0f}M g={x.g:.2f}: {x.CAGR:.2%}/"
                f"{x.Sharpe:.3f}/{x.MaxDD:.1%} halves {x.H1:.3f}/{x.H2:.3f} OOS {x.OOS_Sharpe:.3f}")
    else:
        say("[C] no cell passes 4b at any floor.")

    # ---- B: capacity ladder -> the proposed floor ----
    say(f"\n[B] capacity ladder (g=0.75). ADV = 20d median dollar volume of names HELD; "
        f"%ADV = one rebalance's trade in one name at ${CAP_CAPITAL/1e6:.0f}M of capital, "
        f"as a share of that name's ADV")
    say(f"    {'book':>9} {'floor':>7} {'names':>6} {'turn':>6} {'p25 ADV':>9} {'p50 ADV':>9} "
        f"{'%p25@$1M':>9} {'%p25@$10M':>10} {'%p25@$100M':>11}")
    cap_tbl = grid[grid.g == 0.75].copy()
    for _, x in cap_tbl.sort_values(["book", "floor_musd"]).iterrows():
        say(f"    {x.book:>9} ${x.floor_musd:>5.0f}M {x.mean_names:>6.0f} {x.turnover:>5.1f}x "
            f"{x.adv_p25/1e6:>8.2f}M {x.adv_p50/1e6:>8.2f}M {x.pct_adv_p25_1M:>8.2f}% "
            f"{x.pct_adv_p25_10M:>9.1f}% {x.pct_adv_p25_100M:>10.0f}%")
    cap_tbl.to_csv(OUT / f"{STEM}.capacity.csv", index=False)

    narrow = cap_tbl[cap_tbl.book == f"R{NARROW_N}"].sort_values("floor_musd")
    ok_floors = narrow[narrow.pct_adv_p25_10M <= 100 * CAP_MAX_FRAC]
    if len(ok_floors):
        PROPOSED = float(ok_floors.iloc[0].floor_musd) * 1e6
        say(f"[B] PRE-REGISTERED criterion (smallest floor where ${CAP_CAPITAL/1e6:.0f}M trades "
            f"<= {100*CAP_MAX_FRAC:.0f}% of the p25 held-name ADV in the R{NARROW_N} book): "
            f"PROPOSED FLOOR = ${PROPOSED/1e6:.0f}M")
    else:
        PROPOSED = FLOORS[-1]
        say(f"[B] PRE-REGISTERED criterion NOT met at any ladder value — the ladder's top "
            f"(${PROPOSED/1e6:.0f}M) is used for the re-run table and the clause must say the "
            f"panel has no tradeable floor within the ladder.")
    for _, x in narrow.iterrows():
        say(f"    R{NARROW_N} @ ${x.floor_musd:>5.0f}M: %p25@$10M = {x.pct_adv_p25_10M:>7.2f}% "
            f"{'PASS' if x.pct_adv_p25_10M <= 100*CAP_MAX_FRAC else 'fail'}")
    MOVE = PROPOSED if PROPOSED > 0 else FLOORS[1]
    if MOVE != PROPOSED:
        say(f"[B] the criterion is already met with no screen, so the re-run table below uses "
            f"${MOVE/1e6:.0f}M as the contrast floor (a $0 vs $0 table would be empty).")

    # ---- D: Claim A re-run (the gate's cost on small) ----
    say("\n[D] CLAIM A re-run — EWgate minus EWall (published: the gate DESTROYS ~5.4 pp/yr):")
    say(f"    {'floor':>7} {'g':>5} {'CAGR all':>9} {'CAGR gate':>10} {'dCAGR pp':>9} "
        f"{'dSharpe':>8} {'dMaxDD pp':>10} {'names all':>10} {'names gate':>11}")
    drows = []
    for floor in FLOORS:
        for g in GS:
            a = grid[(grid.book == "EWall") & (grid.floor_musd == floor / 1e6) & (grid.g == g)].iloc[0]
            b = grid[(grid.book == "EWgate") & (grid.floor_musd == floor / 1e6) & (grid.g == g)].iloc[0]
            row = dict(floor_musd=floor / 1e6, g=g, CAGR_all=a.CAGR, CAGR_gate=b.CAGR,
                       dCAGR_pp=100 * (b.CAGR - a.CAGR), dSharpe=b.Sharpe - a.Sharpe,
                       dMaxDD_pp=100 * (b.MaxDD - a.MaxDD),
                       names_all=a.mean_names, names_gate=b.mean_names)
            drows.append(row)
            say(f"    ${floor/1e6:>5.0f}M {g:>5.2f} {a.CAGR:>9.2%} {b.CAGR:>10.2%} "
                f"{row['dCAGR_pp']:>9.2f} {row['dSharpe']:>8.3f} {row['dMaxDD_pp']:>10.2f} "
                f"{a.mean_names:>10.0f} {b.mean_names:>11.0f}")
    claimA = pd.DataFrame(drows)
    claimA.to_csv(OUT / f"{STEM}.claimA.csv", index=False)
    for floor in FLOORS:
        s = claimA[claimA.floor_musd == floor / 1e6]
        say(f"    ${floor/1e6:>5.0f}M summary: median dCAGR {s.dCAGR_pp.median():+.2f} pp, "
            f"median dSharpe {s.dSharpe.median():+.3f}, gate HELPS CAGR in "
            f"{int((s.dCAGR_pp>0).sum())}/{len(s)} gross settings")

    # ---- E: Claim B re-run (four-way gate decomposition at n=40) ----
    say("\n[E] CLAIM B re-run — four-way gate decomposition at n=40, scaler on "
        "(published ordering at floor $0: none 0.797 > 200d 0.693 > vol60 0.524 > both 0.441):")
    say(f"    {'floor':>7} {'g':>5} {'none':>7} {'200d':>7} {'vol60':>7} {'both':>7}  ordering")
    PUB = ["none", "200d", "vol60", "both"]
    erows = []
    for floor in FLOORS:
        for g in GS:
            sh = {gt: float(grid[(grid.book == f"R40-{gt}") & (grid.floor_musd == floor / 1e6)
                                 & (grid.g == g)].iloc[0].Sharpe) for gt in PUB}
            order = sorted(PUB, key=lambda k: -sh[k])
            inv = [f"{PUB[i]}<{PUB[i+1]}" for i in range(3) if sh[PUB[i]] < sh[PUB[i + 1]]]
            erows.append(dict(floor_musd=floor / 1e6, g=g, **{f"Sharpe_{k}": v for k, v in sh.items()},
                              ordering=">".join(order), n_inversions=len(inv),
                              inversions=";".join(inv) or "none"))
            say(f"    ${floor/1e6:>5.0f}M {g:>5.2f} {sh['none']:>7.3f} {sh['200d']:>7.3f} "
                f"{sh['vol60']:>7.3f} {sh['both']:>7.3f}  {'>'.join(order)}"
                f"{'  INVERSIONS: ' + ';'.join(inv) if inv else '  (published order holds)'}")
    claimB = pd.DataFrame(erows)
    claimB.to_csv(OUT / f"{STEM}.claimB.csv", index=False)

    # ---- F: PROTOCOL rule 8 walk-forward at every floor ----
    say(f"\n[F] PROTOCOL rule 8 walk-forward — (n,g) chosen on {start.date()}..{IS_END} only over "
        f"the ranked family {{R5,R10,R20,R40}} x g, OOS {OOS_START}.. read once. Two pre-fixed "
        f"selectors; reported at EVERY floor.")
    spy_is = metrics(spy_r.loc[start:IS_END])
    fam_all = grid[grid.book.isin([f"R{n}" for n in NS])].copy()
    fam_all["n"] = fam_all.book.str.slice(1).astype(int)
    wrows = []
    for floor in FLOORS:
        fam = fam_all[fam_all.floor_musd == floor / 1e6]
        picks = [("S1 argmax IS Sharpe", fam.loc[fam.IS_Sharpe.idxmax()])]
        cap = fam[fam.IS_MaxDD >= 0.60 * spy_is["MaxDD"]]
        picks.append(("S2 argmax IS Sharpe | IS MaxDD <= 60% SPY",
                      cap.loc[cap.IS_Sharpe.idxmax()] if len(cap) else None))
        for label, p in picks:
            if p is None:
                say(f"    ${floor/1e6:>5.0f}M {label}: selector EMPTY (no cell clears the IS "
                    f"drawdown cap)")
                wrows.append(dict(floor_musd=floor / 1e6, selector=label, pick="EMPTY"))
                continue
            say(f"    ${floor/1e6:>5.0f}M {label}: pick {p.book} g={p.g:.2f} | IS Sharpe "
                f"{p.IS_Sharpe:.3f} (SPY IS {spy_is['Sharpe']:.3f}) IS MaxDD {p.IS_MaxDD:.1%} "
                f"(SPY IS {spy_is['MaxDD']:.1%})")
            say(f"           OOS {p.OOS_CAGR:>7.2%}/{p.OOS_Sharpe:.3f}/{p.OOS_MaxDD:.1%} "
                f"| SPY OOS {spy['OOS_CAGR']:.2%}/{spy['OOS_Sharpe']:.3f}/{spy['OOS_MaxDD']:.1%} "
                f"| v1 OOS {base['OOS_CAGR']:.2%}/{base['OOS_Sharpe']:.3f}/{base['OOS_MaxDD']:.1%} "
                f"| full {p.CAGR:.2%}/{p.Sharpe:.3f}/{p.MaxDD:.1%} halves {p.H1:.3f}/{p.H2:.3f} "
                f"| 4a {p.pass4a} 4b {p.pass4b}")
            wrows.append(dict(floor_musd=floor / 1e6, selector=label, pick=f"{p.book} g={p.g:.2f}",
                              IS_Sharpe=p.IS_Sharpe, IS_MaxDD=p.IS_MaxDD, OOS_CAGR=p.OOS_CAGR,
                              OOS_Sharpe=p.OOS_Sharpe, OOS_MaxDD=p.OOS_MaxDD,
                              SPY_OOS_CAGR=spy["OOS_CAGR"], SPY_OOS_Sharpe=spy["OOS_Sharpe"],
                              SPY_OOS_MaxDD=spy["OOS_MaxDD"], v1_OOS_Sharpe=base["OOS_Sharpe"],
                              pass4a=p.pass4a, pass4b=p.pass4b))
    pd.DataFrame(wrows).to_csv(OUT / f"{STEM}.walkforward.csv", index=False)

    # ---- G: cost robustness ----
    say("\n[G] cost ladder 0 / 10 / 25 bps (g=0.75) — Claim A's 'at zero cost' wording checked "
        "at its own rung:")
    crows = []
    for floor in (0.0, MOVE):
        for name in ("EWall", "EWgate", f"R{NARROW_N}", f"R{NARROW_N}u"):
            w = books(floor, 0.75)[name][0]
            line = []
            for c in (0.0, 10.0, 25.0):
                r, _, _ = fast_bt(px, w, cost_bps=c)
                d = stats(r, start)
                crows.append(dict(book=name, floor_musd=floor / 1e6, cost_bps=c,
                                  **{k: d[k] for k in ("CAGR", "Sharpe", "MaxDD", "OOS_Sharpe")}))
                line.append(f"{c:>4.0f}bp {d['CAGR']:>8.2%}/{d['Sharpe']:>6.3f}")
            say(f"    ${floor/1e6:>5.0f}M {name:>9}: " + " | ".join(line))
    cl = pd.DataFrame(crows)
    cl.to_csv(OUT / f"{STEM}.costladder.csv", index=False)
    for floor in (0.0, MOVE):
        a = cl[(cl.book == "EWall") & (cl.floor_musd == floor / 1e6) & (cl.cost_bps == 0)].iloc[0]
        b = cl[(cl.book == "EWgate") & (cl.floor_musd == floor / 1e6) & (cl.cost_bps == 0)].iloc[0]
        say(f"    Claim A at 0 bps, floor ${floor/1e6:.0f}M: dCAGR "
            f"{100*(b.CAGR-a.CAGR):+.2f} pp, dSharpe {b.Sharpe-a.Sharpe:+.3f}")

    # ---- H: verdict-movement table ----
    say(f"\n[H] verdict movement, floor $0 -> ${MOVE/1e6:.0f}M (this is the "
        f"'re-run the rows whose verdicts could move' deliverable):")
    say(f"    {'book':>9} {'g':>5} {'CAGR $0':>8} {'CAGR flr':>9} {'Shrp $0':>8} {'Shrp flr':>9} "
        f"{'4a $0':>6} {'4a flr':>7} {'4b $0':>6} {'4b flr':>7}  moved")
    hrows, moved = [], 0
    for name in sorted(set(grid.book)):
        for g in GS:
            a = grid[(grid.book == name) & (grid.floor_musd == 0.0) & (grid.g == g)].iloc[0]
            b = grid[(grid.book == name) & (grid.floor_musd == MOVE / 1e6) & (grid.g == g)].iloc[0]
            mv = (a.pass4a != b.pass4a) or (a.pass4b != b.pass4b)
            moved += int(mv)
            hrows.append(dict(book=name, g=g, CAGR_0=a.CAGR, CAGR_floor=b.CAGR,
                              Sharpe_0=a.Sharpe, Sharpe_floor=b.Sharpe,
                              dCAGR_pp=100 * (b.CAGR - a.CAGR), dSharpe=b.Sharpe - a.Sharpe,
                              pass4a_0=a.pass4a, pass4a_floor=b.pass4a,
                              pass4b_0=a.pass4b, pass4b_floor=b.pass4b, verdict_moved=mv))
            say(f"    {name:>9} {g:>5.2f} {a.CAGR:>8.2%} {b.CAGR:>9.2%} {a.Sharpe:>8.3f} "
                f"{b.Sharpe:>9.3f} {str(a.pass4a):>6} {str(b.pass4a):>7} {str(a.pass4b):>6} "
                f"{str(b.pass4b):>7}  {'YES' if mv else ''}")
    pd.DataFrame(hrows).to_csv(OUT / f"{STEM}.verdicts.csv", index=False)
    say(f"    verdicts moved in {moved}/{len(hrows)} (book, gross) cells; median dCAGR "
        f"{pd.DataFrame(hrows).dCAGR_pp.median():+.2f} pp, median dSharpe "
        f"{pd.DataFrame(hrows).dSharpe.median():+.3f}")

    # ---- predictions ----
    say("\n[P] pre-registered predictions vs outcome")
    a0 = claimA[(claimA.floor_musd == 0.0) & (claimA.g == 0.75)].iloc[0].dCAGR_pp
    af = claimA[(claimA.floor_musd == MOVE / 1e6) & (claimA.g == 0.75)].iloc[0].dCAGR_pp
    say(f"    P1 Claim A halves under the floor: |dCAGR| {abs(a0):.2f} pp -> {abs(af):.2f} pp "
        f"-> {'CONFIRMED' if abs(af) < 0.5 * abs(a0) else 'REFUTED'}  (signs {a0:+.2f} -> {af:+.2f}"
        f"{', SIGN FLIP' if a0 * af < 0 else ''})")
    bf = claimB[(claimB.floor_musd == MOVE / 1e6) & (claimB.g == 0.75)].iloc[0]
    say(f"    P2 Claim B ordering breaks at the floor: {bf.n_inversions} inversions "
        f"({bf.inversions}) -> {'CONFIRMED' if bf.n_inversions > 0 else 'REFUTED'}")
    n4b = int(grid[grid.floor_musd >= 1.0].pass4b.sum())
    say(f"    P3 no 4b pass at any floor >= $1M: {n4b} passes -> "
        f"{'CONFIRMED' if n4b == 0 else 'REFUTED'}")
    wf = pd.DataFrame(wrows)
    s1 = wf[(wf.selector.str.startswith("S1"))]
    beats = s1[s1.OOS_Sharpe >= spy["OOS_Sharpe"]]
    say(f"    P4 rule-8 pick OOS Sharpe < SPY at every floor: SPY OOS {spy['OOS_Sharpe']:.3f}, "
        f"picks " + ", ".join(f"${r.floor_musd:.0f}M {r.OOS_Sharpe:.3f}" for _, r in s1.iterrows())
        + f" -> {'CONFIRMED' if not len(beats) else 'REFUTED'}")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(_tee) + "\n")


if __name__ == "__main__":
    main()
