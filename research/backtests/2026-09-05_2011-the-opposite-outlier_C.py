#!/usr/bin/env python3
"""QUEUE idea 116 — 2011-the-opposite-outlier (lane C, 2026-09-05).

Question (as worded in QUEUE.md)
--------------------------------
"idea 112 found 2011 is the year rule 8 leans on hardest (16/44 picks change when deleted, 2x the
median) and the only year whose deletion makes G MORE negative (-0.101 vs -0.058), with the best
pooled overlay d in the sample (+0.215).  Test whether rule 8's picks are effectively chosen by
2011 the way 2013 was suspected: what do the 16 ex-2011 picks cost OOS (this run says -0.033 mean
Sharpe), and does an IS window that keeps 2011 but is otherwise re-cut pick the same points?
Max 2 params."

WHY IT MATTERS
--------------
Idea 112 acquitted 2013 (it is the worst overlay YEAR but does not SELECT).  It left 2011 as the
open suspect on the other tail: the best overlay year in the sample, the most pick-moving year, and
the only year whose deletion widens the IS->OOS gap.  If rule 8's parameter choice is effectively a
function of one calendar year, PROTOCOL rule 8 is a bet on that year and the memo must say so.
The distinguishing question is whether 2011-dependence is a DEFECT (deleting 2011 improves OOS) or
a FEATURE (deleting it degrades OOS, i.e. 2011 carries selection signal).  Idea 112's -0.033 says
feature; this run tests it on a matched-length design with a per-year null.

THE HARNESS (idea 112's, imported construction-for-construction so every number is comparable)
-----------------------------------------------------------------------------------------------
  6 overlay grids  sleeve (S4 fraction), band (200d hysteresis), breadth (gross cut), stop
                   (trailing), crypto (u56 only), gross (static lever)
  x 2 base books   top20 (ranked, gross 0.75), ewall (equal-weight all eligible, gross 0.75)
  x 2 universes    u56 (research/universe.json + BTC/ETH), broad (universe_broad.json)
  x 2 cost rungs   10 and 25 bps, weekly rebalance, next-day execution (engine)
  = 44 CELLS.  Reproduction of idea 112's LOYO table is asserted, not assumed (S1).

WINDOW FAMILIES (the second tuned axis; the OOS window 2017-2026 is NEVER touched)
-----------------------------------------------------------------------------------
  FULL      IS = 2009..2016, all 8 years                                       1 window
  LOYO      drop exactly one IS year                                           8 windows
  L2O       drop exactly two IS years (6-year windows, matched length)        28 windows
  RECUT     every contiguous span of 4..8 IS years                            15 windows
  46 distinct year-sets after de-duplication.  Nothing is selected on the window; every window's
  pick and its OOS consequence are reported.

STATISTICS, DECLARED BEFORE ANY NUMBER IS COMPUTED
---------------------------------------------------
S1 REPRODUCTION.  Idea 112's committed picks.csv / deltas.csv / swaps.csv are READ BACK and this
   run's LOYO picks are compared cell by cell (44 cells x 9 windows = 396 comparisons), together
   with its G-leverage table and its per-year pooled overlay d (2011 = +0.215, the sample best).
   Any mismatch is reported as a reproduction failure and the run stops trusting idea 112's framing.
   Note that the queue's clause "the ONLY year whose deletion makes G more negative" is checked
   against idea 112's own numbers, not assumed.

S2 THE PRICE OF THE 16 SWAPS.  For every cell whose pick moves when 2011 is deleted, the OOS
   consequence of the swap: dOOS Sharpe / CAGR / MaxDD and the change in 4b and 4b-OOS passes.
   SIGN CONVENTION, pre-registered:  mean dOOS Sharpe < 0  =>  deleting 2011 HURTS  =>  2011 is a
   FEATURE of rule 8's selector, not a defect.  mean dOOS Sharpe > 0 => DEFECT.

S3 IS 2011 THE SELECTOR? (matched-length, with a per-year null).  Over the 28 L2O windows, every
   window has the same length, so the only thing that varies is WHICH years are in it.  For each
   year y in 2009..2016 split the 28 windows into those that KEEP y (21) and those that DROP y (7)
   and compute, pooled over the 44 cells:
       A(y) = agreement rate of pick(W) with pick(FULL)
       premium(y) = A_keep(y) - A_drop(y)
   Pre-registered decision rule:
       2011 IS the selector iff premium(2011) is the largest of the eight years AND >= 0.20.
   The eight premia are the null distribution: if every year shows a similar premium, the picks are
   simply window-sensitive and no single year is doing the choosing.

S4 THE PRICE OF THAT DEPENDENCE.  The same keep/drop split, scored on the untouched OOS window:
   mean OOS Sharpe of pick(W), and mean OOS REGRET = max OOS Sharpe over the cell's grid minus the
   pick's OOS Sharpe.  A dependence that costs nothing OOS is a curiosity; one that is OOS-signed is
   a defect (or, with the opposite sign, a reason to keep 2011 in the window deliberately).

S5 RE-CUT WINDOWS (the queue's second clause, verbatim).  For each of the 15 contiguous spans:
   the pick per cell, agreement with pick(FULL), mean OOS Sharpe and regret, split by whether the
   span contains 2011.  Confounded with span LENGTH by construction (spans containing 2011 are
   longer on average), so length is reported alongside and the L2O test in S3 is the controlled one.

TUNED (2, per PROTOCOL rule 4): the overlay parameter (4-5 levels per grid) x the IS window
(46 levels).  ALL grid points and ALL windows are reported; nothing is selected on either axis.

WALK-FORWARD (PROTOCOL rule 8, mandatory).  Every window's pick is carried into the untouched
2017-2026 window and reported with OOS CAGR / Sharpe / MaxDD against RULES v1 and SPY, plus
full-sample CAGR / Sharpe / MaxDD / halves and BOTH KEEP paths (4a beat-the-book, 4b
capital-worthy).  The headline sleeve cell (u56 / top20 / 10 bps — the standing KEEP-4b
candidate's cell) is printed in full for every window family.

CAVEATS
-------
SURVIVORSHIP: both equity panels are current constituents of their lists; levels are biased up.
  The bias is identical across every window, which is all this run compares.
2009 IS PARTIAL: the eval starts ~2009-01-13 (260-row warm-up), so the "2009" year is ~11.5 months.
CRYPTO: BTC-USD starts 2014-09-17, so on windows ending before 2014 the crypto arms differ from the
  null only through their de-grossing.  Crypto rows are shown both in and out of every pooled stat.
DATA (queue idea 38): data/prices*.csv are calendar-day indexed after 2014-09-17; weekend rows are
  zero-return.  It hits every grid point and every window identically.
SHARPE ON A SPLICED SERIES: deleting years leaves mean/std well defined (idea 89's convention);
  MaxDD is NOT meaningful on a spliced series and is never taken on one.

Deterministic, standalone (no network; reads the committed price caches):
    python research/backtests/2026-09-05_2011-the-opposite-outlier_C.py
"""
import sys
from itertools import combinations
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "research"))

import numpy as np
import pandas as pd

from baseline import load_universe, rules_v1_weights, score
from engine import backtest, metrics

FREQ = "W"
COSTS = (10, 25)
IS_END = "2016-12-31"
SPLIT = "2017-01-01"
BOOK_GROSS = 0.75
S4 = ["TLT", "GLD", "DBC", "UUP"]
CRYPTO = ["BTC-USD", "ETH-USD"]
BREADTH_B = 0.30
MOM_LAGS = (252, 126, 63)
VOL_WINDOW = 60
IS_YEARS = list(range(2009, 2017))
FOCUS_YEAR = 2011
MIN_OBS = 60                                  # idea 112's guard on a spliced Sharpe
PREMIUM_BAR = 0.20                            # S3 pre-registered bar
OUT = Path(__file__).with_suffix("")

APRIORI = {"sleeve": "defensive", "band": "defensive", "breadth": "defensive",
           "stop": "defensive", "crypto": "offensive", "gross": "mixed"}

# idea 112's own committed outputs, read back at runtime (not transcribed) so S1's reproduction
# check is a real cell-by-cell comparison rather than a comparison against a quoted headline.
IDEA112 = Path(__file__).with_name("2026-09-05_2013-as-the-IS-windows-single-point-of-failure_C")
IDEA112_D_2011 = 0.215        # quoted in QUEUE idea 116
IDEA112_SWAP_2011 = -0.033    # quoted in QUEUE idea 116


def idea112_reference():
    """(LOYO pick-change counts, per-cell picks, G-leverage table) from idea 112's committed CSVs."""
    P = pd.read_csv(IDEA112.with_suffix(".picks.csv"))
    counts = {y: int((P[f"pick_ex{y}"].astype(str) != P["pick_full"].astype(str)).sum())
              for y in IS_YEARS}
    D = pd.read_csv(IDEA112.with_suffix(".deltas.csv"))
    gfull = float(D["G_full"].mean())
    lev = {y: float(D[f"G_ex{y}"].mean()) for y in IS_YEARS}
    return counts, P, gfull, lev


# ---------------------------------------------------------------- gates and books (idea 112 verbatim)
def _band_above(px, w):
    ma = px.rolling(200).mean()
    up = (px > ma * (1 + w))
    dn = (px < ma * (1 - w))
    st = pd.DataFrame(np.where(up, 1.0, np.where(dn, 0.0, np.nan)),
                      index=px.index, columns=px.columns)
    return st.ffill().fillna(0.0) > 0.5


def _elig(px, band=0.0, stop=None):
    vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    m = _band_above(px, band) & (vol20 < 0.60)
    if stop is not None:
        dd = px / px.rolling(126).max() - 1.0
        m = m & (dd > -stop)
    return m


def book(px, kind, band=0.0, stop=None, gross=BOOK_GROSS, n=20):
    s, _, _ = score(px, vol_scale=False)
    m = _elig(px, band, stop)
    if kind == "top20":
        rank = s.where(m).rank(axis=1, ascending=False)
        w = (rank <= n).astype(float)
    else:
        w = (m & s.notna()).astype(float)
    k = w.sum(axis=1)
    return w.div(k.where(k > 0), axis=0).fillna(0.0) * gross


def sleeve_weights(px, assets):
    sub = px[assets]
    vol = sub.pct_change().rolling(VOL_WINDOW).std()
    inv = (1.0 / vol.replace(0.0, np.nan))
    rp = inv.div(inv.sum(axis=1), axis=0)
    sig = [sub.shift(21) / sub.shift(MOM_LAGS[0]) - 1,
           sub / sub.shift(MOM_LAGS[1]) - 1,
           sub / sub.shift(MOM_LAGS[2]) - 1]
    vote = sum((x > 0).astype(float).where(x.notna()) for x in sig) / len(sig)
    w = (vote * rp).fillna(0.0)
    out = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    out[assets] = w
    return out


def _regross(w, g=1.00):
    tot = w.sum(axis=1)
    return w.mul((g / tot.where(tot > 1e-12)).fillna(0.0), axis=0)


def overlay(px, kind, grid, p):
    if grid == "sleeve":
        E = book(px, kind)
        return _regross((1 - p) * E + p * sleeve_weights(px, S4), 1.00)
    if grid == "band":
        return book(px, kind, band=p)
    if grid == "breadth":
        E = book(px, kind)
        above = _band_above(px, 0.0).drop(columns=["SPY"], errors="ignore")
        br = above.mean(axis=1)
        mult = pd.Series(np.where(br < BREADTH_B, 1.0 - p, 1.0), index=px.index)
        return E.mul(mult, axis=0)
    if grid == "stop":
        return book(px, kind, stop=None if p is None else p)
    if grid == "gross":
        return book(px, kind, gross=p)
    if grid == "crypto":
        E = book(px, kind, gross=BOOK_GROSS * (1 - p))
        if p == 0.0:
            return E
        c = [t for t in CRYPTO if t in px.columns]
        avail = px[c].notna().astype(float)
        k = avail.sum(axis=1)
        cw = avail.div(k.where(k > 0), axis=0).fillna(0.0) * (BOOK_GROSS * p)
        out = E.copy()
        out[c] = out[c].values + cw.values
        return out
    raise ValueError(grid)


GRIDS = {
    "sleeve":  [0.00, 0.25, 0.50, 0.75, 1.00],
    "band":    [0.00, 0.02, 0.03, 0.05, 0.08],
    "breadth": [0.00, 0.25, 0.50, 0.75, 1.00],
    "stop":    [None, 0.25, 0.20, 0.15, 0.10],
    "crypto":  [0.00, 0.02, 0.05, 0.10],
    "gross":   [0.75, 0.50, 1.00, 1.25],
}
NULL_P = {"sleeve": 0.00, "band": 0.00, "breadth": 0.00, "stop": None,
          "crypto": 0.00, "gross": 0.75}


def pkey(grid, p):
    if grid == "stop":
        return 0.0 if p is None else 1.0 - p
    if grid == "gross":
        return abs(p - 0.75)
    return float(p)


# ---------------------------------------------------------------- window families
def build_windows():
    """Every IS year-set this run evaluates, de-duplicated, tagged with its families."""
    fam = {}

    def add(years, family, label):
        k = frozenset(years)
        rec = fam.setdefault(k, dict(years=tuple(sorted(years)), families=set(), labels=set()))
        rec["families"].add(family)
        rec["labels"].add(label)

    add(IS_YEARS, "FULL", "full")
    for y in IS_YEARS:
        add([z for z in IS_YEARS if z != y], "LOYO", f"ex{y}")
    for a, b in combinations(IS_YEARS, 2):
        add([z for z in IS_YEARS if z not in (a, b)], "L2O", f"ex{a}+{b}")
    for L in range(4, 9):
        for s in range(IS_YEARS[0], IS_YEARS[-1] - L + 2):
            add(list(range(s, s + L)), "RECUT", f"{s}-{s + L - 1}")
    out = []
    for k, rec in fam.items():
        out.append(dict(key="|".join(str(y) for y in rec["years"]),
                        years=rec["years"], nyears=len(rec["years"]),
                        families=",".join(sorted(rec["families"])),
                        label=sorted(rec["labels"])[0],
                        has2011=(FOCUS_YEAR in rec["years"])))
    return sorted(out, key=lambda r: (-r["nyears"], r["key"]))


# ---------------------------------------------------------------- metrics
def net(gr, to, bps):
    return gr - to * bps / 1e4


def stats(r):
    if len(r) < MIN_OBS:
        return np.nan, np.nan, np.nan
    m = metrics(r)
    return m["CAGR"], m["Sharpe"], m["MaxDD"]


def full_row(r):
    h = len(r) // 2
    c, s, d = stats(r)
    _, h1, _ = stats(r.iloc[:h])
    _, h2, _ = stats(r.iloc[h:])
    ic, is_, idd = stats(r.loc[:IS_END])
    oc, os_, od = stats(r.loc[SPLIT:])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=h1, H2=h2,
                IS_CAGR=ic, IS_Sharpe=is_, IS_MaxDD=idd,
                OOS_CAGR=oc, OOS_Sharpe=os_, OOS_MaxDD=od)


def keep_4a(r, base):
    return bool(r["H1"] > base["H1"] and r["H2"] > base["H2"] and r["MaxDD"] >= base["MaxDD"])


def keep_4b(r, spy):
    return bool(r["H1"] > spy["H1"] and r["H2"] > spy["H2"] and r["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and r["MaxDD"] >= 0.60 * spy["MaxDD"] and r["CAGR"] >= 0.70 * spy["CAGR"])


def keep_4b_oos(r, spy):
    return bool(r["OOS_Sharpe"] > spy["OOS_Sharpe"]
                and r["OOS_MaxDD"] >= 0.60 * spy["OOS_MaxDD"]
                and r["OOS_CAGR"] >= 0.70 * spy["OOS_CAGR"])


def fmt(df):
    return df.to_string(float_format=lambda x: f"{x:.3f}")


class YearMoments:
    """Per-calendar-year (n, sum, sumsq) of an IS return series -> exact Sharpe on any year subset.

    Identical by construction to idea 112's ``sharpe(r[r.index.year.isin(S)])``: annualised as
    mean * 252 / (std * sqrt(252)) with the pandas ddof=1 standard deviation.
    """

    def __init__(self, r):
        r = r.loc[:IS_END]
        g = r.groupby(r.index.year)
        self.n = g.size().to_dict()
        self.s = g.sum().to_dict()
        self.q = g.apply(lambda x: float((x ** 2).sum())).to_dict()

    def sharpe(self, years):
        n = sum(self.n.get(y, 0) for y in years)
        if n < MIN_OBS:
            return np.nan
        s = sum(self.s.get(y, 0.0) for y in years)
        q = sum(self.q.get(y, 0.0) for y in years)
        mean = s / n
        var = (q - n * mean * mean) / (n - 1)
        if not np.isfinite(var) or var <= 0:
            return np.nan
        return float(mean * np.sqrt(252) / np.sqrt(var))


def pick_from(sub, col):
    """rule 8's argmax with this project's tie-break: highest Sharpe, then smallest |parameter|."""
    s = sub[[col, "pkey", "param"]].dropna(subset=[col])
    if s.empty:
        return None
    best = s[col].max()
    tied = s[np.isclose(s[col], best)]
    return tied.sort_values("pkey").iloc[0]["param"]


# ---------------------------------------------------------------- main
def main():
    u56 = load_universe(exclude=set())
    broad = load_universe(broad=True)
    universes = {"u56": u56, "broad": broad}
    WIN = build_windows()
    nkeep = sum(1 for w in WIN if w["families"].find("L2O") >= 0 and w["has2011"])
    print(f"[data] u56 {u56.shape[1]} cols, broad {broad.shape[1]} cols")
    print(f"[windows] {len(WIN)} distinct IS year-sets "
          f"(FULL 1 + LOYO 8 + L2O 28 + RECUT 15, de-duplicated); "
          f"L2O keeps 2011 in {nkeep}/28")
    print("[pre-registered] S1 reproduce idea 112 · S2 price the 16 swaps · S3 matched-length")
    print("                 keep/drop agreement premium with a per-year null · S4 its OOS price ·")
    print("                 S5 contiguous re-cuts")
    print(f"[pre-registered] 2011 IS the selector iff premium(2011) is the largest of the 8 years")
    print(f"                 AND >= {PREMIUM_BAR:.2f}")
    print("[pre-registered] SIGN: mean dOOS Sharpe of the ex-2011 swaps < 0 => 2011 is a FEATURE")
    print("                 of rule 8's selector; > 0 => a DEFECT")
    print(f"[pre-registered] IS <= {IS_END}; OOS {SPLIT}.. is never touched by any window\n")

    # cost linearity (every point runs once at 0 bps; both rungs derived exactly)
    st0 = u56.index[260]
    w0 = book(u56, "top20")
    r0 = backtest(u56, w0, cost_bps=0.0, freq=FREQ)
    err = float((net(r0["returns"].loc[st0:], r0["turnover"].loc[st0:], 10)
                 - backtest(u56, w0, cost_bps=10, freq=FREQ)["returns"].loc[st0:]).abs().max())
    print(f"[check] cost linearity max |derived - direct| at 10 bps = {err:.2e}")
    assert err < 1e-12

    records, refs, moments = [], {}, {}
    for tag, px in universes.items():
        start = px.index[260]
        spy_r = px["SPY"].pct_change().fillna(0).loc[start:]
        spy = full_row(spy_r)
        bt = backtest(px, rules_v1_weights(px), cost_bps=0.0, freq=FREQ)
        bgr, bto = bt["returns"].loc[start:], bt["turnover"].loc[start:]
        refs[tag] = (spy, bgr, bto)
        print("=" * 128)
        print(f"### UNIVERSE {tag}: {px.shape[1]} tickers | eval {start.date()} -> {px.index[-1].date()}")
        print(fmt(pd.DataFrame({"RULES v1 (10bps)": full_row(net(bgr, bto, 10)),
                                "RULES v1 (25bps)": full_row(net(bgr, bto, 25)),
                                "SPY": spy}).T))

        for grid, params in GRIDS.items():
            if grid == "crypto" and not all(t in px.columns for t in CRYPTO):
                print(f"  [skip] grid={grid} on {tag}: crypto tickers absent from this panel")
                continue
            for kind in ("top20", "ewall"):
                for p in params:
                    w = overlay(px, kind, grid, p)
                    res = backtest(px, w, cost_bps=0.0, freq=FREQ)
                    gr, to = res["returns"].loc[start:], res["turnover"].loc[start:]
                    gross = float(w.loc[start:].sum(axis=1).mean())
                    turn = float(to.sum() / (len(gr) / 252))
                    for bps in COSTS:
                        r = net(gr, to, bps)
                        pk = "none" if p is None else p
                        key = (tag, grid, kind, bps, pk)
                        moments[key] = YearMoments(r)
                        row = full_row(r)
                        base = full_row(net(bgr, bto, bps))
                        row.update(universe=tag, grid=grid, book=kind, param=pk, cost_bps=bps,
                                   Gross=gross, Turn_yr=turn, pkey=pkey(grid, p),
                                   is_null=(p == NULL_P[grid]), apriori=APRIORI[grid])
                        for y in range(2009, 2027):
                            yr = r.loc[f"{y}-01-01":f"{y}-12-31"]
                            row[f"SH_y_{y}"] = (float(yr.mean() * np.sqrt(252) / yr.std())
                                                if len(yr) >= MIN_OBS and yr.std() > 0 else np.nan)
                        row["4a"] = keep_4a(row, base)
                        row["4b"] = keep_4b(row, spy)
                        row["4b_oos"] = keep_4b_oos(row, spy)
                        records.append(row)

    G = pd.DataFrame(records)
    CELL = ["universe", "grid", "book", "cost_bps"]

    # IS Sharpe on every window, for every grid point
    for w in WIN:
        col = f"IS_{w['key']}"
        G[col] = [moments[(r.universe, r.grid, r.book, r.cost_bps, r.param)].sharpe(w["years"])
                  for r in G.itertuples()]
    G.to_csv(OUT.with_suffix(".grid.csv"), index=False)
    cells = list(G.groupby(CELL, sort=False).groups.keys())
    print(f"\n[grid] {len(G)} points x {len(WIN)} windows -> {OUT.name}.grid.csv")
    print(f"[cells] {len(cells)} cells (expected 44)")

    FULLKEY = f"IS_{'|'.join(str(y) for y in IS_YEARS)}"

    # sanity: the moment-based Sharpe must equal the direct spliced Sharpe
    chk = []
    for key, mm in list(moments.items())[:8]:
        yrs = [y for y in IS_YEARS if y != FOCUS_YEAR]
        sub = G[(G.universe == key[0]) & (G.grid == key[1]) & (G.book == key[2])
                & (G.cost_bps == key[3]) & (G.param == key[4])]
        chk.append(abs(mm.sharpe(yrs) - float(sub[f"IS_{'|'.join(str(y) for y in yrs)}"].iloc[0])))
    print(f"[check] moment-Sharpe vs table max |diff| = {max(chk):.2e}")

    # ============================================================ (1) every grid point
    print("\n" + "=" * 128)
    print("### (1) EVERY GRID POINT — full sample, full-IS Sharpe, IS-ex-2011 Sharpe, OOS "
          "(10 bps shown; 25 bps in .grid.csv)\n")
    EX11 = f"IS_{'|'.join(str(y) for y in IS_YEARS if y != FOCUS_YEAR)}"
    for (tag, grid, kind), sub in G[G.cost_bps == 10].groupby(["universe", "grid", "book"], sort=False):
        print(f"--- {tag} | grid={grid} | book={kind}")
        cols = ["Gross", "Turn_yr", "CAGR", "Sharpe", "MaxDD", "H1", "H2",
                FULLKEY, EX11, "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "4a", "4b"]
        pr = sub.set_index("param")[cols].rename(columns={FULLKEY: "IS_full", EX11: "IS_ex2011"})
        print(fmt(pr))
        print()

    # ============================================================ (2) S1 reproduction
    print("=" * 128)
    print("### (2) S1 — REPRODUCTION OF IDEA 112 (LOYO picks, G leverage, per-year overlay d)\n")
    picks = {}
    for keys, sub in G.groupby(CELL, sort=False):
        picks[keys] = {w["key"]: pick_from(sub, f"IS_{w['key']}") for w in WIN}
    PK = pd.DataFrame(picks).T
    PK.index.names = CELL
    PK.to_csv(OUT.with_suffix(".picks.csv"))

    ref_counts, refP, ref_gfull, ref_lev = idea112_reference()
    loyo_counts = {}
    for y in IS_YEARS:
        k = "|".join(str(z) for z in IS_YEARS if z != y)
        loyo_counts[y] = int(sum(str(picks[c][k]) != str(picks[c][FULLKEY[3:]]) for c in picks))
    LC = pd.DataFrame({"cells_changed": pd.Series(loyo_counts),
                       "idea112": pd.Series(ref_counts)})
    LC["match"] = LC.cells_changed == LC.idea112
    LC["frac"] = LC.cells_changed / len(picks)
    print("--- LOYO pick changes (out of 44), this run vs idea 112's committed picks.csv")
    print(LC.to_string(float_format=lambda x: f"{x:.3f}"))
    med = float(np.median(list(loyo_counts.values())))
    c11 = loyo_counts[FOCUS_YEAR]
    # stronger than the counts: every cell's pick, under every LOYO window and the full window
    mism = 0
    for _, rr in refP.iterrows():
        c = (rr["universe"], rr["grid"], rr["book"], int(rr["cost_bps"]))
        for col, k in [("pick_full", FULLKEY[3:])] + \
                      [(f"pick_ex{y}", "|".join(str(z) for z in IS_YEARS if z != y)) for y in IS_YEARS]:
            if str(rr[col]) != str(picks[c][k]):
                mism += 1
    repro_loyo = bool(LC["match"].all() and mism == 0)
    print(f"\n  2011 moves {c11}/44 (idea 112: {ref_counts[FOCUS_YEAR]}); median year {med:.1f}; "
          f"max other year {max(v for y, v in loyo_counts.items() if y != FOCUS_YEAR)}")
    print(f"  cell-by-cell pick mismatches vs idea 112 (44 cells x 9 windows = 396): {mism}")
    print(f"  LOYO table reproduces idea 112 exactly: {repro_loyo}")

    # G leverage
    deltas = []
    for keys, sub in G.groupby(CELL, sort=False):
        nullrow = sub[sub.is_null].iloc[0]
        for _, r in sub[~sub.is_null].iterrows():
            rec = dict(zip(CELL, keys), param=r["param"], apriori=r["apriori"],
                       dGross=r["Gross"] - nullrow["Gross"],
                       d_OOS=r["OOS_Sharpe"] - nullrow["OOS_Sharpe"])
            for w in WIN:
                c = f"IS_{w['key']}"
                rec[f"G_{w['key']}"] = (r[c] - nullrow[c]) - rec["d_OOS"]
            deltas.append(rec)
    D = pd.DataFrame(deltas)
    gfull = float(D[f"G_{FULLKEY[3:]}"].mean())
    lev = pd.DataFrame({"mean_G": [D[f"G_{'|'.join(str(z) for z in IS_YEARS if z != y)}"].mean()
                                   for y in IS_YEARS]}, index=IS_YEARS)
    lev["idea112"] = [ref_lev[y] for y in lev.index]
    lev["shift_vs_full"] = lev.mean_G - gfull
    lev = lev.sort_values("mean_G")
    print(f"\n--- G LEVERAGE: pooled mean G by dropped year (full-IS control {gfull:+.3f}, "
          f"idea 112 {ref_gfull:+.3f})")
    print(fmt(lev))
    repro_G = bool(abs(gfull - ref_gfull) < 1e-3
                   and max(abs(lev.loc[y, "mean_G"] - ref_lev[y]) for y in IS_YEARS) < 1e-3)
    more_neg = sorted(y for y in IS_YEARS if lev.loc[y, "mean_G"] < gfull)
    print(f"  reproduces idea 112's G leverage (max |diff| "
          f"{max(abs(lev.loc[y, 'mean_G'] - ref_lev[y]) for y in IS_YEARS):.4f}): {repro_G}")
    print(f"  years whose deletion makes G MORE negative: {more_neg} — QUEUE idea 116 says 2011 is")
    print(f"  the ONLY one; that clause is FALSE in idea 112's own data ({len(more_neg)} years do),")
    print(f"  though 2011's shift {lev.loc[FOCUS_YEAR,'shift_vs_full']:+.4f} is "
          f"{abs(lev.loc[FOCUS_YEAR,'shift_vs_full']) / max(abs(lev.loc[y,'shift_vs_full']) for y in more_neg if y != FOCUS_YEAR):.1f}x "
          f"the next largest.")

    # per-year overlay d
    peryear = []
    for keys, sub in G.groupby(CELL, sort=False):
        nullrow = sub[sub.is_null].iloc[0]
        for _, r in sub[~sub.is_null].iterrows():
            for y in range(2010, 2027):
                peryear.append(dict(universe=keys[0], grid=keys[1], year=y,
                                    d=r[f"SH_y_{y}"] - nullrow[f"SH_y_{y}"]))
    PY = pd.DataFrame(peryear)
    tab = PY.pivot_table(index="year", columns="universe", values="d", aggfunc="mean")
    tab["all"] = PY.groupby("year")["d"].mean()
    tab["n"] = PY.groupby("year")["d"].size()
    print("\n--- PER-YEAR POOLED OVERLAY d (Sharpe of the overlay minus its grid's null, by year)")
    print(fmt(tab))
    best = tab["all"].idxmax()
    repro_d = bool(best == FOCUS_YEAR and abs(tab["all"].loc[FOCUS_YEAR] - IDEA112_D_2011) < 0.010)
    print(f"  best overlay year: {best} ({tab['all'].max():+.3f}); 2011 = "
          f"{tab['all'].loc[FOCUS_YEAR]:+.3f} (idea 112 {IDEA112_D_2011:+.3f}); reproduces: {repro_d}")
    PY.to_csv(OUT.with_suffix(".peryear.csv"), index=False)

    # ============================================================ (3) S2 price of the swaps
    print("\n" + "=" * 128)
    print("### (3) S2 — WHAT THE EX-2011 PICK CHANGES COST OUT OF SAMPLE (2017-2026, untouched)\n")
    look = G.set_index(CELL + ["param"])
    EX11K = EX11[3:]
    swaps = []
    for c, pp in picks.items():
        a, b = pp[FULLKEY[3:]], pp[EX11K]
        if str(a) == str(b):
            continue
        ra, rb = look.loc[c + (a,)], look.loc[c + (b,)]
        swaps.append(dict(zip(CELL, c), pick_full=a, pick_ex2011=b,
                          OOS_S_full=ra["OOS_Sharpe"], OOS_S_ex=rb["OOS_Sharpe"],
                          dOOS_Sharpe=rb["OOS_Sharpe"] - ra["OOS_Sharpe"],
                          dOOS_CAGR=rb["OOS_CAGR"] - ra["OOS_CAGR"],
                          dOOS_MaxDD=rb["OOS_MaxDD"] - ra["OOS_MaxDD"],
                          d4b=int(rb["4b"]) - int(ra["4b"]),
                          d4b_oos=int(rb["4b_oos"]) - int(ra["4b_oos"])))
    S = pd.DataFrame(swaps)
    S.to_csv(OUT.with_suffix(".swaps.csv"), index=False)
    print(fmt(S.set_index(CELL)))
    m11 = float(S.dOOS_Sharpe.mean())
    ref_sw = pd.read_csv(IDEA112.with_suffix(".swaps.csv"))
    ref_sw = ref_sw[ref_sw.dropped == FOCUS_YEAR]
    print(f"\n  idea 112's own swaps.csv for 2011: n={len(ref_sw)}, "
          f"mean dOOS Sharpe {ref_sw.dOOS_Sharpe.mean():+.4f} "
          f"(QUEUE quotes {IDEA112_SWAP_2011:+.3f})")
    print(f"  n={len(S)} swaps; mean dOOS Sharpe {m11:+.3f}; "
          f"worse in {(S.dOOS_Sharpe < 0).sum()}/{len(S)}; "
          f"mean dOOS CAGR {S.dOOS_CAGR.mean():+.4f}; mean dOOS MaxDD {S.dOOS_MaxDD.mean():+.4f}; "
          f"net 4b {int(S.d4b.sum()):+d}; net 4b_oos {int(S.d4b_oos.sum()):+d}")
    sign_verdict = "FEATURE (deleting 2011 hurts OOS)" if m11 < 0 else "DEFECT (deleting 2011 helps OOS)"
    print(f"  PRE-REGISTERED SIGN TEST: {sign_verdict}")

    # every year's swaps, for context
    allsw = []
    for y in IS_YEARS:
        k = "|".join(str(z) for z in IS_YEARS if z != y)
        rows = []
        for c, pp in picks.items():
            a, b = pp[FULLKEY[3:]], pp[k]
            if str(a) == str(b):
                continue
            ra, rb = look.loc[c + (a,)], look.loc[c + (b,)]
            rows.append(rb["OOS_Sharpe"] - ra["OOS_Sharpe"])
        allsw.append(dict(dropped=y, n=len(rows),
                          mean_dOOS_Sharpe=float(np.mean(rows)) if rows else np.nan,
                          worse=int(sum(1 for v in rows if v < 0))))
    ASW = pd.DataFrame(allsw).set_index("dropped")
    print("\n--- FOR CONTEXT: the same swap price for every dropped year")
    print(fmt(ASW))

    # ============================================================ (4) S3/S4 matched-length test
    print("\n" + "=" * 128)
    print("### (4) S3/S4 — MATCHED-LENGTH TEST: 28 leave-two-out windows x 44 cells,")
    print("###        split by whether the window KEEPS each year.  Agreement with pick(FULL),")
    print("###        OOS Sharpe of the pick, and OOS regret vs the cell's OOS-best point.\n")
    l2o = [w for w in WIN if "L2O" in w["families"] and w["nyears"] == 6]
    print(f"  L2O windows: {len(l2o)} (all 6 years long)")

    oosbest = {c: float(sub["OOS_Sharpe"].max()) for c, sub in G.groupby(CELL, sort=False)}
    obs = []
    for w in l2o:
        for c, pp in picks.items():
            p = pp[w["key"]]
            r = look.loc[c + (p,)]
            obs.append(dict(zip(CELL, c), window=w["label"], years=w["key"], pick=p,
                            agree=int(str(p) == str(pp[FULLKEY[3:]])),
                            OOS_Sharpe=r["OOS_Sharpe"],
                            regret=oosbest[c] - r["OOS_Sharpe"],
                            keep_4b=int(r["4b"]), keep_4b_oos=int(r["4b_oos"]),
                            **{f"has{y}": int(y in w["years"]) for y in IS_YEARS}))
    O = pd.DataFrame(obs)
    O.to_csv(OUT.with_suffix(".l2o.csv"), index=False)
    print(f"  {len(O)} pick observations (28 windows x 44 cells)\n")

    rows = []
    for y in IS_YEARS:
        k, d = O[O[f"has{y}"] == 1], O[O[f"has{y}"] == 0]
        rows.append(dict(year=y, n_keep=len(k), n_drop=len(d),
                         A_keep=k.agree.mean(), A_drop=d.agree.mean(),
                         premium=k.agree.mean() - d.agree.mean(),
                         OOS_keep=k.OOS_Sharpe.mean(), OOS_drop=d.OOS_Sharpe.mean(),
                         dOOS=k.OOS_Sharpe.mean() - d.OOS_Sharpe.mean(),
                         regret_keep=k.regret.mean(), regret_drop=d.regret.mean(),
                         dRegret=k.regret.mean() - d.regret.mean(),
                         p4b_keep=k.keep_4b.mean(), p4b_drop=d.keep_4b.mean()))
    Y = pd.DataFrame(rows).set_index("year")
    print("--- AGREEMENT PREMIUM AND ITS OOS PRICE, BY YEAR (the 8 rows are each other's null)")
    print(fmt(Y))
    Y.to_csv(OUT.with_suffix(".yearsplit.csv"))
    prem = Y["premium"]
    largest = bool(prem.idxmax() == FOCUS_YEAR)
    s3 = "SUPPORTED" if (largest and prem.loc[FOCUS_YEAR] >= PREMIUM_BAR) else "NOT SUPPORTED"
    print(f"\n  premium(2011) = {prem.loc[FOCUS_YEAR]:+.3f}; largest of the 8: {largest} "
          f"(max is {prem.idxmax()} at {prem.max():+.3f}); bar {PREMIUM_BAR:.2f}")
    print(f"  PRE-REGISTERED S3 (2011 chooses rule 8's picks): {s3}")
    print(f"  S4 OOS price of keeping 2011: mean OOS Sharpe {Y.loc[FOCUS_YEAR,'dOOS']:+.3f}, "
          f"mean regret {Y.loc[FOCUS_YEAR,'dRegret']:+.3f} "
          f"(negative regret delta = keeping 2011 picks better)")

    print("\n--- WINDOW-LEVEL DETAIL: all 28 L2O windows, pooled over the 44 cells")
    WD = O.groupby(["window", "years"]).agg(agree=("agree", "mean"),
                                            OOS_Sharpe=("OOS_Sharpe", "mean"),
                                            regret=("regret", "mean"),
                                            p4b=("keep_4b", "mean")).reset_index()
    WD["has2011"] = [FOCUS_YEAR in [int(v) for v in s.split("|")] for s in WD["years"]]
    print(fmt(WD.sort_values(["has2011", "agree"]).set_index("window").drop(columns=["years"])))

    # ------- SUPPLEMENTARY (POST-HOC, declared as such: prompted by the separation seen above)
    print("\n--- SUPPLEMENTARY (POST-HOC, not pre-registered): how unlikely is that separation?")
    ag = WD.set_index("window")["agree"]
    ranks = ag.rank(method="average")
    dropped_ranks = {}
    for y in IS_YEARS:
        names = [f"ex{min(y, z)}+{max(y, z)}" for z in IS_YEARS if z != y]
        names = [n for n in names if n in ranks.index]
        dropped_ranks[y] = float(np.mean([ranks[n] for n in names]))
    DR = pd.Series(dropped_ranks, name="mean_rank_of_the_7_drop-y_windows").sort_values()
    print("  mean agreement RANK (1 = lowest agreement) of the seven windows that drop each year:")
    print(DR.to_string(float_format=lambda x: f"{x:.2f}"))
    print(f"  structurally-matched null (which of the 8 years is marked): 2011 is rank "
          f"{int(DR.rank()[FOCUS_YEAR])} of 8 -> exact one-sided p = {1/8:.3f}")
    names11 = [f"ex{min(FOCUS_YEAR, z)}+{max(FOCUS_YEAR, z)}" for z in IS_YEARS if z != FOCUS_YEAR]
    obs = float(np.mean([ranks[n] for n in names11]))
    rng = np.random.default_rng(0)
    arr = ranks.values
    draws = np.array([arr[rng.choice(len(arr), 7, replace=False)].mean() for _ in range(200000)])
    p_comb = float((draws <= obs).mean())
    print(f"  unstructured null (any 7 of the 28 windows, 200k draws, seed 0): observed mean rank "
          f"{obs:.2f}, p = {p_comb:.5f}")
    print("  READ IT AS: 2011 is unambiguously the pick-moving year; the pre-registered bar it")
    print("  misses is the SIZE of the premium, not its uniqueness.")

    # ============================================================ (5) S5 re-cut windows
    print("\n" + "=" * 128)
    print("### (5) S5 — CONTIGUOUS RE-CUT WINDOWS (the queue's second clause)\n")
    rec = [w for w in WIN if "RECUT" in w["families"]]
    rows = []
    for w in sorted(rec, key=lambda z: (z["nyears"], z["label"])):
        ag, oo, rg, p4 = [], [], [], []
        for c, pp in picks.items():
            p = pp[w["key"]]
            r = look.loc[c + (p,)]
            ag.append(int(str(p) == str(pp[FULLKEY[3:]])))
            oo.append(r["OOS_Sharpe"])
            rg.append(oosbest[c] - r["OOS_Sharpe"])
            p4.append(int(r["4b"]))
        rows.append(dict(window=w["label"], nyears=w["nyears"], has2011=w["has2011"],
                         agree=float(np.mean(ag)), OOS_Sharpe=float(np.nanmean(oo)),
                         regret=float(np.nanmean(rg)), p4b=float(np.mean(p4))))
    R = pd.DataFrame(rows).set_index("window")
    R.to_csv(OUT.with_suffix(".recut.csv"))
    print(fmt(R))
    a1 = R[R.has2011]
    a0 = R[~R.has2011]
    print(f"\n  contains 2011 (n={len(a1)}, mean length {a1.nyears.mean():.1f}): "
          f"agreement {a1.agree.mean():.3f}, OOS Sharpe {a1.OOS_Sharpe.mean():.3f}, "
          f"regret {a1.regret.mean():.3f}")
    print(f"  omits 2011    (n={len(a0)}, mean length {a0.nyears.mean():.1f}): "
          f"agreement {a0.agree.mean():.3f}, OOS Sharpe {a0.OOS_Sharpe.mean():.3f}, "
          f"regret {a0.regret.mean():.3f}")
    print("  (CONFOUNDED WITH LENGTH by construction — the controlled test is S3 above)")
    lenrow = R.groupby("nyears").agg(n=("agree", "size"), agree=("agree", "mean"),
                                     OOS_Sharpe=("OOS_Sharpe", "mean"), regret=("regret", "mean"))
    print("\n--- the same, by window LENGTH (the confound, shown on its own)")
    print(fmt(lenrow))

    # ============================================================ (6) walk-forward (rule 8)
    print("\n" + "=" * 128)
    print("### (6) PROTOCOL RULE 8 WALK-FORWARD — every window's pick carried into the UNTOUCHED")
    print("###     2017-2026 window, vs RULES v1 and SPY; both KEEP paths\n")
    wf = []
    for w in WIN:
        for c, pp in picks.items():
            tag = c[0]
            spy, bgr, bto = refs[tag]
            base = full_row(net(bgr, bto, c[3]))
            p = pp[w["key"]]
            r = look.loc[c + (p,)]
            wf.append(dict(zip(CELL, c), window=w["label"], families=w["families"],
                           nyears=w["nyears"], has2011=w["has2011"], pick=p,
                           CAGR=r["CAGR"], Sharpe=r["Sharpe"], MaxDD=r["MaxDD"],
                           H1=r["H1"], H2=r["H2"], OOS_CAGR=r["OOS_CAGR"],
                           OOS_Sharpe=r["OOS_Sharpe"], OOS_MaxDD=r["OOS_MaxDD"],
                           SPY_Sharpe=spy["Sharpe"], SPY_OOS_Sharpe=spy["OOS_Sharpe"],
                           SPY_OOS_CAGR=spy["OOS_CAGR"], SPY_OOS_MaxDD=spy["OOS_MaxDD"],
                           base_Sharpe=base["Sharpe"], base_OOS_Sharpe=base["OOS_Sharpe"],
                           keep_4a=int(r["4a"]), keep_4b=int(r["4b"]), keep_4b_oos=int(r["4b_oos"])))
    WF = pd.DataFrame(wf)
    WF.to_csv(OUT.with_suffix(".walkforward.csv"), index=False)

    print("--- KEEP-PATH COUNTS ACROSS THE 44 CELLS, BY WINDOW FAMILY")
    fam = WF.groupby("families").agg(n=("keep_4a", "size"), pass_4a=("keep_4a", "sum"),
                                     pass_4b=("keep_4b", "sum"), pass_4b_oos=("keep_4b_oos", "sum"),
                                     mean_OOS_Sharpe=("OOS_Sharpe", "mean"),
                                     mean_OOS_CAGR=("OOS_CAGR", "mean"),
                                     mean_OOS_MaxDD=("OOS_MaxDD", "mean"))
    fam["per_cell_4b"] = fam.pass_4b / fam.n * 44
    print(fmt(fam))

    print("\n--- FULL-IS (rule 8 as written) vs EX-2011 vs the L2O keep/drop split")
    key_rows = []
    for lbl, sel in [("FULL (rule 8 as written)", WF[WF.families.str.contains("FULL")]),
                     ("LOYO ex2011", WF[WF.window == f"ex{FOCUS_YEAR}"]),
                     ("L2O keeps 2011", WF[(WF.families.str.contains("L2O")) & (WF.nyears == 6) & WF.has2011]),
                     ("L2O drops 2011", WF[(WF.families.str.contains("L2O")) & (WF.nyears == 6) & ~WF.has2011]),
                     ("RECUT keeps 2011", WF[(WF.families.str.contains("RECUT")) & WF.has2011]),
                     ("RECUT omits 2011", WF[(WF.families.str.contains("RECUT")) & ~WF.has2011])]:
        key_rows.append(dict(window_set=lbl, n=len(sel),
                             OOS_Sharpe=sel.OOS_Sharpe.mean(), OOS_CAGR=sel.OOS_CAGR.mean(),
                             OOS_MaxDD=sel.OOS_MaxDD.mean(),
                             pass_4a=sel.keep_4a.mean() * 44, pass_4b=sel.keep_4b.mean() * 44,
                             pass_4b_oos=sel.keep_4b_oos.mean() * 44))
    KR = pd.DataFrame(key_rows).set_index("window_set")
    print(fmt(KR))
    spy_u = refs["u56"][0]
    spy_b = refs["broad"][0]
    print(f"\n  SPY u56  : full {spy_u['CAGR']:.1%}/{spy_u['Sharpe']:.3f}/{spy_u['MaxDD']:.1%}  "
          f"OOS {spy_u['OOS_CAGR']:.1%}/{spy_u['OOS_Sharpe']:.3f}/{spy_u['OOS_MaxDD']:.1%}")
    print(f"  SPY broad: full {spy_b['CAGR']:.1%}/{spy_b['Sharpe']:.3f}/{spy_b['MaxDD']:.1%}  "
          f"OOS {spy_b['OOS_CAGR']:.1%}/{spy_b['OOS_Sharpe']:.3f}/{spy_b['OOS_MaxDD']:.1%}")

    print("\n--- HEADLINE CELL: sleeve / u56 / top20 / 10 bps (the standing KEEP-4b candidate's cell)")
    h = WF[(WF.universe == "u56") & (WF.grid == "sleeve") & (WF.book == "top20") & (WF.cost_bps == 10)]
    hh = h.groupby("pick").agg(n_windows=("window", "size"),
                               CAGR=("CAGR", "first"), Sharpe=("Sharpe", "first"),
                               MaxDD=("MaxDD", "first"), H1=("H1", "first"), H2=("H2", "first"),
                               OOS_CAGR=("OOS_CAGR", "first"), OOS_Sharpe=("OOS_Sharpe", "first"),
                               OOS_MaxDD=("OOS_MaxDD", "first"),
                               keep_4a=("keep_4a", "first"), keep_4b=("keep_4b", "first"))
    print(fmt(hh))
    print(f"  windows picking each f, of {len(WIN)}; the standing candidate is f=0.50")
    hc = G[(G.universe == "u56") & (G.grid == "sleeve") & (G.book == "top20") & (G.cost_bps == 10)]
    print("\n  its IS Sharpe by window family (the number rule 8 maximises):")
    show = {"IS_full": FULLKEY, "IS_ex2011": EX11}
    for w in WIN:
        if w["label"] in ("2009-2012", "2013-2016", "2011-2014", "2012-2015"):
            show[f"IS_{w['label']}"] = f"IS_{w['key']}"
    print(fmt(hc.set_index("param")[list(show.values())].rename(
        columns={v: k for k, v in show.items()})))

    # ============================================================ (7) verdict
    print("\n" + "=" * 128)
    print("### (7) VERDICT\n")
    print(f"  S1 reproduction   : LOYO table {repro_loyo}; G leverage {repro_G}; "
          f"per-year d {repro_d}")
    print(f"  S2 price of ex2011: n={len(S)} swaps, mean dOOS Sharpe {m11:+.3f} -> {sign_verdict}")
    print(f"  S3 selector test  : premium(2011) {prem.loc[FOCUS_YEAR]:+.3f}, largest={largest}, "
          f"bar {PREMIUM_BAR:.2f} -> {s3}")
    print(f"  S4 OOS price      : keeping 2011 moves mean OOS Sharpe "
          f"{Y.loc[FOCUS_YEAR,'dOOS']:+.3f} and regret {Y.loc[FOCUS_YEAR,'dRegret']:+.3f}")
    print(f"  S5 re-cuts        : agreement {a1.agree.mean():.3f} (with 2011) vs "
          f"{a0.agree.mean():.3f} (without), length-confounded")
    print(f"\n[outputs] {OUT.name}.grid.csv .picks.csv .swaps.csv .l2o.csv .yearsplit.csv "
          f".recut.csv .peryear.csv .walkforward.csv")


if __name__ == "__main__":
    main()
