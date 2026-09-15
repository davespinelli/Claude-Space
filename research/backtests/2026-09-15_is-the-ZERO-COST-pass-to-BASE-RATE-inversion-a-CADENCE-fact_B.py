#!/usr/bin/env python3
"""
IDEA 926 -- does-the-ZERO-COST-pass-to-BASE-RATE-inversion-hold-on-MONTHLY-4b-passes  (lane B)
==============================================================================================

THE QUEUE'S QUESTION (verbatim intent)
--------------------------------------
  Idea 680 measured Spearman +0.6387 between 4b pass and null base rate at 0 bps on WEEKLY
  books, and the whole effect dies at 10 bps because weekly turnover is 8-30x/yr.  Monthly
  books turn over a third as fast, so the cost rung should bite less and the inversion should
  survive further.  Re-run 680's 30 cells at freq='M' and report the rho at each rung.
  Max 2 params (cadence, cost rung).

WHY IT MATTERS FOR CAPITAL
--------------------------
  680's operational conclusion was that PROTOCOL rule 2's 10 bps already does the whole job a
  base-rate clause would do: at 0 bps a coin flip clears 4b often enough that a 4b PASS ranks
  books by how easy their family is, and at 10 bps no coin flip clears it at all.  That
  conclusion was read on WEEKLY books only.  If the collapse is bought by weekly turnover
  rather than by the bar, then every SLOWER book in the record -- and a monthly book is the
  cheapest, most obviously deployable thing this research program can produce -- is certified
  by a rung that does not bite it, and the record's monthly 4b passes are exactly the rows a
  base-rate clause would still be needed for.  This run decides which.

THE MECHANISM UNDER TEST, STATED SO IT CAN FAIL
-----------------------------------------------
  H_TURNOVER  the 0->10 bps collapse of the null 4b base rate is a TURNOVER fact.  Its
              prediction: the cost rung at which the base rate dies scales with 1/turnover, so
              a monthly book (turnover ~1/3 of weekly) keeps a live base rate at 10 bps and the
              zero-cost inversion (rho > 0) survives to a rung where the weekly one is dead.
  H_BAR       the collapse is a property of the 4b BAR against SPY (its DD cap and CAGR floor),
              not of turnover.  Its prediction: base rates and rho move with cost only weakly
              once the book is slow, and the cadence ladder shows no 1/turnover scaling.
  The two are separated by the CADENCE x COST grid below, on realised turnover measured per
  cell rather than assumed.
  Section (E2) adds a POST-HOC reading of the same grid along its common axis -- the ANNUAL
  COST DRAG (cost x realised turnover) a cell actually pays.  It is labelled post-hoc in the
  console because it was written after the grid was read; it selects nothing and moves no
  verdict, and every number it reports is a re-slice of the 480 cells already published.

DESIGN
------
  TUNED (2, and only 2 -- both reported in full at every grid point, nothing selected)
    1. CADENCE    W (680's own, run as an exact REPRODUCTION gate) / 2W / M (the question) / Q.
                  The ladder is the turnover axis: it makes H_TURNOVER falsifiable rather than
                  a two-point story.  2W is a local mask (every other W-end); G0 asserts the
                  local mask reproduces engine.rebalance_mask exactly on W, M and Q.
    2. COST RUNG  0 / 5 / 10 / 25 bps.  0 is fixed BY THE QUESTION (the queue asks for the
                  zero-cost base rate), 10 by PROTOCOL rule 2, 5 and 25 bracket it so the
                  collapse is read as a curve rather than a two-point line.
  NOT TUNED -- copied from idea 680 without change, so the W column is a reproduction
    PANELS        U56 (BINDING -- the candidate's own panel), B136, SMALL439 (labelled
                  replications; no headline verdict is taken from them).
    BOOKS         the record's modal REAL 4b-pass keys: TOP5 / TOP10 / TOP20 / EWELIG / BAND03.
    CLAIM SETS    CORE = gross 0.75 (the record's modal convention), EXT = gross 1.00.
                  3 panels x 2 claim sets x 5 books = 30 cells per cadence, 120 in total.
    NULLS         gross-matched coin flips, identical construction to 680: on every rebalance
                  row the null holds the SAME NUMBER of names at the SAME per-name weight as
                  the book, drawn uniformly from that family's pool.  Only WHICH names changes,
                  so gross, cash drag and de-grossing path are identical row by row (G5).
    DRAWS         500, and the 250-draw prefix is printed as a convergence check (G9).  500 is
                  680's own middle rung and is what makes G3's exact reproduction possible:
                  seeds are per-draw, so this run's W column is the first 500 seeds of 680's
                  1000-draw streams and must match its committed .nulls.csv BIT FOR BIT.
    FIXED         gate = above 200d MA and vol20 < 0.60; warm-up 260 rows; IS <= 2016-12-31 /
                  OOS >= 2017-01-01 (PROTOCOL rule 8); seed base 680 (deliberately 680's, so
                  the reproduction gate is exact).

  STATISTIC, NAMED WITH ITS n (idea 564's standing request).  The headline rho is SPEARMAN on
  n = 30 cells per (cadence, cost) between the book's 4b PASS flag (0/1) and its null's 4b base
  rate; with a binary first argument this is a rank point-biserial.  PEARSON is printed beside
  it, and so is the more interpretable statistic the rho is standing in for: mean null base
  rate among 4b PASSERS vs among FAILERS.  A rho over a grid point with 0 or 30 passers is
  undefined and is printed as nan, never as 0.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G0  local cadence mask == engine.rebalance_mask on W, M, Q                     bar 0 rows
  G1  ctx.run == engine.backtest @10 bps, on every engine-supported cadence      bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                         bar 0.0
  G3  EXACT REPRODUCTION of idea 680: this run's W cadence, 500 draws, costs {0,10,25},
      re-derived against the committed
      2026-09-15_does-any-4b-pass-in-the-record-survive-a-ZERO-COST-BASE-RATE-clause_B.nulls.csv
      on all 30 cells                                                            bar 0.0
  G3b the 2026-09-04 KEEP-4b incumbent re-derived on U56 weekly: 12.66% / 1.0921 / -18.31%
                                                                                 bar 5e-3
  G4  panel triples (SPY and RULES v2) printed for every panel and cadence, both windows
  G5  GROSS MATCH: every null family's mean realised gross within 0.01 of its book's
  G6  determinism: a re-drawn seed reproduces its return stream exactly           bar 0.0
  G7  SMALL439: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first
  G8  TURNOVER MONOTONE: realised turnover falls with slower cadence in every one of the 30
      cells (the queue's premise "monthly turns over a third as fast" is MEASURED here, not
      assumed -- the measured ratio is printed whether or not it is a third)
  G9  NESTING: the 250-draw base rates are exact prefixes of the same 500-draw streams

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  universe.json / universe_broad.json / the SMALL screen are CURRENT-CONSTITUENT lists, so
  every CAGR and drawdown LEVEL below is optimistic.  Direction, as in 680: a coin flip drawn
  from a survivor panel is a BETTER book than one drawn in real time, so every null base rate
  is an UPPER bound and every book's percentile inside its null a LOWER bound -- the bias works
  against the incumbents and for the queue's suspicion.  The cadence contrast, the base-rate
  collapse and rho are all SAME-TAPE comparisons and are unaffected; the 4b LEVELS are against
  SPY, which is not survivorship-inflated, so they are not protected by the same-tape argument.
"""
import os, sys, time, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score        # noqa: E402
from engine import backtest, rebalance_mask                                    # noqa: E402

BAND0 = 0.03
VOLCAP = 0.60
WARM = 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
SEED0 = 680                          # 680's own seed base -- required for G3
CADENCES = ["W", "2W", "M", "Q"]     # TUNED axis 1
COSTS = [0.0, 5.0, 10.0, 25.0]       # TUNED axis 2
HEAD_COST = 0.0                      # the queue's object
DRAW_GRID = [250, 500]
DRAWS = max(DRAW_GRID)
CLAIM_SETS = {"CORE": 0.75, "EXT": 1.00}
BINDING_PANEL = "U56"
BINDING_CADENCE = "M"
BASE_RATE_BAR = 0.05
KEEP4B_INCUMBENT = dict(CAGR=0.1266, Sharpe=1.0921, MaxDD=-0.1831)
REPRO_FILE = (OUT / "2026-09-15_does-any-4b-pass-in-the-record-survive-a-"
                    "ZERO-COST-BASE-RATE-clause_B.nulls.csv")

SMOKE = bool(int(os.environ.get("IDEA926_SMOKE", "0")))
if SMOKE:
    DRAW_GRID = [4, 8]
    DRAWS = max(DRAW_GRID)

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


def cad_mask(idx, cad):
    """True on the last trading day of each period.  W/M/Q delegate to the engine (G0);
    2W keeps every second W-end, counted from the first, so it is a deterministic
    half-frequency of W and not a new convention."""
    if cad in ("W", "M", "Q"):
        return rebalance_mask(idx, cad)
    if cad == "2W":
        w = rebalance_mask(idx, "W")
        hits = np.flatnonzero(w.values)
        keep = hits[::2]
        out = pd.Series(False, index=idx)
        out.iloc[keep] = True
        return out
    raise ValueError(cad)


# ==========================================================================================
# fast runner -- identical to idea 680's Ctx, with the mask made cadence-aware
# ==========================================================================================
class Ctx:
    def __init__(self, px, cad):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = cad_mask(self.idx, cad).values
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
        self.dec = np.maximum(self.reb - 1, 0)

    def shift(self, W):
        return W.reindex(self.idx).fillna(0.0).shift(1).fillna(0.0).values

    def run(self, wt):
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

    def gross(self, wt, i0):
        reb = self.reb[self.reb >= i0]
        return float(wt[reb].sum(axis=1).mean())


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mets(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    vol = r.std() * np.sqrt(252)
    dd = float((eq / np.maximum.accumulate(eq) - 1).min())
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=float(r.mean() * 252 / vol) if vol > 0 else np.nan, MaxDD=dd,
                H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs4b(m, oos_s, ms, spy_oos):
    return dict(L1_H1=m["H1"] > ms["H1"], L2_H2=m["H2"] > ms["H2"], L3_OOS=oos_s > spy_oos,
                L4_DD=abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
                L5_CAGR=m["CAGR"] >= 0.70 * ms["CAGR"])


def pass4b(m, oos_s, ms, spy_oos):
    return all(legs4b(m, oos_s, ms, spy_oos).values())


def pass4a(m, mb):
    return bool(m["H1"] > mb["H1"] and m["H2"] > mb["H2"] and m["MaxDD"] >= mb["MaxDD"])


def failstr(m, oos_s, ms, spy_oos):
    f = [k for k, v in legs4b(m, oos_s, ms, spy_oos).items() if not v]
    return "+".join(f) if f else "-"


def spearman(x, y):
    """Spearman rho with average ranks, and its n.  Returns nan when either side is constant
    (a grid point with 0 or 30 passers has no rho, and printing 0 there would be a lie)."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if len(x) < 3 or np.all(x == x[0]) or np.all(y == y[0]):
        return np.nan
    rx = pd.Series(x).rank().values
    ry = pd.Series(y).rank().values
    return float(np.corrcoef(rx, ry)[0, 1])


def pearson(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    if len(x) < 3 or np.all(x == x[0]) or np.all(y == y[0]):
        return np.nan
    return float(np.corrcoef(x, y)[0, 1])


# ==========================================================================================
# panels, books, nulls  (construction copied from idea 680 unchanged)
# ==========================================================================================
def load_panels():
    if SMOKE:
        return {"U56": load_universe()}, 0
    panels = {"U56": load_universe(), "B136": load_universe(broad=True)}
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in sm.columns if c == "SPY" or c not in bad]
    panels["SMALL439"] = sm[keep]
    return panels, len(sm.columns) - len(keep)


def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def build_books(px, g):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    cand = elig & sc.notna()
    rank = sc.where(elig).rank(axis=1, ascending=False)
    bk = {}
    for k in (5, 10, 20):
        bk[f"TOP{k}"] = (rank <= k).astype(float) * (g / k)
    n_el = elig.sum(axis=1).replace(0, np.nan)
    bk["EWELIG"] = elig.astype(float).div(n_el, axis=0).fillna(0.0) * g
    bk["BAND03"] = band_book(px, BAND0, g)
    return bk, cand


def null_streams(ctx, px, cand, draws, seed0=SEED0):
    """Identical to idea 680's: count and per-name weight copied from the book row by row,
    names drawn uniformly from the family's pool.  Seeds are per-draw, so the 250-draw grid is
    an exact prefix of the 500-draw one (G9) and this run's W column is an exact prefix of
    680's 1000-draw streams (G3)."""
    T, N = ctx.T, ctx.N
    cv = cand.values
    priced = px.notna().values
    reb, dec = ctx.reb, ctx.dec
    POOL = {"ROT": cv[dec], "EW": priced[dec], "BD": priced[dec]}

    def topmask(E, take, rng):
        R = rng.random(E.shape)
        R[~E] = -1.0
        order = np.argsort(-R, axis=1)
        pos = np.argsort(order, axis=1)
        return (pos < take[:, None]) & E

    def gen(kind, wt_book, k=None):
        wrow = wt_book[reb]
        cnt = (wrow > 0).sum(axis=1)
        tot = wrow.sum(axis=1)
        perw = np.where(cnt > 0, tot / np.maximum(cnt, 1), 0.0)
        E = POOL[kind]
        take = np.minimum(E.sum(axis=1), cnt)
        for d in range(draws):
            rng = np.random.default_rng(seed0 + 1_000_000 * {"ROT": 0, "EW": 1, "BD": 2}[kind]
                                        + 10_000 * (k or 0) + d)
            W = np.zeros((T, N))
            W[reb] = topmask(E, take, rng) * perw[:, None]
            yield d, W
    return gen


def panel_context(px, cad):
    ctx = Ctx(px, cad)
    idx = px.index
    i0 = WARM
    oos_mask = np.asarray(idx >= pd.Timestamp(OOS_START))[i0:]
    is_mask = np.asarray(idx <= pd.Timestamp(IS_END))[i0:]
    spy = px["SPY"].pct_change().fillna(0.0).values[i0:]
    out = dict(ctx=ctx, i0=i0, oos=oos_mask, is_=is_mask, spy=mets(spy),
               spy_oos=mets(spy[oos_mask]), spy_is=mets(spy[is_mask]))
    v2 = rules_v2_weights(px, BAND0, 0.75)
    gr, tn = ctx.run(ctx.shift(v2))
    out["v2"] = {}
    for c in COSTS:
        r = (gr - tn * c / 1e4)[i0:]
        out["v2"][c] = dict(full=mets(r), oos=mets(r[oos_mask]), is_=mets(r[is_mask]))
    return out


def score_stream(gr, tn, pc, c):
    i0, oos, is_ = pc["i0"], pc["oos"], pc["is_"]
    r = (gr - tn * c / 1e4)[i0:]
    return mets(r), mets(r[oos]), mets(r[is_])


def pass4b_is(mi, msi):
    return bool(mi["H1"] > msi["H1"] and mi["H2"] > msi["H2"] and
                abs(mi["MaxDD"]) <= 0.60 * abs(msi["MaxDD"]) and
                mi["CAGR"] >= 0.70 * msi["CAGR"])


# ==========================================================================================
def gates_pre(panels, n_dropped):
    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- run before any new number is read")
    P("=" * 100)
    ok = {}
    px = panels[BINDING_PANEL]

    bad = 0
    for cad in ("W", "M", "Q"):
        bad += int((cad_mask(px.index, cad).values !=
                    rebalance_mask(px.index, cad).values).sum())
    ok["G0"] = bad == 0
    P(f"  G0 local cadence mask == engine.rebalance_mask on W/M/Q : {bad} differing rows  "
      f"{'PASS' if ok['G0'] else 'FAIL'}")
    n2w = int(cad_mask(px.index, "2W").sum())
    P(f"     (2W is local by necessity -- the engine has no 2W; it keeps every second of the "
      f"{int(cad_mask(px.index, 'W').sum())} W-ends -> {n2w} rebalances)")

    w = band_book(px, BAND0, 0.75)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, 0.75).values).max())
    ok["G2"] = g2 == 0.0
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights             : {g2:.3e}  "
      f"{'PASS' if ok['G2'] else 'FAIL'}")

    g1w = 0.0
    for cad in ("W", "M", "Q"):
        ctx = Ctx(px, cad)
        gr, turn = ctx.run(ctx.shift(w))
        fast = pd.Series(gr - turn * 10.0 / 1e4, index=px.index)
        slow = backtest(px, w, cost_bps=10.0, freq=cad)["returns"]
        j = px.index[WARM]
        g1w = max(g1w, float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max()))
    ok["G1"] = g1w < 1e-12
    P(f"  G1 ctx.run == engine.backtest @10 bps, worst of W/M/Q   : {g1w:.3e}  "
      f"{'PASS' if ok['G1'] else 'FAIL'}")

    ctxw = Ctx(px, "W")
    bks, cand = build_books(px, 0.75)
    grc, tnc = ctxw.run(ctxw.shift(bks["TOP20"]))
    m = mets((grc - tnc * 10.0 / 1e4)[WARM:])
    d3 = max(abs(m[k] - v) for k, v in KEEP4B_INCUMBENT.items())
    ok["G3b"] = d3 < 5e-3
    P(f"  G3b 2026-09-04 KEEP-4b incumbent (U56 TOP20 EW, W, 10 bps):")
    P(f"      got {m['CAGR']:.2%} / {m['Sharpe']:.4f} / {m['MaxDD']:.2%}   published "
      f"{KEEP4B_INCUMBENT['CAGR']:.2%} / {KEEP4B_INCUMBENT['Sharpe']:.4f} / "
      f"{KEEP4B_INCUMBENT['MaxDD']:.2%}   max|d| {d3:.3e}  "
      f"{'PASS' if ok['G3b'] else 'FAIL'}")

    wt20 = ctxw.shift(bks["TOP20"])
    g6a, _ = ctxw.run(next(null_streams(ctxw, px, cand, 1)("ROT", wt20, 20))[1])
    g6b, _ = ctxw.run(next(null_streams(ctxw, px, cand, 1)("ROT", wt20, 20))[1])
    g6 = float(np.abs(g6a - g6b).max())
    ok["G6"] = g6 == 0.0
    P(f"  G6 determinism (seed {SEED0} re-drawn)                    : {g6:.3e}  "
      f"{'PASS' if ok['G6'] else 'FAIL'}")
    if "SMALL439" in panels:
        P(f"  G7 SMALL439 screen: {n_dropped} tickers with max_1d_move >= 1.0 dropped  "
          f"({panels['SMALL439'].shape[1] - 1} names + SPY)  PASS")
        ok["G7"] = True
    P("  G3 (exact reproduction of idea 680's W column) is evaluated after the nulls are run.")
    return ok


# ==========================================================================================
def main():
    t_start = time.time()
    P("IDEA 926  is-the-ZERO-COST-pass-to-BASE-RATE-inversion-a-CADENCE-fact  (lane B)")
    P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC   seed base {SEED0}   "
      f"draws {DRAW_GRID}   cadences {CADENCES}   costs {COSTS} bps   "
      f"claim sets {list(CLAIM_SETS)}")
    P("the two tuned axes are CADENCE and COST RUNG; every grid point is reported, none chosen")
    P()
    panels, n_dropped = load_panels()
    gk = gates_pre(panels, n_dropped)
    P()

    P("=" * 100)
    P("(B) PANEL TRIPLES (G4) -- SPY and the live book, per cadence, full sample and rule-8 OOS")
    P("=" * 100)
    PC = {}
    for cad in CADENCES:
        for name, px in panels.items():
            pc = panel_context(px, cad)
            PC[(cad, name)] = pc
        P(f"  cadence {cad}")
        for name, px in panels.items():
            pc = PC[(cad, name)]
            s, so, v = pc["spy"], pc["spy_oos"], pc["v2"][10.0]
            P(f"    {name:9s} n={px.shape[1]:4d}  SPY full {s['CAGR']:7.2%} / "
              f"{s['Sharpe']:.4f} / {s['MaxDD']:7.2%} (halves {s['H1']:.3f}/{s['H2']:.3f})  "
              f"OOS {so['CAGR']:7.2%} / {so['Sharpe']:.4f} / {so['MaxDD']:7.2%}")
            P(f"    {'':9s}        RULES v2 @10bps full {v['full']['CAGR']:7.2%} / "
              f"{v['full']['Sharpe']:.4f} / {v['full']['MaxDD']:7.2%}  OOS "
              f"{v['oos']['CAGR']:7.2%} / {v['oos']['Sharpe']:.4f} / {v['oos']['MaxDD']:7.2%}")
        P()

    # ----------------------------------------------------------------------------------
    P("=" * 100)
    P("(C) THE BOOKS -- 30 cells per cadence, every cadence x cost point reported")
    P("=" * 100)
    BOOKROWS, CAND, WTS = [], {}, {}
    for cad in CADENCES:
        for pn, px in panels.items():
            pc = PC[(cad, pn)]
            for cs, g in CLAIM_SETS.items():
                bks, cand = build_books(px, g)
                CAND[(pn, cs)] = cand
                for bn, W in bks.items():
                    wt = pc["ctx"].shift(W)
                    WTS[(cad, pn, cs, bn)] = wt
                    gr, tn = pc["ctx"].run(wt)
                    gross = pc["ctx"].gross(wt, pc["i0"])
                    turn_yr = float(tn[pc["i0"]:].sum() / ((len(tn) - pc["i0"]) / 252.0))
                    for c in COSTS:
                        m, mo, mi = score_stream(gr, tn, pc, c)
                        mb = pc["v2"][c]["full"]
                        BOOKROWS.append(dict(
                            cadence=cad, panel=pn, claim_set=cs, book=bn, gross_nom=g, cost=c,
                            mean_gross=gross, turn_yr=turn_yr,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=m["H1"], H2=m["H2"], OOS_CAGR=mo["CAGR"],
                            OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                            IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                            IS_H1=mi["H1"], IS_H2=mi["H2"],
                            pass4b=pass4b(m, mo["Sharpe"], pc["spy"], pc["spy_oos"]["Sharpe"]),
                            pass4a=pass4a(m, mb),
                            fail4b=failstr(m, mo["Sharpe"], pc["spy"],
                                           pc["spy_oos"]["Sharpe"])))
    books = pd.DataFrame(BOOKROWS)
    dump(books, "books")
    for c in COSTS:
        sub = books[books.cost == c]
        line = "   ".join(f"{cad}: 4b {int(sub[sub.cadence == cad].pass4b.sum()):2d}/30 "
                          f"4a {int(sub[sub.cadence == cad].pass4a.sum()):2d}/30"
                          for cad in CADENCES)
        P(f"  @{c:5.1f} bps   {line}")
    P()
    P("  realised TURNOVER (units/yr, from row 260) -- the queue's premise, MEASURED (G8):")
    P(f"     {'panel/set/book':26s} " + " ".join(f"{cad:>8s}" for cad in CADENCES) +
      "    M/W ratio")
    g8_bad = 0
    t0books = books[books.cost == 0.0]
    for (pn, cs, bn), gdf in t0books.groupby(["panel", "claim_set", "book"], sort=False):
        vals = [float(gdf[gdf.cadence == cad].turn_yr.iloc[0]) for cad in CADENCES]
        g8_bad += int(any(vals[i + 1] > vals[i] for i in range(len(vals) - 1)))
        ratio = vals[CADENCES.index("M")] / vals[CADENCES.index("W")]
        P(f"     {pn + '/' + cs + '/' + bn:26s} " + " ".join(f"{v:8.2f}" for v in vals) +
          f"    {ratio:6.3f}")
    gk["G8"] = g8_bad == 0
    P(f"  G8 turnover monotone in cadence on all 30 cells: {g8_bad} violations  "
      f"{'PASS' if gk['G8'] else 'FAIL'}")
    mw = (t0books[t0books.cadence == "M"].set_index(["panel", "claim_set", "book"]).turn_yr /
          t0books[t0books.cadence == "W"].set_index(["panel", "claim_set", "book"]).turn_yr)
    P(f"     M/W turnover ratio across the 30 cells: median {mw.median():.3f}  "
      f"min {mw.min():.3f}  max {mw.max():.3f}   (the queue assumed 'a third')")
    P()

    # ----------------------------------------------------------------------------------
    P("=" * 100)
    P("(D) THE NULLS -- gross-matched coin flips, per cadence and cost rung")
    P("=" * 100)
    FAM = {"TOP5": ("ROT", 5), "TOP10": ("ROT", 10), "TOP20": ("ROT", 20),
           "EWELIG": ("EW", None), "BAND03": ("BD", None)}
    NULLROWS, DRAWROWS = [], []
    for cad in CADENCES:
        for pn, px in panels.items():
            pc = PC[(cad, pn)]
            for cs, g in CLAIM_SETS.items():
                gen = null_streams(pc["ctx"], px, CAND[(pn, cs)], DRAWS)
                for bn, (kind, k) in FAM.items():
                    t0 = time.time()
                    pv = {c: np.zeros(DRAWS, bool) for c in COSTS}
                    iv = {c: np.zeros(DRAWS, bool) for c in COSTS}
                    sv = {c: np.zeros(DRAWS) for c in COSTS}
                    cv = {c: np.zeros(DRAWS) for c in COSTS}
                    dv = {c: np.zeros(DRAWS) for c in COSTS}
                    ov = {c: np.zeros(DRAWS) for c in COSTS}
                    gsum = 0.0
                    for d, W in gen(kind, WTS[(cad, pn, cs, bn)], k):
                        gr, tn = pc["ctx"].run(W)
                        gsum += pc["ctx"].gross(W, pc["i0"])
                        for c in COSTS:
                            m, mo, mi = score_stream(gr, tn, pc, c)
                            pv[c][d] = pass4b(m, mo["Sharpe"], pc["spy"],
                                              pc["spy_oos"]["Sharpe"])
                            iv[c][d] = pass4b_is(mi, pc["spy_is"])
                            sv[c][d], cv[c][d], dv[c][d] = m["Sharpe"], m["CAGR"], m["MaxDD"]
                            ov[c][d] = mo["Sharpe"]
                    mg_null = gsum / DRAWS
                    brow = books[(books.cadence == cad) & (books.panel == pn) &
                                 (books.claim_set == cs) & (books.book == bn)]
                    mg_book = float(brow.mean_gross.iloc[0])
                    gmatch = abs(mg_null - mg_book)
                    for c in COSTS:
                        b = brow[brow.cost == c].iloc[0]
                        for nd in DRAW_GRID:
                            base = float(pv[c][:nd].mean())
                            NULLROWS.append(dict(
                                cadence=cad, panel=pn, claim_set=cs, book=bn, null=kind,
                                gross_nom=g, cost=c, draws=nd, null_base_rate_4b=base,
                                is_base_rate_4b=float(iv[c][:nd].mean()),
                                book_pass4b=bool(b.pass4b),
                                outside_null=bool(b.pass4b and base <= BASE_RATE_BAR),
                                pct_Sharpe=float((sv[c][:nd] < b.Sharpe).mean()),
                                pct_CAGR=float((cv[c][:nd] < b.CAGR).mean()),
                                pct_MaxDD=float((np.abs(dv[c][:nd]) > abs(b.MaxDD)).mean()),
                                pct_OOS_Sharpe=float((ov[c][:nd] < b.OOS_Sharpe).mean()),
                                p_emp_Sharpe=float((1 + (sv[c][:nd] >= b.Sharpe).sum()) /
                                                   (1 + nd)),
                                null_mean_Sharpe=float(sv[c][:nd].mean()),
                                null_p95_Sharpe=float(np.quantile(sv[c][:nd], 0.95)),
                                book_Sharpe=float(b.Sharpe), book_CAGR=float(b.CAGR),
                                book_MaxDD=float(b.MaxDD), book_turn=float(b.turn_yr),
                                mean_gross_null=mg_null, mean_gross_book=mg_book,
                                gross_match=gmatch))
                        if c == HEAD_COST:
                            for d in range(DRAWS):
                                DRAWROWS.append(dict(cadence=cad, panel=pn, claim_set=cs,
                                                     book=bn, draw=d, pass4b=bool(pv[c][d]),
                                                     Sharpe=sv[c][d], CAGR=cv[c][d],
                                                     MaxDD=dv[c][d], OOS_Sharpe=ov[c][d]))
                    P(f"  {cad:2s} {pn:9s} {cs:4s} {bn:7s} null={kind:3s} "
                      f"gross {mg_book:.3f}/{mg_null:.3f} (|d| {gmatch:.4f})  base rate " +
                      "  ".join(f"@{int(c):2d}bps {float(pv[c].mean()):6.1%}" for c in COSTS) +
                      f"  [{time.time() - t0:.0f}s]")
        P()
    nulls = pd.DataFrame(NULLROWS)
    draws_df = pd.DataFrame(DRAWROWS)
    dump(nulls, "nulls")
    dump(draws_df, "draws")

    gk["G5"] = float(nulls.gross_match.max()) < 0.01
    P(f"  G5 gross match, worst over all {len(CADENCES)}x30 families: "
      f"{float(nulls.gross_match.max()):.4f}  {'PASS' if gk['G5'] else 'FAIL'}")
    nest_ok = True
    for (cad, pn, cs, bn), gdf in draws_df.groupby(["cadence", "panel", "claim_set", "book"]):
        v = gdf.sort_values("draw").pass4b.values
        for nd in DRAW_GRID:
            got = float(nulls[(nulls.cadence == cad) & (nulls.panel == pn) &
                              (nulls.claim_set == cs) & (nulls.book == bn) &
                              (nulls.cost == HEAD_COST) &
                              (nulls.draws == nd)].null_base_rate_4b.iloc[0])
            nest_ok &= abs(float(v[:nd].mean()) - got) == 0.0
    gk["G9"] = nest_ok
    P(f"  G9 nesting: the 250-draw base rates are prefixes of the same {DRAWS}-draw streams  "
      f"{'PASS' if nest_ok else 'FAIL'}")

    # G3 -- exact reproduction of idea 680's W column
    if REPRO_FILE.exists() and not SMOKE:
        ref = pd.read_csv(REPRO_FILE)
        ref = ref[(ref.draws == 500) & (ref.cost.isin([0.0, 10.0, 25.0]))]
        mine = nulls[(nulls.cadence == "W") & (nulls.draws == 500) &
                     (nulls.cost.isin([0.0, 10.0, 25.0]))]
        j = mine.merge(ref[["panel", "claim_set", "book", "cost", "null_base_rate_4b",
                            "book_Sharpe"]],
                       on=["panel", "claim_set", "book", "cost"], suffixes=("", "_ref"))
        d_base = float(np.abs(j.null_base_rate_4b - j.null_base_rate_4b_ref).max())
        d_sh = float(np.abs(j.book_Sharpe - j.book_Sharpe_ref).max())
        gk["G3"] = (len(j) == 90) and d_base == 0.0 and d_sh == 0.0
        P(f"  G3 EXACT reproduction of idea 680 on its W column ({len(j)} of 90 cells matched):"
          f" base rate max|d| {d_base:.3e}, book Sharpe max|d| {d_sh:.3e}  "
          f"{'PASS' if gk['G3'] else 'FAIL'}")
    else:
        P("  G3 SKIPPED (reference .nulls.csv absent or SMOKE)")
    P()

    # ----------------------------------------------------------------------------------
    P("=" * 100)
    P("(E) THE ANSWER -- rho(4b pass, null base rate) at every cadence x cost point, n=30")
    P("=" * 100)
    P("  statistic: SPEARMAN (rank point-biserial, binary first argument), n = 30 cells;")
    P("  PEARSON printed beside it; nan where the pass flag is constant (no rho exists).")
    P()
    P(f"     {'cadence':8s} {'cost':>6s} {'4b passes':>10s} {'rho_S':>8s} {'rho_P':>8s} "
      f"{'mean base|PASS':>15s} {'mean base|fail':>15s} {'mean base':>10s} {'max base':>9s} "
      f"{'cells>0.05':>11s} {'outside':>8s}")
    RHO = []
    for cad in CADENCES:
        for c in COSTS:
            sub = nulls[(nulls.cadence == cad) & (nulls.cost == c) & (nulls.draws == DRAWS)]
            y = sub.null_base_rate_4b.values
            x = sub.book_pass4b.values.astype(float)
            rs, rp = spearman(x, y), pearson(x, y)
            mp = float(y[x == 1].mean()) if (x == 1).any() else np.nan
            mf = float(y[x == 0].mean()) if (x == 0).any() else np.nan
            row = dict(cadence=cad, cost=c, n=len(sub), n_pass4b=int(x.sum()),
                       rho_spearman=rs, rho_pearson=rp, mean_base_pass=mp,
                       mean_base_fail=mf, mean_base=float(y.mean()), max_base=float(y.max()),
                       cells_above_bar=int((y > BASE_RATE_BAR).sum()),
                       outside_null=int(sub.outside_null.sum()),
                       mean_turn=float(sub.book_turn.mean()))
            RHO.append(row)
            f = lambda v: "     nan" if not np.isfinite(v) else f"{v:8.4f}"
            P(f"     {cad:8s} {c:6.1f} {int(x.sum()):10d} {f(rs)} {f(rp)} "
              f"{(f'{mp:15.1%}' if np.isfinite(mp) else '            nan')} "
              f"{(f'{mf:15.1%}' if np.isfinite(mf) else '            nan')} "
              f"{float(y.mean()):10.1%} {float(y.max()):9.1%} "
              f"{int((y > BASE_RATE_BAR).sum()):11d} {int(sub.outside_null.sum()):8d}")
        P()
    rho = pd.DataFrame(RHO)
    dump(rho, "rho")

    P("  H_TURNOVER's prediction is that the base rate dies at a cost rung scaling with "
      "1/turnover.")
    P("  mean null base rate by cadence x cost (the collapse curve), and the mean realised "
      "book turnover:")
    P(f"     {'cadence':8s} {'turn/yr':>8s} " +
      " ".join(f"{'@' + str(int(c)) + 'bps':>10s}" for c in COSTS))
    for cad in CADENCES:
        r = rho[rho.cadence == cad]
        P(f"     {cad:8s} {float(r.mean_turn.iloc[0]):8.2f} " +
          " ".join(f"{float(r[r.cost == c].mean_base.iloc[0]):10.2%}" for c in COSTS))
    P()
    P("  per-cell detail at the queue's own rung (0 bps) and PROTOCOL's (10 bps), "
      f"{DRAWS} draws, cadence {BINDING_CADENCE} (binding) then W (reproduction):")
    for cad in (BINDING_CADENCE, "W"):
        P(f"    cadence {cad}")
        P(f"       {'panel':9s} {'set':4s} {'book':7s} {'4b@0':5s} {'base@0':>8s} "
          f"{'pct(Sh)@0':>10s} {'4b@10':5s} {'base@10':>8s} {'pct(Sh)@10':>11s}  outside@0?")
        for (pn, cs, bn), gdf in nulls[(nulls.cadence == cad) &
                                       (nulls.draws == DRAWS)].groupby(
                ["panel", "claim_set", "book"], sort=False):
            r0 = gdf[gdf.cost == 0.0].iloc[0]
            r10 = gdf[gdf.cost == 10.0].iloc[0]
            P(f"       {pn:9s} {cs:4s} {bn:7s} "
              f"{'PASS' if r0.book_pass4b else 'fail':5s} {r0.null_base_rate_4b:8.1%} "
              f"{r0.pct_Sharpe:10.1%} "
              f"{'PASS' if r10.book_pass4b else 'fail':5s} {r10.null_base_rate_4b:8.1%} "
              f"{r10.pct_Sharpe:11.1%}  {'YES' if r0.outside_null else 'no'}")
        P()
      # ------------------------------------------------------------------------------
    # (E2) POST-HOC, and labelled as such.  This block was written AFTER the grid above was
    # read; it is NOT a pre-registered hypothesis and nothing below selects, tunes or moves a
    # verdict.  It exists because the cadence x cost table has an obvious common axis -- the
    # ANNUAL COST DRAG a cell actually pays, cost x realised turnover -- and the queue's
    # question is exactly whether the rung or the drag is what kills the null.  Descriptive
    # across the 480 (cadence, panel, set, book, cost) cells, on the same days and names.
    P("  (E2) POST-HOC (not pre-registered): is the base rate a function of the ANNUAL COST")
    P("       DRAG (cost x realised turnover) rather than of the cost RUNG?")
    nz = nulls[nulls.draws == DRAWS].copy()
    nz["drag"] = nz.cost * nz.book_turn / 1e4
    live_cells = nz[nz.null_base_rate_4b > 0]
    P(f"       Spearman over all {len(nz)} cells   vs cost {spearman(nz.cost, nz.null_base_rate_4b):+.4f}"
      f"   vs turnover {spearman(nz.book_turn, nz.null_base_rate_4b):+.4f}"
      f"   vs cost x turnover {spearman(nz.drag, nz.null_base_rate_4b):+.4f}")
    P(f"       Spearman over the {len(live_cells)} cells with a NONZERO base rate (where the "
      f"statistic can move):")
    P(f"                                     vs cost {spearman(live_cells.cost, live_cells.null_base_rate_4b):+.4f}"
      f"   vs turnover {spearman(live_cells.book_turn, live_cells.null_base_rate_4b):+.4f}"
      f"   vs cost x turnover {spearman(live_cells.drag, live_cells.null_base_rate_4b):+.4f}")
    EDGES = [-1e-9, 1e-9, 0.0025, 0.005, 0.01, 0.02, 1.0]
    LABS = ["0", "<25bp", "25-50bp", "50-100bp", "100-200bp", ">200bp"]
    nz["bucket"] = pd.cut(nz.drag, EDGES, labels=LABS)
    P(f"       mean null 4b base rate by annual drag bucket (bp/yr of NAV):")
    P(f"          {'drag':10s} {'cells':>6s} {'mean base':>10s} {'max base':>9s} "
      f"{'cells>5%':>9s}")
    for lab, gdf in nz.groupby("bucket", observed=True):
        P(f"          {lab:10s} {len(gdf):6d} {gdf.null_base_rate_4b.mean():10.2%} "
          f"{gdf.null_base_rate_4b.max():9.1%} "
          f"{int((gdf.null_base_rate_4b > BASE_RATE_BAR).sum()):9d}")
    P("       matched-drag contrast -- different (cadence, rung) pairs that pay the SAME drag:")
    for cad, c in [("W", 5.0), ("M", 10.0), ("2W", 10.0), ("W", 10.0), ("M", 25.0),
                   ("2W", 25.0)]:
        s = nz[(nz.cadence == cad) & (nz.cost == c)]
        P(f"          {cad:2s} @{int(c):2d} bps   drag {s.drag.mean() * 1e4:6.1f} bp/yr   "
          f"mean base {s.null_base_rate_4b.mean():6.2%}   cells>5% "
          f"{int((s.null_base_rate_4b > BASE_RATE_BAR).sum()):2d}")
    dump(nz[["cadence", "panel", "claim_set", "book", "cost", "book_turn", "drag",
             "null_base_rate_4b", "book_pass4b", "outside_null"]], "drag")
    P()
    P("  draw-axis convergence (0 bps, binding panel U56, cadence M):")
    for cs in CLAIM_SETS:
        for bn in FAM:
            vals = [float(nulls[(nulls.cadence == BINDING_CADENCE) &
                                (nulls.panel == BINDING_PANEL) & (nulls.claim_set == cs) &
                                (nulls.book == bn) & (nulls.cost == HEAD_COST) &
                                (nulls.draws == nd)].null_base_rate_4b.iloc[0])
                    for nd in DRAW_GRID]
            P(f"     {cs:4s} {bn:7s}  " +
              "  ".join(f"n={nd}: {v:6.1%}" for nd, v in zip(DRAW_GRID, vals)))
    P()

    # ----------------------------------------------------------------------------------
    P("=" * 100)
    P("(F) RULE 8 WALK-FORWARD -- chosen on 2009-2016 only, 2017-2026 read once")
    P("=" * 100)
    P("  Three IS-only choosers over the 10 books on each panel, at every cadence x cost:")
    P("    CH_SHARPE  best IS Sharpe (no clause)   CH_4bIS  best IS Sharpe among IS-4b-level")
    P("    CH_BASE    best IS Sharpe among books whose IS-window null base rate <= 0.05")
    P("  Both KEEP paths are evaluated on the untouched OOS window: 4b vs SPY, 4a vs RULES v2.")
    WF = []
    for cad in CADENCES:
        for pn, px in panels.items():
            pc = PC[(cad, pn)]
            for c in COSTS:
                cand = books[(books.cadence == cad) & (books.panel == pn) &
                             (books.cost == c)].copy()
                br = nulls[(nulls.cadence == cad) & (nulls.panel == pn) & (nulls.cost == c) &
                           (nulls.draws == DRAWS)]
                cand = cand.merge(br[["claim_set", "book", "null_base_rate_4b",
                                      "is_base_rate_4b"]],
                                  on=["claim_set", "book"], how="left")
                cand["IS_ok"] = (cand.IS_H1 > pc["spy_is"]["H1"]) & \
                                (cand.IS_H2 > pc["spy_is"]["H2"]) & \
                                (cand.IS_CAGR >= 0.70 * pc["spy_is"]["CAGR"]) & \
                                (cand.IS_MaxDD.abs() <= 0.60 * abs(pc["spy_is"]["MaxDD"]))
                picks = {"CH_SHARPE": cand.sort_values("IS_Sharpe", ascending=False).iloc[0]}
                s4 = cand[cand.IS_ok].sort_values("IS_Sharpe", ascending=False)
                picks["CH_4bIS"] = s4.iloc[0] if len(s4) else None
                sb = cand[cand.is_base_rate_4b <= BASE_RATE_BAR].sort_values(
                    "IS_Sharpe", ascending=False)
                picks["CH_BASE"] = sb.iloc[0] if len(sb) else None
                for ch, r in picks.items():
                    if r is None:
                        WF.append(dict(cadence=cad, panel=pn, cost=c, chooser=ch, pick="EMPTY"))
                        continue
                    v2o, so = pc["v2"][c]["oos"], pc["spy_oos"]
                    WF.append(dict(
                        cadence=cad, panel=pn, cost=c, chooser=ch,
                        pick=f"{r.claim_set}/{r.book}", IS_Sharpe=r.IS_Sharpe,
                        base_rate=r.null_base_rate_4b, is_base_rate=r.is_base_rate_4b,
                        OOS_CAGR=r.OOS_CAGR, OOS_Sharpe=r.OOS_Sharpe, OOS_MaxDD=r.OOS_MaxDD,
                        OOS_4b=bool(r.OOS_Sharpe > so["Sharpe"] and
                                    abs(r.OOS_MaxDD) <= 0.60 * abs(so["MaxDD"]) and
                                    r.OOS_CAGR >= 0.70 * so["CAGR"]),
                        OOS_4a=bool(r.OOS_Sharpe > v2o["Sharpe"] and
                                    r.OOS_MaxDD >= v2o["MaxDD"]),
                        SPY_OOS_CAGR=so["CAGR"], SPY_OOS_Sharpe=so["Sharpe"],
                        SPY_OOS_MaxDD=so["MaxDD"], V2_OOS_CAGR=v2o["CAGR"],
                        V2_OOS_Sharpe=v2o["Sharpe"], V2_OOS_MaxDD=v2o["MaxDD"]))
    wf = pd.DataFrame(WF)
    dump(wf, "walkforward")
    live = wf[wf["pick"] != "EMPTY"]
    for cad in CADENCES:
        sub = live[live.cadence == cad]
        P(f"  cadence {cad}: 4b {int(sub.OOS_4b.sum()):2d} of {len(sub):2d} live picks, "
          f"4a {int(sub.OOS_4a.sum()):2d} of {len(sub):2d}   "
          f"(EMPTY {int((wf[wf.cadence == cad]['pick'] == 'EMPTY').sum())})   "
          f"mean OOS Sharpe {sub.OOS_Sharpe.mean():.3f}, mean OOS CAGR "
          f"{sub.OOS_CAGR.mean():.2%}")
    P()
    P("  by chooser (the base-rate clause is CH_BASE -- what it costs is the point):")
    for ch in ("CH_SHARPE", "CH_4bIS", "CH_BASE"):
        s = live[live.chooser == ch]
        P(f"     {ch:10s} picks {len(s):3d}  OOS 4b {int(s.OOS_4b.sum()):2d}  "
          f"4a {int(s.OOS_4a.sum()):2d}  mean OOS Sharpe {s.OOS_Sharpe.mean():.3f}  "
          f"mean OOS CAGR {s.OOS_CAGR.mean():.2%}")
    P()
    P(f"  the binding cadence ({BINDING_CADENCE}) in full, all panels and rungs:")
    for pn in panels:
        for _, r in wf[(wf.cadence == BINDING_CADENCE) & (wf.panel == pn)].iterrows():
            if r["pick"] == "EMPTY":
                P(f"     {pn:9s} {r.cost:5.1f} bps {r.chooser:10s}  IS set EMPTY -- no pick")
                continue
            P(f"     {pn:9s} {r.cost:5.1f} bps {r.chooser:10s} pick {r['pick']:12s} "
              f"(IS Sh {r.IS_Sharpe:5.2f}, IS base {r.is_base_rate:5.1%})  OOS "
              f"{r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:5.3f} / {r.OOS_MaxDD:7.2%}  "
              f"4b {'PASS' if r.OOS_4b else 'fail'} 4a {'PASS' if r.OOS_4a else 'fail'}  "
              f"[SPY {r.SPY_OOS_CAGR:6.2%}/{r.SPY_OOS_Sharpe:5.3f}/{r.SPY_OOS_MaxDD:7.2%} | "
              f"v2 {r.V2_OOS_CAGR:6.2%}/{r.V2_OOS_Sharpe:5.3f}/{r.V2_OOS_MaxDD:7.2%}]")
    P()
    best = live.sort_values("OOS_Sharpe", ascending=False).head(5)
    P("  best 5 OOS picks in the whole grid (reported, NOT selected -- each is one chooser's"
      " own IS-only pick):")
    for _, r in best.iterrows():
        P(f"     {r.cadence:2s} {r.panel:9s} {r.cost:5.1f} bps {r.chooser:10s} {r['pick']:12s}"
          f"  OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:5.3f} / {r.OOS_MaxDD:7.2%}  "
          f"4b {'PASS' if r.OOS_4b else 'fail'} 4a {'PASS' if r.OOS_4a else 'fail'}")
    P()

    P("=" * 100)
    P("(G) GATES")
    P("=" * 100)
    for k in sorted(gk):
        P(f"  {k}: {'PASS' if gk[k] else 'FAIL'}")
    P(f"  {sum(bool(v) for v in gk.values())} of {len(gk)} pass")
    P()
    P(f"total runtime {time.time() - t_start:.0f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    print(f"wrote {STEM}.console.txt")


if __name__ == "__main__":
    main()
