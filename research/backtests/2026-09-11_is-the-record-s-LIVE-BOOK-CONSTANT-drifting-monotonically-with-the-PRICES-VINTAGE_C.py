#!/usr/bin/env python3
"""
IDEA 692 -- is-the-record-s-LIVE-BOOK-CONSTANT-drifting-monotonically-with-the-PRICES-VINTAGE
=============================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 523's G3b reads live RULES v2 on U56 @10bps at 8.61%/1.1998/-12.05% against idea 415
  G2's 8.66%/1.2056/-12.05% with MaxDD EXACT, and attributes the gap to prices.csv now ending
  2026-09-10 rather than to idea 518's start-date effect.  Rebuild the constant at every
  committed vintage end-date and report whether Sharpe decays monotonically with appended days,
  so future gates can be stated as (constant, vintage) pairs.  Bears on 514/517/519/520.
  Max 2 params (vintage, gate bar).

WHAT IS NEW HERE (and why the record could not do this before)
--------------------------------------------------------------
  Ideas 514 and 519 both record that the sandbox clone is SHALLOW (50 commits), so 514 reached
  exactly ONE real vintage step and 519 modelled the restatement channel with SYNTHETIC draws
  calibrated to 514's published envelope (max |dreturn| 3.000e-04).  This run begins with
  `git fetch --unshallow`, which exposes all EIGHT committed vintages of data/prices.csv
  (2026-09-03 .. 2026-09-10).  Every number below is measured on the REAL committed files, so
  the append channel and the restatement channel are separated without a model of either.

DESIGN
------
  PANEL     U56 -- research/universe.json through baseline.load_universe's exact fallback path
            (PROTOCOL rule 1).  B136 is carried on the APPEND ladder only, as a non-tuned
            replication: data/prices_broad.csv has just 3 commits and no usable vintage ladder.
  BOOKS     LIVE   = baseline.rules_v2_weights(band 0.03, gross 0.75), weekly, 10 bps.  This is
                     the constant the queue is asking about.
            CAND20 = the standing 2026-09-04 KEEP-4b candidate (top-20 by composite with NO vol
                     scaler, fixed 0.75/20 per name) -- carried so the run can say whether a
                     CAPITAL verdict, not just a gate constant, moves with the vintage.
            SPY    = each vintage's OWN SPY column (the benchmark is restated by the same vendor
                     in the same file, so it must move with the panel).
  LADDERS   TRUE  : the 8 committed files as they stand        -> append + restatement
            TRUNC : v8 (2026-09-10) cut back to each of those 8 end-dates -> append ALONE
            TRUE - TRUNC at a shared end-date is the RESTATEMENT channel, measured not modelled.
            LONG  : v8 cut at every month-end 2017-01..2026-08 (116 rungs) and at every one of
                    the last 252 trading days -- the power the 8-day committed ladder lacks.
  TUNED (2) VINTAGE (the ladder rung) x GATE BAR in {5e-4, 1e-3, 5e-3, 1e-2, 2e-2, 5e-2}
            applied to |dSharpe|.  ALL rungs and ALL six bars are reported.
  FIXED     band 0.03, gross 0.75, n=20, vol cap 0.60, cadence W, 10 bps (PROTOCOL rule 2),
            warm-up 260 rows, IS/OOS split 2016-12-31 / 2017-01-01 (PROTOCOL rule 8).  None was
            chosen by outcome; all are the record's standing conventions.
  WINDOWS   OWN    : [px.index[260], vintage end] -- the record's own convention, what a reader
                     of that vintage would have printed.
            COMMON : [v8.index[260], 2026-09-03] -- every vintage's shared span, so a difference
                     on this window CANNOT be an appended day.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  fast_backtest == engine.backtest on v8 @10 bps                            bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                        bar 0.0
  G3  v8 reproduces idea 523's G3b live constant 8.61% / 1.1998 / -12.05%       bar 5e-3
  G4  the 8 pinned commit hashes extract to the pinned (rows, cols, last date)  exact
  G5  weights are CAUSAL: w(px[:d]) == w(px)[:d] for both books                 bar 0.0
      (this is what licenses building weights once and truncating them)
  G6  TRUNC(v8, d) is a prefix of v8, value-for-value                           bar 0.0
  G7  the universe's tickers are present in all 8 vintages                      exact
  G8  v1/v2 carry 1248 WEEKEND rows and v3..v8 carry 0 -- pinned literals, so a
      panel-construction regime break cannot be silently read as appended days  exact

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  U56 and B136 are today's constituents; every LEVEL printed below is biased upward and none is
  a tradeable estimate.  The claims this run makes are WITHIN-PANEL differences between two
  vintages of the same file over the same names, which the same bias applies to on both sides
  and which therefore largely differences out.
"""
import subprocess, sys, json, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score, EXCLUDE   # noqa: E402
from engine import backtest, rebalance_mask                                        # noqa: E402

COST0, FREQ = 10.0, "W"
BAND0, GROSS0, NCAND, VOLCAP, WARM = 0.03, 0.75, 20, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
BARS = [5e-4, 1e-3, 5e-3, 1e-2, 2e-2, 5e-2]

# the 8 committed vintages of data/prices.csv, oldest first -- (tag, sha, rows, cols, last date)
VINTAGES = [
    ("v1", "fb20817495930b01dfb4124d70c5a5c1c71acac5", 6059, 58, "2026-09-04"),
    ("v2", "0ede228245a20593eabce4b06b697af3a526ac31", 6060, 58, "2026-09-04"),
    ("v3", "c006b4393032f7df9e9d994a6fc6587ac1454d55", 4698, 58, "2026-09-03"),
    ("v4", "50585c86703498c95f946f0d264661d10f445145", 4699, 58, "2026-09-04"),
    ("v5", "f138ee9ae99dccef84f0ce40e6c2312b2ce36deb", 4699, 58, "2026-09-04"),
    ("v6", "9ee888f4530a14a7d5877d177fdedda728e42196", 4700, 58, "2026-09-08"),
    ("v7", "7a93b0753db30204495b5f009fa263eaa9572bd7", 4701, 58, "2026-09-09"),
    ("v8", "60e8c36a522639fadaeb1d1b5895134b53a6d21f", 4702, 58, "2026-09-10"),
]
WEEKEND_ROWS = {"v1": 1248, "v2": 1248, "v3": 0, "v4": 0, "v5": 0, "v6": 0, "v7": 0, "v8": 0}
PUB_523 = dict(CAGR=0.0861, Sharpe=1.1998, MaxDD=-0.1205)     # idea 523 G3b, read 2026-09-11
PUB_415 = dict(CAGR=0.0866, Sharpe=1.2056, MaxDD=-0.1205)     # idea 415 G2,  read 2026-09-10

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ---------------------------------------------------------------------------------------------
def fast_backtest(prices, weights, freq=FREQ, cost=COST0):
    """Vectorised equivalent of engine.backtest's return stream (G1 pins it at 1e-12)."""
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    m = rebalance_mask(idx, freq).values
    m = np.concatenate([[False], m[:-1]]).copy()
    m[0] = True
    T, Ncol = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, Ncol)), C[:-1]])
    reb = np.flatnonzero(m)
    seg = np.searchsorted(reb, np.arange(T), side="right") - 1
    s0 = reb[seg]
    W0 = wt[s0]
    h = W0 * (Cp / Cp[s0])
    V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
    held = h / V[:, None]
    s0p = reb[np.maximum(seg - 1, 0)]
    W0p = wt[s0p]
    hp = W0p * (Cp / Cp[s0p])
    Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
    heldp = hp / Vp[:, None]
    heldp[reb[0]] = 0.0
    turn = np.zeros(T)
    turn[reb] = np.abs(wt[reb] - heldp[reb]).sum(axis=1)
    return pd.Series((held * rets).sum(axis=1) - turn * cost / 1e4, index=idx)


def M0(r):
    v = r.std() * np.sqrt(252)
    return (r.mean() * 252) / v if v else np.nan


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    h = len(r) // 2
    return dict(CAGR=eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan,
                Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band=BAND0, gross=GROSS0):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def cand_book(px, n=NCAND, gross=GROSS0):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    r = sc.where(elig).rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (gross / n)


BOOKS = {"LIVE": band_book, "CAND20": cand_book}


def keeppaths(m, oos_s, mb, ms, spy_oos):
    """PROTOCOL rule 4.  4a: Sharpe > live book in BOTH halves and MaxDD no worse.
       4b: Sharpe > SPY in both halves AND OOS, MaxDD <= 60% of SPY's, CAGR >= 70% of SPY's."""
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > spy_oos)
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
           and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return bool(p4a), bool(p4b)


def fail4b(m, oos_s, ms, spy_oos):
    f = []
    if not m["H1"] > ms["H1"]: f.append("H1")
    if not m["H2"] > ms["H2"]: f.append("H2")
    if not oos_s > spy_oos: f.append("OOS")
    if not abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]): f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]: f.append("CAGR")
    return "+".join(f) if f else "-"


# ---------------------------------------------------------------------------------------------
def universe_tickers():
    U = json.loads((ROOT / "research" / "universe.json").read_text())
    return sorted({t for g in U.values() for t in g} - set(EXCLUDE))


def read_vintage(sha, tickers, cache_dir):
    """Replicates engine.load_prices' offline fallback exactly, on a git-extracted file."""
    f = cache_dir / f"{sha[:10]}.csv"
    if not f.exists():
        f.write_bytes(subprocess.run(["git", "-C", str(ROOT), "show", f"{sha}:data/prices.csv"],
                                     capture_output=True, check=True).stdout)
    raw = pd.read_csv(f, index_col=0, parse_dates=True)
    px = raw[list(tickers)].loc["2008-01-01":]
    return raw, px.dropna(how="all").ffill()


def spearman(x, y):
    rx = pd.Series(x).rank().values
    ry = pd.Series(y).rank().values
    return float(np.corrcoef(rx, ry)[0, 1])


def sign_flips(v):
    d = np.diff(np.asarray(v, float))
    s = np.sign(d[d != 0])
    return int((s[1:] != s[:-1]).sum()), int((d > 0).sum()), int((d < 0).sum())


# ---------------------------------------------------------------------------------------------
def main():
    cache_dir = Path("/tmp/idea692_vintages")
    cache_dir.mkdir(exist_ok=True)
    T = universe_tickers()

    P("=" * 104)
    P("IDEA 692 -- is the record's LIVE BOOK CONSTANT drifting monotonically with the PRICES VINTAGE?")
    P("=" * 104)
    P(f"  universe.json tickers: {len(T)}   cost {COST0:.0f} bps   cadence {FREQ}   "
      f"band {BAND0}   gross {GROSS0}   warm-up {WARM} rows")

    # ---------------- (A) gates -------------------------------------------------------------
    P("")
    P("=" * 104)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 104)
    ok = True
    RAW, PX = {}, {}
    g4 = []
    for tag, sha, nrow, ncol, last in VINTAGES:
        raw, px = read_vintage(sha, T, cache_dir)
        RAW[tag], PX[tag] = raw, px
        got = (raw.shape[0], raw.shape[1], str(raw.index.max().date()))
        g4.append((tag, got == (nrow, ncol, last), got))
    bad4 = [t for t, good, _ in g4 if not good]
    P(f"  G4 8 pinned commits extract to pinned (rows, cols, last)     : "
      f"{'PASS' if not bad4 else 'FAIL ' + str(bad4)}")
    ok &= not bad4
    for tag, good, got in g4:
        P(f"       {tag}  rows {got[0]:5d}  cols {got[1]}  last {got[2]}")

    g7 = all(set(T) <= set(RAW[t].columns) for t in RAW)
    P(f"  G7 every universe ticker present in all 8 vintages           : {'PASS' if g7 else 'FAIL'}")
    ok &= g7

    g8 = {t: int((RAW[t].index.dayofweek >= 5).sum()) for t in RAW}
    g8ok = g8 == WEEKEND_ROWS
    P(f"  G8 weekend rows per vintage == pinned {WEEKEND_ROWS}")
    P(f"       got {g8}   {'PASS' if g8ok else 'FAIL'}")
    ok &= g8ok

    px8 = PX["v8"]
    w8 = band_book(px8)
    g2 = float(np.nanmax(np.abs(w8.values - rules_v2_weights(px8, BAND0, GROSS0).values)))
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights                  : {g2:.3e}  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    ok &= g2 == 0.0

    slow = backtest(px8, w8, cost_bps=COST0, freq=FREQ)["returns"]
    fast = fast_backtest(px8, w8)
    j8 = px8.index[WARM]
    g1 = float(np.nanmax(np.abs(slow.loc[j8:].values - fast.loc[j8:].values)))
    P(f"  G1 fast_backtest == engine.backtest @10 bps                  : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12

    m8 = M(fast.loc[j8:])
    d3 = {k: abs(m8[k] - v) for k, v in PUB_523.items()}
    P(f"  G3 v8 reproduces idea 523 G3b 8.61% / 1.1998 / -12.05%       : got "
      f"{m8['CAGR']:.2%} / {m8['Sharpe']:.4f} / {m8['MaxDD']:.2%}  max|d| {max(d3.values()):.3e}  "
      f"{'PASS' if max(d3.values()) < 5e-3 else 'FAIL'}")
    ok &= max(d3.values()) < 5e-3

    dcut = px8.index[-40]
    g5 = 0.0
    for bn, bf in BOOKS.items():
        a = bf(px8.loc[:dcut]).values
        b = bf(px8).loc[:dcut].values
        g5 = max(g5, float(np.nanmax(np.abs(a - b))))
    P(f"  G5 weights causal: w(px[:d]) == w(px)[:d], both books        : {g5:.3e}  "
      f"{'PASS' if g5 == 0.0 else 'FAIL'}")
    ok &= g5 == 0.0

    sub = px8.loc[:dcut]
    g6 = float(np.nanmax(np.abs(sub.values - px8.loc[sub.index].values)))
    g6ok = (g6 == 0.0) and list(sub.index) == list(px8.index[:len(sub)])
    P(f"  G6 TRUNC(v8,d) is a value-for-value prefix of v8             : {g6:.3e}  "
      f"{'PASS' if g6ok else 'FAIL'}")
    ok &= g6ok
    P(f"  GATES: {'ALL PASS' if ok else 'FAILURE -- numbers below are NOT to be read'}")
    if not ok:
        raise SystemExit("gate failure")

    # ---------------- (B) the two channels, measured on the real files -----------------------
    P("")
    P("=" * 104)
    P("(B) WHAT ACTUALLY CHANGES BETWEEN COMMITTED VINTAGES (cell level, U56 tickers)")
    P("=" * 104)
    P("  consecutive pairs: rows appended, and the cell-level envelope on the shared span.")
    P("  SAMECON = both files share a panel construction (G8's weekend-row regime); a pair that")
    P("  straddles the 2026-09-04 rebuild is NOT a restatement measurement and is marked so.")
    P(f"  {'pair':<10}{'con':>5}{'+rows':>7}{'shared':>8}{'maxdPX_rel':>13}{'maxdRET':>12}"
      f"{'cells>1e-9':>12}{'cells>1e-4':>12}{'worst ticker':>15}")
    cell = []
    for (ta, _, _, _, _), (tb, _, _, _, _) in zip(VINTAGES[:-1], VINTAGES[1:]):
        a, b = PX[ta], PX[tb]
        idx = a.index.intersection(b.index)
        A, B = a.loc[idx], b.loc[idx]
        rel = np.abs(A / B - 1.0)
        dr = np.abs(A.pct_change() - B.pct_change()).iloc[1:]
        worst = dr.max().idxmax() if dr.notna().any().any() else "-"
        same = WEEKEND_ROWS[ta] == WEEKEND_ROWS[tb]
        row = dict(pair=f"{ta}->{tb}", same_construction=same,
                   added=len(b.index) - len(idx), shared=len(idx),
                   max_rel_px=float(np.nanmax(rel.values)), max_dret=float(np.nanmax(dr.values)),
                   cells_1e9=int(np.nansum(dr.values > 1e-9)),
                   cells_1e4=int(np.nansum(dr.values > 1e-4)), worst_ticker=str(worst))
        cell.append(row)
        P(f"  {row['pair']:<10}{str(same):>5}{row['added']:>7}{row['shared']:>8}"
          f"{row['max_rel_px']:>13.3e}{row['max_dret']:>12.3e}{row['cells_1e9']:>12}"
          f"{row['cells_1e4']:>12}{row['worst_ticker']:>15}")
    cells = pd.DataFrame(cell)
    sc = cells[cells.same_construction]
    P("")
    P("  Idea 514 published a restatement envelope of max |dreturn| = 3.000e-04 and idea 519")
    P("  calibrated its synthetic draws to it.  Measured on the REAL files, SAME-CONSTRUCTION")
    P(f"  pairs only: envelope spans {sc.max_dret.min():.3e} .. {sc.max_dret.max():.3e}, i.e. "
      f"{sc.max_dret.min()/3.0e-4:.2f}x .. {sc.max_dret.max()/3.0e-4:.2f}x that bound.")
    P(f"  The widest is {sc.loc[sc.max_dret.idxmax(), 'pair']} on "
      f"{sc.loc[sc.max_dret.idxmax(), 'worst_ticker']} with only "
      f"{int(sc.loc[sc.max_dret.idxmax(), 'cells_1e4'])} cells above 1e-4 out of "
      f"{int(sc.loc[sc.max_dret.idxmax(), 'cells_1e9'])} that move at all -- the SPARSE-LARGE")
    P("  corner idea 519 recorded as untested.  It is not hypothetical; it is in the record's")
    P("  own committed files.")
    dump(cells, "cells")

    # ---------------- (C) the constant at every vintage --------------------------------------
    P("")
    P("=" * 104)
    P("(C) THE GRID -- the constant at every vintage rung, both channels, both books")
    P("=" * 104)
    COMMON_END = "2026-09-03"
    jc = px8.index[WARM]

    def arm(px, book, label, channel, tag, endd):
        w = BOOKS[book](px)
        r = fast_backtest(px, w).loc[px.index[WARM]:]
        spy = px["SPY"].pct_change().fillna(0.0).loc[px.index[WARM]:]
        base = fast_backtest(px, band_book(px)).loc[px.index[WARM]:]
        m, ms, mb = M(r), M(spy), M(base)
        rc = r.loc[jc:COMMON_END]
        mo = M(r.loc[OOS_START:])
        mis = M(r.loc[:IS_END])
        so, ss = mo["Sharpe"], M0(spy.loc[OOS_START:])
        p4a, p4b = keeppaths(m, so, mb, ms, spy_oos=ss)
        return dict(channel=channel, vintage=tag, book=book, end=endd, rows=len(px),
                    start=str(px.index[WARM].date()), n_ret=len(r),
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"], H2=m["H2"],
                    Sharpe_common=M0(rc), CAGR_common=M(rc)["CAGR"], MaxDD_common=M(rc)["MaxDD"],
                    IS_Sharpe=mis["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_Sharpe=so,
                    OOS_MaxDD=mo["MaxDD"], SPY_Sharpe=ms["Sharpe"], SPY_CAGR=ms["CAGR"],
                    SPY_MaxDD=ms["MaxDD"], SPY_OOS_Sharpe=ss,
                    base_Sharpe=mb["Sharpe"], base_OOS_Sharpe=M0(base.loc[OOS_START:]),
                    pass4a=p4a, pass4b=p4b, fail4b=fail4b(m, so, ms, ss))

    rows = []
    for tag, sha, _, _, last in VINTAGES:
        for book in BOOKS:
            rows.append(arm(PX[tag], book, tag, "TRUE", tag, last))
            tr = px8.loc[:PX[tag].index.max()]
            rows.append(arm(tr, book, tag, "TRUNC", tag, str(tr.index.max().date())))
    G = pd.DataFrame(rows)
    for book in BOOKS:
        P("")
        P(f"  BOOK = {book}")
        P(f"  {'chan':<6}{'vint':<5}{'end':<12}{'rows':>6}{'start':>12}{'CAGR':>9}{'Sharpe':>9}"
          f"{'MaxDD':>9}{'H1':>7}{'H2':>7}{'Sh_com':>9}{'ISsh':>7}{'OOSsh':>7}{'4a':>4}{'4b':>4}"
          f"{'fail4b':>18}")
        for _, r in G[G.book == book].sort_values(["channel", "vintage"]).iterrows():
            P(f"  {r.channel:<6}{r.vintage:<5}{r.end:<12}{r.rows:>6}{r.start:>12}{r.CAGR:>9.2%}"
              f"{r.Sharpe:>9.4f}{r.MaxDD:>9.2%}{r.H1:>7.2f}{r.H2:>7.2f}{r.Sharpe_common:>9.4f}"
              f"{r.IS_Sharpe:>7.2f}{r.OOS_Sharpe:>7.2f}{str(r.pass4a):>4}{str(r.pass4b):>4}"
              f"{r.fail4b:>18}")
    dump(G, "grid")

    # ---------------- (D) does the record's own pair of readings live here? ------------------
    P("")
    P("=" * 104)
    P("(D) THE QUEUE'S TWO PUBLISHED READINGS, LOCATED ON THE LADDER")
    P("=" * 104)
    live = G[(G.book == "LIVE")]
    for nm, pub in (("idea 523 G3b (read 2026-09-11)", PUB_523), ("idea 415 G2  (read 2026-09-10)", PUB_415)):
        d = live.assign(dev=lambda x: (x.CAGR - pub["CAGR"]).abs().combine(
            (x.Sharpe - pub["Sharpe"]).abs(), max).combine((x.MaxDD - pub["MaxDD"]).abs(), max))
        best = d.sort_values("dev").iloc[0]
        P(f"  {nm}: published {pub['CAGR']:.2%} / {pub['Sharpe']:.4f} / {pub['MaxDD']:.2%}")
        P(f"      nearest rung  {best.channel}/{best.vintage} (end {best.end})  "
          f"{best.CAGR:.2%} / {best.Sharpe:.4f} / {best.MaxDD:.2%}   max|d| {best.dev:.3e}"
          f"   {'REPRODUCED at 5e-3' if best.dev < 5e-3 else 'NOT reproduced at 5e-3'}")
        within = d[d.dev < 5e-3]
        P(f"      rungs within 5e-3: {len(within)} of {len(d)}  "
          f"[{', '.join(within.channel + '/' + within.vintage)}]")

    # ---------------- (E) monotonicity, the headline ----------------------------------------
    P("")
    P("=" * 104)
    P("(E) IS THE DRIFT MONOTONE? -- committed ladder, then the long append ladder")
    P("=" * 104)
    mono = []
    for book in BOOKS:
        for chan in ("TRUE", "TRUNC"):
            s = G[(G.book == book) & (G.channel == chan)].sort_values("end")
            v = s.Sharpe.values
            fl, up, dn = sign_flips(v)
            rho = spearman(np.arange(len(v)), v)
            mono.append(dict(ladder=f"committed-{chan}", book=book, rungs=len(v),
                             rho=rho, flips=fl, up=up, down=dn,
                             span=float(v.max() - v.min())))
            P(f"  committed {chan:<6} {book:<7} n={len(v)}  Spearman(end,Sharpe) {rho:+.4f}  "
              f"sign flips {fl}  up {up} / down {dn}  Sharpe span {v.max()-v.min():.4f}")

    # long append ladder on v8 (and B136), month-ends 2017..2026 and the last 252 days
    P("")
    P("  LONG APPEND LADDER (v8 truncated; append channel alone, no restatement by construction)")
    panels = {"U56": px8}
    try:
        panels["B136"] = load_universe(broad=True)
    except Exception as e:                                        # pragma: no cover
        P(f"  (B136 unavailable: {type(e).__name__})")
    longrows = []
    for pname, px in panels.items():
        idx = px.index
        me = pd.Series(idx, index=idx).groupby([idx.year, idx.month]).max()
        me = [d for d in me.values if pd.Timestamp(d) > pd.Timestamp("2017-01-31")]
        daily = list(idx[-252:])
        rungs = sorted(set(pd.Timestamp(d) for d in me) | set(pd.Timestamp(d) for d in daily))
        for book in BOOKS:
            w = BOOKS[book](px)
            full = fast_backtest(px, w)
            for d in rungs:
                r = full.loc[px.index[WARM]:d]
                if len(r) < 500:
                    continue
                m = M(r)
                longrows.append(dict(panel=pname, book=book, end=str(pd.Timestamp(d).date()),
                                     n_ret=len(r), appended=int((idx > d).sum()),
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=m["H1"], H2=m["H2"]))
    L = pd.DataFrame(longrows)
    dump(L, "ladder")
    for pname in panels:
        for book in BOOKS:
            s = L[(L.panel == pname) & (L.book == book)].sort_values("end")
            v = s.Sharpe.values
            fl, up, dn = sign_flips(v)
            rho = spearman(np.arange(len(v)), v)
            mono.append(dict(ladder=f"long-{pname}", book=book, rungs=len(v), rho=rho,
                             flips=fl, up=up, down=dn, span=float(v.max() - v.min())))
            P(f"  long {pname:<5} {book:<7} n={len(v):>4}  Spearman(end,Sharpe) {rho:+.4f}  "
              f"sign flips {fl}  up {up} / down {dn}  Sharpe span {v.max()-v.min():.4f}  "
              f"[{v.min():.4f}, {v.max():.4f}]")
    dump(pd.DataFrame(mono), "monotonicity")
    P("")
    P("  A monotone series has ZERO sign flips.  Read the flip counts above before accepting")
    P("  any (constant, vintage) extrapolation.")

    # ---------------- (F) the gate bar: how long does a published constant keep? -------------
    P("")
    P("=" * 104)
    P("(F) PARAM 2 -- GATE BAR x VINTAGE: the shelf life of a published constant, in appended days")
    P("=" * 104)
    shelf = []
    for pname in panels:
        for book in BOOKS:
            s = L[(L.panel == pname) & (L.book == book)].sort_values("appended")
            s = s[s.appended <= 252]
            final = s[s.appended == s.appended.min()].Sharpe.iloc[0]
            dev = (s.Sharpe - final).abs().values
            app = s.appended.values
            for bar in BARS:
                over = app[dev > bar]
                first = int(over.min()) if len(over) else None
                shelf.append(dict(panel=pname, book=book, bar=bar,
                                  first_exceed_days=first if first is not None else -1,
                                  frac_within=float((dev <= bar).mean()),
                                  max_dev_252d=float(dev.max())))
    S = pd.DataFrame(shelf)
    P(f"  {'panel':<7}{'book':<8}{'bar':>9}{'1st exceed (appended days)':>28}{'frac of 252 rungs within':>27}")
    for _, r in S.iterrows():
        fe = "never in 252d" if r.first_exceed_days < 0 else f"{int(r.first_exceed_days)}"
        P(f"  {r.panel:<7}{r.book:<8}{r.bar:>9.0e}{fe:>28}{r.frac_within:>27.3f}")
    P("")
    P("  Same bars applied to the COMMITTED ladder.  TRUE minus TRUNC at a shared end-date is")
    P("  the RESTATEMENT channel alone -- but ONLY for a vintage built the same way v8 is.  The")
    P("  v1/v2 rows straddle the 2026-09-04 panel rebuild (G8: 1248 weekend rows), so their gap")
    P("  is CONSTRUCTION + restatement and is marked BREAK; it is not a restatement reading.")
    P(f"  {'book':<8}{'vintage':<9}{'con':>7}{'dSharpe':>12}{'dCAGR':>10}{'dMaxDD':>10}"
      f"{'bars cleared':>40}")
    chan_rows = []
    for book in BOOKS:
        for tag, _, _, _, _ in VINTAGES:
            t = G[(G.book == book) & (G.vintage == tag) & (G.channel == "TRUE")].iloc[0]
            u = G[(G.book == book) & (G.vintage == tag) & (G.channel == "TRUNC")].iloc[0]
            ds, dc, dd = t.Sharpe - u.Sharpe, t.CAGR - u.CAGR, t.MaxDD - u.MaxDD
            cleared = ",".join(f"{b:.0e}" for b in BARS if abs(ds) <= b) or "none"
            con = "BREAK" if WEEKEND_ROWS[tag] != WEEKEND_ROWS["v8"] else "same"
            chan_rows.append(dict(book=book, vintage=tag, construction=con, dSharpe=ds,
                                  dCAGR=dc, dMaxDD=dd, bars_cleared=cleared,
                                  verdict4b_true=t.pass4b, verdict4b_trunc=u.pass4b,
                                  flip=bool(t.pass4b != u.pass4b)))
            P(f"  {book:<8}{tag:<9}{con:>7}{ds:>12.4f}{dc:>10.2%}{dd:>10.2%}{cleared:>40}")
    C = pd.DataFrame(chan_rows)
    dump(C, "channels")
    dump(S, "shelflife")
    pure = C[C.construction == "same"]
    P(f"  RESTATEMENT channel on same-construction vintages: max |dSharpe| "
      f"{pure.dSharpe.abs().max():.4f}, max |dCAGR| {pure.dCAGR.abs().max():.4%}, "
      f"max |dMaxDD| {pure.dMaxDD.abs().max():.4%}  ({len(pure)} rows)")
    P(f"  4b verdict flips TRUE vs TRUNC at the same end-date: {int(C.flip.sum())} of {len(C)}")
    P("")
    P("  The SPARSE-LARGE corner, read off the book rather than the cells: v1 and v2 share a")
    P("  construction and differ by ONE appended row plus the PLTR restatement above, so their")
    P("  book-level gap is the largest single-step restatement the record's own files contain.")
    for book in BOOKS:
        a = G[(G.book == book) & (G.channel == "TRUE") & (G.vintage == "v1")].iloc[0]
        b = G[(G.book == book) & (G.channel == "TRUE") & (G.vintage == "v2")].iloc[0]
        P(f"    {book:<8} dSharpe {b.Sharpe - a.Sharpe:+.4f}   dCAGR {b.CAGR - a.CAGR:+.4%}   "
          f"dMaxDD {b.MaxDD - a.MaxDD:+.4%}   clears "
          f"{','.join(f'{x:.0e}' for x in BARS if abs(b.Sharpe - a.Sharpe) <= x) or 'no bar'}")

    # ---------------- (G) rule 8 -------------------------------------------------------------
    P("")
    P("=" * 104)
    P("(G) RULE 8 WALK-FORWARD (required) -- the VINTAGE treated as the dial the chooser tunes")
    P("=" * 104)
    P("  Chooser: pick the vintage rung with the highest IS Sharpe (through 2016-12-31), then")
    P("  read that pick's 2017-2026 OOS untouched, against live RULES v2 OOS and SPY OOS.")
    wf = []
    for book in BOOKS:
        for chan in ("TRUE", "TRUNC"):
            s = G[(G.book == book) & (G.channel == chan)]
            pick = s.sort_values("IS_Sharpe", ascending=False).iloc[0]
            is_spread = float(s.IS_Sharpe.max() - s.IS_Sharpe.min())
            sx = s[~s.vintage.isin(["v1", "v2"])]
            is_spread_ex = float(sx.IS_Sharpe.max() - sx.IS_Sharpe.min())
            oos_spread = float(s.OOS_Sharpe.max() - s.OOS_Sharpe.min())
            blind = s[s.vintage == "v8"].iloc[0]
            wf.append(dict(book=book, channel=chan, pick=pick.vintage, IS_Sharpe=pick.IS_Sharpe,
                           IS_spread=is_spread, IS_spread_ex_break=is_spread_ex,
                           OOS_spread=oos_spread,
                           OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                           OOS_MaxDD=pick.OOS_MaxDD, base_OOS_Sharpe=pick.base_OOS_Sharpe,
                           SPY_OOS_Sharpe=pick.SPY_OOS_Sharpe,
                           blind_v8_OOS_Sharpe=blind.OOS_Sharpe,
                           cost_of_choosing=pick.OOS_Sharpe - blind.OOS_Sharpe))
            P(f"  {book:<7} {chan:<6} pick {pick.vintage}  IS Sharpe {pick.IS_Sharpe:.4f}  "
              f"IS spread {is_spread:.2e} (ex-BREAK {is_spread_ex:.2e})"
              f"  ->  OOS {pick.OOS_CAGR:.2%} / {pick.OOS_Sharpe:.4f} / "
              f"{pick.OOS_MaxDD:.2%}   vs RULES v2 OOS {pick.base_OOS_Sharpe:.4f}  "
              f"SPY OOS {pick.SPY_OOS_Sharpe:.4f}   OOS spread over rungs {oos_spread:.2e}   "
              f"blind-v8 cost {pick.OOS_Sharpe - blind.OOS_Sharpe:+.4f}")
    W = pd.DataFrame(wf)
    dump(W, "walkforward")

    # full OOS table vs baseline and SPY on the live vintage
    P("")
    P("  OOS (2017-01-01 .. each book's own end, vintage v8) CAGR / Sharpe / MaxDD:")
    for book in BOOKS:
        r = G[(G.book == book) & (G.channel == "TRUE") & (G.vintage == "v8")].iloc[0]
        P(f"    {book:<8} {r.OOS_CAGR:>8.2%} / {r.OOS_Sharpe:.4f} / {r.OOS_MaxDD:>8.2%}")
    r8 = G[(G.book == "LIVE") & (G.channel == "TRUE") & (G.vintage == "v8")].iloc[0]
    spy8 = px8["SPY"].pct_change().fillna(0.0).loc[jc:]
    mo_spy = M(spy8.loc[OOS_START:])
    P(f"    {'RULES v2':<8} {r8.OOS_CAGR:>8.2%} / {r8.OOS_Sharpe:.4f} / {r8.OOS_MaxDD:>8.2%}   (baseline)")
    P(f"    {'SPY':<8} {mo_spy['CAGR']:>8.2%} / {mo_spy['Sharpe']:.4f} / {mo_spy['MaxDD']:>8.2%}")

    # ---------------- (H) both KEEP paths ----------------------------------------------------
    P("")
    P("=" * 104)
    P("(H) BOTH KEEP PATHS AT EVERY VINTAGE RUNG (PROTOCOL rule 4)")
    P("=" * 104)
    for book in BOOKS:
        s = G[G.book == book]
        P(f"  {book:<8} 4a passes {int(s.pass4a.sum())}/{len(s)}   4b passes {int(s.pass4b.sum())}/{len(s)}"
          f"   distinct 4b fail-sets: {sorted(set(s.fail4b))}")
    flips4b = G.groupby(["book", "channel"]).pass4b.nunique()
    P(f"  4b verdict is vintage-INVARIANT within every (book, channel): "
      f"{'YES' if (flips4b == 1).all() else 'NO -- ' + str(flips4b[flips4b > 1].to_dict())}")
    P("")
    P("  NOTHING PROMOTED: LIVE is the incumbent itself and CAND20 is the standing candidate;")
    P("  this run adds no book and takes no KEEP.")

    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
