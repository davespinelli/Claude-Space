#!/usr/bin/env python3
"""QUEUE idea 244 — how-many-published-count-dials-are-gross-dials   (cloud, 2026-09-08).

Question (verbatim from QUEUE)
-----------------------------
"idea 240 found idea 73's fixed GROSS/n weight de-grosses a wide book without saying so (U56 n=60
realised gross 0.474 vs 0.721 at n=20) and that closing the channel halves the width premium and
flips two cells.  Census every count/position-number sweep in the record for the same
construction, re-quote each at matched realised gross, and report how many published count
findings are gross-ladder points.  Max 2 params."

What is on trial.  Not a book: a CONSTRUCTION.  Two ways to hold "the top n names at equal
weight" differ whenever the eligible set is smaller than n:

    FIXED  w_i = g / n   on every admitted name        -> realised gross = g * E_t / n  (E_t < n)
    NORM   w_i = g / k_t on every admitted name, k_t = min(n, E_t)  -> realised gross = g always

FIXED is idea 73's published construction.  Widening n under FIXED therefore does two things at
once: it broadens the book AND it de-grosses it, exactly and only when breadth is low.  That
second channel is a breadth-conditional exposure overlay that no published count sweep names.  If
the record's width findings are partly that overlay, they are gross-ladder points wearing a count
label.

PART A  CENSUS of the committed record.  Which published count/width sweeps use FIXED, which use
        NORM, and how many publish a realised-gross column at all?  The construction lives in the
        CODE, not the CSVs, so the census reads the committed .py scripts mechanically and the
        committed CSVs for the dial and for gross coverage.  UNKNOWN is counted, never guessed.
  A1  Scripts carrying a COUNT DIAL (a swept n/k/width/topn), found from their own source.
  A2  Construction classification: FIXED / NORM / BOTH / UNKNOWN, by source regex.
  A3  GROSS COVERAGE: of the count-dial files, how many publish any realised-gross column.
  A4  SATURATION EXPOSURE: of the count-dial CSVs, how many sweep an n above the panel's own
      median eligible count (where the channel is open) — the population of published findings
      that COULD be gross-ladder points.

PART B  MEASUREMENT on live prices, both constructions built side by side.
  B1  GATES.  `fast_bt` vs `engine.backtest` on returns AND turnover; the cost-rung identity;
      FIXED at n=5, g=0.75 nests `baseline.rules_v1_weights`; NORM == FIXED wherever E_t >= n
      (the channel is provably CLOSED off saturation).
  B2  THE CHANNEL.  Realised gross and saturation share by (panel, n) — the size of the thing.
  B3  THE WIDTH CURVE under both conventions, and its RESTATEMENT at matched realised gross.
      How many width comparisons flip sign when the channel is closed?
  B4  4b AND 4a on every grid point, both conventions, both cost rungs.  How many verdicts flip?
  B5  RULE 8.  n chosen on IS <= 2016-12-31 by IS Sharpe under each convention, 2017-2026 read
      ONCE; does the convention change the pick, and what does it cost OOS vs RULES v2 and SPY?

THE TWO TUNED PARAMETERS (PROTOCOL 4): n (6 values) and g (3 values).  The CONVENTION is the
treatment under test, not a dial; the cost rung is a reported dimension.  All grid points
reported.

PRE-REGISTERED PREDICTIONS (written before any number below was read)
  P1  A MAJORITY of the record's count-dial files publish NO realised-gross column, so the
      channel is un-checkable from the committed artefacts alone.
  P2  Under FIXED, realised gross falls monotonically in n on all 3 panels once n passes the
      panel's median eligible count, and at the top of the grid it is below 0.6 * nominal g on
      at least 2 panels.
  P3  |Sharpe(widest n) - Sharpe(n=20)| is SMALLER under NORM than under FIXED on at least 2 of
      3 panels — i.e. part of the published width effect is the gross channel, not width.
  P4  At least one (panel, n, g, rung) cell FLIPS its 4b verdict between the two conventions.
  P5  The rule-8 IS chooser picks a DIFFERENT n under the two conventions on at least 1 of 3
      panels.

CAVEATS carried, not buried
  * SURVIVORSHIP (idea 54): u56, broad136 and the sub-$2B panel are CURRENT-constituent lists
    with no delistings.  Every arm inherits it equally, so the paired FIXED-minus-NORM contrasts
    that carry this run's answer are largely protected; every LEVEL is biased upward and none is
    a tradable estimate.  The small panel drops the 44 names with max_1d_move >= 1.0 first.
  * The source census is a REGEX over committed scripts.  It can only see constructions written
    the ordinary way; anything expressed through a helper it cannot read is UNKNOWN and is
    counted as UNKNOWN.  No file's verdict is inferred from its prose.
  * Realised gross is reported as the mean over rebalance days of the target weight sum; a book
    drifts between rebalances, so instantaneous gross differs from it.  Both conventions are
    measured the same way, so the CONTRAST is unaffected.
  * Idea 144: a re-dialled book is the same book.  Nothing here proposes a new signal.

Deterministic, standalone.  Writes .console.txt .census.csv .channel.csv .grid.csv .flips.csv
.walkforward.csv .params.csv
"""
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score   # noqa: E402
from engine import backtest, rebalance_mask                                     # noqa: E402

STEM = "2026-09-08_how-many-published-count-dials-are-gross-dials_cloud"
OUT = ROOT / "research" / "backtests"

N_GRID = [5, 10, 20, 40, 60, 90]         # tuned parameter 1
G_GRID = [0.50, 0.75, 1.00]              # tuned parameter 2
RUNGS = [10, 25]
FREQ = "W"
IS_END, OOS_START = "2016-12-31", "2017-01-01"
N_REF = 20                               # the width the record most often quotes against

_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _lines.append(s)


T0 = time.time()
P("=" * 118)
P("IDEA 244  how-many-published-count-dials-are-gross-dials   (cloud, 2026-09-08)")
P("=" * 118)

# =====================================================================================
# PART A — CENSUS
# =====================================================================================
P("\n" + "-" * 118)
P("A1-A4  CENSUS of the committed record — count dials, their construction, their gross coverage")
P("-" * 118)

COUNT_DIAL_SRC = re.compile(
    r"(N_GRID|NGRID|n_grid|N_VALUES|WIDTHS|K_GRID|TOPN|TOP_N|for\s+n\s+in\s*[\[\(]|"
    r"for\s+k\s+in\s*[\[\(]|n\s*in\s*\[\s*\d+\s*,\s*\d+)")
FIXED_SRC = re.compile(r"(gross|GROSS|\bg\b|w)\s*/\s*(n|N)\b")
NORM_SRC = re.compile(r"div\([^)]*sum\(axis=1\)|/\s*k_t|/\s*k\b|\.sum\(axis=1\)\s*,\s*axis=0\)")
GROSS_COL = re.compile(r"(gross|GROSS)", re.I)
COUNT_COL = {"n", "N", "k", "K", "m", "width", "topn", "top_n", "n_names", "count", "nn"}

scripts = sorted(p for p in OUT.glob("*.py") if not p.name.startswith(STEM))
crows = []
for sp in scripts:
    src = sp.read_text(errors="ignore")
    if not COUNT_DIAL_SRC.search(src):
        continue
    f, nm = bool(FIXED_SRC.search(src)), bool(NORM_SRC.search(src))
    cls = "BOTH" if (f and nm) else ("FIXED" if f else ("NORM" if nm else "UNKNOWN"))
    stem = sp.name[:-3]
    sibs = [p for p in OUT.glob(f"{stem}.*") if p.suffix in (".csv", ".gz")]
    gross_col = swept_n = max_n = 0
    for p in sibs:
        try:
            head = pd.read_csv(p, nrows=0)
        except Exception:
            continue
        cols = list(head.columns)
        if any(GROSS_COL.fullmatch(str(c)) or str(c).lower() in
               ("gross", "realised_gross", "real_gross", "g", "gross_real") for c in cols):
            gross_col = 1
        nc = [c for c in cols if str(c) in COUNT_COL]
        if nc:
            try:
                d = pd.read_csv(p, usecols=nc[:1])
            except Exception:
                continue
            v = pd.to_numeric(d[nc[0]], errors="coerce").dropna()
            if v.nunique() >= 3:
                swept_n = 1
                max_n = max(max_n, int(v.max()))
    crows.append(dict(script=sp.name, construction=cls, publishes_gross_col=gross_col,
                      csv_sweeps_count=swept_n, max_swept_n=max_n, n_sibling_csvs=len(sibs)))
CEN = pd.DataFrame(crows)
CEN.to_csv(OUT / f"{STEM}.census.csv", index=False)
P(f"  committed scripts scanned: {len(scripts)};  carrying a COUNT DIAL in source: {len(CEN)}")
vc = CEN.construction.value_counts()
P("  construction, by source regex (UNKNOWN counted, never guessed): "
  + ", ".join(f"{k} {v} ({v / len(CEN):.0%})" for k, v in vc.items()))
fx = CEN[CEN.construction.isin(["FIXED", "BOTH"])]
P(f"  files whose source contains the FIXED g/n construction: {len(fx)} "
  f"({len(fx) / len(CEN):.0%} of count-dial files)")
nog = int((CEN.publishes_gross_col == 0).sum())
P(f"  count-dial files publishing NO realised-gross column: {nog} of {len(CEN)} "
  f"({nog / len(CEN):.1%}) -> P1 predicted a majority: {'HIT' if nog / len(CEN) > 0.5 else 'MISS'}")
nog_fx = int((fx.publishes_gross_col == 0).sum())
P(f"  ... restricted to FIXED/BOTH files: {nog_fx} of {len(fx)} "
  f"({nog_fx / max(len(fx), 1):.1%}) publish no gross column")
sw = CEN[CEN.csv_sweeps_count == 1]
P(f"  count-dial files whose committed CSVs actually sweep a count column (>=3 values): "
  f"{len(sw)};  of those, max swept n >= 40 in {int((sw.max_swept_n >= 40).sum())} and >= 60 in "
  f"{int((sw.max_swept_n >= 60).sum())}")
exposed = sw[(sw.max_swept_n >= 40) & (sw.construction.isin(["FIXED", "BOTH"]))]
P(f"  EXPOSED POPULATION — FIXED/BOTH construction AND a swept n >= 40 (where u56's eligible "
  f"count runs out): {len(exposed)} files, of which {int((exposed.publishes_gross_col == 0).sum())} "
  f"publish no gross column and are therefore un-checkable from their own artefacts")

# =====================================================================================
# PART B — MEASUREMENT
# =====================================================================================
P("\n" + "-" * 118)
P("B0  PANELS")
P("-" * 118)


def small_panel():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    return px[[c for c in px.columns if c not in bad]]


PANELS = {"u56": load_universe(), "broad136": load_universe(broad=True),
          "small439": small_panel()}
for k, v in PANELS.items():
    P(f"  {k:<9} {v.shape[1]:>4} cols x {len(v):,} days  {v.index[0].date()} -> {v.index[-1].date()}"
      + ("   [44 max_1d_move>=1.0 names dropped]" if k == "small439" else ""))
P("  SURVIVORSHIP: current-constituent lists.  Levels biased up; the FIXED-minus-NORM contrast "
  "is the load-bearing number.")


def fast_bt(px, w, cost_bps=10.0, freq=FREQ):
    rets = px.pct_change().fillna(0.0).values
    wt = w.reindex(px.index).fillna(0.0).shift(1).fillna(0.0).values
    mask = rebalance_mask(px.index, freq).shift(1, fill_value=False).values
    T, N = rets.shape
    cur = np.zeros(N)
    held = np.empty((T, N))
    turn = np.zeros(T)
    for i in range(T):
        if mask[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum()
            cur = new.copy()
        held[i] = cur
        growth = cur * (1.0 + rets[i])
        tot = growth.sum() + (1.0 - cur.sum())
        if tot > 0:
            cur = growth / tot
    return (pd.Series((held * rets).sum(axis=1) - turn * cost_bps / 1e4, index=px.index),
            pd.Series(turn, index=px.index))


def mets(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    return (float(eq.iloc[-1] ** (1 / yrs) - 1), float(r.mean() * 252 / vol) if vol else np.nan,
            float((eq / eq.cummax() - 1).min()))


def eligible(px):
    s, above, vol20 = score(px, vol_scale=True)
    return s.where(above & (vol20 < 0.60))


def count_book(px, n, g, conv):
    """FIXED: g/n on every admitted name (de-grosses under saturation).
       NORM : g/k_t on every admitted name, k_t = min(n, E_t) (gross pinned)."""
    elig = eligible(px)
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float).where(elig.notna(), 0.0)
    if conv == "FIXED":
        return sel * (g / n)
    k = sel.sum(axis=1).replace(0, np.nan)
    return sel.div(k, axis=0).fillna(0.0) * g


P("\n" + "-" * 118)
P("B1  GATES — nothing below is read until these pass")
P("-" * 118)
gpx = PANELS["u56"]
w = count_book(gpx, 20, 0.75, "FIXED")
rf, tf = fast_bt(gpx, w, 10.0)
eng = backtest(gpx, w, cost_bps=10.0, freq=FREQ)
g1, g2 = float(np.abs(rf - eng["returns"]).max()), float(np.abs(tf - eng["turnover"]).max())
P(f"  fast_bt vs engine.backtest @10bps: returns {g1:.3e};  turnover {g2:.3e}")
r0, t0 = fast_bt(gpx, w, 0.0)
g3 = float(np.abs((r0 - t0 * 25 / 1e4) - backtest(gpx, w, cost_bps=25.0, freq=FREQ)["returns"]).max())
P(f"  cost-rung identity net(25) = net(0) - turnover*25/1e4: {g3:.3e}")
g4 = float(np.abs(count_book(gpx, 5, 5 * 0.15, "FIXED").fillna(0)
                  - rules_v1_weights(gpx).fillna(0)).max().max())
P(f"  FIXED at n=5, g=0.75 nests baseline.rules_v1_weights: {g4:.3e}")
wF = count_book(gpx, 5, 0.75, "FIXED")
wN = count_book(gpx, 5, 0.75, "NORM")
kt = (wF > 0).sum(axis=1)                      # names actually admitted that day
un = kt == 5
g5 = float(np.abs(wF[un] - wN[un]).max().max())
P(f"  NORM == FIXED on every day with k_t == n (the channel is provably CLOSED off saturation, "
  f"{int(un.sum()):,} of {len(un):,} days at n=5): {g5:.3e}")
P(f"  [note] k_t < n on {int((kt < 5).sum()):,} days at n=5 even though eligible E_t >= 5 on "
  f"{int((eligible(gpx).notna().sum(axis=1) >= 5).sum()):,}: `rank <= n` drops TIED names, so "
  f"the FIXED book de-grosses on ties as well as on breadth.  Both conventions share the same "
  f"selection, so the contrast is unaffected; saturation below is measured on k_t, not E_t.")
GOK = max(g1, g2, g3, g4, g5) < 1e-12
P(f"  GATES {'PASS' if GOK else 'FAIL'}")
assert GOK, "gate failure"

P("\n" + "-" * 118)
P("B2  THE CHANNEL — realised gross and saturation by (panel, n) at nominal g = 1.00")
P("-" * 118)
ch = []
for pname, px in PANELS.items():
    E = eligible(px).notna().sum(axis=1)
    rb = rebalance_mask(px.index, FREQ)
    Erb = E[rb].loc[px.index[260]:]
    P(f"  [{pname}] eligible names per rebalance day: median {Erb.median():.0f}, "
      f"p10 {Erb.quantile(0.1):.0f}, p90 {Erb.quantile(0.9):.0f}, max {Erb.max():.0f}")
    for n in N_GRID:
        wF = count_book(px, n, 1.00, "FIXED")
        gr = wF.sum(axis=1)[rb].loc[px.index[260]:]
        ktrb = (wF > 0).sum(axis=1)[rb].loc[px.index[260]:]
        sat = float((ktrb < n).mean())          # measured on admitted names, not eligible names
        ch.append(dict(panel=pname, n=n, median_elig=float(Erb.median()),
                       realised_gross_mean=float(gr.mean()), realised_gross_median=float(gr.median()),
                       realised_gross_p10=float(gr.quantile(0.1)), sat_share=sat))
        P(f"      n={n:>3}  realised gross (nominal 1.00): mean {gr.mean():.3f} "
          f"median {gr.median():.3f} p10 {gr.quantile(0.1):.3f};  saturated on {sat:.1%} of "
          f"rebalance days")
CH = pd.DataFrame(ch)
CH.to_csv(OUT / f"{STEM}.channel.csv", index=False)
mono = []
for pname in PANELS:
    s = CH[CH.panel == pname].sort_values("n")
    med = s.median_elig.iloc[0]
    tail = s[s.n >= med]
    ok = bool((tail.realised_gross_mean.diff().dropna() <= 1e-12).all()) and len(tail) > 1
    lowest = float(s.realised_gross_mean.iloc[-1])
    mono.append((pname, ok, lowest))
    P(f"  [{pname}] monotone-decreasing realised gross for n >= median eligible ({med:.0f}): "
      f"{'YES' if ok else 'NO'};  realised gross at the widest n: {lowest:.3f}")
p2 = all(o for _, o, _ in mono) and sum(1 for _, _, l in mono if l < 0.6) >= 2
P(f"  P2 {'HIT' if p2 else 'MISS'}")

P("\n" + "-" * 118)
P("B3/B4  THE GRID — 3 panels x 6 widths x 3 gross x 2 conventions x 2 rungs, weekly, next-day")
P("-" * 118)
rows = []
for pname, px in PANELS.items():
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    h = len(spy) // 2
    sC, sS, sD = mets(spy)
    sH1, sH2 = mets(spy.iloc[:h])[1], mets(spy.iloc[h:])[1]
    sO = mets(spy.loc[OOS_START:])[1]
    P(f"  [{pname}] SPY: CAGR {sC:.2%} Sharpe {sS:.3f} (H1 {sH1:.3f}/H2 {sH2:.3f}) "
      f"MaxDD {sD:.2%}; OOS Sharpe {sO:.3f}")
    br0, bt0 = fast_bt(px, rules_v2_weights(px), 0.0)
    rb = rebalance_mask(px.index, FREQ)
    for conv in ("FIXED", "NORM"):
        for n in N_GRID:
            for g in G_GRID:
                w = count_book(px, n, g, conv)
                r0, t0 = fast_bt(px, w, 0.0)
                gr = float(w.sum(axis=1)[rb].loc[start:].mean())
                for c in RUNGS:
                    r = (r0 - t0 * c / 1e4).loc[start:]
                    C, S, D = mets(r)
                    H1, H2 = mets(r.iloc[:h])[1], mets(r.iloc[h:])[1]
                    OC, OS_, OD = mets(r.loc[OOS_START:])
                    bl = (br0 - bt0 * c / 1e4).loc[start:]
                    bC, bS, bD = mets(bl)
                    bH1, bH2 = mets(bl.iloc[:h])[1], mets(bl.iloc[h:])[1]
                    bars = dict(H1=H1 > sH1, H2=H2 > sH2, OOS=OS_ > sO,
                                DD=D >= 0.6 * sD, CAGR=C >= 0.7 * sC)
                    rows.append(dict(panel=pname, conv=conv, n=n, gross=g, cost=c,
                                     realised_gross=gr, CAGR=C, Sharpe=S, MaxDD=D, H1=H1, H2=H2,
                                     OOS_Sharpe=OS_, OOS_CAGR=OC, OOS_MaxDD=OD,
                                     turnover=float(t0.loc[start:].sum() / (len(r) / 252)),
                                     pass4b=all(bars.values()),
                                     fail4b="|".join(k for k, v in bars.items() if not v) or "-",
                                     pass4a=(H1 > bH1 and H2 > bH2 and D >= bD),
                                     spy_CAGR=sC, spy_Sharpe=sS, spy_MaxDD=sD, spy_OOS_Sharpe=sO,
                                     base_Sharpe=bS, base_CAGR=bC, base_MaxDD=bD))
GR = pd.DataFrame(rows)
GR.to_csv(OUT / f"{STEM}.grid.csv", index=False)
P(f"  grid points: {len(GR)} (all reported in {STEM}.grid.csv)")

P("\n  WIDTH CURVE, both conventions, at nominal g = 1.00, 10 bps "
  "(Sharpe is invariant to a CONSTANT gross; it is not invariant to FIXED's breadth-conditional one)")
for pname in PANELS:
    P(f"  [{pname}]   n     FIXED: rgross  CAGR   Sharpe   MaxDD  |  NORM:  CAGR   Sharpe   MaxDD "
      f" |  dSharpe(F-N)  dCAGR   dMaxDD")
    for n in N_GRID:
        f = GR[(GR.panel == pname) & (GR.conv == "FIXED") & (GR.n == n) & (GR.gross == 1.0)
               & (GR.cost == 10)].iloc[0]
        nn = GR[(GR.panel == pname) & (GR.conv == "NORM") & (GR.n == n) & (GR.gross == 1.0)
                & (GR.cost == 10)].iloc[0]
        P(f"            {n:>3}          {f.realised_gross:.3f} {f.CAGR:7.2%} {f.Sharpe:8.3f} "
          f"{f.MaxDD:7.2%}  |       {nn.CAGR:7.2%} {nn.Sharpe:8.3f} {nn.MaxDD:7.2%}  |  "
          f"{f.Sharpe - nn.Sharpe:+8.4f}  {f.CAGR - nn.CAGR:+7.2%} {f.MaxDD - nn.MaxDD:+7.2%}")

P("\n  WIDTH PREMIUM — Sharpe(n) - Sharpe(n=%d), the quantity published count sweeps report" % N_REF)
prem = []
for pname in PANELS:
    for c in RUNGS:
        line = f"  [{pname} @{c}bps] "
        for conv in ("FIXED", "NORM"):
            ref = GR[(GR.panel == pname) & (GR.conv == conv) & (GR.n == N_REF)
                     & (GR.gross == 1.0) & (GR.cost == c)].Sharpe.iloc[0]
            wide = GR[(GR.panel == pname) & (GR.conv == conv) & (GR.n == max(N_GRID))
                      & (GR.gross == 1.0) & (GR.cost == c)].Sharpe.iloc[0]
            narrow = GR[(GR.panel == pname) & (GR.conv == conv) & (GR.n == min(N_GRID))
                        & (GR.gross == 1.0) & (GR.cost == c)].Sharpe.iloc[0]
            line += (f"{conv}: wide-ref {wide - ref:+.4f}  narrow-ref {narrow - ref:+.4f}   ")
            prem.append(dict(panel=pname, cost=c, conv=conv, wide_minus_ref=wide - ref,
                             narrow_minus_ref=narrow - ref))
        P(line)
PREM = pd.DataFrame(prem)
p3 = 0
for pname in PANELS:
    f = abs(PREM[(PREM.panel == pname) & (PREM.conv == "FIXED") & (PREM.cost == 10)].wide_minus_ref.iloc[0])
    nn = abs(PREM[(PREM.panel == pname) & (PREM.conv == "NORM") & (PREM.cost == 10)].wide_minus_ref.iloc[0])
    p3 += int(nn < f)
    P(f"  [{pname} @10bps] |wide - ref| FIXED {f:.4f} vs NORM {nn:.4f} -> the channel accounts "
      f"for {(f - nn) / f * 100 if f else float('nan'):.0f}% of the published magnitude")
P(f"  P3 (NORM smaller on >=2 of 3 panels): {'HIT' if p3 >= 2 else 'MISS'} ({p3}/3)")

P("\n  PAIRWISE WIDTH COMPARISONS — does closing the channel FLIP the sign of 'wider is better'?")
flips = []
for pname in PANELS:
    for g in G_GRID:
        for c in RUNGS:
            for i, n1 in enumerate(N_GRID):
                for n2 in N_GRID[i + 1:]:
                    q = GR[(GR.panel == pname) & (GR.gross == g) & (GR.cost == c)]
                    dF = (q[(q.conv == "FIXED") & (q.n == n2)].Sharpe.iloc[0]
                          - q[(q.conv == "FIXED") & (q.n == n1)].Sharpe.iloc[0])
                    dN = (q[(q.conv == "NORM") & (q.n == n2)].Sharpe.iloc[0]
                          - q[(q.conv == "NORM") & (q.n == n1)].Sharpe.iloc[0])
                    flips.append(dict(panel=pname, gross=g, cost=c, n1=n1, n2=n2,
                                      dS_FIXED=dF, dS_NORM=dN,
                                      flip=bool(np.sign(dF) != np.sign(dN))))
FL = pd.DataFrame(flips)
FL.to_csv(OUT / f"{STEM}.flips.csv", index=False)
P(f"  pairwise comparisons: {len(FL)};  SIGN FLIPS when the channel is closed: "
  f"{int(FL.flip.sum())} ({FL.flip.mean():.1%})")
for pname in PANELS:
    s = FL[FL.panel == pname]
    P(f"    [{pname}] {int(s.flip.sum())} of {len(s)} ({s.flip.mean():.1%});  mean |dS| FIXED "
      f"{s.dS_FIXED.abs().mean():.4f} vs NORM {s.dS_NORM.abs().mean():.4f}")

P("\n  4b / 4a VERDICT FLIPS between the two conventions (same panel, n, gross, rung)")
piv = GR.pivot_table(index=["panel", "n", "gross", "cost"], columns="conv",
                     values=["pass4b", "pass4a"], aggfunc="first")
f4b = piv[("pass4b", "FIXED")] != piv[("pass4b", "NORM")]
f4a = piv[("pass4a", "FIXED")] != piv[("pass4a", "NORM")]
P(f"  cells: {len(piv)};  4b verdict flips {int(f4b.sum())};  4a verdict flips {int(f4a.sum())}")
P(f"  4b passes: FIXED {int(piv[('pass4b', 'FIXED')].sum())}, "
  f"NORM {int(piv[('pass4b', 'NORM')].sum())};  4a passes: FIXED "
  f"{int(piv[('pass4a', 'FIXED')].sum())}, NORM {int(piv[('pass4a', 'NORM')].sum())}")
if int(f4b.sum()):
    for k in piv[f4b].index[:12]:
        P(f"      FLIP 4b: panel={k[0]} n={k[1]} g={k[2]} {k[3]}bps  FIXED="
          f"{piv.loc[k, ('pass4b', 'FIXED')]} NORM={piv.loc[k, ('pass4b', 'NORM')]}")
P(f"  P4 (at least one 4b flip): {'HIT' if int(f4b.sum()) >= 1 else 'MISS'}")

P("\n" + "-" * 118)
P("B5  RULE 8 — n chosen on IS <= 2016-12-31 by IS Sharpe under EACH convention, "
  "2017-2026 read once")
P("-" * 118)
wf = []
for pname, px in PANELS.items():
    start = px.index[260]
    spy = px["SPY"].pct_change().fillna(0.0).loc[start:]
    br0, bt0 = fast_bt(px, rules_v2_weights(px), 0.0)
    for c in RUNGS:
        picks = {}
        for conv in ("FIXED", "NORM"):
            cand = []
            for n in N_GRID:
                for g in G_GRID:
                    r0, t0 = fast_bt(px, count_book(px, n, g, conv), 0.0)
                    r = (r0 - t0 * c / 1e4).loc[start:]
                    cand.append((n, g, mets(r.loc[:IS_END])[1], r))
            picks[conv] = max(cand, key=lambda x: x[2])
        so = spy.loc[OOS_START:]
        bo = (br0 - bt0 * c / 1e4).loc[start:].loc[OOS_START:]
        sC, sS, sD = mets(so)
        bC, bS, bD = mets(bo)
        row = dict(panel=pname, cost=c, spy_OOS_CAGR=sC, spy_OOS_Sharpe=sS, spy_OOS_MaxDD=sD,
                   base_OOS_CAGR=bC, base_OOS_Sharpe=bS, base_OOS_MaxDD=bD,
                   same_pick=(picks["FIXED"][0] == picks["NORM"][0]))
        for conv in ("FIXED", "NORM"):
            n, g, iss, r = picks[conv]
            C, S, D = mets(r.loc[OOS_START:])
            row[f"{conv}_n"] = n
            row[f"{conv}_g"] = g
            row[f"{conv}_IS"] = iss
            row[f"{conv}_OOS_CAGR"] = C
            row[f"{conv}_OOS_Sharpe"] = S
            row[f"{conv}_OOS_MaxDD"] = D
        wf.append(row)
        P(f"  [{pname} @{c}bps] FIXED picks n={picks['FIXED'][0]} g={picks['FIXED'][1]:.2f} "
          f"-> OOS {row['FIXED_OOS_CAGR']:7.2%} / {row['FIXED_OOS_Sharpe']:.3f} / "
          f"{row['FIXED_OOS_MaxDD']:7.2%}   |   NORM picks n={picks['NORM'][0]} "
          f"g={picks['NORM'][1]:.2f} -> OOS {row['NORM_OOS_CAGR']:7.2%} / "
          f"{row['NORM_OOS_Sharpe']:.3f} / {row['NORM_OOS_MaxDD']:7.2%}   |   RULES v2 "
          f"{bC:7.2%} / {bS:.3f} / {bD:7.2%}   |   SPY {sC:7.2%} / {sS:.3f} / {sD:7.2%}")
WF = pd.DataFrame(wf)
WF.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
diff = int((~WF[WF.cost == 10].same_pick).sum())
P(f"  @10bps the convention changes the IS-chosen n on {diff} of 3 panels -> "
  f"P5 {'HIT' if diff >= 1 else 'MISS'}")
P(f"  OOS Sharpe, FIXED pick minus NORM pick: "
  + ", ".join(f"{r.panel}@{r.cost} {r.FIXED_OOS_Sharpe - r.NORM_OOS_Sharpe:+.4f}"
              for _, r in WF.iterrows()))
P(f"  picks beating SPY OOS: FIXED {int((WF.FIXED_OOS_Sharpe > WF.spy_OOS_Sharpe).sum())}/"
  f"{len(WF)}, NORM {int((WF.NORM_OOS_Sharpe > WF.spy_OOS_Sharpe).sum())}/{len(WF)};  beating "
  f"RULES v2 OOS: FIXED {int((WF.FIXED_OOS_Sharpe > WF.base_OOS_Sharpe).sum())}/{len(WF)}, "
  f"NORM {int((WF.NORM_OOS_Sharpe > WF.base_OOS_Sharpe).sum())}/{len(WF)}")

pd.DataFrame([dict(param="n", values=str(N_GRID)), dict(param="gross", values=str(G_GRID)),
              dict(param="convention (treatment, not a dial)", values="FIXED|NORM"),
              dict(param="cost_bps (reported)", values=str(RUNGS)),
              dict(param="freq (fixed)", values=FREQ),
              dict(param="IS_END", values=IS_END)]).to_csv(OUT / f"{STEM}.params.csv", index=False)

P("\n" + "=" * 118)
P(f"done in {time.time() - T0:.1f}s")
P("=" * 118)
(OUT / f"{STEM}.console.txt").write_text("\n".join(_lines) + "\n")
