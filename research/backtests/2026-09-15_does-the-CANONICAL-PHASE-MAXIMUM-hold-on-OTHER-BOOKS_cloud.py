#!/usr/bin/env python3
"""Idea 942 (cloud, 2026-09-15) -- does the CANONICAL PHASE MAXIMUM hold on the record's OTHER
committed MONTHLY and QUARTERLY books?

THE QUESTION (queue, 2026-09-15)
  Idea 938 found the canonical month-end is the MAXIMUM of its own 21-phase family at 16 of 16
  grid points on TOP20 (`canon pctile 1.000` at U56/CORE, U56/EXT, B136/CORE, B136/EXT x
  0 / 5 / 10 / 25 bps), which is either a property of that book or a property of month-end
  itself (window dressing, month-end flows, the 21-day momentum lookback aliasing onto the
  rebalance date).  Re-run the same phase grid on EWELIG, BAND03, TOP5 and TOP10 and on the Q
  cadence (63 phases), and report whether 'canonical = max' is universal, book-specific, or a
  lookback-alias.

WHY THE BOOK SET IS ITSELF THE DISCRIMINATOR
  The queue names three candidate carriers.  The book set the queue chose separates them with no
  extra dial, which is why this run does not spend one:
    WINDOW DRESSING / MONTH-END FLOWS  a property of the DATE.  It would hold on every book that
                                       trades on that date, including books with no momentum
                                       signal at all.
    THE 21-DAY LOOKBACK ALIAS          a property of the SIGNAL.  `baseline.score` uses
                                       `px.shift(21) / px.shift(252) - 1`, and 21 trading days is
                                       one month, so on a month-end rebalance the 12-1 momentum
                                       window snaps to a month boundary.  This can only act
                                       through a book that USES the composite.
    A PROPERTY OF TOP20                neither; it would not survive a change of k.
  **EWELIG and BAND03 have no momentum lookback whatsoever** -- EWELIG ranks nothing (it holds
  every eligible name) and BAND03 is a pure 200d-band book.  So if `canonical = max` survives on
  them, the lookback-alias story is dead without any lookback sweep at all; if it dies on exactly
  those two while holding on TOP05/10/20, the alias story is the survivor.  A direct lookback
  probe on TOP20 is run anyway, REPORTED and never selected on, as confirmation.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL rule 4: max 2 tuned parameters)
  TUNED 1  BOOK SET, 5 levels, every one reported:
           TOP20  938's own book and the G3 anchor (composite rank, k = 20, no vol scaler)
           TOP05  TOP10   the same construction at k = 5 and k = 10 (the queue's TOP5 / TOP10)
           EWELIG equal weight over EVERY eligible name (above 200d MA, vol20 < 0.60).  NO rank,
                  NO lookback.  The 2026-09-03 memo's Finding 2 book.
           BAND03 the 200d +/-3% band book == `rules_v2_weights`, the LIVE rules.  NO lookback.
  TUNED 2  CADENCE, 2 levels, both reported:
           M  21 day-of-month phases (938's grid, exactly)
           Q  63 day-of-quarter phases (the queue's ask)
  REPORTED AXES, nothing fitted on any of them, every point published:
           panel   U56 / B136 / SMALL          (3)
           gross   CORE = 0.75 / EXT = 1.00    (2, 938's own CLAIM_SETS)
           cost    0 / 5 / 10 / 25 / 50 bps    (5; 10 bps carries every verdict, PROTOCOL rule 2)
           statistic  CAGR (938's) and Sharpe, both printed for every cell
           lookback probe  the composite's short shift in {0, 5, 10, 21, 42, 63} on TOP20

PRE-REGISTERED BARS (fixed before any number of this run was read; both directions reported)
  H_UNIV   'canonical = max' is UNIVERSAL iff the canonical phase is the CAGR argmax of its own
           family in >= 90% of the (book x panel x gross x cadence x rung) cells.
  H_BOOK   it is BOOK-SPECIFIC iff TOP20 holds at >= 90% of ITS cells while the pooled non-TOP20
           rate is < 50%.
  H_ALIAS  it is a LOOKBACK ALIAS iff the pooled rate over the three COMPOSITE books
           (TOP05/10/20) is >= 90% AND the pooled rate over the two LOOKBACK-FREE books
           (EWELIG, BAND03) is < 50%.
  H_Q      it is a PERIOD-END fact rather than a MONTH-END fact iff the Q-cadence rate is within
           20 pp of the M-cadence rate.  A large M-over-Q gap makes it a month-end fact.
  H_G3     938's 16 of 16 reproduces EXACTLY on this run's machinery (U56/B136 x CORE/EXT x
           0/5/10/25 bps, TOP20, M).  Any miss is printed, not absorbed.
  H_WF     (PROTOCOL rule 8, REQUIRED) phase AND book chosen on 2009-2016 ALONE, 2017-2026 read
           ONCE, BOTH KEEP paths adjudicated against the live RULES v2 baseline and against SPY.
           This is the part that decides whether the finding is worth any capital: a phase that
           is the in-sample maximum is worth nothing if it is not the out-of-sample one.

SURVIVORSHIP (PROTOCOL rule 9)
  U56 / B136 / SMALL are CURRENT-CONSTITUENT lists (SMALL additionally drops every ticker with
  `max_1d_move` >= 1.0 per `data/small_meta.csv`).  Every CAGR, Sharpe and drawdown LEVEL below
  is optimistic and none is a capital claim on its own.  Direction for THIS run: the phase
  contrasts are SAME-TAPE, SAME-UNIVERSE, SAME-WEIGHTS comparisons that differ only in WHICH DAY
  the identical book trades, so the 'canonical = max' tallies are unaffected by panel
  composition.  The 4b LEVELS in the walk-forward are read against SPY, which is not
  survivorship-inflated, so a survivor panel makes books look BETTER and 4b failures RARER.
"""
import os, sys, time, warnings
from pathlib import Path
import numpy as np, pandas as pd

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, band_state, score   # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

BAND0, VOLCAP, WARM = 0.03, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
HEAD_COST = 10.0
DOM_N, DOQ_N = 21, 63                      # TUNED axis 2 -- 938's monthly grid, and the Q grid
CLAIM_SETS = {"CORE": 0.75, "EXT": 1.00}   # 938's own gross conventions
RUNGS = [0.0, 5.0, 10.0, 25.0, 50.0]
G3_RUNGS = [0.0, 5.0, 10.0, 25.0]          # the four 938 published
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
UNIV_BAR, BOOK_BAR, ALIAS_BAR, Q_BAR = 0.90, 0.50, 0.90, 0.20
LOOKBACKS = [0, 5, 10, 21, 42, 63]
SMOKE = bool(int(os.environ.get("IDEA942_SMOKE", "0")))
LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}.csv"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df)} rows)")


# ==========================================================================================
# (1) the phase machinery -- copied VERBATIM from idea 938 so this run NESTS it (G0/G1)
# ==========================================================================================
def offset_mask(idx, per, d):
    """True d trading days BEFORE the last trading day of each period (per in {'W','M','Q'}).
    d = 0 reproduces engine.rebalance_mask(idx, per) exactly (G0)."""
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Ctx:
    """Fast runner -- byte-identical to idea 938's.  G1 asserts it against engine.backtest."""
    def __init__(self, px, mask):
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        m = np.asarray(mask.values, bool)
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


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    return float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan


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
    return dict(H1=m["H1"] > ms["H1"], H2=m["H2"] > ms["H2"], OOS=oos_s > spy_oos,
                DD=abs(m["MaxDD"]) <= 0.60 * abs(ms["MaxDD"]),
                CAGR=m["CAGR"] >= 0.70 * ms["CAGR"])


def failstr(lg):
    order = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
    f = [order[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


# ==========================================================================================
# (2) THE BOOK SET -- TUNED axis 1.  Every book is run at every phase, gross and rung.
# ==========================================================================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    """== rules_v2_weights(px, band, g) -- asserted at G2.  NO momentum lookback."""
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def elig_mask(px):
    _, above, vol20 = score(px, vol_scale=False)
    return above & (vol20 < VOLCAP)


def ew_elig(px, g):
    """EWELIG: equal weight over EVERY eligible name, de-grossed to cash when none.
    NO ranking and therefore NO momentum lookback -- the 2026-09-03 memo's Finding 2."""
    e = elig_mask(px).astype(float).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_book(px, g, k, shift_short=21):
    """938's `ranked_w1`: composite rank WITHOUT the /sqrt(vol20) term, top k at g/k.
    shift_short is the composite's 12-1 momentum short leg; 21 is the committed convention
    and the only value any verdict is read at."""
    if shift_short == 21:
        sc, above, vol20 = score(px, vol_scale=False)
    else:
        mom = px.shift(shift_short) / px.shift(252) - 1
        r6 = px / px.shift(126) - 1
        r3 = px / px.shift(63) - 1
        comp = (mom.rank(axis=1, pct=True) + r6.rank(axis=1, pct=True)
                + r3.rank(axis=1, pct=True)) / 3
        above = px > px.rolling(200).mean()
        vol20 = px.pct_change().rolling(20).std() * np.sqrt(252)
        sc = comp * (0.5 + 0.5 * above.astype(float))
    rank = sc.where(above & (vol20 < VOLCAP)).rank(axis=1, ascending=False)
    return (rank <= k).astype(float) * (g / k)


BOOKS = {                                   # name -> (fn(px, g), uses_composite_lookback)
    "TOP05":  (lambda p, g: ranked_book(p, g, 5), True),
    "TOP10":  (lambda p, g: ranked_book(p, g, 10), True),
    "TOP20":  (lambda p, g: ranked_book(p, g, 20), True),    # 938's book, the G3 anchor
    "EWELIG": (lambda p, g: ew_elig(p, g), False),
    "BAND03": (lambda p, g: band_book(p, BAND0, g), False),  # == RULES v2 at g = 0.75 (G2)
}
COMPOSITE_BOOKS = [b for b, (_, u) in BOOKS.items() if u]
LOOKBACKFREE_BOOKS = [b for b, (_, u) in BOOKS.items() if not u]


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    keep = [c for c in px.columns if c == "SPY" or c not in bad]
    return px[keep], len(bad)


# ==========================================================================================
def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 942 (cloud, 2026-09-15) -- does the CANONICAL PHASE MAXIMUM hold on the record's")
    P("OTHER committed MONTHLY and QUARTERLY books?")
    P("PROTOCOL: 10 bps carries every verdict, next-day execution, both KEEP paths, rule 8.")
    P("=" * 100)
    P()
    P("PRE-REGISTERED BARS (printed before any number of this run is read)")
    P(f"  H_UNIV   canonical is the CAGR argmax of its own family in >= {UNIV_BAR:.0%} of cells")
    P(f"  H_BOOK   TOP20 >= {UNIV_BAR:.0%} of its cells while pooled non-TOP20 < {BOOK_BAR:.0%}")
    P(f"  H_ALIAS  composite books (TOP05/10/20) >= {ALIAS_BAR:.0%} AND lookback-free books "
      f"(EWELIG, BAND03) < {BOOK_BAR:.0%}")
    P(f"  H_Q      Q-cadence rate within {Q_BAR:.0%} of the M-cadence rate (else month-end fact)")
    P("  H_G3     938's 16 of 16 (TOP20, M, U56/B136 x CORE/EXT x 0/5/10/25 bps) reproduces")
    P("  H_WF     rule 8: phase AND book chosen on 2009-2016 ALONE, 2017-2026 read ONCE")
    P()

    panels = {"U56": load_universe()}
    if not SMOKE:
        panels["B136"] = load_universe(broad=True)
        sm, ndrop = load_small()
        panels["SMALL"] = sm
        P(f"  SMALL panel: {sm.shape[1] - 1} names + SPY benchmark ({ndrop} tickers with "
          f"max_1d_move >= 1.0 dropped per data/small_meta.csv)")
    else:
        panels["B136"] = load_universe(broad=True)
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(A) GATES -- run before any number of the hypothesis is read")
    P("=" * 100)
    gk = {}
    px = panels["U56"]

    bad = 0
    for per in ("W", "M", "Q"):
        m0, _ = offset_mask(px.index, per, 0)
        bad += int((m0.values != rebalance_mask(px.index, per).values).sum())
    gk["G0"] = bad == 0
    P(f"  G0 offset_mask(.,per,0) == engine.rebalance_mask on W/M/Q  : {bad} differing rows   "
      f"{'PASS' if gk['G0'] else 'FAIL'}")

    w75 = band_book(px, BAND0, 0.75)
    g2 = float(np.abs(w75.values - rules_v2_weights(px, BAND0, 0.75).values).max())
    gk["G2"] = g2 == 0.0
    P(f"  G2 BAND03 @0.75 == rules_v2_weights (the LIVE rules)       : {g2:.3e}   "
      f"{'PASS' if gk['G2'] else 'FAIL'}")

    g1 = 0.0
    for per in ("M", "Q"):
        ctx = Ctx(px, offset_mask(px.index, per, 0)[0])
        gr, tn = ctx.run(ctx.shift(w75))
        fast = pd.Series(gr - tn * HEAD_COST / 1e4, index=px.index)
        slow = backtest(px, w75, cost_bps=HEAD_COST, freq=per)["returns"]
        j = px.index[WARM]
        g1 = max(g1, float(np.abs(slow.loc[j:].values - fast.loc[j:].values).max()))
    gk["G1"] = g1 < 1e-12
    P(f"  G1 Ctx.run == engine.backtest @10 bps, worse of M and Q    : {g1:.3e}   "
      f"{'PASS' if gk['G1'] else 'FAIL'}")

    # G4 -- the phase grid is FAIR: every phase trades the same number of times per year
    yrs = (len(px.index) - WARM) / 252.0
    grows, g4_bad = [], 0
    for per, n_ph in (("M", DOM_N), ("Q", DOQ_N)):
        for d in range(n_ph):
            m, clipped = offset_mask(px.index, per, d)
            n = int(m.values[WARM:].sum())
            rpy = n / yrs
            lo, hi = (11.5, 12.5) if per == "M" else (3.6, 4.4)
            if not (lo <= rpy <= hi):
                g4_bad += 1
            grows.append(dict(cadence=per, phase=d, reb_per_yr=rpy, clipped_periods=clipped,
                              n_rebalances=n))
    gk["G4"] = g4_bad == 0
    gdf0 = pd.DataFrame(grows)
    P(f"  G4 every phase trades 12/yr (M) or 4/yr (Q)                : {g4_bad} out-of-band "
      f"of {len(gdf0)} phases   {'PASS' if gk['G4'] else 'FAIL'}")
    for per in ("M", "Q"):
        s = gdf0[gdf0.cadence == per]
        P(f"     {per}: {len(s)} phases, reb/yr {s.reb_per_yr.min():.2f}..{s.reb_per_yr.max():.2f}"
          f", clipped periods {s.clipped_periods.min()}..{s.clipped_periods.max()}")
    dump(gdf0, "phases")

    g5 = 0.0
    for _ in range(2):
        ctx = Ctx(px, offset_mask(px.index, "M", 0)[0])
        gr, _t = ctx.run(ctx.shift(ranked_book(px, 0.75, 20)))
        g5 = max(g5, float(np.abs(gr - ctx.run(ctx.shift(ranked_book(px, 0.75, 20)))[0]).max()))
    gk["G5"] = g5 == 0.0
    P(f"  G5 determinism (TOP20 monthly canonical re-derived twice)  : {g5:.3e}   "
      f"{'PASS' if gk['G5'] else 'FAIL'}")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(B) THE PHASE GRID -- 5 books x 3 panels x 2 gross x (21 M + 63 Q) phases x 5 rungs")
    P("=" * 100)
    ROWS = []
    for pname, p in panels.items():
        idx = p.index
        spy = p["SPY"].pct_change().fillna(0.0).values[WARM:]
        oos = np.asarray(idx >= pd.Timestamp(OOS_START))[WARM:]
        is_ = np.asarray(idx <= pd.Timestamp(IS_END))[WARM:]
        ms, ms_o, ms_i = mets(spy), mets(spy[oos]), mets(spy[is_])
        # every book's weights, once per (book, gross); phases only change the MASK
        Wt = {(b, cs): BOOKS[b][0](p, g) for b in BOOKS for cs, g in CLAIM_SETS.items()}
        for per, n_ph in (("M", DOM_N), ("Q", DOQ_N)):
            for d in range(n_ph):
                ctx = Ctx(p, offset_mask(idx, per, d)[0])
                for (b, cs), W in Wt.items():
                    gr, tn = ctx.run(ctx.shift(W))
                    gr_w, tn_w = gr[WARM:], tn[WARM:]
                    for c in RUNGS:
                        r = gr_w - tn_w * c / 1e4
                        m = mets(r)
                        ROWS.append(dict(
                            panel=pname, book=b, gross=cs, cadence=per, phase=d, cost_bps=c,
                            CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                            H1=m["H1"], H2=m["H2"],
                            IS_CAGR=cagr(r[is_]), IS_Sharpe=sharpe(r[is_]),
                            OOS_CAGR=cagr(r[oos]), OOS_Sharpe=sharpe(r[oos]),
                            OOS_MaxDD=float((np.cumprod(1 + r[oos])
                                             / np.maximum.accumulate(np.cumprod(1 + r[oos]))
                                             - 1).min()),
                            OOS_H1=mets(r[oos])["H1"], OOS_H2=mets(r[oos])["H2"],
                            turn_per_yr=float(tn_w.sum() / (len(r) / 252.0)),
                            spy_CAGR=ms["CAGR"], spy_Sharpe=ms["Sharpe"], spy_MaxDD=ms["MaxDD"],
                            spy_H1=ms["H1"], spy_H2=ms["H2"],
                            spy_OOS_Sharpe=ms_o["Sharpe"], spy_IS_Sharpe=ms_i["Sharpe"]))
                del ctx
        P(f"  panel {pname} done  ({time.time() - t0:.0f}s)")
    grid = pd.DataFrame(ROWS)
    dump(grid, "grid")
    P(f"  {len(grid):,} grid rows = {len(panels)} panels x {len(BOOKS)} books x "
      f"{len(CLAIM_SETS)} gross x {DOM_N + DOQ_N} phases x {len(RUNGS)} rungs")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(C) 'CANONICAL = MAX' -- the object under test, one cell per family")
    P("=" * 100)
    CELLS = []
    keys = ["panel", "book", "gross", "cadence", "cost_bps"]
    for k, sub in grid.groupby(keys, sort=False):
        sub = sub.sort_values("phase")
        n = len(sub)
        canon = sub[sub.phase == 0].iloc[0]
        for stat in ("CAGR", "Sharpe"):
            v = sub[stat].values
            rank = float((v <= canon[stat]).sum() / n)
            CELLS.append(dict(zip(keys, k)) | dict(
                stat=stat, n_phases=n, canon=canon[stat], fam_min=float(np.nanmin(v)),
                fam_med=float(np.nanmedian(v)), fam_max=float(np.nanmax(v)),
                spread=float(np.nanmax(v) - np.nanmin(v)),
                argmax_phase=int(sub.phase.values[int(np.nanargmax(v))]),
                canon_pctile=rank, canon_is_max=bool(rank >= 1.0)))
    cells = pd.DataFrame(CELLS)
    dump(cells, "cells")
    cg = cells[cells.stat == "CAGR"]

    # ---- H_G3: reproduce 938's 16 of 16 exactly --------------------------------------------
    g3 = cg[(cg.book == "TOP20") & (cg.cadence == "M") & (cg.panel.isin(["U56", "B136"]))
            & (cg.cost_bps.isin(G3_RUNGS))]
    n_g3 = int(g3.canon_is_max.sum())
    gk["G3"] = (len(g3) == 16) and (n_g3 == 16)
    P(f"  G3 938's published 16 of 16 (TOP20/M, U56+B136 x CORE/EXT x 0/5/10/25 bps): "
      f"{n_g3} of {len(g3)} canon_pctile == 1.000   {'PASS' if gk['G3'] else 'FAIL'}")
    if n_g3 != len(g3):
        for _, r in g3[~g3.canon_is_max].iterrows():
            P(f"     MISS {r.panel}/{r.gross}/{r.cost_bps:.0f}bps  canon {r.canon:.4f} "
              f"pctile {r.canon_pctile:.3f} argmax phase {r.argmax_phase}")
    P(f"  GATES {sum(1 for v in gk.values() if v)} of {len(gk)} PASS  "
      f"({', '.join(k for k, v in gk.items() if not v) or 'none failing'})")
    P()

    # ---- the tallies -----------------------------------------------------------------------
    P("  canonical-is-CAGR-max rate, by BOOK x CADENCE (pooled over panel x gross x rung):")
    tab = (cg.groupby(["book", "cadence"]).canon_is_max.agg(["mean", "sum", "count"])
           .rename(columns={"mean": "rate", "sum": "n_max", "count": "n_cells"}).reset_index())
    piv = tab.pivot(index="book", columns="cadence", values="rate")
    P(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    dump(tab, "bookrate")
    P()
    P("  same, by BOOK x PANEL at the verdict rung (10 bps), M cadence:")
    h = cg[(cg.cost_bps == HEAD_COST) & (cg.cadence == "M")]
    P(h.pivot_table(index="book", columns="panel", values="canon_is_max", aggfunc="mean")
      .to_string(float_format=lambda x: f"{x:.3f}"))
    P()
    P("  the families themselves at 10 bps / CORE / M -- canonical against its own spread:")
    v = cg[(cg.cost_bps == HEAD_COST) & (cg.gross == "CORE") & (cg.cadence == "M")]
    P(v[["panel", "book", "canon", "fam_min", "fam_med", "fam_max", "spread",
         "argmax_phase", "canon_pctile"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P()
    P("  and at 10 bps / CORE / Q (63 phases):")
    vq = cg[(cg.cost_bps == HEAD_COST) & (cg.gross == "CORE") & (cg.cadence == "Q")]
    P(vq[["panel", "book", "canon", "fam_min", "fam_med", "fam_max", "spread",
          "argmax_phase", "canon_pctile"]]
      .to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    P()

    r_all = float(cg.canon_is_max.mean())
    r_top20 = float(cg[cg.book == "TOP20"].canon_is_max.mean())
    r_non = float(cg[cg.book != "TOP20"].canon_is_max.mean())
    r_comp = float(cg[cg.book.isin(COMPOSITE_BOOKS)].canon_is_max.mean())
    r_free = float(cg[cg.book.isin(LOOKBACKFREE_BOOKS)].canon_is_max.mean())
    r_m = float(cg[cg.cadence == "M"].canon_is_max.mean())
    r_q = float(cg[cg.cadence == "Q"].canon_is_max.mean())
    P(f"  pooled rates over {len(cg)} (book, panel, gross, cadence, rung) cells:")
    P(f"     ALL {r_all:.3f} · TOP20 {r_top20:.3f} · non-TOP20 {r_non:.3f}")
    P(f"     composite books (TOP05/10/20) {r_comp:.3f} · lookback-free (EWELIG, BAND03) "
      f"{r_free:.3f}")
    P(f"     M cadence {r_m:.3f} · Q cadence {r_q:.3f}   (gap {abs(r_m - r_q):.3f})")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(D) THE LOOKBACK PROBE -- REPORTED, never selected on")
    P("=" * 100)
    P("  If 'canonical = max' is the 21-day momentum leg aliasing onto the month boundary, the")
    P("  argmax phase should MOVE when the short leg moves off 21 trading days.")
    LB = []
    pl = panels["U56"]
    idxl = pl.index
    for sh in LOOKBACKS:
        W = ranked_book(pl, 0.75, 20, shift_short=sh)
        vals = []
        for d in range(DOM_N):
            ctx = Ctx(pl, offset_mask(idxl, "M", d)[0])
            gr, tn = ctx.run(ctx.shift(W))
            vals.append(cagr((gr - tn * HEAD_COST / 1e4)[WARM:]))
            del ctx
        vals = np.array(vals)
        LB.append(dict(shift_short=sh, canon_CAGR=vals[0], fam_max=float(vals.max()),
                       argmax_phase=int(vals.argmax()),
                       canon_pctile=float((vals <= vals[0]).sum() / len(vals)),
                       canon_is_max=bool(vals.argmax() == 0),
                       spread_pp=float((vals.max() - vals.min()) * 100)))
    lbdf = pd.DataFrame(LB)
    P(lbdf.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    dump(lbdf, "lookback")
    n_lb = int(lbdf.canon_is_max.sum())
    P(f"  canonical stays the argmax at {n_lb} of {len(lbdf)} lookbacks (U56/TOP20/CORE/M/10bps)."
      f"  {'The argmax does NOT track the lookback.' if n_lb == len(lbdf) else 'The argmax MOVES with the lookback.'}")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(E) RULE 8 WALK-FORWARD -- phase AND book chosen on 2009-2016 ALONE, 2017-2026 ONCE")
    P("=" * 100)
    WF = []
    hg = grid[(grid.cost_bps == HEAD_COST) & (grid.gross == "CORE")]
    for pname, p in panels.items():
        bw = rules_v2_weights(p, BAND0, 0.75)
        bctx = Ctx(p, offset_mask(p.index, "W", 0)[0])
        bg, bt = bctx.run(bctx.shift(bw))
        br = (bg - bt * HEAD_COST / 1e4)[WARM:]
        oos = np.asarray(p.index >= pd.Timestamp(OOS_START))[WARM:]
        mb_o = mets(br[oos])
        for cad in ("M", "Q"):
            s = hg[(hg.panel == pname) & (hg.cadence == cad)]
            for rule, pick in (
                    ("IS_CAGR_max", s.loc[s.IS_CAGR.idxmax()]),
                    ("IS_Sharpe_max", s.loc[s.IS_Sharpe.idxmax()]),
                    ("CANONICAL_phase0_bestISbook",
                     s[s.phase == 0].loc[s[s.phase == 0].IS_Sharpe.idxmax()])):
                lg = dict(H1=pick.H1 > pick.spy_H1, H2=pick.H2 > pick.spy_H2,
                          OOS=pick.OOS_Sharpe > pick.spy_OOS_Sharpe,
                          DD=abs(pick.OOS_MaxDD) <= 0.60 * abs(pick.spy_MaxDD),
                          CAGR=pick.OOS_CAGR >= 0.70 * pick.spy_CAGR)
                WF.append(dict(
                    panel=pname, cadence=cad, rule=rule,
                    picked=f"{pick.book}/ph{int(pick.phase):02d}",
                    IS_CAGR=pick.IS_CAGR, IS_Sharpe=pick.IS_Sharpe,
                    OOS_CAGR=pick.OOS_CAGR, OOS_Sharpe=pick.OOS_Sharpe,
                    OOS_MaxDD=pick.OOS_MaxDD,
                    spy_CAGR=pick.spy_CAGR, spy_OOS_Sharpe=pick.spy_OOS_Sharpe,
                    spy_MaxDD=pick.spy_MaxDD, base_OOS_Sharpe=mb_o["Sharpe"],
                    base_OOS_MaxDD=mb_o["MaxDD"], base_OOS_H1=mb_o["H1"],
                    base_OOS_H2=mb_o["H2"],
                    OOS_pass4a=bool(pick.OOS_H1 > mb_o["H1"] and pick.OOS_H2 > mb_o["H2"]
                                    and pick.OOS_MaxDD >= mb_o["MaxDD"]),
                    OOS_pass4b=all(lg.values()), OOS_fail4b=failstr(lg)))
        del bctx
    wdf = pd.DataFrame(WF)
    P(wdf[["panel", "cadence", "rule", "picked", "IS_CAGR", "IS_Sharpe", "OOS_CAGR",
           "OOS_Sharpe", "OOS_MaxDD", "spy_CAGR", "spy_OOS_Sharpe", "base_OOS_Sharpe",
           "OOS_pass4a", "OOS_pass4b", "OOS_fail4b"]]
      .to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    dump(wdf, "walkforward")
    P(f"  rule-8 OOS 4b PASS {int(wdf.OOS_pass4b.sum())} of {len(wdf)}; "
      f"4a PASS {int(wdf.OOS_pass4a.sum())} of {len(wdf)}.")
    n_ph0 = int((wdf.rule.isin(["IS_CAGR_max", "IS_Sharpe_max"]))
                .mul(wdf.picked.str.endswith("ph00")).sum())
    n_ch = int(wdf.rule.isin(["IS_CAGR_max", "IS_Sharpe_max"]).sum())
    P(f"  the IS choosers land on the CANONICAL phase in {n_ph0} of {n_ch} (panel, cadence, "
      f"chooser) cells -- the in-sample maximum is not the canonical one in the rest.")
    P()

    # --------------------------------------------------------------------------------------
    P("=" * 100)
    P("(F) VERDICT")
    P("=" * 100)
    h_univ = r_all >= UNIV_BAR
    h_book = (r_top20 >= UNIV_BAR) and (r_non < BOOK_BAR)
    h_alias = (r_comp >= ALIAS_BAR) and (r_free < BOOK_BAR)
    h_q = abs(r_m - r_q) <= Q_BAR
    hyp = [("H_UNIV", h_univ, f"pooled canonical-is-max rate {r_all:.3f} over {len(cg)} cells"),
           ("H_BOOK", h_book, f"TOP20 {r_top20:.3f} vs non-TOP20 {r_non:.3f}"),
           ("H_ALIAS", h_alias, f"composite {r_comp:.3f} vs lookback-free {r_free:.3f}; "
                                f"argmax stays canonical at {n_lb} of {len(lbdf)} lookbacks"),
           ("H_Q", h_q, f"M {r_m:.3f} vs Q {r_q:.3f}, gap {abs(r_m - r_q):.3f}"),
           ("H_G3", gk["G3"], f"938's 16 of 16 replayed: {n_g3} of {len(g3)}"),
           ("H_WF", True, f"rule 8 on {len(wdf)} cells; OOS 4b {int(wdf.OOS_pass4b.sum())}, "
                          f"4a {int(wdf.OOS_pass4a.sum())}")]
    hdf = pd.DataFrame([dict(hypothesis=h, supported=bool(v), evidence=e) for h, v, e in hyp])
    P(hdf.to_string(index=False))
    dump(hdf, "hypotheses")
    P()
    P(f"  done in {time.time() - t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES) + "\n")
    return grid, cells, wdf


if __name__ == "__main__":
    main()
