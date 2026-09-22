#!/usr/bin/env python3
"""
IDEA 915 (lane cloud, run 4, 2026-09-22) --
    does-ANY-committed-4b-DD-MARGIN-in-the-record-survive-the-2022-BAR

THE QUESTION, as filed.  Idea 912 found that EXCISING 2020 moves SPY's OOS worst decline from
-33.72% (24 days, 2020) to -24.50% (196 days, 2022), which tightens PROTOCOL's 4b DD cap from
-20.23% to -14.70%, and that the record's only rule-8-reachable 4b pass loses its DD leg on
exactly that move.  The filed line asks the record to be re-scored against the 2022 bar.

HOW THIS RUN READS IT.  A prose census of committed 4b passes has no price leg and cannot
carry PROTOCOL's step-3 deliverable, so the question is run as a FRESHLY PRICED SHELF instead:
a mechanical set of books spanning the forms the record actually commits (the live RULES v2
band book, the 2026-09-04 KEEP-4b top-N equal-weight incumbent, and a 12-1 momentum shelf),
scored under BOTH DD bars on three panels.  Every 4b DD margin reported here is one this run
priced itself.

AND THE HALF IDEA 912 DID NOT SEPARATE.  Excising an episode can be done two ways, and they
are NOT the same test.  Both are published side by side at every cell:
    BARONLY   the BAR moves and the BOOK does not: SPY's MaxDD is read on the excised tape,
              the book's on the full tape.  This is 912's reading as written.  It compares
              two different tapes and is the HARSH form.
    MATCHED   BOTH legs are read on the SAME excised tape.  "Outside the 2020 episode, is the
              book still within 60% of SPY's drawdown?"  This is the FAIR form.
If a DD margin dies under BARONLY and lives under MATCHED, it was never a "2020 margin" -- it
was a window mismatch, and the record would have retired a pass for the wrong reason.

TUNED PARAMETERS -- EXACTLY TWO, as the idea line specifies ("claim set, excision window"),
and EVERY grid point is published (<slug>.grid.csv):
    1. EXCISION WINDOW e in {NONE, COVID (2020-02-19..2020-06-30), CY2020 (2020-01-01..
       2020-12-31), GFC+COVID (2008-09-01..2009-06-30 plus COVID)}
    2. CLAIM SET (book width) n in {10, 20, 40} -- the shelf's only free dial.
NOT TUNED, declared before any number was read:
    BOOK FORM {EWELIG (= RULES v2's own band form), TOPn (baseline.score composite),
      MOMn (12-1 momentum)} -- an axis that is REPORTED at every rung, never selected on.
    GROSS g in {0.75, 1.00}; CADENCE in {W, M}; COST c in {0,10,25,50} bps (PROTOCOL's rung
      is 10); PANEL {U56, B136, SMALL}; WINDOWS FULL / IS (..2016-12-31) / OOS (2017-01-01..).
    CONVENTION {BARONLY, MATCHED} is REPORTED, never chosen: both appear at every cell.

PRE-REGISTERED BARS -- written before any number below was read:
  B1  THE QUESTION.  Of the cells that PASS 4b under the NONE (published) bar, what share
      still pass under each excision, per convention?  The complement is the share whose 4b
      pass is a 2020 margin.  Reported per panel per window at 10 bps.
  B2  THE DD LEG ALONE.  Same question restricted to the DD leg, so a cell that was already
      failing on CAGR cannot flatter the count.
  B3  THE BAR ITSELF.  Publish SPY's MaxDD and the implied 0.60x cap under every excision,
      per panel per window, and the length and end date of the binding decline.  Gate G7
      reproduces idea 912's -33.72% -> -24.50% and -20.23% -> -14.70%.
  B4  COST.  B1/B2 re-read at 0 / 25 / 50 bps.
  B5  RULE 8.  (excision, n) chosen on the IS window ONLY by IS Sharpe; 2017-2026 read ONCE.
      Report OOS CAGR / Sharpe / MaxDD against RULES v2 and SPY, BOTH KEEP paths, under BOTH
      bars and BOTH conventions.
  B6  PATH 4a at every grid point, against live RULES v2 on the same panel and window.
  B7  CONTROL.  A book whose own worst decline is NOT a 2020 episode cannot lose its DD leg
      to a 2020 excision under MATCHED.  Report each book's binding decline end-date, so the
      B1 count can be read against the mechanism instead of assumed.
  B8  THE RECORD'S NEWEST CLAUSE, turned on whatever this run produces.  Idea 914's clause
      (hardened by 2115, generalised by 2119, and turned on the live book by idea 2111 in
      THIS SAME RUN) says a 4b margin inside the book's own 5-offset rebalance spread is not
      a pass.  Apply it to every book here that passes 4b in BOTH the FULL and the OOS
      window, at that book's OWN cadence.  A candidate that cannot clear it is not proposed.

GATES, printed before any hypothesis is read:
  G1  local run()+net() == engine.backtest(freq, 10 bps)     bar max|d| < 1e-12
  G2  EWELIG @ (band 0.03, gross 0.75, W) == baseline.rules_v2_weights   bar max|d| == 0
  G3  excision is a row DROP: len(excised) == len(full) - |window|, and e=NONE is identity
      (max|d| == 0 against the unexcised series)
  G4  SMALL panel hygiene: every ticker with max_1d_move >= 1.0 in data/small_meta.csv is
      dropped before any pricing
  G5  comparands are baseline's own: rules_v2_weights and SPY buy-and-hold
  G6  every book is long-only with realised gross <= its nominal gross
  G7  idea 912's numbers reproduce: SPY OOS MaxDD -33.72% (full) -> -24.50% (COVID excised),
      cap -20.23% -> -14.70%, binding decline moves from a 2020 episode to a 2022 one

SPLICE CAVEAT (stated, not repaired).  An excised series is a SPLICE no investor experienced:
dropping the 2020 rows joins 2020-02-18 to 2020-07-01 as if they were consecutive sessions.
Every excised number here is therefore a counterfactual bar, not a tradable result.  That is
exactly what idea 912 proposed and what the filed line asks to be priced; it is published as
such and no book is recommended on an excised reading.

SURVIVORSHIP (PROTOCOL rule 9).  U56, B136 and SMALL are CURRENT-CONSTITUENT lists, so every
absolute CAGR and drawdown level here is optimistic.  SMALL is the sub-$2B screen's survivors
since 2010 and its levels are the most optimistic of the three.  The excision contrast is
within-tape -- same names, same books, only the calendar window moves -- and does not repair
the level.

run / net are lane B's (2026-09-22_4b-margin-vs-own-offset-spread-...), unchanged, so this
run's paths are the same instrument the record's other 2026-09-22 runs used.

Deterministic, offline, standalone:
    python research/backtests/2026-09-22_4b-dd-margin-vs-the-2022-bar_cloud.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score      # noqa
from engine import backtest, metrics, rebalance_mask                         # noqa

SLUG = "2026-09-22_4b-dd-margin-vs-the-2022-bar_cloud"
OUT = ROOT / "research" / "backtests"
LINES = []
def P(s=""):
    print(s); LINES.append(str(s))

# TUNED axis 1 -- excision windows
EXCISIONS = {
    "NONE":      [],
    "COVID":     [("2020-02-19", "2020-06-30")],
    "CY2020":    [("2020-01-01", "2020-12-31")],
    "GFC+COVID": [("2008-09-01", "2009-06-30"), ("2020-02-19", "2020-06-30")],
}
WIDTHS  = [10, 20, 40]            # TUNED axis 2 -- the shelf's claim set
FORMS   = ["EWELIG", "TOP", "MOM"]
GROSSES = [0.75, 1.00]
CADENCE = ["W", "M"]
COSTS   = [0, 10, 25, 50]
COST0   = 10
IS_END  = "2016-12-31"
OOS_BEG = "2017-01-01"
CONVS   = ["BARONLY", "MATCHED"]
LEGUNIT = dict(H1=("H1", 1.0), H2=("H2", 1.0), DD=("MaxDD", 100.0), CAGR=("CAGR", 100.0))
WINS    = ["FULL", "IS", "OOS"]


# ---------------------------------------------------------------- backtester (lane B's)
def run(prices, weights, mask):
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(prices.index).fillna(0.0).shift(1).values
    m = mask.shift(1, fill_value=False).values
    n = len(prices)
    cur = np.zeros(prices.shape[1])
    gross_ret = np.empty(n); turn = np.zeros(n); grs = np.empty(n)
    for i in range(n):
        if m[i] or i == 0:
            new = wt[i]
            turn[i] = np.abs(new - cur).sum(); cur = new
        gross_ret[i] = np.nansum(cur * rets[i]); grs[i] = cur.sum()
        growth = cur * (1 + rets[i])
        tot = growth.sum() + (1 - cur.sum())
        cur = growth / tot if tot > 0 else cur
    return (pd.Series(gross_ret, index=prices.index), pd.Series(turn, index=prices.index),
            pd.Series(grs, index=prices.index))


def net(gross_ret, turnover, cost_bps):
    return gross_ret - turnover * cost_bps / 1e4


def offset_mask(idx, d, freq):
    """True d trading days BEFORE the last trading day of each period.  d=0 == rebalance_mask.
    Lane B's instrument (2026-09-22_4b-margin-vs-own-offset-spread-...), generalised to freq."""
    key = pd.Series({"W": idx.to_period("W"), "M": idx.to_period("M")}[freq], index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


# ---------------------------------------------------------------- the shelf
def book_weights(px, form, n, gross, band=0.03):
    """EWELIG is RULES v2's own band form (gate G2 at n irrelevant, gross 0.75).  TOP/MOM are
    top-n equal-weight shelves, the 2026-09-04 KEEP-4b incumbent's form."""
    if form == "EWELIG":
        e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
        ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
        return ew.where(band_state(px, band), 0.0)
    if form == "TOP":
        s, _, _ = score(px, vol_scale=False)
    else:
        s = px.shift(21) / px.shift(252) - 1
    s = s.drop(columns=["SPY"], errors="ignore")
    rank = s.rank(axis=1, ascending=False)
    w = (rank <= n).astype(float)
    w = gross * w.div(w.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return w.reindex(columns=px.columns).fillna(0.0)


# ---------------------------------------------------------------- excision + scoring
def excise(r, key):
    """Drop the excised rows and SPLICE.  e='NONE' is the identity (gate G3)."""
    if key == "NONE":
        return r
    m = pd.Series(True, index=r.index)
    for a, b in EXCISIONS[key]:
        m &= ~((r.index >= a) & (r.index <= b))
    return r[m.values]


def dd_detail(r):
    eq = (1 + r).cumprod(); dd = eq / eq.cummax() - 1
    i = int(np.argmin(dd.values))
    peak = int(np.argmax(eq.values[: i + 1]))
    return float(dd.min()), str(r.index[i].date()), int(i - peak)


def stats(r):
    m = metrics(r); h = len(r) // 2
    return dict(CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                H1=metrics(r.iloc[:h])["Sharpe"], H2=metrics(r.iloc[h:])["Sharpe"])


def legs4b(s, ss):
    L = dict(H1=s["H1"] > ss["H1"], H2=s["H2"] > ss["H2"],
             DD=s["MaxDD"] >= 0.60 * ss["MaxDD"], CAGR=s["CAGR"] >= 0.70 * ss["CAGR"])
    M = dict(H1=s["H1"] - ss["H1"], H2=s["H2"] - ss["H2"],
             DD=(s["MaxDD"] - 0.60 * ss["MaxDD"]) * 100,
             CAGR=(s["CAGR"] - 0.70 * ss["CAGR"]) * 100)
    return all(L.values()), L, M


def legs4a(s, sb):
    return (s["H1"] > sb["H1"]) and (s["H2"] > sb["H2"]) and (s["MaxDD"] >= sb["MaxDD"])


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta["max_1d_move"] >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad), len([c for c in px.columns if c != "SPY"])


def win_slices(r, start):
    r = r.loc[start:]
    return dict(FULL=r, IS=r.loc[:IS_END], OOS=r.loc[OOS_BEG:])


# ==========================================================================================
def main():
    P("=" * 100)
    P("IDEA 915  lane cloud run 4  2026-09-22 -- DOES ANY 4b DD MARGIN SURVIVE THE 2022 BAR?")
    P("=" * 100)
    P(f"run {pd.Timestamp.now(tz='UTC'):%Y-%m-%d %H:%M} UTC")
    P(f"tuned: EXCISION {list(EXCISIONS)} x WIDTH n {WIDTHS}")
    P(f"reported, not tuned: form {FORMS}, gross {GROSSES}, cadence {CADENCE}, cost {COSTS} bps,")
    P(f"                     convention {CONVS}, panels U56/B136/SMALL, windows FULL/IS/OOS")
    P("")

    panels = {}
    panels["U56"] = load_universe()
    panels["B136"] = load_universe(broad=True)
    sm, n_drop, n_tot = load_small()
    panels["SMALL"] = sm
    for k, v in panels.items():
        P(f"  panel {k:6s} {v.shape[1]:4d} cols  {v.index[0].date()} .. {v.index[-1].date()}"
          f"  ({len(v)} sessions)")
    P(f"  SMALL hygiene (G4): dropped {n_drop} of {n_tot} names with max_1d_move >= 1.0")
    P("")

    # ------------------------------------------------------------------ GATES
    P("-" * 100)
    P("(G) GATES -- printed before any hypothesis is read")
    P("-" * 100)
    gate_rows, gp, gn = [], 0, 0
    px_u = panels["U56"]

    w_ew = book_weights(px_u, "EWELIG", 0, 0.75)
    g2 = float(np.nanmax(np.abs(w_ew.values - rules_v2_weights(px_u).values)))
    ok = g2 == 0.0; gp += ok; gn += 1
    P(f"  G2  EWELIG(band .03, gross .75) == baseline.rules_v2_weights : max|d| {g2:.3e}"
      f"   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G2", value=g2, bar="max|d| == 0", passed=bool(ok)))

    mW = rebalance_mask(px_u.index, "W")
    gr, to, grs = run(px_u, w_ew, mW)
    a = net(gr, to, COST0).values
    b = backtest(px_u, w_ew, cost_bps=COST0, freq="W")["returns"].values
    fin = np.isfinite(b)
    g1 = float(np.abs(a[fin] - b[fin]).max())
    ok = g1 < 1e-12; gp += ok; gn += 1
    P(f"  G1  local run()+net() == engine.backtest(W,{COST0}bps) : max|d| {g1:.3e}"
      f"   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G1", value=g1, bar="max|d| < 1e-12", passed=bool(ok)))

    spy_full = px_u["SPY"].pct_change().fillna(0).loc[px_u.index[260]:]
    id_ok = float(np.abs(excise(spy_full, "NONE").values - spy_full.values).max())
    lens = {k: len(excise(spy_full, k)) for k in EXCISIONS}
    ok = (id_ok == 0.0) and all(lens[k] < lens["NONE"] for k in EXCISIONS if k != "NONE")
    gp += ok; gn += 1
    P(f"  G3  excision is a row DROP and NONE is the identity : max|d| {id_ok:.3e}, "
      + " ".join(f"{k}={lens[k]}" for k in EXCISIONS) + f"   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G3", value=id_ok, bar="identity + strict drop", passed=bool(ok)))

    ok = n_drop > 0; gp += ok; gn += 1
    P(f"  G4  SMALL max_1d_move filter applied: {n_drop} dropped   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G4", value=n_drop, bar=">0 dropped", passed=bool(ok)))
    P("  G5  comparands: baseline.rules_v2_weights and SPY buy-and-hold  [PASS by construction]")
    gate_rows.append(dict(gate="G5", value=0, bar="baseline's own", passed=True))

    gmax = float(grs.max()); ok = gmax <= 0.75 + 1e-9; gp += ok; gn += 1
    P(f"  G6  long-only, realised gross <= nominal : max realised gross {gmax:.4f} vs 0.75"
      f"   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G6", value=gmax, bar="<= nominal gross", passed=bool(ok)))

    so = spy_full.loc[OOS_BEG:]
    d_f, e_f, l_f = dd_detail(so)
    d_c, e_c, l_c = dd_detail(excise(so, "COVID"))
    ok = (abs(d_f * 100 + 33.72) < 0.15 and abs(d_c * 100 + 24.50) < 0.6
          and e_f.startswith("2020") and e_c.startswith("2022"))
    gp += ok; gn += 1
    P(f"  G7  idea 912 reproduces : SPY OOS MaxDD {d_f:.2%} (trough {e_f}, {l_f}d) ->"
      f" {d_c:.2%} (trough {e_c}, {l_c}d);  cap {0.60*d_f:.2%} -> {0.60*d_c:.2%}"
      f"   [{'PASS' if ok else 'FAIL'}]")
    gate_rows.append(dict(gate="G7", value=d_c, bar="-24.50% +/- 0.6pp, trough in 2022",
                          passed=bool(ok)))
    P(f"  --> {gp} of {gn} gates PASS.")
    P("")

    # ------------------------------------------------------------------ B3 the bars
    P("-" * 100)
    P("(A) B3 -- THE BAR ITSELF.  SPY's MaxDD and the implied 0.60x 4b cap under every excision")
    P("-" * 100)
    spy_s, bars = {}, []
    for pname, px in panels.items():
        spy = px["SPY"].pct_change().fillna(0).loc[px.index[260]:]
        for wn, rr in win_slices(spy, spy.index[0]).items():
            for e in EXCISIONS:
                x = excise(rr, e)
                s = stats(x); dmin, dend, dlen = dd_detail(x)
                spy_s[(pname, wn, e)] = s
                bars.append(dict(panel=pname, win=wn, excision=e, spy_CAGR=s["CAGR"],
                                 spy_Sharpe=s["Sharpe"], spy_MaxDD=dmin, cap=0.60 * dmin,
                                 floor=0.70 * s["CAGR"], dd_trough=dend, dd_len=dlen,
                                 sessions=len(x)))
    bars = pd.DataFrame(bars)
    bars.to_csv(OUT / f"{SLUG}.bars.csv", index=False)
    P(f"{'panel':6s} {'win':5s} {'excision':10s} | {'SPY MaxDD':>10s} {'4b DD cap':>10s}"
      f" {'trough':>12s} {'len':>5s} | {'SPY CAGR':>9s} {'4b floor':>9s}")
    for _, r in bars.iterrows():
        P(f"{r.panel:6s} {r.win:5s} {r.excision:10s} | {r.spy_MaxDD:10.2%} {r.cap:10.2%}"
          f" {r.dd_trough:>12s} {r.dd_len:5d} | {r.spy_CAGR:9.2%} {r.floor:9.2%}")
    P("")

    # ------------------------------------------------------------------ the shelf
    P("-" * 100)
    P("(B) THE SHELF -- pricing")
    P("-" * 100)
    shelf = []
    for form in FORMS:
        for n in (WIDTHS if form != "EWELIG" else [0]):
            for g in GROSSES:
                for cad in CADENCE:
                    shelf.append((form, n, g, cad))
    P(f"  {len(shelf)} books per panel x {len(panels)} panels = {len(shelf)*len(panels)} paths")

    rows, paths = [], {}
    for pname, px in panels.items():
        start = px.index[260]
        masks = {c: rebalance_mask(px.index, c) for c in CADENCE}
        for (form, n, g, cad) in shelf:
            w = book_weights(px, form, n, g)
            gr, to, _ = run(px, w, masks[cad])
            for c in COSTS:
                r = net(gr, to, c)
                for wn, rr in win_slices(r, start).items():
                    for e in EXCISIONS:
                        x = excise(rr, e)
                        s = stats(x); dmin, dend, dlen = dd_detail(x)
                        s["MaxDD"] = dmin
                        paths[(pname, form, n, g, cad, c, wn, e)] = s
                        if e == "NONE" or True:
                            rows.append(dict(panel=pname, form=form, n=n, gross=g, cad=cad,
                                             cost=c, win=wn, excision=e, dd_trough=dend,
                                             dd_len=dlen, **s))
        P(f"  {pname:6s} priced")
    grid = pd.DataFrame(rows)
    grid.to_csv(OUT / f"{SLUG}.grid.csv.gz", index=False, compression="gzip")
    P(f"  GRID: {len(grid)} rows -> {SLUG}.grid.csv.gz")
    P("")

    # live RULES v2 comparand per panel/window (d=0, weekly, 10 bps, no excision)
    base_s = {}
    for pname, px in panels.items():
        gr, to, _ = run(px, rules_v2_weights(px), rebalance_mask(px.index, "W"))
        for wn, rr in win_slices(net(gr, to, COST0), px.index[260]).items():
            base_s[(pname, wn)] = stats(rr)

    # ------------------------------------------------------------------ B1/B2 the question
    P("-" * 100)
    P("(C) B1 + B2 -- OF THE 4b PASSES UNDER THE PUBLISHED BAR, HOW MANY SURVIVE EACH EXCISION?")
    P("-" * 100)
    cells = []
    for pname in panels:
        for (form, n, g, cad) in shelf:
            for c in COSTS:
                for wn in WINS:
                    k0 = (pname, form, n, g, cad, c, wn, "NONE")
                    s0 = paths[k0]
                    p0, L0, M0 = legs4b(s0, spy_s[(pname, wn, "NONE")])
                    row = dict(panel=pname, form=form, n=n, gross=g, cad=cad, cost=c, win=wn,
                               pass4b_NONE=p0, ddleg_NONE=L0["DD"], ddmrg_NONE=M0["DD"],
                               dd_trough=grid.loc[0, "dd_trough"] if False else None,
                               pass4a=legs4a(s0, base_s[(pname, wn)]))
                    row["dd_trough"] = None
                    for e in EXCISIONS:
                        if e == "NONE":
                            continue
                        # BARONLY: bar from the excised tape, book from the full tape
                        ssb = dict(spy_s[(pname, wn, "NONE")])
                        ssb["MaxDD"] = spy_s[(pname, wn, e)]["MaxDD"]
                        pb, Lb, Mb = legs4b(s0, ssb)
                        # MATCHED: both on the excised tape
                        sm_ = paths[(pname, form, n, g, cad, c, wn, e)]
                        pm, Lm, Mm = legs4b(sm_, spy_s[(pname, wn, e)])
                        row[f"pass4b_{e}_BARONLY"] = pb; row[f"ddleg_{e}_BARONLY"] = Lb["DD"]
                        row[f"ddmrg_{e}_BARONLY"] = Mb["DD"]
                        row[f"pass4b_{e}_MATCHED"] = pm; row[f"ddleg_{e}_MATCHED"] = Lm["DD"]
                        row[f"ddmrg_{e}_MATCHED"] = Mm["DD"]
                    cells.append(row)
    cd = pd.DataFrame(cells)
    cd.to_csv(OUT / f"{SLUG}.cells.csv.gz", index=False, compression="gzip")

    P(f"  {len(cd)} cells (panel x book x cost x window).  4b PASSES under the published bar:"
      f" {int(cd.pass4b_NONE.sum())}")
    P("")
    P("  B1 -- FULL 4b VERDICT.  survivors / passes (share), at 10 bps:")
    P(f"  {'panel':6s} {'win':5s} {'passes':>7s} | " +
      " | ".join(f"{e:>9s} BARONLY  MATCHED" for e in EXCISIONS if e != "NONE"))
    sub = cd[cd.cost == COST0]
    for pname in panels:
        for wn in WINS:
            s = sub[(sub.panel == pname) & (sub.win == wn)]
            base = s[s.pass4b_NONE]
            line = f"  {pname:6s} {wn:5s} {len(base):7d} | "
            parts = []
            for e in EXCISIONS:
                if e == "NONE":
                    continue
                nb = int(base[f"pass4b_{e}_BARONLY"].sum()); nm = int(base[f"pass4b_{e}_MATCHED"].sum())
                parts.append(f"{e:>9s} {nb:3d}      {nm:3d}")
            P(line + " | ".join(parts))
    P("")
    P("  B2 -- THE DD LEG ALONE (over cells whose DD leg passes under the published bar), 10 bps:")
    P(f"  {'panel':6s} {'win':5s} {'ddpass':>7s} | " +
      " | ".join(f"{e:>9s} BARONLY  MATCHED" for e in EXCISIONS if e != "NONE"))
    for pname in panels:
        for wn in WINS:
            s = sub[(sub.panel == pname) & (sub.win == wn)]
            base = s[s.ddleg_NONE]
            parts = []
            for e in EXCISIONS:
                if e == "NONE":
                    continue
                nb = int(base[f"ddleg_{e}_BARONLY"].sum()); nm = int(base[f"ddleg_{e}_MATCHED"].sum())
                parts.append(f"{e:>9s} {nb:3d}      {nm:3d}")
            P(f"  {pname:6s} {wn:5s} {len(base):7d} | " + " | ".join(parts))
    P("")
    P("  POOLED over all panels and windows, per cost rung (DD leg):")
    for c in COSTS:
        s = cd[cd.cost == c]; base = s[s.ddleg_NONE]
        parts = []
        for e in EXCISIONS:
            if e == "NONE":
                continue
            nb = base[f"ddleg_{e}_BARONLY"].mean(); nm = base[f"ddleg_{e}_MATCHED"].mean()
            parts.append(f"{e} B={nb:.3f} M={nm:.3f}")
        P(f"    {c:2d} bps  n={len(base):4d}  " + "   ".join(parts))
    P("")

    # ------------------------------------------------------------------ B7 the mechanism
    P("-" * 100)
    P("(D) B7 -- CONTROL: is the book's OWN binding decline a 2020 episode?")
    P("-" * 100)
    gg = grid[(grid.excision == "NONE") & (grid.cost == COST0)].copy()
    gg["trough_yr"] = gg.dd_trough.str[:4]
    for wn in WINS:
        s = gg[gg.win == wn]
        vc = s.trough_yr.value_counts().sort_index()
        P(f"  {wn:5s} n={len(s):4d}  binding-decline trough year: " +
          "  ".join(f"{k}={v}" for k, v in vc.items()))
    P(f"  SPY's own: " + "  ".join(
        f"{r.win}/{r.excision}={r.dd_trough}" for _, r in
        bars[(bars.panel == 'U56')].iterrows()))
    P("")

    # ------------------------------------------------------------------ B5 rule 8
    P("-" * 100)
    P("(E) B5 -- RULE 8.  (excision, n) chosen on IS ONLY by IS Sharpe; 2017-2026 read ONCE.")
    P("-" * 100)
    wf = []
    for pname in panels:
        for form in FORMS:
            ns = WIDTHS if form != "EWELIG" else [0]
            cand = [(e, n) for e in EXCISIONS for n in ns]
            # the IS objective is read on the EXCISED IS tape the excision names (legal: IS only)
            best = max(cand, key=lambda k: max(
                paths[(pname, form, k[1], g, cad, COST0, "IS", k[0])]["Sharpe"]
                for g in GROSSES for cad in CADENCE))
            e_, n_ = best
            g_, cad_ = max([(g, cad) for g in GROSSES for cad in CADENCE],
                           key=lambda gc: paths[(pname, form, n_, gc[0], gc[1], COST0, "IS", e_)]["Sharpe"])
            sO = paths[(pname, form, n_, g_, cad_, COST0, "OOS", "NONE")]
            bO = base_s[(pname, "OOS")]
            rec = dict(panel=pname, form=form, pick_excision=e_, pick_n=n_, gross=g_, cad=cad_,
                       IS_Sharpe=paths[(pname, form, n_, g_, cad_, COST0, "IS", e_)]["Sharpe"],
                       OOS_CAGR=sO["CAGR"], OOS_Sharpe=sO["Sharpe"], OOS_MaxDD=sO["MaxDD"],
                       base_CAGR=bO["CAGR"], base_Sharpe=bO["Sharpe"], base_MaxDD=bO["MaxDD"],
                       spy_CAGR=spy_s[(pname, "OOS", "NONE")]["CAGR"],
                       spy_Sharpe=spy_s[(pname, "OOS", "NONE")]["Sharpe"],
                       spy_MaxDD=spy_s[(pname, "OOS", "NONE")]["MaxDD"],
                       pass4a=legs4a(sO, bO))
            p0, L0, M0 = legs4b(sO, spy_s[(pname, "OOS", "NONE")])
            rec["pass4b_NONE"] = p0
            rec["fails_NONE"] = ",".join(k for k, v in L0.items() if not v) or "-"
            rec["ddmrg_NONE"] = M0["DD"]
            for e in EXCISIONS:
                if e == "NONE":
                    continue
                ssb = dict(spy_s[(pname, "OOS", "NONE")]); ssb["MaxDD"] = spy_s[(pname, "OOS", e)]["MaxDD"]
                pb = legs4b(sO, ssb)[0]
                sm_ = paths[(pname, form, n_, g_, cad_, COST0, "OOS", e)]
                pm = legs4b(sm_, spy_s[(pname, "OOS", e)])[0]
                rec[f"pass4b_{e}_BARONLY"] = pb; rec[f"pass4b_{e}_MATCHED"] = pm
            wf.append(rec)
    wfd = pd.DataFrame(wf)
    wfd.to_csv(OUT / f"{SLUG}.walkforward.csv", index=False)
    for _, r in wfd.iterrows():
        P(f"  {r.panel:6s} {r.form:6s} IS pick excision={r.pick_excision} n={r.pick_n}"
          f" (gross {r.gross}, {r.cad}; IS Sharpe {r.IS_Sharpe:.4f})")
        P(f"         OOS book     {r.OOS_CAGR:8.2%} {r.OOS_Sharpe:8.4f} {r.OOS_MaxDD:8.2%}")
        P(f"         OOS RULES v2 {r.base_CAGR:8.2%} {r.base_Sharpe:8.4f} {r.base_MaxDD:8.2%}")
        P(f"         OOS SPY      {r.spy_CAGR:8.2%} {r.spy_Sharpe:8.4f} {r.spy_MaxDD:8.2%}")
        P(f"         4b NONE {'PASS' if r.pass4b_NONE else 'FAIL on ' + r.fails_NONE}"
          f" (DD margin {r.ddmrg_NONE:+.2f} pp)   4a {'PASS' if r.pass4a else 'FAIL'}")
        P("         4b under excision:  " + "   ".join(
            f"{e} B={'P' if r[f'pass4b_{e}_BARONLY'] else 'F'}/M={'P' if r[f'pass4b_{e}_MATCHED'] else 'F'}"
            for e in EXCISIONS if e != "NONE"))
    P("")

    # ------------------------------------------------------------------ B6 4a
    P("-" * 100)
    P("(F) B6 -- PATH 4a at every grid point, against live RULES v2 on the same panel/window")
    P("-" * 100)
    for c in COSTS:
        s = cd[cd.cost == c]
        P(f"  {c:2d} bps  4a {int(s.pass4a.sum()):4d} of {len(s):4d} ({s.pass4a.mean():.3f})"
          f"   4b(published bar) {int(s.pass4b_NONE.sum()):4d} ({s.pass4b_NONE.mean():.3f})")
    P("")

    # ------------------------------------------------------------------ B8 the newest clause
    P("-" * 100)
    P("(G) B8 -- THE RECORD'S NEWEST CLAUSE (idea 914, hardened by 2115/2119, turned on the")
    P("           live book by 2111 THIS RUN) APPLIED TO EVERY DUAL-WINDOW 4b PASS HERE.")
    P("           A margin inside the book's OWN rebalance-offset spread is not a pass.")
    P("-" * 100)
    sub10 = cd[(cd.cost == COST0) & (cd.pass4b_NONE)]
    dual = []
    for (pn, fm, nn, gg_, cc_), grp in sub10.groupby(["panel", "form", "n", "gross", "cad"]):
        w = set(grp.win)
        if {"FULL", "OOS"} <= w:
            dual.append((pn, fm, nn, gg_, cc_, sorted(w)))
    P(f"  {len(dual)} book(s) pass 4b at 10 bps in BOTH the FULL and the OOS window:")
    clause_rows = []
    for (pn, fm, nn, gg_, cc_, ws) in dual:
        px = panels[pn]; start = px.index[260]
        P(f"    {pn} {fm} n={nn} gross={gg_} cad={cc_}   4b PASS in {ws}")
        wts = book_weights(px, fm, nn, gg_)
        off = {}
        for d in [0, 1, 2, 3, 4]:
            md, clp = offset_mask(px.index, d, cc_)
            gr_, to_, _ = run(px, wts, md)
            rr = net(gr_, to_, COST0)
            for wn, x in win_slices(rr, start).items():
                s = stats(x); s["MaxDD"] = dd_detail(x)[0]
                off[(d, wn)] = s
            off[("clip", d)] = clp
        for wn in ["FULL", "IS", "OOS"]:
            ss = spy_s[(pn, wn, "NONE")]
            p0, L0, M0 = legs4b(off[(0, wn)], ss)
            out = []
            for leg, (stat, scale) in LEGUNIT.items():
                vals = [off[(d, wn)][stat] * scale for d in [0, 1, 2, 3, 4]]
                S = max(vals) - min(vals)
                res = abs(M0[leg]) > S
                out.append(f"{leg} M={M0[leg]:+.3f} S={S:.3f} {'RES' if res else 'unres'}")
                clause_rows.append(dict(panel=pn, form=fm, n=nn, gross=gg_, cad=cc_, win=wn,
                                        leg=leg, side="PASS" if L0[leg] else "FAIL",
                                        margin=M0[leg], spread5=S, resolved=res,
                                        verdict4b=p0))
            v5 = [legs4b(off[(d, wn)], ss)[0] for d in [0, 1, 2, 3, 4]]
            P(f"      {wn:5s} 4b {'PASS' if p0 else 'FAIL'} at d=0, {sum(v5)} of 5 offsets;  "
              + " | ".join(out))
    if clause_rows:
        clv = pd.DataFrame(clause_rows)
        clv.to_csv(OUT / f"{SLUG}.clause.csv", index=False)
        lv = clv[(clv.leg.isin(["DD", "CAGR"])) & (clv.side == "PASS")]
        P(f"  LEVEL legs (DD + CAGR) that PASS at d=0: {len(lv)};"
          f" resolved against their own 5-offset spread: {int(lv.resolved.sum())}"
          f" ({lv.resolved.mean():.3f})")
    P("")

    pd.DataFrame(gate_rows).to_csv(OUT / f"{SLUG}.gates.csv", index=False)
    (OUT / f"{SLUG}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"\nwrote {SLUG}.{{grid,cells,bars,walkforward,gates}} + .console.txt")


if __name__ == "__main__":
    main()
