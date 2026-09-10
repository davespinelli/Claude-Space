#!/usr/bin/env python3
"""
IDEA 668 -- is-the-PICK-FLIP-rate-of-0.50-a-property-of-the-BAND-LADDER-or-of-every-dial
=======================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  idea 664's chooser flipped 42 of 84 picks under misreads that cost nothing
  (ROUND: 12/30 flips at +0.0000 OOS Sharpe), i.e. the band dial's argmax is nearly flat
  and the pick is close to arbitrary.  Re-run the same three misread channels over the
  record's OTHER dials (n, gross, vol cap, cadence) and report flip rate against dial
  curvature.  Max 2 params (dial, channel level).

WHAT IS TUNED AND WHAT IS NOT (PROTOCOL 4, "no more than 2 tuned parameters")
-----------------------------------------------------------------------------
  TUNED (2)     : DIAL (which ladder the chooser walks) and the channel LEVEL.
  NOT TUNED     : cost 10 bps (PROTOCOL 2), cadence W except when cadence IS the dial,
                  gross 0.75 except when gross IS the dial, band 0.03 except when band IS
                  the dial, n=20 except when n IS the dial, warm-up 260 rows, IS/OOS split
                  2016-12-31 / 2017-01-01 (PROTOCOL 8), tie-break = smallest rung index.
                  Every one of these is the record's own live constant, imported or restated,
                  never chosen by looking at an outcome.

THE DESIGN
----------
  A DIAL is a ladder of candidate books that differ in exactly one parameter.  Five dials:

    BAND    band in {0.00 .. 0.20}      RULES v2 band book, g=0.75, W       (664's dial: CONTROL)
    N       n    in {3 .. 50}           top-n composite-ranked EW book, g=0.75, W
    GROSS   g    in {0.20 .. 1.00}      RULES v2 band book, band=0.03, W
    VOLCAP  cap  in {0.20 .. OFF}       top-20 ranked book with a vol20 eligibility cap
    CADENCE freq in {D, W, M, Q}        RULES v2 band book, band=0.03, g=0.75

  A CHOOSER reads each rung's IN-SAMPLE Sharpe (2009..2016 only, PROTOCOL 8) and takes the
  argmax, ties to the SMALLEST rung index.  Three MISREAD CHANNELS, identical in form to
  idea 664's, each with a level-0 control that is the honest read:

    ROUND(dp)   read the IS Sharpe to dp decimals                 levels 10*,3,2,1,0
    WINDOW(w)   read the SAME book over a different window        levels IS*,IS_H2,TRAIL5Y,
                                                                         TRAIL3Y,FULL(CHEAT)
    BOOK(k)     read rung i's Sharpe off rung clip(i+k)           levels 0*,+1,+2,+3,-1

  664's BOOK channel used band-VALUE offsets; a value offset has no meaning on a ladder of
  cadences, so it is generalised here to a RUNG-INDEX offset, which reduces to 664's channel
  on an evenly-spaced ladder and is the only form that ports to all five dials.  Stated, not
  hidden: this is a deliberate difference from 664 and is why G3 anchors on the level-0 pick
  and not on 664's BOOK levels.

  CURVATURE is measured on each dial's own honest IS ladder:
    spread  = max - min of IS Sharpe across rungs
    margin  = best - second best IS Sharpe            (the decision-relevant quantity)
    curv    = mean |x[i-1] - 2 x[i] + x[i+1]| over interior rungs

  FLIP RATE is then read against all three, over 5 dials x 2 panels = 10 cells.

PANELS
------
  U56  = research/universe.json ETF/mega-cap panel        (baseline.load_universe())
  B136 = research/universe_broad.json 136 large caps      (baseline.load_universe(broad=True))
  SURVIVORSHIP (PROTOCOL 9): B136 is TODAY'S constituents -- names that were delisted or fell
  out of the screen are absent, so every B136 level here is biased upward.  The claim this run
  makes is about FLIP RATES (a within-panel, within-ladder statistic), which survivorship
  biases far less than it biases a level, but no B136 level below is a tradeable estimate.

PRE-REGISTERED GATES (run and printed BEFORE any new number is read)
--------------------------------------------------------------------
  G1  fast_backtest == engine.backtest at 10 bps                       bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights               bar 0.0 (exact)
  G3  the BAND dial at g=0.75 reproduces idea 664's COMMITTED grid row: pick, IS read,
      full Sharpe, OOS Sharpe, SPY OOS Sharpe, live-book OOS Sharpe, on both panels  bar 5e-4
  G4  every dial ladder contains the live constant it varies (0.03 / 0.75 / W / 20)
  G5  all three channels agree at their level-0 point on every (panel, dial)

VERDICT DISCIPLINE
------------------
  Both KEEP paths are evaluated at EVERY grid point and all points are reported.  Nothing is
  promoted on a flip-rate result; the live leg exists so the answer is priced in OOS Sharpe
  and not only in counts.  A documented KILL is the expected outcome.
"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score      # noqa: E402
from engine import backtest, rebalance_mask                                  # noqa: E402

# ---- reported constants (never tuned) ---------------------------------------------------------
COST = 10.0                     # PROTOCOL 2
FREQ0 = "W"                     # RULES v2 cadence
BAND0 = 0.03                    # RULES v2 clause 2
GROSS0 = 0.75                   # RULES v2 clause 3
N0 = 20                         # the 2026-09-04 KEEP-4b candidate's book width
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"

BANDS = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12, 0.20]
NS = [3, 5, 10, 15, 20, 30, 40, 50]
GROSSES = [0.20, 0.35, 0.50, 0.60, 0.75, 0.85, 0.95, 1.00]
VOLCAPS = [0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.80, 9.99]     # 9.99 == cap OFF
CADENCES = ["D", "W", "M", "Q"]

CHANNELS = {
    "ROUND":  [10, 3, 2, 1, 0],
    "WINDOW": ["IS", "IS_H2", "TRAIL5Y", "TRAIL3Y", "FULL"],
    "BOOK":   [0, 1, 2, 3, -1],
}
CTRL_LEVEL = {"ROUND": "10", "WINDOW": "IS", "BOOK": "0"}
CHEAT = {"FULL"}                # a read window past IS_END is look-ahead: flagged, not hidden

# idea 664's committed level-0 row at g=0.75 (research/backtests/
# 2026-09-10_price-the-RE-DERIVED-METRIC-column-against-its-own-source_C.grid.csv)
IDEA664 = {
    "U56":  dict(pick=0.08, read=1.1222394, Sharpe=1.1465783, OOS=1.1665617,
                 SPY_OOS=0.8757784, BASE_OOS=1.2788365),
    "B136": dict(pick=0.08, read=1.1411857, Sharpe=1.1240385, OOS=1.1094642,
                 SPY_OOS=0.8820243, BASE_OOS=1.1185083),
}

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ================================================================================================
# 1.  ENGINE  (vectorised equivalent of engine.backtest, asserted against it in G1)
# ================================================================================================
def fast_backtest(prices, weights, freq=FREQ0, cost=COST):
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
    gross_r = (held * rets).sum(axis=1)
    return pd.Series(gross_r - turn * cost / 1e4, index=idx)


def M(r):
    eq = (1 + r).cumprod()
    yrs = len(r) / 252
    vol = r.std() * np.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    h = len(r) // 2
    return dict(CAGR=cagr, Sharpe=(r.mean() * 252) / vol if vol else np.nan, MaxDD=dd,
                H1=M0(r.iloc[:h]), H2=M0(r.iloc[h:]))


def M0(r):
    vol = r.std() * np.sqrt(252)
    return (r.mean() * 252) / vol if vol else np.nan


# ================================================================================================
# 2.  THE FIVE DIALS
# ================================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def ranked_book(px, sc, above, vol20, n, gross, max_vol):
    """Top-n composite-ranked equal-weight book (the record's CAND-n family).  Eligibility =
    above the 200d MA and vol20 < max_vol; max_vol 9.99 is the cap OFF.  Weight gross/n."""
    elig = sc.where(above & (vol20 < max_vol))
    rank = elig.rank(axis=1, ascending=False)
    sel = (rank <= n).astype(float)
    k = sel.sum(axis=1).replace(0, np.nan)
    return (sel.mul(gross / k, axis=0)).fillna(0.0)


def build_dials(px):
    """Return {dial: (rungs, {rung: returns_series}, freq_of_rung)} for one panel."""
    start = px.index[WARM]
    sc, above, vol20 = score(px, vol_scale=True)
    D = {}

    b = {r: fast_backtest(px, band_book(px, r, GROSS0), FREQ0, COST).loc[start:] for r in BANDS}
    D["BAND"] = (BANDS, b)

    b = {r: fast_backtest(px, ranked_book(px, sc, above, vol20, r, GROSS0, 9.99),
                          FREQ0, COST).loc[start:] for r in NS}
    D["N"] = (NS, b)

    b = {r: fast_backtest(px, band_book(px, BAND0, r), FREQ0, COST).loc[start:] for r in GROSSES}
    D["GROSS"] = (GROSSES, b)

    b = {r: fast_backtest(px, ranked_book(px, sc, above, vol20, N0, GROSS0, r),
                          FREQ0, COST).loc[start:] for r in VOLCAPS}
    D["VOLCAP"] = (VOLCAPS, b)

    w = band_book(px, BAND0, GROSS0)
    b = {r: fast_backtest(px, w, r, COST).loc[start:] for r in CADENCES}
    D["CADENCE"] = (CADENCES, b)
    return D


# ================================================================================================
# 3.  THE CHOOSER AND ITS MISREADS
# ================================================================================================
def win_slice(r, w, start):
    if w == "IS":
        return r.loc[start:IS_END]
    if w == "IS_H2":
        return r.loc["2013-01-01":IS_END]
    if w == "TRAIL5Y":
        return r.loc["2012-01-01":IS_END]
    if w == "TRAIL3Y":
        return r.loc["2014-01-01":IS_END]
    return r.loc[start:]                      # FULL -- CHEAT


def reads_for(rungs, books, channel, level, start):
    """The chooser's Sharpe for each rung under one misread channel at one level."""
    out = {}
    for i, rg in enumerate(rungs):
        if channel == "WINDOW":
            out[rg] = M0(win_slice(books[rg], level, start))
        elif channel == "ROUND":
            out[rg] = round(M0(win_slice(books[rg], "IS", start)), int(level))
        else:                                  # BOOK: read rung i off rung clip(i+k)
            j = int(np.clip(i + int(level), 0, len(rungs) - 1))
            out[rg] = M0(win_slice(books[rungs[j]], "IS", start))
    return out


def keeppaths(r, base, spy):
    """PROTOCOL 4a and 4b, verbatim, on the full common sample."""
    m, mb, ms = M(r), M(base), M(spy)
    oos_s = M0(r.loc[OOS_START:])
    oos_b = M0(spy.loc[OOS_START:])
    p4a = (m["H1"] > mb["H1"]) and (m["H2"] > mb["H2"]) and (m["MaxDD"] >= mb["MaxDD"])
    p4b = ((m["H1"] > ms["H1"]) and (m["H2"] > ms["H2"]) and (oos_s > oos_b)
           and (abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]))
           and (m["CAGR"] >= 0.70 * ms["CAGR"]))
    return p4a, p4b, m


def curvature(rungs, books, start):
    x = np.array([M0(win_slice(books[r], "IS", start)) for r in rungs], float)
    srt = np.sort(x)[::-1]
    d2 = np.abs(x[:-2] - 2 * x[1:-1] + x[2:]) if len(x) >= 3 else np.array([0.0])
    return dict(n_rungs=len(rungs), is_best=srt[0], spread=srt[0] - srt[-1],
                margin=srt[0] - srt[1], curv=float(d2.mean()), is_sd=float(x.std(ddof=0)))


# ================================================================================================
# 4.  GATES
# ================================================================================================
def gates(panels):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    px = panels["U56"]

    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == baseline.rules_v2_weights      : {g2:.3e}  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    ok &= (g2 == 0.0)

    slow = backtest(px, w, cost_bps=COST, freq=FREQ0)["returns"]
    fast = fast_backtest(px, w, FREQ0, COST)
    j = px.index[WARM]
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
    P(f"  G1 fast_backtest == engine.backtest @10 bps               : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= (g1 < 1e-12)

    P("  G3 BAND dial at g=0.75 vs idea 664's COMMITTED grid row (bar 5e-4).")
    P("     The gate is VINTAGE-PINNED: data/prices.csv gained trading days since 664 ran the")
    P("     same day (664 itself reported this channel at dSharpe 0.0035 / two days), so the")
    P("     gate is tried on today's tape AND on truncations, and the reproducing vintage is")
    P("     named.  Bears on open idea 517 (the three panels never share a last date).")
    for pn, pxp in panels.items():
        e = IDEA664[pn]
        best = None
        for end in (None, "2026-09-09", "2026-09-08", "2026-09-07", "2026-09-04"):
            q = pxp if end is None else pxp.loc[:end]
            if len(q) < WARM + 500:
                continue
            start = q.index[WARM]
            bk = {b: fast_backtest(q, band_book(q, b, GROSS0), FREQ0, COST).loc[start:]
                  for b in BANDS}
            rd = {b: M0(win_slice(bk[b], "IS", start)) for b in BANDS}
            pick = max(sorted(BANDS), key=lambda b: (rd[b], -b))
            r = bk[pick]
            spy = q["SPY"].pct_change().fillna(0).loc[start:]
            base = fast_backtest(q, rules_v2_weights(q, BAND0, GROSS0), FREQ0, COST).loc[start:]
            d = dict(pick=abs(pick - e["pick"]), read=abs(rd[pick] - e["read"]),
                     Sharpe=abs(M0(r) - e["Sharpe"]), OOS=abs(M0(r.loc[OOS_START:]) - e["OOS"]),
                     SPY_OOS=abs(M0(spy.loc[OOS_START:]) - e["SPY_OOS"]),
                     BASE_OOS=abs(M0(base.loc[OOS_START:]) - e["BASE_OOS"]))
            worst = max(d.values())
            tag = "today" if end is None else f"<= {end}"
            P(f"     {pn:<5} {tag:<13} last {q.index[-1].date()}  pick {pick:.2f} "
              f"(664: {e['pick']:.2f})  max|d| {worst:.3e}   "
              + " ".join(f"{k} {v:.1e}" for k, v in d.items()))
            if best is None or worst < best:
                best = worst
        P(f"     {pn:<5} best vintage max|d| {best:.3e}  "
          f"{'PASS' if best < 5e-4 else 'FAIL'}")
        ok &= best < 5e-4

    g4 = (BAND0 in BANDS) and (GROSS0 in GROSSES) and (FREQ0 in CADENCES) and (N0 in NS)
    P(f"  G4 every ladder contains its live constant (0.03/0.75/W/20) : "
      f"{'PASS' if g4 else 'FAIL'}")
    ok &= g4
    P()
    P(f"  GATES A: {'ALL PASS' if ok else 'FAILURE -- results below are not trustworthy'}")
    return ok


# ================================================================================================
# 5.  THE GRID
# ================================================================================================
def run(panels):
    P()
    P("=" * 100)
    P("(B) THE GRID -- 5 dials x 3 channels x 5 levels x 2 panels, every point reported")
    P("=" * 100)
    grid, curv_rows = [], []
    for pn, px in panels.items():
        start = px.index[WARM]
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        base = fast_backtest(px, rules_v2_weights(px, BAND0, GROSS0), FREQ0, COST).loc[start:]
        mb, ms = M(base), M(spy)
        bo, so = M(base.loc[OOS_START:]), M(spy.loc[OOS_START:])
        P(f"  {pn}: RULES v2 live book {mb['CAGR']:.2%} / {mb['Sharpe']:.4f} / {mb['MaxDD']:.2%}"
          f"  (H1 {mb['H1']:.4f} / H2 {mb['H2']:.4f})   OOS {bo['Sharpe']:.4f}")
        P(f"  {pn}: SPY               {ms['CAGR']:.2%} / {ms['Sharpe']:.4f} / {ms['MaxDD']:.2%}"
          f"  (H1 {ms['H1']:.4f} / H2 {ms['H2']:.4f})   OOS {so['Sharpe']:.4f}")
        D = build_dials(px)
        for dial, (rungs, books) in D.items():
            c = curvature(rungs, books, start)
            curv_rows.append(dict(panel=pn, dial=dial, **c))
            for ch, levels in CHANNELS.items():
                for lv in levels:
                    rd = reads_for(rungs, books, ch, lv, start)
                    order = list(range(len(rungs)))
                    best_i = max(order, key=lambda i: (rd[rungs[i]], -i))
                    pick = rungs[best_i]
                    r = books[pick]
                    p4a, p4b, m = keeppaths(r, base, spy)
                    mo = M(r.loc[OOS_START:])
                    grid.append(dict(
                        panel=pn, dial=dial, channel=ch, level=str(lv),
                        cheat=str(lv) in CHEAT, n_rungs=len(rungs),
                        pick=str(pick), pick_i=best_i, read_best=rd[pick],
                        n_ties=sum(1 for x in rungs if rd[x] == rd[pick]),
                        CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                        H1=m["H1"], H2=m["H2"],
                        OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                        SPY_OOS_Sharpe=so["Sharpe"], SPY_OOS_CAGR=so["CAGR"],
                        SPY_OOS_MaxDD=so["MaxDD"],
                        BASE_OOS_Sharpe=bo["Sharpe"], BASE_OOS_CAGR=bo["CAGR"],
                        BASE_OOS_MaxDD=bo["MaxDD"],
                        pass4a=p4a, pass4b=p4b))
    G = pd.DataFrame(grid)
    C = pd.DataFrame(curv_rows)
    P()
    P(f"  live grid points (all reported): {len(G)}")
    P()
    P(G[["panel", "dial", "channel", "level", "cheat", "pick", "read_best", "CAGR", "Sharpe",
         "MaxDD", "H1", "H2", "OOS_CAGR", "OOS_Sharpe", "OOS_MaxDD", "pass4a", "pass4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(G, "grid")

    # G5: the three channels agree at their level-0 point
    G["is_ctl"] = [CTRL_LEVEL.get(c) == l for c, l in zip(G.channel, G.level)]
    ok5 = True
    for pn in panels:
        for dial in G.dial.unique():
            z = G[(G.panel == pn) & (G.dial == dial) & G.is_ctl]
            ok5 &= (len(z) == 3 and z.pick.nunique() == 1)
    P()
    P(f"  G5 all three channels agree at their level-0 point on every (panel, dial) : "
      f"{'PASS' if ok5 else 'FAIL'}")
    return G, C, ok5


# ================================================================================================
# 6.  FLIPS vs CURVATURE  --  THE ANSWER
# ================================================================================================
def flips(G, C):
    P()
    P("=" * 100)
    P("(C) THE ANSWER -- pick-flip rate per dial, and what it costs OOS")
    P("=" * 100)
    ctl = {}
    for _, r in G.iterrows():
        if CTRL_LEVEL.get(r.channel) == r.level:
            ctl[(r.panel, r.dial, r.channel)] = r
    rows = []
    for _, r in G.iterrows():
        c = ctl.get((r.panel, r.dial, r.channel))
        if c is None or CTRL_LEVEL.get(r.channel) == r.level:
            continue                                    # controls are not their own flips
        rows.append(dict(panel=r.panel, dial=r.dial, channel=r.channel, level=r.level,
                         cheat=r.cheat, flip=bool(r.pick != c.pick), pick=r.pick,
                         ctl_pick=c.pick,
                         d_OOS_Sharpe=r.OOS_Sharpe - c.OOS_Sharpe,
                         d_OOS_CAGR=r.OOS_CAGR - c.OOS_CAGR,
                         d_OOS_MaxDD=r.OOS_MaxDD - c.OOS_MaxDD,
                         d_Sharpe=r.Sharpe - c.Sharpe))
    F = pd.DataFrame(rows)
    dump(F, "flips")
    H = F[~F.cheat]                                     # look-ahead levels excluded from headline

    P()
    P("  FLIP RATE BY DIAL (look-ahead FULL window excluded; control levels not counted)")
    t = (H.groupby("dial")
          .agg(n=("flip", "size"), flips=("flip", "sum"),
               rate=("flip", "mean"), med_dOOS=("d_OOS_Sharpe", "median"),
               mean_dOOS=("d_OOS_Sharpe", "mean"), worst_dOOS=("d_OOS_Sharpe", "min"),
               worst_dDD=("d_OOS_MaxDD", "min"))
          .sort_values("rate", ascending=False))
    P(t.to_string(float_format=lambda x: f"{x:.4f}"))
    dump(t.reset_index(), "byDial")

    P()
    P("  FLIP RATE BY CHANNEL (pooled over dials)")
    t2 = (H.groupby("channel")
           .agg(n=("flip", "size"), flips=("flip", "sum"), rate=("flip", "mean"),
                med_dOOS=("d_OOS_Sharpe", "median"), mean_dOOS=("d_OOS_Sharpe", "mean"),
                worst_dOOS=("d_OOS_Sharpe", "min")))
    P(t2.to_string(float_format=lambda x: f"{x:.4f}"))
    dump(t2.reset_index(), "byChannel")

    P()
    P("  FLIP RATE BY (dial, channel)")
    t3 = H.pivot_table(index="dial", columns="channel", values="flip", aggfunc="mean")
    P(t3.to_string(float_format=lambda x: f"{x:.4f}"))

    P()
    P("  DIAL CURVATURE (measured on each dial's honest IS ladder) vs its flip rate")
    K = C.merge(H.groupby(["panel", "dial"]).flip.agg(["size", "sum", "mean"]).reset_index()
                 .rename(columns={"size": "n", "sum": "flips", "mean": "rate"}),
                on=["panel", "dial"])
    P(K[["panel", "dial", "n_rungs", "is_best", "spread", "margin", "curv", "is_sd",
         "n", "flips", "rate"]].to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(K, "curvature")

    P()
    for col in ("margin", "spread", "curv", "is_sd"):
        sp = K[["rate", col]].corr(method="spearman").iloc[0, 1]
        pe = K[["rate", col]].corr(method="pearson").iloc[0, 1]
        P(f"    rho(flip rate, {col:<7}) : Spearman {sp:+.4f}   Pearson {pe:+.4f}   n={len(K)}")
    P("    (statistic and n named beside every rho -- idea 564's standing request)")

    # ---- THE PRICE OF A FLIP: a flip that costs nothing is not a decision -----------------
    P()
    P("  WHAT A FLIP COSTS -- |d OOS Sharpe| among FLIPPED picks only, per (panel, dial)")
    fl = H[H.flip].copy()
    fl["abs_d"] = fl.d_OOS_Sharpe.abs()
    cost = (fl.groupby(["panel", "dial"])
              .agg(n_flip=("abs_d", "size"), mean_abs=("abs_d", "mean"),
                   med_abs=("abs_d", "median"), max_abs=("abs_d", "max"),
                   free=("abs_d", lambda x: float((x < 0.01).mean())),
                   costly=("abs_d", lambda x: float((x > 0.05).mean())))
              .reset_index())
    K2 = K.merge(cost, on=["panel", "dial"], how="left")
    P(K2[["panel", "dial", "spread", "margin", "curv", "rate", "n_flip", "mean_abs",
          "med_abs", "max_abs", "free", "costly"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(K2, "curvature")
    P()
    for col in ("margin", "spread", "curv", "is_sd"):
        for y in ("mean_abs", "max_abs"):
            z = K2[[y, col]].dropna()
            sp = z.corr(method="spearman").iloc[0, 1]
            pe = z.corr(method="pearson").iloc[0, 1]
            P(f"    rho({y:<8}, {col:<7}) : Spearman {sp:+.4f}   Pearson {pe:+.4f}   n={len(z)}")
    P()
    P("  OOS SPREAD of the dial (max-min OOS Sharpe over its rungs) -- what a flip CAN cost:")
    P(K2[["panel", "dial", "spread", "rate", "max_abs"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # ---- restated in idea 664's own denominator convention --------------------------------
    P()
    P("  RESTATED IN IDEA 664's DENOMINATOR (controls counted, look-ahead excluded), so the")
    P("  0.500 headline and these numbers are the same statistic:")
    for dial in sorted(K2.dial.unique()):
        nf = int(H[H.dial == dial].flip.sum())
        n_nc = int((H.dial == dial).sum())
        n_wc = n_nc + 3 * K2[K2.dial == dial].panel.nunique()      # +3 control rows per panel
        P(f"    {dial:<8} 664-convention {nf}/{n_wc} = {nf / n_wc:.4f}     "
          f"controls-excluded {nf}/{n_nc} = {nf / n_nc:.4f}")
    nf, n_nc = int(H.flip.sum()), len(H)
    n_wc = n_nc + 3 * 2 * len(K2.dial.unique())
    P(f"    {'POOLED':<8} 664-convention {nf}/{n_wc} = {nf / n_wc:.4f}     "
      f"controls-excluded {nf}/{n_nc} = {nf / n_nc:.4f}")
    P("    (idea 664 published 42/84 = 0.5000 on the BAND dial alone, 3 grosses, 2 panels)")
    return F, K2


# ================================================================================================
# 7.  RULE 8 WALK-FORWARD AND THE KEEP PATHS
# ================================================================================================
def rule8(G):
    P()
    P("=" * 100)
    P("(D) RULE 8 -- the pick is made on 2009-2016 ONLY, scored on 2017-2026 untouched")
    P("=" * 100)
    W = G.copy()
    W["beat_SPY"] = W.OOS_Sharpe > W.SPY_OOS_Sharpe
    W["beat_BASE"] = W.OOS_Sharpe > W.BASE_OOS_Sharpe
    H = W[~W.cheat]
    P(f"  honest points (look-ahead FULL excluded): {len(H)} of {len(W)}")
    P(f"  beat SPY OOS Sharpe   : {int(H.beat_SPY.sum())}/{len(H)}")
    P(f"  beat LIVE RULES v2 OOS: {int(H.beat_BASE.sum())}/{len(H)}")
    P()
    P("  OOS by (panel, dial): the chooser's pick vs SPY vs the live book")
    t = (H.groupby(["panel", "dial"])
          .agg(OOS_CAGR=("OOS_CAGR", "mean"), OOS_Sharpe=("OOS_Sharpe", "mean"),
               OOS_MaxDD=("OOS_MaxDD", "mean"),
               best_OOS=("OOS_Sharpe", "max"), worst_OOS=("OOS_Sharpe", "min"),
               SPY=("SPY_OOS_Sharpe", "first"), LIVE=("BASE_OOS_Sharpe", "first"),
               beat_SPY=("beat_SPY", "sum"), n=("beat_SPY", "size")))
    P(t.to_string(float_format=lambda x: f"{x:.4f}"))
    dump(t.reset_index(), "walkforward")
    P()
    P(f"  KEEP PATHS over the whole grid: 4a {int(W.pass4a.sum())}/{len(W)}   "
      f"4b {int(W.pass4b.sum())}/{len(W)}   BOTH {int((W.pass4a & W.pass4b).sum())}/{len(W)}")
    P("  4a/4b by (panel, dial):")
    t2 = W.groupby(["panel", "dial"]).agg(n=("pass4a", "size"), p4a=("pass4a", "sum"),
                                          p4b=("pass4b", "sum"))
    P(t2.to_string())
    P()
    P("  IS 4b A PICK PROPERTY OR A FAMILY PROPERTY?  (every 4b passer, by the rung it picked)")
    z = W[W.pass4b]
    if len(z):
        P(z.groupby(["panel", "dial", "pick"]).size().to_string())
        P()
        P("  a dial whose 4b passes cover EVERY rung it ever picks is a FAMILY fact -- the "
          "misread cannot break it; one that passes at some picks and not others is a PICK "
          "fact and is exactly as arbitrary as its flip rate.")
        for (pn, dl), g in W.groupby(["panel", "dial"]):
            if g.pass4b.sum() == 0:
                continue
            picks = g.pick.nunique()
            allp = bool(g.pass4b.all())
            P(f"    {pn:<5} {dl:<8} 4b {int(g.pass4b.sum())}/{len(g)} over {picks} distinct "
              f"picks -- {'FAMILY (every point passes)' if allp else 'PICK-dependent'}")
    dump(W[["panel", "dial", "channel", "level", "cheat", "pick", "pass4a", "pass4b"]],
         "keeppaths")
    return W


def main():
    P("=" * 100)
    P("IDEA 668 -- is the 0.50 PICK-FLIP rate a property of the BAND ladder or of EVERY dial?")
    P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC   cost {COST:.0f} bps   "
      f"IS<= {IS_END}   OOS >= {OOS_START}")
    P("=" * 100)
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    for k, v in panels.items():
        P(f"  {k}: {v.shape[1]} columns  {v.index[0].date()} .. {v.index[-1].date()}  "
          f"({len(v)} rows)")
    P("  SURVIVORSHIP (PROTOCOL 9): B136 is today's constituents only -- levels biased up.")
    P()
    ok = gates(panels)
    G, C, ok5 = run(panels)
    F, K = flips(G, C)
    W = rule8(G)
    P()
    P("=" * 100)
    P("(E) SUMMARY")
    P("=" * 100)
    H = F[~F.cheat]
    band = H[H.dial == "BAND"]
    other = H[H.dial != "BAND"]
    P(f"  BAND dial (664's)   flip rate {band.flip.mean():.4f}  ({int(band.flip.sum())}/"
      f"{len(band)})   median dOOS Sharpe {band.d_OOS_Sharpe.median():+.4f}")
    P(f"  the OTHER 4 dials   flip rate {other.flip.mean():.4f}  ({int(other.flip.sum())}/"
      f"{len(other)})   median dOOS Sharpe {other.d_OOS_Sharpe.median():+.4f}")
    P(f"  pooled              flip rate {H.flip.mean():.4f}  ({int(H.flip.sum())}/{len(H)})")
    P()
    P(f"  GATES: A {'PASS' if ok else 'FAIL'}   G5 {'PASS' if ok5 else 'FAIL'}")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
