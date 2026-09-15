#!/usr/bin/env python3
"""
IDEA 926 -- does-the-ZERO-COST-pass-to-BASE-RATE-inversion-hold-on-the-record-s-MONTHLY-4b-passes
=================================================================================================
                                                                                    (lane B)

THE QUEUE'S QUESTION (verbatim)
-------------------------------
  Idea 680 measured Spearman +0.6387 between 4b pass and null base rate at 0 bps on WEEKLY
  books, and the whole effect dies at 10 bps because weekly turnover is 8-30x/yr.  Monthly
  books turn over a third as fast, so the cost rung should bite less and the inversion should
  survive further.  Re-run 680's 30 cells at freq='M' and report the rho at each rung.
  Max 2 params (cadence, cost rung).

WHY IT MATTERS FOR CAPITAL
--------------------------
  Idea 680's finding is the sharpest indictment in the record of the 4b bar as evidence: at
  ZERO cost, whether a book passes 4b PREDICTS how easy its family is (rho +0.6387), i.e. the
  bar was ranking admission families, not rules.  680 then showed the whole thing evaporates at
  PROTOCOL rule 2's 10 bps, and concluded the protocol's own cost rung already does the job.
  That conclusion is only safe if it is a fact about COST, not about weekly TURNOVER.  If the
  inversion is really a cost-DRAG fact -- cost_bps x turnover -- then any book that trades a
  third as often gets a third of the protection, and the record's MONTHLY 4b passes (a large
  block of it: BAND03_M, the CAND ladders at freq='M', idea 919's whole line) are still being
  certified by their family at 10 bps.  Capital follows 4b rows.  This run prices whether
  680's all-clear transfers to the slower books or stops at the weekly ones.

WHAT IS RE-RUN, EXACTLY
-----------------------
  680's 30 cells, unmodified in construction: 3 panels (U56 / B136 / SMALL439) x 2 claim sets
  (CORE gross 0.75, EXT gross 1.00) x 5 books (TOP5, TOP10, TOP20, EWELIG, BAND03), each with
  its own gross-matched rotating coin-flip null (same name count, same per-name weight, same
  pool, selection replaced by a draw).  The ONLY thing that changes is the rebalance grid.
  `build_books`, `null_streams`, `legs4b`, `pass4b`, `pass4a` and the Ctx runner are copied
  from 680's script byte-for-byte in behaviour; G3 re-derives 680's own weekly headline from
  this file's code path before any new number is read.

  TUNED (2, and only 2)
    1. CADENCE     W / M / Q.  W is 680's published grid and is the REPRODUCTION arm, not a
                   free choice; M is the queue's object; Q is the extrapolation that says
                   whether whatever M shows is a cadence LAW or a single point.  All three
                   reported in full at every cost rung.
    2. COST RUNG   0 / 2 / 5 / 10 / 25 / 50 bps.  0 is 680's object, 10 is PROTOCOL rule 2's
                   binding rung, the rest exist so the rho(cost) curve has enough points to
                   locate its ZERO CROSSING per cadence and so the three cadences OVERLAP in
                   realised cost DRAG (see the drag test).  No rung is chosen by outcome.
  NOT TUNED
    DRAWS          400, FIXED.  Nested prefixes 100/200/400 are printed as a convergence
                   diagnostic only -- the draw count is never chosen, and every headline is
                   quoted at 400.
    FIXED          gate = above 200d MA and vol20 < 0.60; warm-up 260 rows; band 0.03;
                   IS <= 2016-12-31 / OOS >= 2017-01-01 (PROTOCOL rule 8); seed base 926.
  PANELS           U56 is BINDING (680's own binding panel).  B136 and SMALL439 run identically
                   as a LABELLED REPLICATION and are not a third tuned axis.

PRE-REGISTERED HYPOTHESES (stated before the run; both bars fixed here)
-----------------------------------------------------------------------
  H_SURVIVE  (the queue's claim)   rho(pass4b, null base rate) at 10 bps is POSITIVE on
             MONTHLY books and larger than weekly's published -0.1048.
             PASS iff  rho_M(10 bps) > 0  AND  rho_M(10 bps) > rho_W(10 bps).
  H_DRAG     (the mechanism)  the inversion is a function of realised cost DRAG
             (cost_bps x book turnover / 1e4), not of the cost rung, so the three cadences'
             rho(drag) curves lie on ONE curve and their ZERO CROSSINGS in drag agree.
             PASS iff the three cadences' zero-crossing drags lie inside a 2.0x band
             (max/min <= 2.0), against a 3x+ spread in the crossing COSTS.
  Both are reported whichever way they come out; neither is a KEEP path.

PRE-REGISTERED GATES (printed before any new number is read)
------------------------------------------------------------
  G1  ctx.run == engine.backtest @ 10 bps, on EVERY cadence                     bar 1e-12
  G2  band_book(0.03, 0.75) == baseline.rules_v2_weights                        bar 0.0
  G3  680 REPRODUCTION on the weekly arm from THIS file's code path:
      4b pass counts over the 30 cells = 7 / 4 / 2 at 0 / 10 / 25 bps           bar exact
      (the book leg is draw-free and must reproduce exactly)
      rho(pass, base rate) = +0.6387 @0 bps and -0.1048 @10 bps                 bar 0.10
      (400 draws here vs 680's 1000, so the base-rate leg carries sampling noise)
      mean null base rate over the 30 cells 0.1953 @0 bps                       bar 0.05
  G3b the 2026-09-04 KEEP-4b incumbent (U56 TOP20 EW, 0.75, WEEKLY, 10 bps):
      published 12.66% / 1.0921 / -18.31%                                       bar 5e-3
  G4  panel triples (SPY and RULES v2) printed for every panel and cadence, both windows
  G5  GROSS MATCH: every null family's mean realised gross within 0.01 of its book's
  G6  determinism: seed 926 re-run reproduces its return stream exactly          bar 0.0
  G7  SMALL439: every ticker with max_1d_move >= 1.0 in data/small_meta.csv dropped first
  G8  NESTING: the 100/200 base rates are computed from prefixes of the same 400 draw
      streams (asserted on the stored per-draw pass vector)                      bar 0.0
  G9  CADENCE ORDER: mean book turnover strictly decreasing W > M > Q on every panel
      (the queue's "a third as fast" premise, checked rather than assumed)

SURVIVORSHIP (PROTOCOL 9)
-------------------------
  universe.json / universe_broad.json / the SMALL screen are CURRENT-CONSTITUENT lists, so
  every CAGR and drawdown LEVEL below is optimistic.  The direction is the same one 680 stated
  and it again works against the incumbents: a coin flip drawn from a survivor panel is a
  BETTER book than one drawn in real time, so every null base rate below is an UPPER bound and
  every book's percentile inside its null a LOWER bound.  The 4b bar is against SPY, which is
  not survivorship-inflated, so the 4b LEVELS are not protected by the usual same-tape
  argument; the base rates, the rho(cost) curves and the cadence contrasts are all same-tape
  comparisons and are unaffected by it.
"""
import sys, os, time, warnings
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
SEED0 = 926
FREQ_GRID = ["W", "M", "Q"]                    # TUNED axis 1
COSTS = [0.0, 2.0, 5.0, 10.0, 25.0, 50.0]      # TUNED axis 2
HEAD_COST = 0.0                                # 680's object
PROTO_COST = 10.0                              # PROTOCOL rule 2
DRAW_GRID = [100, 200, 400]                    # NOT tuned: convergence diagnostic only
DRAWS = max(DRAW_GRID)
CLAIM_SETS = {"CORE": 0.75, "EXT": 1.00}
BINDING_PANEL = "U56"
BASE_RATE_BAR = 0.05

# idea 680's published weekly headline -- the reproduction target (G3)
PUB680 = dict(rho0=+0.6387, rho10=-0.1048, mean_base0=0.1953,
              n_pass={0.0: 7, 10.0: 4, 25.0: 2})
KEEP4B_INCUMBENT = dict(CAGR=0.1266, Sharpe=1.0921, MaxDD=-0.1831)

SMOKE = bool(int(os.environ.get("IDEA926_SMOKE", "0")))
if SMOKE:
    DRAW_GRID = [4, 8, 12]
    DRAWS = max(DRAW_GRID)

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
# statistics (no scipy in this sandbox)
# ==========================================================================================
def _rank(a):
    """average ranks, ties shared (what Spearman needs when one side is a 0/1 flag)."""
    a = np.asarray(a, float)
    order = np.argsort(a, kind="mergesort")
    r = np.empty(len(a), float)
    r[order] = np.arange(len(a), dtype=float)
    # average the ranks inside each tie group
    s = np.sort(a)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        if j > i:
            r[np.isin(a, s[i])] = (i + j) / 2.0
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = _rank(x), _rank(y)
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


# ==========================================================================================
# fast runner -- behaviour identical to idea 680's Ctx (G1 asserts it against engine.backtest)
# ==========================================================================================
class Ctx:
    def __init__(self, px, freq):
        self.idx = px.index
        self.freq = freq
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


def pass4b_is(mi, msi):
    return bool(mi["H1"] > msi["H1"] and mi["H2"] > msi["H2"] and
                abs(mi["MaxDD"]) <= 0.60 * abs(msi["MaxDD"]) and
                mi["CAGR"] >= 0.70 * msi["CAGR"])


def failstr(m, oos_s, ms, spy_oos):
    f = [k for k, v in legs4b(m, oos_s, ms, spy_oos).items() if not v]
    return "+".join(f) if f else "-"


# ==========================================================================================
# panels / books / nulls -- copied from idea 680
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
    """Gross-matched rotating coin flips on THIS cadence's rebalance grid.

    On every rebalance row the book holds n(t) names at a common per-name weight w(t); the null
    holds n(t) names drawn uniformly from the family's pool at the SAME w(t).  Count and weight
    are copied from the book, so gross, cash drag and de-grossing path are identical and the
    only thing that changes is WHICH names are held.  Slowing the cadence slows the null by
    exactly the same construction, which is what makes the cadence axis clean.
    """
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


def panel_context(px, freq):
    ctx = Ctx(px, freq)
    idx = px.index
    i0 = WARM
    oos_mask = np.asarray(idx >= pd.Timestamp(OOS_START))[i0:]
    is_mask = np.asarray(idx <= pd.Timestamp(IS_END))[i0:]
    spy = px["SPY"].pct_change().fillna(0.0).values[i0:]
    out = dict(ctx=ctx, i0=i0, idx=idx, oos=oos_mask, is_=is_mask,
               spy=mets(spy), spy_oos=mets(spy[oos_mask]), spy_is=mets(spy[is_mask]))
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


# ==========================================================================================
def gates_static(panels, n_dropped):
    """G1 / G2 / G6 / G7 -- everything that does not need the weekly 680 reproduction."""
    ok = {}
    px = panels[BINDING_PANEL]
    w = band_book(px, BAND0, 0.75)
    g2 = float(np.abs(w.values - rules_v2_weights(px, BAND0, 0.75).values).max())
    ok["G2"] = g2 == 0.0
    P(f"  G2 band_book(0.03,0.75) == rules_v2_weights      : {g2:.3e}  "
      f"{'PASS' if ok['G2'] else 'FAIL'}")

    worst = 0.0
    for f in FREQ_GRID:
        ctx = Ctx(px, f)
        gr, turn = ctx.run(ctx.shift(w))
        fast = pd.Series(gr - turn * 10.0 / 1e4, index=px.index)
        slow = backtest(px, w, cost_bps=10.0, freq=f)["returns"]
        j = px.index[WARM]
        d = float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max())
        worst = max(worst, d)
        P(f"     G1 cadence {f}: ctx.run vs engine.backtest @10 bps  {d:.3e}")
    ok["G1"] = worst < 1e-12
    P(f"  G1 worst over all cadences                       : {worst:.3e}  "
      f"{'PASS' if ok['G1'] else 'FAIL'}")

    ctx = Ctx(px, "M")
    bks, cand = build_books(px, 0.75)
    wt20 = ctx.shift(bks["TOP20"])
    a, _ = ctx.run(next(null_streams(ctx, px, cand, 1)("ROT", wt20, 20))[1])
    b, _ = ctx.run(next(null_streams(ctx, px, cand, 1)("ROT", wt20, 20))[1])
    g6 = float(np.abs(a - b).max())
    ok["G6"] = g6 == 0.0
    P(f"  G6 determinism (seed {SEED0} re-drawn, cadence M)   : {g6:.3e}  "
      f"{'PASS' if ok['G6'] else 'FAIL'}")
    if "SMALL439" in panels:
        P(f"  G7 SMALL439 screen: {n_dropped} tickers with max_1d_move >= 1.0 dropped  "
          f"({panels['SMALL439'].shape[1] - 1} names + SPY)  PASS")
        ok["G7"] = True
    return ok


# ==========================================================================================
def main():
    t_start = time.time()
    P("IDEA 926  does-the-ZERO-COST-pass-to-BASE-RATE-inversion-hold-on-MONTHLY-4b-passes "
      "(lane B)")
    P(f"run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC   seed base {SEED0}   "
      f"cadences {FREQ_GRID}   costs {COSTS} bps   draws {DRAWS} (nested {DRAW_GRID})")
    P()
    panels, n_dropped = load_panels()

    P("=" * 100)
    P("(A) PRE-REGISTERED GATES -- structural half, run before any new number is read")
    P("=" * 100)
    gk = gates_static(panels, n_dropped)
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(B) PANEL TRIPLES (G4) -- SPY and the live book, full sample from row 260 and rule-8 OOS")
    P("=" * 100)
    PC = {}
    for pn, px in panels.items():
        for f in FREQ_GRID:
            PC[(pn, f)] = panel_context(px, f)
        pc = PC[(pn, "W")]
        s, so = pc["spy"], pc["spy_oos"]
        P(f"  {pn:9s} n={px.shape[1]:4d}  {px.index[WARM].date()}..{px.index[-1].date()}")
        P(f"     SPY        full {s['CAGR']:7.2%} / {s['Sharpe']:.4f} / {s['MaxDD']:7.2%}  "
          f"(halves {s['H1']:.3f}/{s['H2']:.3f})   OOS {so['CAGR']:7.2%} / "
          f"{so['Sharpe']:.4f} / {so['MaxDD']:7.2%}")
        for f in FREQ_GRID:
            v = PC[(pn, f)]["v2"][PROTO_COST]
            P(f"     RULES v2 [{f}] full {v['full']['CAGR']:7.2%} / "
              f"{v['full']['Sharpe']:.4f} / {v['full']['MaxDD']:7.2%}  (halves "
              f"{v['full']['H1']:.3f}/{v['full']['H2']:.3f})   OOS {v['oos']['CAGR']:7.2%} / "
              f"{v['oos']['Sharpe']:.4f} / {v['oos']['MaxDD']:7.2%}   [live cadence is W]")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(C) THE BOOKS -- 680's 30 cells, re-run on each cadence's rebalance grid")
    P("=" * 100)
    BOOKROWS, CAND, WTS = [], {}, {}
    for pn, px in panels.items():
        for f in FREQ_GRID:
            pc = PC[(pn, f)]
            for cs, g in CLAIM_SETS.items():
                bks, cand = build_books(px, g)
                CAND[(pn, cs)] = cand
                for bn, W in bks.items():
                    wt = pc["ctx"].shift(W)
                    WTS[(pn, f, cs, bn)] = wt
                    gr, tn = pc["ctx"].run(wt)
                    gross = pc["ctx"].gross(wt, pc["i0"])
                    tpy = float(tn[pc["i0"]:].sum() / ((len(tn) - pc["i0"]) / 252.0))
                    for c in COSTS:
                        m, mo, mi = score_stream(gr, tn, pc, c)
                        mb = pc["v2"][c]["full"]
                        BOOKROWS.append(dict(
                            panel=pn, cadence=f, claim_set=cs, book=bn, gross_nom=g, cost=c,
                            mean_gross=gross, turn_per_yr=tpy, drag_bps=c * tpy,
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

    P("  4b / 4a pass counts over the 30 cells (3 panels x 2 claim sets x 5 books), by cell:")
    P(f"     {'cadence':8s} {'cost':>6s}  {'4b':>7s}  {'4a':>7s}   {'mean turn/yr':>12s}   "
      f"{'mean drag (bps/yr)':>18s}")
    for f in FREQ_GRID:
        for c in COSTS:
            sub = books[(books.cadence == f) & (books.cost == c)]
            P(f"     {f:8s} {c:6.0f}  {int(sub.pass4b.sum()):3d}/{len(sub):<3d}  "
              f"{int(sub.pass4a.sum()):3d}/{len(sub):<3d}   {sub.turn_per_yr.mean():12.2f}   "
              f"{sub.drag_bps.mean():18.1f}")
        P()
    P("  G9 CADENCE ORDER -- mean book turnover per year, by panel (the queue's premise):")
    g9 = True
    for pn in panels:
        t = [float(books[(books.panel == pn) & (books.cadence == f) &
                         (books.cost == 0.0)].turn_per_yr.mean()) for f in FREQ_GRID]
        g9 &= (t[0] > t[1] > t[2])
        P(f"     {pn:9s} " + "  ".join(f"{f}: {v:6.2f}x" for f, v in zip(FREQ_GRID, t)) +
          f"   W/M ratio {t[0] / max(t[1], 1e-9):.2f}x   W/Q {t[0] / max(t[2], 1e-9):.2f}x")
    gk["G9"] = bool(g9)
    P(f"     G9 strictly decreasing W > M > Q on every panel: "
      f"{'PASS' if gk['G9'] else 'FAIL'}")
    P()

    b_inc = books[(books.panel == BINDING_PANEL) & (books.cadence == "W") &
                  (books.claim_set == "CORE") & (books.book == "TOP20") &
                  (books.cost == PROTO_COST)].iloc[0]
    d3b = max(abs(float(b_inc[k]) - v) for k, v in KEEP4B_INCUMBENT.items())
    gk["G3b"] = d3b < 5e-3
    P(f"  G3b 2026-09-04 KEEP-4b incumbent (U56 CORE/TOP20, WEEKLY, 10 bps): got "
      f"{b_inc.CAGR:.2%} / {b_inc.Sharpe:.4f} / {b_inc.MaxDD:.2%}   published "
      f"{KEEP4B_INCUMBENT['CAGR']:.2%} / {KEEP4B_INCUMBENT['Sharpe']:.4f} / "
      f"{KEEP4B_INCUMBENT['MaxDD']:.2%}   max|d| {d3b:.3e}  "
      f"{'PASS' if gk['G3b'] else 'FAIL'}")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(D) THE NULLS -- gross-matched coin flips on each cadence's own grid")
    P("=" * 100)
    FAM = {"TOP5": ("ROT", 5), "TOP10": ("ROT", 10), "TOP20": ("ROT", 20),
           "EWELIG": ("EW", None), "BAND03": ("BD", None)}
    NULLROWS, DRAWROWS = [], []
    for pn, px in panels.items():
        for f in FREQ_GRID:
            pc = PC[(pn, f)]
            for cs, g in CLAIM_SETS.items():
                gen = null_streams(pc["ctx"], px, CAND[(pn, cs)], DRAWS)
                for bn, (kind, k) in FAM.items():
                    t0 = time.time()
                    pv = {c: np.zeros(DRAWS, bool) for c in COSTS}
                    iv = {c: np.zeros(DRAWS, bool) for c in COSTS}
                    sv = {c: np.zeros(DRAWS) for c in COSTS}
                    cvv = {c: np.zeros(DRAWS) for c in COSTS}
                    dv = {c: np.zeros(DRAWS) for c in COSTS}
                    ov = {c: np.zeros(DRAWS) for c in COSTS}
                    gsum = 0.0
                    for d, W in gen(kind, WTS[(pn, f, cs, bn)], k):
                        gr, tn = pc["ctx"].run(W)
                        gsum += pc["ctx"].gross(W, pc["i0"])
                        for c in COSTS:
                            m, mo, mi = score_stream(gr, tn, pc, c)
                            pv[c][d] = pass4b(m, mo["Sharpe"], pc["spy"],
                                              pc["spy_oos"]["Sharpe"])
                            iv[c][d] = pass4b_is(mi, pc["spy_is"])
                            sv[c][d], cvv[c][d], dv[c][d] = m["Sharpe"], m["CAGR"], m["MaxDD"]
                            ov[c][d] = mo["Sharpe"]
                    mg_null = gsum / DRAWS
                    brow = books[(books.panel == pn) & (books.cadence == f) &
                                 (books.claim_set == cs) & (books.book == bn)]
                    mg_book = float(brow.mean_gross.iloc[0])
                    gmatch = abs(mg_null - mg_book)
                    for c in COSTS:
                        b = brow[brow.cost == c].iloc[0]
                        for nd in DRAW_GRID:
                            base = float(pv[c][:nd].mean())
                            NULLROWS.append(dict(
                                panel=pn, cadence=f, claim_set=cs, book=bn, null=kind,
                                gross_nom=g, cost=c, draws=nd, null_base_rate_4b=base,
                                is_base_rate_4b=float(iv[c][:nd].mean()),
                                book_pass4b=bool(b.pass4b), book_pass4a=bool(b.pass4a),
                                outside_null=bool(b.pass4b and base <= BASE_RATE_BAR),
                                pct_Sharpe=float((sv[c][:nd] < b.Sharpe).mean()),
                                pct_CAGR=float((cvv[c][:nd] < b.CAGR).mean()),
                                pct_MaxDD=float((np.abs(dv[c][:nd]) > abs(b.MaxDD)).mean()),
                                pct_OOS_Sharpe=float((ov[c][:nd] < b.OOS_Sharpe).mean()),
                                p_emp_Sharpe=float((1 + (sv[c][:nd] >= b.Sharpe).sum()) /
                                                   (1 + nd)),
                                null_mean_Sharpe=float(sv[c][:nd].mean()),
                                book_Sharpe=float(b.Sharpe), book_CAGR=float(b.CAGR),
                                book_MaxDD=float(b.MaxDD), turn_per_yr=float(b.turn_per_yr),
                                drag_bps=float(b.drag_bps), mean_gross_null=mg_null,
                                mean_gross_book=mg_book, gross_match=gmatch))
                        if c == HEAD_COST:
                            for d in range(DRAWS):
                                DRAWROWS.append(dict(panel=pn, cadence=f, claim_set=cs,
                                                     book=bn, draw=d, pass4b=bool(pv[c][d]),
                                                     Sharpe=sv[c][d], CAGR=cvv[c][d],
                                                     MaxDD=dv[c][d], OOS_Sharpe=ov[c][d]))
                    P(f"  {pn:9s} [{f}] {cs:4s} {bn:7s} null={kind:3s}  gross book "
                      f"{mg_book:.3f} vs null {mg_null:.3f} (|d| {gmatch:.4f})   base rate "
                      f"@0bps {float(pv[0.0].mean()):6.1%}  @10bps "
                      f"{float(pv[10.0].mean()):6.1%}  @50bps {float(pv[50.0].mean()):6.1%}"
                      f"   [{time.time() - t0:.0f}s]")
        P()
    nulls = pd.DataFrame(NULLROWS)
    draws_df = pd.DataFrame(DRAWROWS)
    dump(nulls, "nulls")
    dump(draws_df, "draws")

    g5 = float(nulls.gross_match.max())
    gk["G5"] = g5 < 0.01
    P(f"  G5 gross match, worst over all "
      f"{nulls[['panel','cadence','claim_set','book']].drop_duplicates().shape[0]} families: "
      f"{g5:.4f}  {'PASS' if gk['G5'] else 'FAIL'}")
    nest_ok = True
    for (pn, f, cs, bn), gdf in draws_df.groupby(["panel", "cadence", "claim_set", "book"]):
        v = gdf.sort_values("draw").pass4b.values
        for nd in DRAW_GRID:
            got = float(nulls[(nulls.panel == pn) & (nulls.cadence == f) &
                              (nulls.claim_set == cs) & (nulls.book == bn) &
                              (nulls.cost == HEAD_COST) &
                              (nulls.draws == nd)].null_base_rate_4b.iloc[0])
            nest_ok &= abs(float(v[:nd].mean()) - got) == 0.0
    gk["G8"] = bool(nest_ok)
    P(f"  G8 nesting: the 100/200 base rates are exact prefixes of the same {DRAWS} streams  "
      f"{'PASS' if gk['G8'] else 'FAIL'}")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(E) G3 -- reproduce idea 680's WEEKLY headline from this file's code path")
    P("=" * 100)
    RHO = {}
    for f in FREQ_GRID:
        for c in COSTS:
            sub = nulls[(nulls.cadence == f) & (nulls.cost == c) &
                        (nulls.draws == DRAWS)].sort_values(["panel", "claim_set", "book"])
            RHO[(f, c)] = dict(
                rho=spearman(sub.book_pass4b.astype(float).values,
                             sub.null_base_rate_4b.values),
                n_pass=int(sub.book_pass4b.sum()), n=len(sub),
                mean_base=float(sub.null_base_rate_4b.mean()),
                max_base=float(sub.null_base_rate_4b.max()),
                base_pass=float(sub[sub.book_pass4b].null_base_rate_4b.mean())
                if sub.book_pass4b.any() else np.nan,
                base_fail=float(sub[~sub.book_pass4b].null_base_rate_4b.mean())
                if (~sub.book_pass4b).any() else np.nan,
                above05=int((sub.null_base_rate_4b > 0.05).sum()),
                above50=int((sub.null_base_rate_4b > 0.50).sum()),
                outside=int(sub.outside_null.sum()),
                mean_drag=float(sub.drag_bps.mean()))
    d_cnt = {c: abs(RHO[("W", c)]["n_pass"] - PUB680["n_pass"][c]) for c in PUB680["n_pass"]}
    d_r0 = abs(RHO[("W", 0.0)]["rho"] - PUB680["rho0"])
    d_r10 = abs(RHO[("W", PROTO_COST)]["rho"] - PUB680["rho10"])
    d_mb = abs(RHO[("W", 0.0)]["mean_base"] - PUB680["mean_base0"])
    gk["G3"] = (max(d_cnt.values()) == 0) and d_r0 < 0.10 and d_r10 < 0.10 and d_mb < 0.05
    P(f"  4b pass counts on the weekly arm  got "
      f"{ {int(c): RHO[('W', c)]['n_pass'] for c in PUB680['n_pass']} }  published "
      f"{ {int(c): v for c, v in PUB680['n_pass'].items()} }   max|d| {max(d_cnt.values())}")
    P(f"  rho @ 0 bps   got {RHO[('W', 0.0)]['rho']:+.4f}  published "
      f"{PUB680['rho0']:+.4f}   |d| {d_r0:.4f}  (bar 0.10, {DRAWS} draws vs 680's 1000)")
    P(f"  rho @10 bps   got {RHO[('W', PROTO_COST)]['rho']:+.4f}  published "
      f"{PUB680['rho10']:+.4f}   |d| {d_r10:.4f}  (bar 0.10)")
    P(f"  mean base rate @0 bps  got {RHO[('W', 0.0)]['mean_base']:.4f}  published "
      f"{PUB680['mean_base0']:.4f}   |d| {d_mb:.4f}  (bar 0.05)")
    P(f"  G3: {'PASS' if gk['G3'] else 'FAIL'}")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(F) THE ANSWER -- rho(4b pass, null base rate) at every cadence x cost rung")
    P("=" * 100)
    P(f"  30 cells per (cadence, cost).  rho is Spearman on (0/1 pass, base rate); "
      f"{DRAWS} draws.")
    P(f"     {'cad':3s} {'cost':>5s} {'drag':>7s} {'rho':>8s} {'4b pass':>8s} "
      f"{'base|pass':>10s} {'base|fail':>10s} {'mean base':>10s} {'max base':>9s} "
      f"{'>0.05':>6s} {'>0.50':>6s} {'outside':>8s}")
    ROWS = []
    for f in FREQ_GRID:
        for c in COSTS:
            r = RHO[(f, c)]
            P(f"     {f:3s} {c:5.0f} {r['mean_drag']:7.1f} {r['rho']:+8.4f} "
              f"{r['n_pass']:3d}/{r['n']:<4d} {r['base_pass']:10.3f} {r['base_fail']:10.3f} "
              f"{r['mean_base']:10.4f} {r['max_base']:9.3f} {r['above05']:6d} "
              f"{r['above50']:6d} {r['outside']:8d}")
            ROWS.append(dict(cadence=f, cost=c, **r))
        P()
    rho_df = pd.DataFrame(ROWS)
    dump(rho_df, "rho")

    # zero crossings, in COST and in DRAG
    P("  ZERO CROSSING of rho(cost), per cadence (linear interpolation between grid rungs):")
    CROSS = {}
    for f in FREQ_GRID:
        s = rho_df[rho_df.cadence == f].sort_values("cost")
        xs, ys, dg = s.cost.values, s.rho.values, s.mean_drag.values
        cc = dd = np.nan
        for i in range(len(xs) - 1):
            if np.isfinite(ys[i]) and np.isfinite(ys[i + 1]) and ys[i] > 0 >= ys[i + 1]:
                t = ys[i] / (ys[i] - ys[i + 1])
                cc = xs[i] + t * (xs[i + 1] - xs[i])
                dd = dg[i] + t * (dg[i + 1] - dg[i])
                break
        CROSS[f] = (cc, dd)
        P(f"     {f}: rho crosses zero at cost {cc:6.2f} bps   "
          f"(mean realised drag {dd:7.1f} bps/yr)")
    cs_ = [v[0] for v in CROSS.values() if np.isfinite(v[0])]
    ds_ = [v[1] for v in CROSS.values() if np.isfinite(v[1])]
    spread_cost = max(cs_) / min(cs_) if len(cs_) == len(FREQ_GRID) and min(cs_) > 0 else np.nan
    spread_drag = max(ds_) / min(ds_) if len(ds_) == len(FREQ_GRID) and min(ds_) > 0 else np.nan
    P(f"     spread of crossing COSTS {spread_cost:.2f}x   spread of crossing DRAGS "
      f"{spread_drag:.2f}x")
    P()

    P("  PRE-REGISTERED HYPOTHESES")
    rW10, rM10 = RHO[("W", PROTO_COST)]["rho"], RHO[("M", PROTO_COST)]["rho"]
    h_surv = bool(rM10 > 0 and rM10 > rW10)
    P(f"     H_SURVIVE  rho_M(10 bps) = {rM10:+.4f}  vs  rho_W(10 bps) = {rW10:+.4f}   "
      f"-> {'PASS' if h_surv else 'FAIL'}  (needs > 0 and > weekly)")
    h_drag = bool(np.isfinite(spread_drag) and spread_drag <= 2.0)
    P(f"     H_DRAG     crossing drags {[f'{v:.0f}' for v in ds_]} bps/yr, spread "
      f"{spread_drag:.2f}x (bar 2.0x); crossing costs "
      f"{[f'{v:.1f}' for v in cs_]} bps, spread {spread_cost:.2f}x   "
      f"-> {'PASS' if h_drag else 'FAIL'}")
    P()

    P(f"  per-cell detail, MONTHLY cadence at PROTOCOL's own rung ({PROTO_COST:.0f} bps), "
      f"{DRAWS} draws:")
    P(f"     {'panel':9s} {'set':4s} {'book':7s} {'4b':4s} {'base rate':>9s} {'pct(Sh)':>8s} "
      f"{'pct(OOS)':>9s} {'p_emp':>7s} {'turn':>6s} {'drag':>7s}  outside?")
    for _, r in nulls[(nulls.cadence == "M") & (nulls.cost == PROTO_COST) &
                      (nulls.draws == DRAWS)].iterrows():
        P(f"     {r.panel:9s} {r.claim_set:4s} {r.book:7s} "
          f"{'PASS' if r.book_pass4b else 'fail':4s} {r.null_base_rate_4b:9.1%} "
          f"{r.pct_Sharpe:8.1%} {r.pct_OOS_Sharpe:9.1%} {r.p_emp_Sharpe:7.3f} "
          f"{r.turn_per_yr:6.2f} {r.drag_bps:7.1f}  "
          f"{'YES' if r.outside_null else 'no'}")
    P()
    P("  draw-axis convergence (binding panel U56, cadence M, 10 bps):")
    for cs in CLAIM_SETS:
        for bn in FAM:
            row = [float(nulls[(nulls.panel == BINDING_PANEL) & (nulls.cadence == "M") &
                               (nulls.claim_set == cs) & (nulls.book == bn) &
                               (nulls.cost == PROTO_COST) &
                               (nulls.draws == nd)].null_base_rate_4b.iloc[0])
                   for nd in DRAW_GRID]
            P(f"     {cs:4s} {bn:7s}  " +
              "  ".join(f"n={nd}: {v:6.1%}" for nd, v in zip(DRAW_GRID, row)))
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(G) RULE 8 WALK-FORWARD -- parameters chosen on 2009-2016 only, 2017-2026 read once")
    P("=" * 100)
    P("  Four IS-only choosers.  CH_* pick inside one cadence; CH_ANYCAD lets the CADENCE")
    P("  itself be chosen in sample, which is the walk-forward this idea actually needs.")
    P("    CH_SHARPE   best IS Sharpe                                    (no clause)")
    P("    CH_4bIS     best IS Sharpe among books passing the IS 4b LEVEL legs")
    P("    CH_BASE     best IS Sharpe among books with IS base rate <= 0.05")
    P("    CH_ANYCAD   best IS Sharpe over ALL cadences x books x claim sets")
    WF = []
    for pn, px in panels.items():
        for c in COSTS:
            br_all = nulls[(nulls.panel == pn) & (nulls.cost == c) & (nulls.draws == DRAWS)]
            cand_all = books[(books.panel == pn) & (books.cost == c)].merge(
                br_all[["cadence", "claim_set", "book", "null_base_rate_4b",
                        "is_base_rate_4b"]],
                on=["cadence", "claim_set", "book"], how="left")
            for f in FREQ_GRID + ["ANY"]:
                pc = PC[(pn, "W" if f == "ANY" else f)]
                cand = cand_all if f == "ANY" else cand_all[cand_all.cadence == f]
                cand = cand.copy()
                cand["IS_ok"] = (cand.IS_H1 > pc["spy_is"]["H1"]) & \
                                (cand.IS_H2 > pc["spy_is"]["H2"]) & \
                                (cand.IS_CAGR >= 0.70 * pc["spy_is"]["CAGR"]) & \
                                (cand.IS_MaxDD.abs() <= 0.60 * abs(pc["spy_is"]["MaxDD"]))
                if f == "ANY":
                    picks = {"CH_ANYCAD":
                             cand.sort_values("IS_Sharpe", ascending=False).iloc[0]}
                else:
                    picks = {}
                    picks["CH_SHARPE"] = cand.sort_values("IS_Sharpe",
                                                          ascending=False).iloc[0]
                    s4 = cand[cand.IS_ok].sort_values("IS_Sharpe", ascending=False)
                    picks["CH_4bIS"] = s4.iloc[0] if len(s4) else None
                    sb = cand[cand.is_base_rate_4b <= BASE_RATE_BAR].sort_values(
                        "IS_Sharpe", ascending=False)
                    picks["CH_BASE"] = sb.iloc[0] if len(sb) else None
                for ch, r in picks.items():
                    if r is None:
                        WF.append(dict(panel=pn, cadence=f, cost=c, chooser=ch, pick="EMPTY"))
                        continue
                    pcr = PC[(pn, r.cadence)]
                    v2o, so = pcr["v2"][c]["oos"], pcr["spy_oos"]
                    WF.append(dict(
                        panel=pn, cadence=f, cost=c, chooser=ch,
                        pick=f"{r.cadence}/{r.claim_set}/{r.book}", IS_Sharpe=r.IS_Sharpe,
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
    for pn in panels:
        P(f"  {pn}:")
        for _, r in wf[wf.panel == pn].iterrows():
            if r["pick"] == "EMPTY":
                P(f"     [{r.cadence:3s}] {r.cost:4.0f} bps  {r.chooser:10s}  IS set EMPTY")
                continue
            P(f"     [{r.cadence:3s}] {r.cost:4.0f} bps  {r.chooser:10s}  pick "
              f"{r['pick']:16s} (IS Sh {r.IS_Sharpe:5.2f}, IS base {r.is_base_rate:5.1%}) "
              f"OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:5.3f} / {r.OOS_MaxDD:7.2%}   "
              f"4b {'PASS' if r.OOS_4b else 'fail'}  4a {'PASS' if r.OOS_4a else 'fail'}   "
              f"[SPY {r.SPY_OOS_CAGR:6.2%}/{r.SPY_OOS_Sharpe:5.3f}/{r.SPY_OOS_MaxDD:7.2%}"
              f" | v2 {r.V2_OOS_CAGR:6.2%}/{r.V2_OOS_Sharpe:5.3f}/{r.V2_OOS_MaxDD:7.2%}]")
        P()
    live = wf[wf["pick"] != "EMPTY"]
    P(f"  rule-8 totals: 4b {int(live.OOS_4b.sum())} of {len(live)} live picks, "
      f"4a {int(live.OOS_4a.sum())} of {len(live)}   "
      f"(EMPTY on {int((wf['pick'] == 'EMPTY').sum())})")
    for ch, gdf in live.groupby("chooser"):
        P(f"     {ch:10s}  4b {int(gdf.OOS_4b.sum()):2d}/{len(gdf):<3d}  "
          f"4a {int(gdf.OOS_4a.sum()):2d}/{len(gdf):<3d}  mean OOS Sharpe "
          f"{gdf.OOS_Sharpe.mean():5.3f}  mean OOS CAGR {gdf.OOS_CAGR.mean():6.2%}")
    P()
    P("  best OOS cells among the live picks (by OOS Sharpe):")
    for _, r in live.sort_values("OOS_Sharpe", ascending=False).head(5).iterrows():
        P(f"     {r.panel:9s} [{r.cadence:3s}] {r.cost:4.0f} bps {r.chooser:10s} "
          f"{r['pick']:16s}  OOS {r.OOS_CAGR:7.2%} / {r.OOS_Sharpe:5.3f} / "
          f"{r.OOS_MaxDD:7.2%}  4b {'PASS' if r.OOS_4b else 'fail'}  "
          f"4a {'PASS' if r.OOS_4a else 'fail'}")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(H) KEEP PATHS -- both, at PROTOCOL's own rung, full sample")
    P("=" * 100)
    k4b = books[(books.cost == PROTO_COST) & books.pass4b]
    k4a = books[(books.cost == PROTO_COST) & books.pass4a]
    P(f"  4a (beat the live book, both halves + MaxDD): {len(k4a)} of "
      f"{len(books[books.cost == PROTO_COST])} cells")
    for _, r in k4a.iterrows():
        P(f"     {r.panel:9s} [{r.cadence}] {r.claim_set:4s} {r.book:7s}  "
          f"{r.CAGR:7.2%} / {r.Sharpe:6.3f} / {r.MaxDD:7.2%}")
    P(f"  4b (capital-worthy, full sample legs): {len(k4b)} of "
      f"{len(books[books.cost == PROTO_COST])} cells")
    for _, r in k4b.iterrows():
        nb = nulls[(nulls.panel == r.panel) & (nulls.cadence == r.cadence) &
                   (nulls.claim_set == r.claim_set) & (nulls.book == r.book) &
                   (nulls.cost == PROTO_COST) & (nulls.draws == DRAWS)].iloc[0]
        P(f"     {r.panel:9s} [{r.cadence}] {r.claim_set:4s} {r.book:7s}  "
          f"{r.CAGR:7.2%} / {r.Sharpe:6.3f} / {r.MaxDD:7.2%}  halves "
          f"{r.H1:5.2f}/{r.H2:5.2f}  OOS {r.OOS_Sharpe:5.3f}  null base rate "
          f"{nb.null_base_rate_4b:5.1%}  outside null "
          f"{'YES' if nb.outside_null else 'no'}")
    P("  NOTE: a full-sample 4b pass is NOT a KEEP; rule 8's OOS leg is section (G) and every")
    P("  such cell is an already-published book, not a new rule.  Nothing is promoted here.")
    P()

    P("=" * 100)
    P("(I) GATES")
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
