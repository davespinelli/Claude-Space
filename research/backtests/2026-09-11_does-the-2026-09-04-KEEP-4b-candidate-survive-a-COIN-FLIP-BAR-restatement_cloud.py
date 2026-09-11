#!/usr/bin/env python3
"""
IDEA 502 -- does-the-2026-09-04-KEEP-4b-candidate-survive-a-COIN-FLIP-BAR-restatement
=====================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 486 found 4b alone passes on 747 of 3,000 random B136 CAND-20 draw books (24.9%), i.e.
  the 4b bar is cleared by a quarter of random 20-name lists on that panel.  Restate the
  standing 2026-09-04 KEEP-4b candidate (U56 top-20 equal weight, no vol scaler) against its
  OWN panel's random-draw 4b base rate: draw 1,000 U56 20-name sub-panels, compute the 4b pass
  share, and report the candidate's percentile inside it at 0/10/25 bps.  If the live candidate
  sits inside its own null the KEEP needs a base-rate clause.  Max 2 params (draws, cost rung).

WHY IT MATTERS FOR CAPITAL
--------------------------
  A KEEP is a claim that a RULE cleared a bar.  If a coin flip clears the same bar at a
  respectable rate, the bar certifies the FAMILY (20 gated large-cap names at 0.75 gross), not
  the rule, and the live recommendation should say so out loud before any capital follows it.

THE TWO NULLS (both structural comparands, neither a tuned parameter)
---------------------------------------------------------------------
  RANDFIX  a FIXED random list of 20 tradable names, held through the SAME gate (above the
           200d MA, vol20 < 0.60) at the SAME fixed 0.75/20 per name, de-grossing to cash for
           every gated-out name.  This is the candidate with its ranking replaced by a coin
           flip, and it is the null idea 486's "random 20-name list" language describes.
  RANDROT  20 names drawn uniformly at random FROM THE ELIGIBLE SET at every weekly rebalance,
           same fixed 0.75/20 per name.  RANDFIX differs from the candidate in two ways at once
           (which names, and how often the list turns over); RANDROT matches the candidate's
           rotation and turnover and differs ONLY in whether the 20 names are chosen by the
           composite score or by a coin flip.  It is the better-powered null, and it is
           reported beside RANDFIX throughout rather than instead of it.

DESIGN
------
  CANDIDATE  the standing 2026-09-04 KEEP-4b book, pinned in code by G3: composite score with
             NO vol scaler, rank over ALL columns (SPY included, as `baseline` does), top 20
             eligible at a FIXED 0.75/20 per name, de-gross to cash below 20 eligible, vol20
             cap 0.60, weekly cadence.
  TUNED (2)  DRAWS (250 / 500 / 1,000 -- nested, so the 250 grid is the first 250 seeds of the
             1,000) and COST RUNG (0 / 10 / 25 bps).  Every point of the 3 x 3 is reported.
  FIXED      n = 20, gross 0.75, the gate, cadence W, warm-up 260 rows, IS/OOS split
             2016-12-31 / 2017-01-01 (PROTOCOL rule 8), seed base 502.  None chosen by outcome.
  PANELS     U56 is the BINDING panel -- it is the candidate's own panel and the one the queue
             names.  B136 and SMALL439 are run identically as a LABELLED REPLICATION of idea
             486's 24.9% claim (which was made on B136); no verdict in this run is taken from
             them, and they are not a third tuned axis.

  PERCENTILE convention: the candidate's percentile is the share of null books it BEATS
             (Sharpe/CAGR: null < candidate; MaxDD: |null| > |candidate|).  The one-sided
             empirical p is the complementary share, 1 - percentile + ties.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  ctx_backtest == engine.backtest @10 bps on a dense book                     bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                          bar 0.0
  G3  the standing 2026-09-04 KEEP-4b incumbent re-derived on the FULL U56 panel:
      top-20 equal weight, no vol scaler, published 12.66% / 1.0921 / -18.31%     bar 5e-3
  G4  every null book holds at most 20 names and weights them at exactly 0.75/20, so its gross
      is 0.75 x (names held / 20) -- the candidate's own convention, not a re-grossed one
  G5  the cost rungs are applied to ONE gross-return stream per book (r_c = r_gross - turnover
      x c/1e4), so the three rungs differ by cost and by nothing else                bar 1e-15
  G6  the draws are reproducible: re-running seed 502+0 reproduces its return stream exactly
  G7  SMALL439: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first
  G8  RANDROT built on the rebalance rows == the same book written densely (a full weights
      frame forward-filled between rebalances and shifted), return and turnover  bar 1e-15

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  B136 is today's constituents and SMALL439 is the current sub-$2B screen only (see
  data/SMALL_PANEL_README.md); names acquired, delisted or grown out of the screen are absent,
  so every LEVEL on those panels is biased upward.  The bias matters here in a specific and
  reportable way: a random 20-name list drawn from a survivor panel is a BETTER book than a
  random list drawn in real time would have been, so the null's 4b pass share is an UPPER
  bound on the true coin-flip base rate and the candidate's percentile inside it is a LOWER
  bound.  That direction favours the queue's suspicion, not the incumbent, and is stated here
  rather than buried.  U56 carries the same bias in milder form.
"""
import sys, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score        # noqa: E402
from engine import backtest, rebalance_mask                                    # noqa: E402

COSTS = [0.0, 10.0, 25.0]         # TUNED axis 2
DRAW_GRID = [250, 500, 1000]      # TUNED axis 1 (nested)
DRAWS = max(DRAW_GRID)
FREQ = "W"
BAND0, GROSS0 = 0.03, 0.75
NCAND = 20
VOLCAP = 0.60
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED0 = 502
BINDING_PANEL, BINDING_COST = "U56", 10.0

KEEP4B_INCUMBENT = dict(CAGR=0.1266, Sharpe=1.0921, MaxDD=-0.1831)

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ------------------------------------------------------------------------------------------
class Ctx:
    """Everything in the return calculation that does NOT depend on the weights, hoisted out of
    the draw loop.  ctx.run(W) returns (gross return stream, turnover stream); the cost rungs
    are applied afterwards to that one stream (G5)."""

    def __init__(self, px, freq=FREQ):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = rebalance_mask(self.idx, freq).values
        m = np.concatenate([[False], m[:-1]]).copy()
        m[0] = True
        self.T, self.N = self.rets.shape
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.N)), C[:-1]])
        self.reb = np.flatnonzero(m)
        seg = np.searchsorted(self.reb, np.arange(self.T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.ratio = self.Cp / self.Cp[self.s0]
        self.ratiop = self.Cp / self.Cp[self.s0p]

    def exposure(self, wt, turn, i0):
        """(mean realised gross, annualised turnover) of a book from row i0 on.  Gross is read
        on the rebalance rows -- the only rows the book's weights are ever set on."""
        reb = self.reb[self.reb >= i0]
        yrs = (self.T - i0) / 252.0
        return float(wt[reb].sum(axis=1).mean()), float(turn[i0:].sum() / yrs)

    def run(self, weights):
        wt = weights.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values \
            if isinstance(weights, pd.DataFrame) else weights
        W0 = wt[self.s0]
        h = W0 * self.ratio
        V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
        held = h / V[:, None]
        W0p = wt[self.s0p]
        hp = W0p * self.ratiop
        Vp = hp.sum(axis=1) + (1.0 - W0p.sum(axis=1))
        heldp = hp / Vp[:, None]
        heldp[self.reb[0]] = 0.0
        turn = np.zeros(self.T)
        turn[self.reb] = np.abs(wt[self.reb] - heldp[self.reb]).sum(axis=1)
        return (held * self.rets).sum(axis=1), turn

    def shift(self, W):
        """weights DataFrame -> the shifted ndarray ctx.run expects."""
        return W.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values


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


def band_book(px, band, gross):
    return ew_gross(px, gross).where(band_state(px, band) & px.notna(), 0.0)


def ranked_w(sc, elig, n, gross):
    r = sc.where(elig).rank(axis=1, ascending=False)
    return (r <= n).astype(float) * (gross / n)


def keeppaths(m, oos_s, mb, ms, spy_oos):
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


# ------------------------------------------------------------------------------------------
def load_panels():
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    panels["SMALL439"] = sm[keep]
    return panels, len(sm.columns) - len(keep)


def null_books(px, elig, ctx, seed, dense=False):
    """The two coin-flip books for one draw seed, as SHIFTED weight ndarrays (what ctx.run
    consumes).  `ctx.run` reads the shifted array only on the rebalance rows `ctx.reb`, which
    correspond to the weights decided at the previous close (the rebalance-mask day), so the
    books are built directly on those rows.  dense=True builds the same book the slow way -- a
    full weights DataFrame, forward-filled between rebalances and shifted -- and G8 asserts the
    two give an identical return stream."""
    rng = np.random.default_rng(seed)
    T, N = len(px.index), len(px.columns)
    ev = elig.values
    tri = np.array([i for i, c in enumerate(px.columns) if c != "SPY"])
    reb = ctx.reb
    dec = np.maximum(reb - 1, 0)             # the close at which each rebalance is decided

    # RANDFIX -- one fixed random list of 20 names, held through the same gate
    pick = rng.permutation(tri)[:NCAND]
    fixed = np.zeros((T, N))
    fixed[:, pick] = ev[:, pick] * (GROSS0 / NCAND)
    fix = np.vstack([np.zeros((1, N)), fixed[:-1]])

    # RANDROT -- 20 names drawn uniformly from the ELIGIBLE set at every weekly rebalance
    E = ev[dec].copy()
    E[:, [i for i in range(N) if i not in set(tri.tolist())]] = False   # SPY never held
    R = rng.random(E.shape)
    R[~E] = -1.0
    order = np.argsort(-R, axis=1)
    pos = np.argsort(order, axis=1)
    take = np.minimum(E.sum(axis=1), NCAND)
    sel = (pos < take[:, None]) & E
    rot = np.zeros((T, N))
    rot[reb] = sel * (GROSS0 / NCAND)

    if dense:
        W = np.full((T, N), np.nan)
        W[dec] = sel * (GROSS0 / NCAND)
        W = pd.DataFrame(W, index=px.index, columns=px.columns).ffill().fillna(0.0)
        return {"RANDFIX": fix, "RANDROT": rot, "RANDROT_dense": ctx.shift(W)}
    return {"RANDFIX": fix, "RANDROT": rot}


def gates(panels, n_dropped):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = True
    px = panels["U56"]
    w = band_book(px, BAND0, GROSS0)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, GROSS0).values).max())
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights             : {g2:.3e}  "
      f"{'PASS' if g2 == 0.0 else 'FAIL'}")
    ok &= g2 == 0.0

    ctx = Ctx(px)
    gr, turn = ctx.run(ctx.shift(w))
    fast = pd.Series(gr - turn * 10.0 / 1e4, index=px.index)
    slow = backtest(px, w, cost_bps=10.0, freq=FREQ)["returns"]
    j = px.index[WARM]
    g1 = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
    P(f"  G1 ctx_backtest == engine.backtest @10 bps              : {g1:.3e}  "
      f"{'PASS' if g1 < 1e-12 else 'FAIL'}")
    ok &= g1 < 1e-12

    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    cand = ranked_w(sc, elig, NCAND, GROSS0)
    gr_c, turn_c = ctx.run(ctx.shift(cand))
    m = M(pd.Series(gr_c - turn_c * 10.0 / 1e4, index=px.index).loc[j:])
    d = {k: abs(m[k] - v) for k, v in KEEP4B_INCUMBENT.items()}
    P("  G3 2026-09-04 KEEP-4b incumbent (U56 top-20 EW, no vol scaler) re-derived:")
    P(f"     got {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}   published "
      f"{KEEP4B_INCUMBENT['CAGR']:.2%} / {KEEP4B_INCUMBENT['Sharpe']:.4f} / "
      f"{KEEP4B_INCUMBENT['MaxDD']:.2%}   max|d| {max(d.values()):.3e}  "
      f"{'PASS' if max(d.values()) < 5e-3 else 'FAIL'}")
    ok &= max(d.values()) < 5e-3

    nb = null_books(px, elig, ctx, SEED0)
    g4 = True
    for k, wt in nb.items():
        held = (wt > 0).sum(axis=1)
        wmax = float(np.abs(wt[wt > 0] - GROSS0 / NCAND).max()) if (wt > 0).any() else 0.0
        gross_ok = float(np.abs(wt.sum(axis=1) - GROSS0 / NCAND * held).max())
        g4 &= (held.max() <= NCAND) and wmax < 1e-15 and gross_ok < 1e-12
        P(f"  G4 {k}: max names held {held.max()} (<= {NCAND}), per-name weight deviation "
          f"{wmax:.3e}, gross == 0.75 x held/20 to {gross_ok:.3e}  "
          f"{'PASS' if held.max() <= NCAND and wmax < 1e-15 else 'FAIL'}")
    ok &= g4

    r0 = pd.Series(gr_c - turn_c * 0.0, index=px.index)
    r10 = pd.Series(gr_c - turn_c * 10.0 / 1e4, index=px.index)
    g5 = float(np.abs((r0 - r10) - turn_c * 10.0 / 1e4).max())
    P(f"  G5 cost rungs applied to ONE gross stream               : {g5:.3e}  "
      f"{'PASS' if g5 < 1e-15 else 'FAIL'}")
    ok &= g5 < 1e-15

    nb2 = null_books(px, elig, ctx, SEED0, dense=True)
    g6 = max(float(np.abs(nb[k] - nb2[k]).max()) for k in nb)
    P(f"  G6 draws reproducible (seed {SEED0} re-run)               : {g6:.3e}  "
      f"{'PASS' if g6 == 0.0 else 'FAIL'}")
    ok &= g6 == 0.0

    gs, ts = ctx.run(nb2["RANDROT"])
    gd, td = ctx.run(nb2["RANDROT_dense"])
    g8 = max(float(np.abs(gs - gd).max()), float(np.abs(ts - td).max()))
    P(f"  G8 RANDROT built on rebalance rows == the dense ffilled book: {g8:.3e}  "
      f"{'PASS' if g8 < 1e-15 else 'FAIL'}")
    ok &= g8 < 1e-15

    P(f"  G7 SMALL439 dropped {n_dropped} tickers with max_1d_move >= 1.0 : "
      f"{'PASS' if n_dropped > 0 else 'FAIL'}")
    ok &= n_dropped > 0
    P()
    P(f"  GATES: {'ALL PASS' if ok else 'FAILURE -- results below are not trustworthy'}")
    return ok


# ------------------------------------------------------------------------------------------
def run(panels):
    P()
    P("=" * 100)
    P(f"(B) THE COIN-FLIP NULL -- {DRAWS} draws x 2 nulls x 3 cost rungs x {len(panels)} panels")
    P("=" * 100)
    draw_rows, cand_rows = [], []
    for pn, px in panels.items():
        start = px.index[WARM]
        ctx = Ctx(px)
        sc, above, vol20 = score(px, vol_scale=False)
        elig = above & (vol20 < VOLCAP)
        spy = px["SPY"].pct_change().fillna(0).loc[start:]
        ms, spy_oos = M(spy), M0(spy.loc[OOS_START:])
        spy_o = M(spy.loc[OOS_START:])
        gr_b, tu_b = ctx.run(ctx.shift(rules_v2_weights(px, BAND0, GROSS0)))
        wt_c = ctx.shift(ranked_w(sc, elig, NCAND, GROSS0))
        gr_c, tu_c = ctx.run(wt_c)
        i0 = px.index.get_loc(start)
        cg, ct = ctx.exposure(wt_c, tu_c, i0)
        P()
        P(f"  --- {pn}  ({len(px.columns) - 1} tradable names, {start.date()} -> "
          f"{px.index[-1].date()}) ---")
        P(f"      SPY {ms['CAGR']:.2%} / {ms['Sharpe']:.3f} / {ms['MaxDD']:.2%}  "
          f"(H1 {ms['H1']:.3f} H2 {ms['H2']:.3f}; OOS {spy_o['CAGR']:.2%} / {spy_oos:.3f} / "
          f"{spy_o['MaxDD']:.2%})   4b floors: CAGR >= {0.70 * ms['CAGR']:.2%}, "
          f"|MaxDD| <= {0.60 * abs(ms['MaxDD']):.2%}")
        mb_all, cand_all = {}, {}
        for c in COSTS:
            rb = pd.Series(gr_b - tu_b * c / 1e4, index=px.index).loc[start:]
            rc = pd.Series(gr_c - tu_c * c / 1e4, index=px.index).loc[start:]
            mb_all[c] = M(rb)
            m, mo = M(rc), M(rc.loc[OOS_START:])
            p4a, p4b = keeppaths(m, mo["Sharpe"], mb_all[c], ms, spy_oos)
            cand_all[c] = dict(m=m, mo=mo, is_s=M0(rc.loc[:IS_END]), p4a=p4a, p4b=p4b)
            P(f"      CANDIDATE @{c:>4.1f} bps  {m['CAGR']:7.2%} / {m['Sharpe']:6.3f} / "
              f"{m['MaxDD']:7.2%}  H1 {m['H1']:.3f} H2 {m['H2']:.3f}  OOS {mo['CAGR']:7.2%} / "
              f"{mo['Sharpe']:6.3f} / {mo['MaxDD']:7.2%}  4a {'Y' if p4a else 'n'} "
              f"4b {'Y' if p4b else 'n'}  fail4b {fail4b(m, mo['Sharpe'], ms, spy_oos)}")
            cand_rows.append(dict(panel=pn, cost=c, **{k: m[k] for k in
                                  ("CAGR", "Sharpe", "MaxDD", "H1", "H2")},
                                  IS_Sharpe=cand_all[c]["is_s"], OOS_CAGR=mo["CAGR"],
                                  OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                                  keep4a=p4a, keep4b=p4b,
                                  fail4b=fail4b(m, mo["Sharpe"], ms, spy_oos),
                                  SPY_CAGR=ms["CAGR"], SPY_Sharpe=ms["Sharpe"],
                                  SPY_MaxDD=ms["MaxDD"], SPY_OOS_Sharpe=spy_oos,
                                  v2_Sharpe=mb_all[c]["Sharpe"], v2_MaxDD=mb_all[c]["MaxDD"],
                                  mean_gross=cg, turnover_yr=ct))
        P(f"      CANDIDATE exposure: mean realised gross {cg:.4f}, turnover "
          f"{ct:.2f}x/yr   mean eligible names {elig.sum(axis=1).loc[start:].mean():.1f}")
        for s in range(DRAWS):
            nb = null_books(px, elig, ctx, SEED0 + s)
            for bk, wt in nb.items():
                gr, tu = ctx.run(wt)
                g_mean, t_yr = ctx.exposure(wt, tu, i0)
                for c in COSTS:
                    r = pd.Series(gr - tu * c / 1e4, index=px.index).loc[start:]
                    m, mo = M(r), M(r.loc[OOS_START:])
                    p4a, p4b = keeppaths(m, mo["Sharpe"], mb_all[c], ms, spy_oos)
                    draw_rows.append(dict(panel=pn, book=bk, draw=s, cost=c, CAGR=m["CAGR"],
                                          Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=m["H1"],
                                          H2=m["H2"], IS_Sharpe=M0(r.loc[:IS_END]),
                                          OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"],
                                          OOS_MaxDD=mo["MaxDD"], keep4a=p4a, keep4b=p4b,
                                          mean_gross=g_mean, turnover_yr=t_yr))
            if (s + 1) % 250 == 0:
                P(f"      ... {s + 1}/{DRAWS} draws")
    return pd.DataFrame(draw_rows), pd.DataFrame(cand_rows)


def pct_beat(null_vals, cand, higher_better=True):
    v = np.asarray(null_vals, dtype=float)
    return float(np.mean(v < cand) if higher_better else np.mean(np.abs(v) > abs(cand)))


def summarise(draws, cand):
    P()
    P("=" * 100)
    P("(C) THE COIN-FLIP BAR -- null 4b pass share and the candidate's percentile inside it")
    P("=" * 100)
    rows = []
    for pn in draws.panel.unique():
        P()
        P(f"  --- {pn}{'   [BINDING PANEL]' if pn == BINDING_PANEL else '   [replication only]'}")
        cdx = cand[(cand.panel == pn) & (cand.cost == BINDING_COST)].iloc[0]
        for bk in ["RANDFIX", "RANDROT"]:
            s = draws[(draws.panel == pn) & (draws.book == bk) & (draws.cost == BINDING_COST)]
            P(f"      EXPOSURE  {bk:<8} median gross {s.mean_gross.median():.4f}, turnover "
              f"{s.turnover_yr.median():.2f}x/yr   vs CANDIDATE gross {cdx.mean_gross:.4f}, "
              f"turnover {cdx.turnover_yr:.2f}x/yr")
        P("      book     draws  cost |  4a share   4b share |  cand pctile: Sharpe  CAGR  "
          "MaxDD  OOS_Sharpe | one-sided p (Sharpe)")
        for bk in ["RANDFIX", "RANDROT"]:
            for nd in DRAW_GRID:
                for c in COSTS:
                    s = draws[(draws.panel == pn) & (draws.book == bk) & (draws.cost == c)
                              & (draws.draw < nd)]
                    cd = cand[(cand.panel == pn) & (cand.cost == c)].iloc[0]
                    pr = dict(panel=pn, book=bk, draws=nd, cost=c,
                              null_4a=float(s.keep4a.mean()), null_4b=float(s.keep4b.mean()),
                              null_Sharpe_med=float(s.Sharpe.median()),
                              null_CAGR_med=float(s.CAGR.median()),
                              null_MaxDD_med=float(s.MaxDD.median()),
                              null_OOS_Sharpe_med=float(s.OOS_Sharpe.median()),
                              null_gross_med=float(s.mean_gross.median()),
                              null_turnover_med=float(s.turnover_yr.median()),
                              cand_gross=cd.mean_gross, cand_turnover=cd.turnover_yr,
                              cand_Sharpe=cd.Sharpe, cand_CAGR=cd.CAGR, cand_MaxDD=cd.MaxDD,
                              cand_OOS_Sharpe=cd.OOS_Sharpe, cand_keep4b=bool(cd.keep4b),
                              pct_Sharpe=pct_beat(s.Sharpe, cd.Sharpe),
                              pct_CAGR=pct_beat(s.CAGR, cd.CAGR),
                              pct_MaxDD=pct_beat(s.MaxDD, cd.MaxDD, False),
                              pct_OOS_Sharpe=pct_beat(s.OOS_Sharpe, cd.OOS_Sharpe))
                    pr["p_Sharpe"] = 1.0 - pr["pct_Sharpe"]
                    rows.append(pr)
                    P(f"      {bk:<8}{nd:>5}{c:>6.1f} |  {pr['null_4a']:7.1%}   "
                      f"{pr['null_4b']:7.1%} |  {pr['pct_Sharpe']:12.1%} {pr['pct_CAGR']:6.1%} "
                      f"{pr['pct_MaxDD']:6.1%} {pr['pct_OOS_Sharpe']:10.1%} | "
                      f"{pr['p_Sharpe']:8.3f}")
    return pd.DataFrame(rows)


def walkforward(draws, cand):
    P()
    P("=" * 100)
    P("(D) PROTOCOL RULE 8 -- chooser on 2009-2016 only, scored 2017-2026 untouched")
    P("=" * 100)
    P("      Two pre-registered legs.  LEG 1: pick the single BEST null book by IS Sharpe and")
    P("      score it OOS -- this is what 'a lucky coin flip' is worth after the fact.")
    P("      LEG 2: the candidate's percentile inside the null computed on OOS ROWS ONLY, so no")
    P("      part of the comparison touches the window the candidate's family was chosen on.")
    rows = []
    for pn in draws.panel.unique():
        for bk in ["RANDFIX", "RANDROT"]:
            for c in COSTS:
                s = draws[(draws.panel == pn) & (draws.book == bk) & (draws.cost == c)]
                cd = cand[(cand.panel == pn) & (cand.cost == c)].iloc[0]
                pick = s.loc[s.IS_Sharpe.idxmax()]
                r = dict(panel=pn, book=bk, cost=c, pick_draw=int(pick.draw),
                         pick_IS_Sharpe=pick.IS_Sharpe, pick_OOS_CAGR=pick.OOS_CAGR,
                         pick_OOS_Sharpe=pick.OOS_Sharpe, pick_OOS_MaxDD=pick.OOS_MaxDD,
                         cand_IS_Sharpe=cd.IS_Sharpe, cand_OOS_CAGR=cd.OOS_CAGR,
                         cand_OOS_Sharpe=cd.OOS_Sharpe, cand_OOS_MaxDD=cd.OOS_MaxDD,
                         med_OOS_Sharpe=float(s.OOS_Sharpe.median()),
                         pct_OOS_Sharpe=pct_beat(s.OOS_Sharpe, cd.OOS_Sharpe),
                         pct_OOS_CAGR=pct_beat(s.OOS_CAGR, cd.OOS_CAGR),
                         pct_OOS_MaxDD=pct_beat(s.OOS_MaxDD, cd.OOS_MaxDD, False),
                         cand_beats_pick=bool(cd.OOS_Sharpe > pick.OOS_Sharpe))
                rows.append(r)
                if c == BINDING_COST:
                    P(f"      {pn:<9}{bk:<8} IS-best draw #{r['pick_draw']:<4} "
                      f"(IS {r['pick_IS_Sharpe']:.3f} vs cand {r['cand_IS_Sharpe']:.3f})  ->  "
                      f"OOS {r['pick_OOS_CAGR']:7.2%} / {r['pick_OOS_Sharpe']:6.3f} / "
                      f"{r['pick_OOS_MaxDD']:7.2%}   cand OOS {r['cand_OOS_CAGR']:7.2%} / "
                      f"{r['cand_OOS_Sharpe']:6.3f} / {r['cand_OOS_MaxDD']:7.2%}   cand OOS "
                      f"pctile {r['pct_OOS_Sharpe']:.1%}")
    return pd.DataFrame(rows)


def verdict(pctiles, wf):
    P()
    P("=" * 100)
    P("(E) THE ANSWER")
    P("=" * 100)
    b = pctiles[(pctiles.panel == BINDING_PANEL) & (pctiles.cost == BINDING_COST)
                & (pctiles.draws == DRAWS)]
    for _, r in b.iterrows():
        P(f"  {BINDING_PANEL} @{BINDING_COST:.0f} bps, {DRAWS} draws, null = {r.book}:  "
          f"null 4b pass share {r.null_4b:.1%}   candidate 4b {'PASS' if r.cand_keep4b else 'FAIL'}"
          f"   candidate percentile Sharpe {r.pct_Sharpe:.1%} / CAGR {r.pct_CAGR:.1%} / "
          f"MaxDD {r.pct_MaxDD:.1%} / OOS Sharpe {r.pct_OOS_Sharpe:.1%}")
    P()
    P("  Idea 486's claim, re-measured on ITS panel (B136, 10 bps, 1000 draws):")
    for _, r in pctiles[(pctiles.panel == "B136") & (pctiles.cost == BINDING_COST)
                        & (pctiles.draws == DRAWS)].iterrows():
        P(f"    null {r.book}: 4b pass share {r.null_4b:.1%} "
          f"(486 published 24.9% on 3,000 draws)   candidate percentile {r.pct_Sharpe:.1%}")
    P()
    P("  Draw-count stability of the binding pass share (tuned axis 1):")
    for bk in ["RANDFIX", "RANDROT"]:
        s = pctiles[(pctiles.panel == BINDING_PANEL) & (pctiles.cost == BINDING_COST)
                    & (pctiles.book == bk)]
        P(f"    {bk:<8}" + "   ".join(f"{int(r.draws)} draws {r.null_4b:.1%} "
                                      f"(pctile {r.pct_Sharpe:.1%})" for _, r in s.iterrows()))
    P()
    P("  Cost stability of the binding pass share (tuned axis 2, 1000 draws):")
    for bk in ["RANDFIX", "RANDROT"]:
        s = pctiles[(pctiles.panel == BINDING_PANEL) & (pctiles.draws == DRAWS)
                    & (pctiles.book == bk)]
        P(f"    {bk:<8}" + "   ".join(f"{r.cost:.0f} bps {r.null_4b:.1%} "
                                      f"(pctile {r.pct_Sharpe:.1%}, cand 4b "
                                      f"{'Y' if r.cand_keep4b else 'n'})"
                                      for _, r in s.iterrows()))


def record_crosscheck():
    """Reconcile idea 486's '747/3000 = 24.9%' with the record's own committed draws.  486's
    books are CAND-20 books built on random SUB-PANELS -- they still rank -- which is NOT the
    'random 20-name list' this run's nulls implement.  The nearest committed artefact carrying
    a per-draw 4b flag for that construction is idea 504's B136 grid."""
    P()
    P("=" * 100)
    P("(F) RECORD CROSS-CHECK -- what construction is idea 486's 24.9% actually a rate FOR?")
    P("=" * 100)
    f = OUT / ("2026-09-10_price-the-EW-ALL-control-for-the-top-20-book-on-the-1000-draw-grid"
               "_cloud.draws.csv")
    if not f.exists():
        P(f"  committed artefact {f.name} not found -- cross-check SKIPPED, nothing inferred")
        return None
    d = pd.read_csv(f)
    rows = []
    for pn in sorted(d.panel.unique()):
        for c in sorted(d.cost.unique()):
            s = d[(d.panel == pn) & (d.cost == c)]
            r = dict(source=f.name, panel=pn, cost=c, draws=len(s),
                     CAND20_4b=float(s.CAND20_keep4b.mean()),
                     EWall_4b=float(s.EWall_keep4b.mean()) if "EWall_keep4b" in s else np.nan)
            rows.append(r)
            if c == BINDING_COST:
                P(f"  {pn:<9} @{c:>4.1f} bps, {len(s)} committed draws: CAND-20-on-a-random-"
                  f"sub-panel 4b share {r['CAND20_4b']:.1%}   (this run's random-LIST share on "
                  f"the same panel: see section C)")
    return pd.DataFrame(rows)


def main():
    panels, n_dropped = load_panels()
    ok = gates(panels, n_dropped)
    draws, cand = run(panels)
    pctiles = summarise(draws, cand)
    wf = walkforward(draws, cand)
    xc = record_crosscheck()
    verdict(pctiles, wf)
    P()
    if xc is not None:
        dump(xc, "crosscheck")
    dump(draws, "draws")
    dump(cand, "candidate")
    dump(pctiles, "percentiles")
    dump(wf, "walkforward")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"  wrote {STEM}.console.txt")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
