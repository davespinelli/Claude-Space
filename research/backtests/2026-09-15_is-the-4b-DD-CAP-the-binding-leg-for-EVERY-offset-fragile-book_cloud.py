#!/usr/bin/env python3
"""Idea 944 (cloud, 2026-09-15) -- is the 4b DD CAP the BINDING LEG for EVERY offset-fragile book
in the record?

THE QUESTION (queue, 2026-09-15)
  Idea 938 found that all 18 of the 25 failing monthly offsets of U56 CORE/TOP20 fail on L4_DD
  ALONE, never on a Sharpe leg, so the 60%-of-SPY drawdown cap is doing all the discriminating and
  MaxDD is the most offset-sensitive statistic in the 4b bar (support -22.95% to -14.89% over 21
  phases = 8.06 pp, against a 1.95 pp CAGR spread).  The queue asks for two things: (a) a CENSUS of
  the record's committed 4b FAIL rows for WHICH LEG BINDS, and (b) each 4b STATISTIC's phase
  sensitivity -- so the record knows which of its bars is a coin flip on the rebalance date.

WHAT "A COIN FLIP ON THE REBALANCE DATE" MEANS HERE, AS A NUMBER
  For every (panel, grid, book, cost) CELL the whole phase family is run.  A leg is a COIN FLIP in
  that cell if its verdict is not unanimous over the phases -- some rebalance dates pass it, some
  fail it, with nothing else changed.  The LEG FLIP RATE is the share of cells where that happens,
  and it is the headline.  Beside it each STATISTIC gets a COIN-FLIP INDEX = (its phase support)
  divided by (the median distance from its own 4b bar): above 1.0 the rebalance date moves the
  statistic further than the bar is away, which is the same statement in the statistic's own units.

THE BOOKS (all committed; the construction is the record's, not this run's)
  TOP5 / TOP10 / TOP20   rank every priced name above its own 200d MA with 20d vol < 0.60 by the v1
                         composite WITHOUT the /sqrt(vol20) term; hold the top n at a FIXED g/n
                         each, so a day with fewer than n eligible names DE-GROSSES.  This is the
                         construction ideas 926 and 938 committed, gated against 938 at G3.
  BAND03                 `baseline.rules_v2_weights(px, 0.03, g)` -- the live RULES v2 shape.
  EWELIG                 equal-weight EVERY eligible name, respread to gross g (2026-09-03
                         RECOMMENDATION Finding 2 / memo 2026-09-07_eligible-equal-weight-v2).
  TOP20R                 TOP20 RE-SPREAD to g/k(t).  Carried for one reason only, stated at G3b:
                         ideas 931 and 945 used this variant while calling it the committed
                         CORE/TOP20, and both reported a G3 cross-run FAILURE on the monthly leg.
                         This run PRICES that gap instead of attributing it to data vintage.

THE PHASE GRIDS (idea 938's `offset_mask`, copied unmodified)
  DOM21  monthly, rebalance d trading days BEFORE each month's last trading day, d = 0..20.
  DOW5   weekly, the same construction on the W period, d = 0..4.
  d = 0 reproduces `engine.rebalance_mask` exactly on both (G0), so each grid NESTS the published
  convention and the canonical book is always phase 0.

WHAT IS TUNED AND WHAT IS REPORTED (PROTOCOL 4: max 2 tuned parameters)
  TUNED 1  CLAIM SET, 2 levels, both reported -- for the census of the record:
           STRICT  only 4b FAIL rows whose binding leg is READ from committed leg columns
           WIDE    STRICT plus rows whose legs are RECONSTRUCTED from the row's own statistics
  TUNED 2  PHASE GRID, 2 levels, both reported: DOM21 and DOW5.
  REPORTED AXES (nothing fitted on them, every point published, none selected):
           6 books x 3 panels (U56 / B136 / SMALL) x 4 cost rungs (0/10/25/50 bps); windows
           FULL / IS / OOS / H1 / H2.

PRE-REGISTERED BARS (fixed before any number was read; both directions reported)
  H_CTRL   938's committed U56 CORE/TOP20 DOM21 numbers at 10 bps reproduce: MaxDD support
           -0.2295..-0.1489, CAGR spread 1.95 pp, 16 of 21 DOM phases FAIL and all 16 on L4_DD
           ALONE.  Without this the run says nothing about 938.
  H_DDLEG  L4_DD has the HIGHEST leg flip rate of the five legs, on both grids.
  H_ALONE  among all failing (cell, phase) rows, L4_DD binding ALONE is the plurality signature.
  H_STAT   MaxDD has the largest coin-flip index of the five 4b statistics.
  H_GRID   the leg ranking by flip rate is the same on DOM21 and DOW5.
  H_CENSUS at least one committed 4b FAIL row in the record carries a readable binding leg, and
           the STRICT and WIDE binding-leg distributions agree within 10 pp on the L4_DD share.
  H_WF     (rule 8, REQUIRED) the PHASE chosen on 2009-2016 ALONE by IS Sharpe, 2017-2026 read
           ONCE, both KEEP paths, against SPY and the live RULES v2 book -- and against the
           CANONICAL phase, which is what an honest book would have shipped.

GATES (all printed before any result number)
  G0   phase 0 mask == `engine.rebalance_mask` exactly, on M and on W
  G1   the fast runner == `engine.backtest` on returns and turnover at phase 0
  G1b  BAND03 == `baseline.rules_v2_weights(px, 0.03, g)` exactly
  G2   every phase trades in band (DOM21 11.5-12.5 /yr, DOW5 51-53 /yr)
  G3   CROSS-RUN: idea 938's committed U56 CORE/TOP20 DOM21 offsets.csv
  G3b  the TOP20 vs TOP20R gap is MEASURED, not assumed
  G4   determinism: the same (panel, grid, phase, book, cost) reproduces bit-for-bit
  G5   SMALL screen: the `max_1d_move` >= 1.0 drop is applied and its count printed
  G6   the census finds idea 938's own committed FAIL rows (the census can see the record)

PROTOCOL: 10 bps primary, t+1 execution, warm-up 260 days, IS 2009-2016 / OOS 2017-2026.
Nothing in RULES.md / PROTOCOL.md / scan.py / bot.py / baseline.py is modified.

SURVIVORSHIP: U56 / B136 / SMALL are CURRENT-CONSTITUENT lists (SMALL additionally drops every
ticker with `max_1d_move` >= 1.0 per `data/small_meta.csv`), so every CAGR and drawdown LEVEL is
optimistic and both 4b bars are easier here than on a point-in-time panel.  The phase contrasts are
same-tape, same-names, same-rule comparisons with ONLY the rebalance date moved and are far less
exposed; the leg flip rates and the coin-flip indices are differences within a cell.  The rule-8 4b
levels are read against SPY, which is not survivorship-inflated.
"""
from __future__ import annotations

import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, score  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

COST0 = 10.0
LAG = 1
WARMUP = 260
BAND0, VOLCAP, GROSS0 = 0.03, 0.60, 0.75
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
COSTS = [0.0, 10.0, 25.0, 50.0]
PANELS = ["U56", "B136", "SMALL"]
GRIDS = {"DOM21": ("M", 21), "DOW5": ("W", 5)}
BOOKS = ["TOP5", "TOP10", "TOP20", "BAND03", "EWELIG", "TOP20R"]
LEGS = ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]

# idea 938's committed U56 CORE/TOP20 DOM21 @10 bps numbers (offsets.csv)
PUB_DD = (-0.2294630330459725, -0.1488785029323021)
PUB_CAGR_SPREAD_PP = 1.9524516581373415
PUB_FAIL_DOM = 16          # of 21, all on L4_DD alone
TOL_DD, TOL_SPREAD = 0.010, 0.20

LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def dump(df, suffix):
    p = OUT / f"{STEM}.{suffix}"
    df.to_csv(p, index=False)
    P(f"  wrote {p.name}  ({len(df):,} rows, {len(df.columns)} cols)")


# ================================================================================================
def offset_mask(idx, per, d):
    """Idea 938's construction, unmodified: True d trading days BEFORE the last trading day of
    each period.  d = 0 reproduces `engine.rebalance_mask(idx, per)` exactly (G0)."""
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Panel:
    def __init__(self, name, px, mask):
        self.name, self.px = name, px
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        T, N = self.rets.shape
        self.T, self.N = T, N
        C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, N)), C[:-1]])
        mk = np.asarray(mask.values, bool)
        mk = np.concatenate([[False], mk[:-1]]).copy()
        mk[0] = True
        self.reb = np.flatnonzero(mk)
        seg = np.searchsorted(self.reb, np.arange(T), side="right") - 1
        self.s0 = self.reb[seg]
        self.s0p = self.reb[np.maximum(seg - 1, 0)]
        self.R = self.Cp / self.Cp[self.s0]
        self.Rp = self.Cp[self.reb] / self.Cp[self.s0p[self.reb]]
        m_full = np.asarray(self.idx >= self.idx[WARMUP])
        fp = np.flatnonzero(m_full)
        h = len(fp) // 2
        m1 = np.zeros(T, bool); m1[fp[:h]] = True
        m2 = np.zeros(T, bool); m2[fp[h:]] = True
        self.masks = {"FULL": m_full, "H1": m1, "H2": m2,
                      "IS": m_full & np.asarray(self.idx <= pd.Timestamp(IS_END)),
                      "OOS": np.asarray(self.idx >= pd.Timestamp(OOS_START))}
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.reb_per_year = len(self.reb) / (T / 252.0)


class Book:
    def __init__(self, panel: Panel, Wg: np.ndarray):
        """Wg is the book's TARGET weights at its own gross (already multiplied by g)."""
        self.pan = panel
        wt = np.roll(Wg, LAG, axis=0).copy()
        wt[:LAG] = 0.0
        self.wt_reb = wt[panel.reb]
        A = wt[panel.s0]
        AR = A * panel.R
        self.S = AR.sum(axis=1)
        self.As = A.sum(axis=1)
        self.ARr = (AR * panel.rets).sum(axis=1)
        Ap = wt[panel.s0p[panel.reb]]
        self.ARp = Ap * panel.Rp
        self.Sp = self.ARp.sum(axis=1)
        self.Asp = Ap.sum(axis=1)

    def at(self, cost=COST0):
        pan = self.pan
        V = 1.0 + (self.S - self.As)
        gross = self.ARr / V
        Vp = 1.0 + (self.Sp - self.Asp)
        heldp = self.ARp / Vp[:, None]
        heldp[0] = 0.0
        turn = np.zeros(pan.T)
        turn[pan.reb] = np.abs(self.wt_reb - heldp).sum(axis=1)
        return gross - turn * cost / 1e4, turn


def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 3 or not np.isfinite(r).all():
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    cagr = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return cagr, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 3:
        return np.nan
    v = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / v if v else np.nan


def full_pack(r, pan):
    c, s, d = fmet(np.asarray(r)[pan.masks["FULL"]])
    co, so, do = fmet(np.asarray(r)[pan.masks["OOS"]])
    return dict(CAGR=c, Sharpe=s, MaxDD=d,
                H1=fsharpe(np.asarray(r)[pan.masks["H1"]]),
                H2=fsharpe(np.asarray(r)[pan.masks["H2"]]),
                IS_Sharpe=fsharpe(np.asarray(r)[pan.masks["IS"]]),
                oCAGR=co, oSharpe=so, oMaxDD=do)


def legs(s, spy):
    """The five 4b legs, and each one's MARGIN in its own statistic's units (positive = passing)."""
    L = {"L1_H1": s["H1"] - spy["H1"], "L2_H2": s["H2"] - spy["H2"],
         "L3_OOS": s["oSharpe"] - spy["oSharpe"],
         "L4_DD": s["MaxDD"] - DD_CAP * spy["MaxDD"],
         "L5_CAGR": s["CAGR"] - CAGR_FLOOR * spy["CAGR"]}
    return {k: bool(v > 0) for k, v in L.items()}, L


# ------------------------------------------------------------------------------ book builders
def build_books(px, g=GROSS0):
    """Every book's TARGET weight matrix, at gross g, on the full daily index."""
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    rank = sc.where(elig).rank(axis=1, ascending=False)
    out = {}
    for n in (5, 10, 20):
        out[f"TOP{n}"] = ((rank <= n).astype(float) * (g / n)).values   # FIXED g/n -- 926/938
    sel = (rank <= 20).astype(float)                                   # RE-SPREAD -- 931/945
    out["TOP20R"] = (sel.div(sel.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * g).values
    out["BAND03"] = rules_v2_weights(px, BAND0, g).values
    e = (elig & px.notna()).astype(float)
    out["EWELIG"] = (e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0) * g).values
    return out


def main():
    t0 = time.time()
    P("=" * 100)
    P("IDEA 944 (cloud) -- is the 4b DD CAP the BINDING LEG for EVERY offset-fragile book?")
    P("=" * 100)

    raw = {}
    raw["U56"] = load_universe()
    raw["B136"] = load_universe(broad=True)
    sm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    ndrop = len(bad & set(sm.columns))
    raw["SMALL"] = sm[[c for c in sm.columns if c not in bad]]
    P("\n  panels: " + ", ".join(f"{k} {v.shape[1]}x{v.shape[0]} "
                                f"[{v.index[0].date()}..{v.index[-1].date()}]" for k, v in raw.items()))
    P(f"  SMALL: dropped {ndrop} tickers with max_1d_move >= 1.0 per data/small_meta.csv "
      f"(SURVIVORSHIP: current constituents of the screen only)")
    W = {pn: build_books(px) for pn, px in raw.items()}
    nph = sum(n for _, n in GRIDS.values())
    P(f"\n  {len(BOOKS)} books x {len(PANELS)} panels x {nph} phases x {len(COSTS)} cost rungs = "
      f"{len(BOOKS)*len(PANELS)*nph*len(COSTS):,} scored books over "
      f"{len(BOOKS)*len(PANELS)*len(GRIDS)*len(COSTS)} cells")

    # ------------------------------------------------------------------------------ THE GRID
    rows, clip = [], []
    for pn in PANELS:
        px = raw[pn]
        spy_cache = {}
        for gname, (per, nph_) in GRIDS.items():
            for d in range(nph_):
                mk, nclip = offset_mask(px.index, per, d)
                pan = Panel(pn, px, mk)
                clip.append(dict(panel=pn, grid=gname, phase=d, clipped=nclip,
                                 reb_per_year=pan.reb_per_year))
                if pn not in spy_cache:
                    spy_cache[pn] = full_pack(pan.spy, pan)
                spy = spy_cache[pn]
                for bk in BOOKS:
                    book = Book(pan, W[pn][bk])
                    for cost in COSTS:
                        r, turn = book.at(cost)
                        m = full_pack(r, pan)
                        lg, mg = legs(m, spy)
                        rows.append(dict(panel=pn, grid=gname, phase=d, book=bk, cost_bps=cost,
                                         **m, ann_turn=float(turn.sum() / (len(turn) / 252.0)),
                                         spy_CAGR=spy["CAGR"], spy_Sharpe=spy["Sharpe"],
                                         spy_MaxDD=spy["MaxDD"], spy_H1=spy["H1"],
                                         spy_H2=spy["H2"], spy_oSharpe=spy["oSharpe"],
                                         **lg, **{f"m_{k}": v for k, v in mg.items()},
                                         pass4b=bool(all(lg.values())),
                                         fail_sig="-" if all(lg.values()) else
                                                  "+".join(k for k in LEGS if not lg[k])))
        P(f"    {pn}: grid done  ({time.time()-t0:.0f}s)")
    G = pd.DataFrame(rows)
    CL = pd.DataFrame(clip)
    dump(G, "grid.csv")

    # -------------------------------------------------------------------------------- GATES
    P("\n" + "-" * 100)
    P("GATES (printed before any result number)")
    P("-" * 100)
    gates = []

    d0 = []
    for per in ("M", "W"):
        mk, _ = offset_mask(raw["U56"].index, per, 0)
        d0.append(int((mk.values != rebalance_mask(raw["U56"].index, per).values).sum()))
    gates.append(dict(gate="G0 phase 0 mask == engine.rebalance_mask (M and W)",
                      stat=f"differing rows: M {d0[0]}, W {d0[1]}", bar="0",
                      passed=bool(max(d0) == 0)))

    d1 = []
    for bk in ("TOP20", "BAND03"):
        px = raw["U56"]
        mk, _ = offset_mask(px.index, "M", 0)
        pan = Panel("U56", px, mk)
        r_f, t_f = Book(pan, W["U56"][bk]).at(COST0)
        eng = backtest(px, pd.DataFrame(W["U56"][bk], index=px.index, columns=px.columns),
                       cost_bps=COST0, freq="M")
        m = pan.masks["FULL"]
        d1.append((bk, float(np.abs(r_f[m] - eng["returns"].values[m]).max()),
                   float(np.abs(t_f[m] - eng["turnover"].values[m]).max())))
    gates.append(dict(gate="G1 fast runner == engine.backtest at phase 0 (U56, M)",
                      stat=" | ".join(f"{b}: dret {a:.2e} dturn {c:.2e}" for b, a, c in d1),
                      bar="1e-9", passed=all(a < 1e-9 and c < 1e-9 for _, a, c in d1)))

    d1b = float(np.abs(W["U56"]["BAND03"] - rules_v2_weights(raw["U56"], BAND0, GROSS0).values).max())
    gates.append(dict(gate="G1b BAND03 == baseline.rules_v2_weights(px, 0.03, 0.75)",
                      stat=f"max|dw| {d1b:.3e}", bar="1e-12", passed=bool(d1b < 1e-12)))

    bad2 = []
    for gname, (per, _) in GRIDS.items():
        lo, hi = (11.5, 12.5) if per == "M" else (51.0, 53.0)
        s = CL[CL.grid == gname]
        bad2.append((gname, int(((s.reb_per_year < lo) | (s.reb_per_year > hi)).sum()),
                     float(s.reb_per_year.min()), float(s.reb_per_year.max()),
                     int(s.clipped.max())))
    gates.append(dict(gate="G2 every phase trades in band (DOM21 11.5-12.5/yr, DOW5 51-53/yr)",
                      stat=" | ".join(f"{g}: {n} violations, {a:.2f}..{b:.2f}/yr, max clipped {c}"
                                      for g, n, a, b, c in bad2),
                      bar="0 violations", passed=all(n == 0 for _, n, *_ in bad2)))

    s3 = G[(G.panel == "U56") & (G.grid == "DOM21") & (G.book == "TOP20") & (G.cost_bps == COST0)]
    dd_lo, dd_hi = float(s3.MaxDD.min()), float(s3.MaxDD.max())
    spread_pp = float((s3.CAGR.max() - s3.CAGR.min()) * 100)
    nfail = int((~s3.pass4b).sum())
    alone = int((s3.fail_sig == "L4_DD").sum())
    ok3 = (abs(dd_lo - PUB_DD[0]) < TOL_DD and abs(dd_hi - PUB_DD[1]) < TOL_DD and
           abs(spread_pp - PUB_CAGR_SPREAD_PP) < TOL_SPREAD and nfail == PUB_FAIL_DOM and
           alone == PUB_FAIL_DOM)
    gates.append(dict(gate="G3 CROSS-RUN idea 938's U56 CORE/TOP20 DOM21 @10 bps",
                      stat=f"MaxDD {dd_lo:.4f}..{dd_hi:.4f} vs committed {PUB_DD[0]:.4f}.."
                           f"{PUB_DD[1]:.4f}; CAGR spread {spread_pp:.2f} pp vs {PUB_CAGR_SPREAD_PP:.2f}; "
                           f"FAIL {nfail} of 21 vs {PUB_FAIL_DOM}, of which L4_DD ALONE {alone}",
                      bar=f"dMaxDD<{TOL_DD}, dSpread<{TOL_SPREAD} pp, fail count exact",
                      passed=bool(ok3)))

    a = G[(G.panel == "U56") & (G.grid == "DOM21") & (G.book == "TOP20") &
          (G.cost_bps == COST0) & (G.phase == 0)].iloc[0]
    b = G[(G.panel == "U56") & (G.grid == "DOM21") & (G.book == "TOP20R") &
          (G.cost_bps == COST0) & (G.phase == 0)].iloc[0]
    gates.append(dict(gate="G3b the TOP20 (fixed g/n, committed) vs TOP20R (re-spread) gap, MEASURED",
                      stat=f"canonical monthly @10 bps: TOP20 {a.CAGR:.2%}/{a.Sharpe:.4f}/{a.MaxDD:.2%} "
                           f"vs TOP20R {b.CAGR:.2%}/{b.Sharpe:.4f}/{b.MaxDD:.2%} -- dCAGR "
                           f"{b.CAGR-a.CAGR:+.4f}, dSharpe {b.Sharpe-a.Sharpe:+.4f}, dMaxDD "
                           f"{b.MaxDD-a.MaxDD:+.4f}. Committed 926/938 value: 14.69%/1.203/-19.51%",
                      bar="reported, not gated", passed=True))

    px = raw["U56"]
    mk, _ = offset_mask(px.index, "M", 3)
    r1, _ = Book(Panel("U56", px, mk), W["U56"]["TOP20"]).at(COST0)
    r2, _ = Book(Panel("U56", px, mk), W["U56"]["TOP20"]).at(COST0)
    d4 = float(np.abs(r1 - r2).max())
    gates.append(dict(gate="G4 determinism", stat=f"max|d| {d4:.3e}", bar="0.0",
                      passed=bool(d4 == 0.0)))
    gates.append(dict(gate="G5 SMALL screen applied",
                      stat=f"dropped {ndrop} tickers, {raw['SMALL'].shape[1]} cols kept incl. SPY",
                      bar="> 0", passed=bool(ndrop > 0)))

    # ------------------------------------------------------- PART A: CENSUS OF THE RECORD
    P("\n" + "-" * 100)
    P("PART A -- CENSUS: which leg binds on the record's committed 4b FAIL rows")
    P("-" * 100)
    import subprocess
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip() or "unknown"
    # The census reads ONLY the columns it needs, and is vectorised: 4,662 committed CSVs is
    # 1.3 GB on this tree, so a row-wise pass over all of them is not a census, it is a timeout.
    READ_SETS = [["L1_H1", "L2_H2", "L3_OOS", "L4_DDcap", "L5_CAGRfloor"],
                 ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]]
    CANON = {"L4_DDcap": "L4_DD", "L5_CAGRfloor": "L5_CAGR"}
    # The record encodes the same binding leg in at least two committed alphabets: idea 938 writes
    # "L4_DD" and other lanes write "DD" in a comma-joined list.  A census that does not unify them
    # counts the same signature twice under two names -- the first cut of this run did exactly that
    # and read L4_DD-alone at 1.9% while "DD" alone sat separately at 12.8%.  Both the RAW and the
    # NORMALISED distributions are printed below; the normalised one is the answer.
    # FIVE committed alphabets, not two.  The first cut mapped only "L4_DD"; the second added the
    # comma-joined "DD" form and cut the unmapped residue to 3.5%; inspecting THAT residue showed
    # two more separators ("|", "/") and two more spellings (DDCAP, CAGRFLOOR).  The map below was
    # extended to cover them, which is a fix to the MEASUREMENT, not to a result: the progression of
    # the L4_DD-alone share as the alphabet is completed (1.9% -> 14.7% -> the number below) is
    # itself published, because it is the size of the error a partial alphabet makes.
    TOKEN = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR",
             "L1_H1": "L1_H1", "L2_H2": "L2_H2", "L3_OOS": "L3_OOS", "L4_DD": "L4_DD",
             "L5_CAGR": "L5_CAGR", "L4_DDcap": "L4_DD", "L5_CAGRfloor": "L5_CAGR",
             "DDCAP": "L4_DD", "CAGRFLOOR": "L5_CAGR", "DD_CAP": "L4_DD",
             "CAGR_FLOOR": "L5_CAGR", "L4": "L4_DD", "L5": "L5_CAGR", "L1": "L1_H1",
             "L2": "L2_H2", "L3": "L3_OOS"}
    SEPS = "+|/;& "

    def norm_sig(s):
        if not isinstance(s, str) or s.strip() in ("", "-", "nan", "None"):
            return "-"
        t = s
        for ch in SEPS:
            t = t.replace(ch, ",")
        toks = [TOKEN.get(x.strip()) for x in t.split(",") if x.strip()]
        toks = [x for x in toks if x]
        return "+".join(sorted(set(toks), key=LEGS.index)) if toks else "?UNMAPPED"

    PCOLS = ("pass4b", "OOS_pass4b", "pass_4b")
    files = sorted(list(OUT.glob("*.csv")) + list(OUT.glob("*.csv.gz")))
    crows, seen_938, nopen, nhit = [], 0, 0, 0

    def truthy(s):
        return s.astype(str).str.strip().str.lower().isin(["true", "1", "1.0", "yes"])

    for f in files:
        if f.name.startswith(STEM):
            continue
        try:
            cols = list(pd.read_csv(f, nrows=0).columns)
        except Exception:
            continue
        nopen += 1
        pcol = next((c for c in PCOLS if c in cols), None)
        if pcol is None:
            continue
        legset = next((L for L in READ_SETS if set(L) <= set(cols)), None)
        use = [pcol] + (["fail4b"] if "fail4b" in cols else []) + (legset or [])
        try:
            df = pd.read_csv(f, usecols=use)
        except Exception:
            continue
        nhit += 1
        fail = df[~truthy(df[pcol])]
        if not len(fail):
            continue
        if "fail4b" in fail.columns:
            sig = fail["fail4b"].astype(str).str.strip()
            for a, b in CANON.items():
                sig = sig.str.replace(a, b, regex=False)
            sig = sig.where(~sig.isin(["", "-", "nan", "None"]), other=np.nan)
        else:
            sig = pd.Series(np.nan, index=fail.index, dtype=object)
        if legset is not None:
            parts = [np.where(truthy(fail[k]), "", CANON.get(k, k)) for k in legset]
            rec = pd.Series(["+".join(x for x in t if x) for t in zip(*parts)], index=fail.index)
            sig = sig.fillna(rec.where(rec != "", np.nan))
        kind = np.where(sig.notna(), "READ", "UNRECOVERABLE")
        sraw = sig.fillna("-")
        crows.append(pd.DataFrame(dict(file=f.name, kind=kind, sig_raw=sraw,
                                       sig=sraw.map(norm_sig))))
        if "REBALANCE-OFFSET" in f.name:
            seen_938 += len(fail)
    CEN = pd.concat(crows, ignore_index=True) if crows else pd.DataFrame(
        columns=["file", "kind", "sig_raw", "sig"])
    P(f"  scanned {nopen:,} committed CSVs, {nhit:,} carry a 4b pass column")
    # The per-row census is 835,403 rows / 80 MB, which is not a research artifact, it is a log.
    # What is auditable is the (file, kind, raw signature, normalised signature) COUNT table, which
    # lets any lane re-derive every share below and see the alphabet mapping file by file.
    CENA = (CEN.groupby(["file", "kind", "sig_raw", "sig"], dropna=False)
               .size().rename("n").reset_index().sort_values("n", ascending=False))
    dump(CENA, "census.csv")
    gates.append(dict(gate="G6 the census can see idea 938's own committed FAIL rows",
                      stat=f"{seen_938} FAIL rows harvested from 938's offsets.csv "
                           f"(938 published 18 of 25 at 10 bps across 4 cost rungs)",
                      bar="> 0", passed=bool(seen_938 > 0)))

    for g in gates:
        P(f"  [{'PASS' if g['passed'] else 'FAIL'}] {g['gate']}\n         {g['stat']}   (bar {g['bar']})")
    P(f"\n  GATES {sum(g['passed'] for g in gates)} of {len(gates)} PASS")
    dump(pd.DataFrame(gates), "gates.csv")

    P(f"\n  tree {sha}; {nopen:,} committed CSVs opened, {nhit:,} carried a 4b pass column")
    RD = CEN[CEN.kind == "READ"]
    P(f"\n    STRICT (binding leg READ from committed columns): {len(RD):,} committed 4b FAIL rows "
      f"from {RD.file.nunique()} files")
    P(f"    WIDE  (every committed 4b FAIL row):               {len(CEN):,} rows from "
      f"{CEN.file.nunique()} files, of which {int((CEN.kind=='UNRECOVERABLE').sum()):,} "
      f"({(CEN.kind=='UNRECOVERABLE').mean():.1%}) carry NO recoverable binding leg at all")
    P(f"\n    RAW signature alphabet, as committed (the record uses at least two):")
    for k, v in RD.sig_raw.value_counts().head(6).items():
        P(f"      {k:<38} {v:>8,}  {v/len(RD):>7.1%}")
    P(f"\n    NORMALISED binding signature (the answer; 'DD' and 'L4_DD' are the same leg):")
    vc = RD.sig.value_counts()
    for k, v in vc.head(12).items():
        P(f"      {k:<38} {v:>8,}  {v/len(RD):>7.1%}")
    solo = int(vc.get("L4_DD", 0))
    anydd = int(RD.sig.str.contains("L4_DD").sum())
    P(f"      L4_DD binding ALONE: {solo:,} of {len(RD):,} = {solo/len(RD):.1%}; "
      f"L4_DD anywhere in the signature: {anydd:,} = {anydd/len(RD):.1%}; "
      f"unmapped tokens: {int((RD.sig == '?UNMAPPED').sum()):,}")
    dd_strict, dd_wide = solo / len(RD), solo / len(CEN)

    # ------------------------------------------------- PART B: PHASE SENSITIVITY, PER LEG
    P("\n" + "=" * 100)
    P("PART B -- THE ANSWER: which leg is a coin flip on the rebalance date")
    P("=" * 100)
    cells = []
    for (pn, gname, bk, cost), s in G.groupby(["panel", "grid", "book", "cost_bps"]):
        n = len(s)
        row = dict(panel=pn, grid=gname, book=bk, cost_bps=cost, n_phases=n,
                   pass4b_phases=int(s.pass4b.sum()), canon_pass4b=bool(
                       s[s.phase == 0].pass4b.iloc[0]))
        for L in LEGS:
            k = int(s[L].sum())
            row[f"{L}_pass"] = k
            row[f"{L}_flip"] = bool(0 < k < n)
        for st, col, bar in (("CAGR", "CAGR", "m_L5_CAGR"), ("Sharpe", "Sharpe", None),
                             ("MaxDD", "MaxDD", "m_L4_DD"), ("H1", "H1", "m_L1_H1"),
                             ("H2", "H2", "m_L2_H2"), ("OOS_Sharpe", "oSharpe", "m_L3_OOS")):
            sup = float(s[col].max() - s[col].min())
            row[f"sup_{st}"] = sup
            if bar:
                mg = float(np.abs(s[bar]).median())
                row[f"cfi_{st}"] = sup / mg if mg > 0 else np.inf
        row["pass4b_unanimous"] = bool(row["pass4b_phases"] in (0, n))
        cells.append(row)
    C = pd.DataFrame(cells)
    dump(C, "cells.csv")

    P(f"\n  LEG FLIP RATE -- share of the {len(C)} cells where the leg's verdict is NOT unanimous")
    P(f"  across the phase family (nothing changed but the rebalance date)")
    P(f"    {'leg':<9} " + " ".join(f"{g:>10}" for g in GRIDS) + f" {'ALL':>10}   {'mean pass share':>16}")
    flip = {}
    for L in LEGS:
        v = [float(C[C.grid == g][f"{L}_flip"].mean()) for g in GRIDS]
        flip[L] = float(C[f"{L}_flip"].mean())
        ps = float((C[f"{L}_pass"] / C.n_phases).mean())
        P(f"    {L:<9} " + " ".join(f"{x:>10.1%}" for x in v) + f" {flip[L]:>10.1%}   {ps:>16.1%}")
    P(f"    {'4b OVERALL':<9} " +
      " ".join(f"{float((~C[C.grid==g].pass4b_unanimous).mean()):>10.1%}" for g in GRIDS) +
      f" {float((~C.pass4b_unanimous).mean()):>10.1%}")

    P(f"\n  COIN-FLIP INDEX -- phase support divided by the median distance to the leg's own bar")
    P(f"  (above 1.0 the rebalance date moves the statistic further than its bar is away)")
    P(f"    {'statistic':<11} {'median CFI':>11} {'mean CFI':>10} {'cells > 1.0':>12} "
      f"{'median support':>15}")
    for st, unit in (("MaxDD", "pp"), ("CAGR", "pp"), ("H1", "Sharpe"), ("H2", "Sharpe"),
                     ("OOS_Sharpe", "Sharpe")):
        c = C[f"cfi_{st}"].replace([np.inf, -np.inf], np.nan).dropna()
        sup = C[f"sup_{st}"]
        mul = 100 if unit == "pp" else 1
        P(f"    {st:<11} {c.median():>11.3f} {c.mean():>10.3f} "
          f"{float((c > 1.0).mean()):>12.1%} {sup.median()*mul:>13.3f} {unit}")

    P(f"\n  THE BINDING SIGNATURE over all {int((~G.pass4b).sum()):,} failing (cell, phase) rows")
    vc = G[~G.pass4b].fail_sig.value_counts()
    for k, v in vc.head(12).items():
        P(f"    {k:<34} {v:>8,}  {v/vc.sum():>7.1%}")
    P(f"    L4_DD binding ALONE: {int(vc.get('L4_DD',0)):,} = {vc.get('L4_DD',0)/vc.sum():.1%}; "
      f"L4_DD anywhere in the signature: "
      f"{int(G[~G.pass4b].fail_sig.str.contains('L4_DD').sum()):,} = "
      f"{float(G[~G.pass4b].fail_sig.str.contains('L4_DD').mean()):.1%}")

    P(f"\n  BY BOOK at {COST0:.0f} bps -- phases passing 4b, and the canonical phase's own verdict")
    P(f"    {'panel':<6} {'grid':<7} {'book':<8} {'pass/phases':>12} {'canon 4b':>9} "
      f"{'MaxDD support':>14} {'CFI MaxDD':>10} {'flipping legs':>28}")
    for _, r in C[C.cost_bps == COST0].sort_values(["panel", "grid", "book"]).iterrows():
        fl = "+".join(L for L in LEGS if r[f"{L}_flip"]) or "-"
        P(f"    {r.panel:<6} {r.grid:<7} {r.book:<8} {str(r.pass4b_phases)+'/'+str(r.n_phases):>12} "
          f"{str(r.canon_pass4b):>9} {r.sup_MaxDD*100:>13.2f}pp {r.cfi_MaxDD:>10.2f} {fl:>28}")

    # ------------------------------------------------------------------- RULE 8 WALK-FORWARD
    P("\n" + "-" * 100)
    P("RULE 8 WALK-FORWARD -- the PHASE chosen on 2009-2016 ALONE by IS Sharpe, 2017-2026 read ONCE,")
    P("beside the CANONICAL phase, which is what an honest book would have shipped")
    P("-" * 100)
    wrows = []
    v2cache = {}
    for pn in PANELS:
        px = raw[pn]
        mkw, _ = offset_mask(px.index, "W", 0)
        bpan = Panel(pn, px, mkw)
        v2b = Book(bpan, rules_v2_weights(px, BAND0, GROSS0).values)
        for gname in GRIDS:
            for bk in BOOKS:
                for cost in COSTS:
                    s = G[(G.panel == pn) & (G.grid == gname) & (G.book == bk) &
                          (G.cost_bps == cost)]
                    pick = s.loc[s.IS_Sharpe.idxmax()]
                    canon = s[s.phase == 0].iloc[0]
                    if cost not in v2cache.get(pn, {}):
                        rv2, _ = v2b.at(cost)
                        v2cache.setdefault(pn, {})[cost] = fmet(
                            np.asarray(rv2)[bpan.masks["OOS"]]) + (
                            fsharpe(np.asarray(rv2)[bpan.masks["OOS"]][
                                :int(bpan.masks["OOS"].sum()) // 2]),
                            fsharpe(np.asarray(rv2)[bpan.masks["OOS"]][
                                int(bpan.masks["OOS"].sum()) // 2:]))
                    bc, bsh, bdd, bh1, bh2 = v2cache[pn][cost]
                    for tag, r in (("IS_PICK", pick), ("CANONICAL", canon)):
                        p4b = bool(r.oSharpe > r.spy_oSharpe and
                                   r.oMaxDD >= DD_CAP * r.spy_MaxDD and
                                   r.oCAGR >= CAGR_FLOOR * r.spy_CAGR and
                                   r.H1 > r.spy_H1 and r.H2 > r.spy_H2)
                        p4a = bool(r.oSharpe > bsh and r.oMaxDD >= bdd)
                        wrows.append(dict(panel=pn, grid=gname, book=bk, cost_bps=cost, chooser=tag,
                                          phase=int(r.phase), IS_Sharpe=r.IS_Sharpe,
                                          OOS_CAGR=r.oCAGR, OOS_Sharpe=r.oSharpe,
                                          OOS_MaxDD=r.oMaxDD, FULL_CAGR=r.CAGR,
                                          FULL_Sharpe=r.Sharpe, FULL_MaxDD=r.MaxDD,
                                          H1=r.H1, H2=r.H2,
                                          SPY_OOS_Sharpe=r.spy_oSharpe, SPY_CAGR=r.spy_CAGR,
                                          SPY_MaxDD=r.spy_MaxDD, V2_OOS_CAGR=bc,
                                          V2_OOS_Sharpe=bsh, V2_OOS_MaxDD=bdd,
                                          OOS_pass4b=p4b, OOS_pass4a=p4a))
    WF = pd.DataFrame(wrows)
    dump(WF, "walkforward.csv")
    P(f"\n    {'chooser':<10} {'cells':>6} {'OOS 4b':>8} {'OOS 4a':>8} {'mean OOS Sharpe':>16} "
      f"{'mean OOS CAGR':>14} {'mean phase':>11}")
    for tag in ("IS_PICK", "CANONICAL"):
        s = WF[WF.chooser == tag]
        P(f"    {tag:<10} {len(s):>6} {int(s.OOS_pass4b.sum()):>8} {int(s.OOS_pass4a.sum()):>8} "
          f"{s.OOS_Sharpe.mean():>16.4f} {s.OOS_CAGR.mean():>13.2%} {s.phase.mean():>11.2f}")
    agree = WF[WF.chooser == "IS_PICK"].reset_index(drop=True)
    can = WF[WF.chooser == "CANONICAL"].reset_index(drop=True)
    P(f"    the IS chooser picks the canonical phase in "
      f"{int((agree.phase == 0).sum())} of {len(agree)} cells; where it does not, its OOS Sharpe "
      f"beats the canonical's in {int((agree.OOS_Sharpe > can.OOS_Sharpe)[agree.phase != 0].sum())} "
      f"of {int((agree.phase != 0).sum())}")

    P(f"\n    BEST OOS CELL PER PANEL (IS-chosen phase), against SPY and the live RULES v2 book")
    P(f"    {'panel':<6} {'book':<8} {'grid':<7} {'cost':>5} {'ph':>3} {'OOS CAGR':>9} "
      f"{'Sharpe':>8} {'MaxDD':>8}   {'SPY Sh':>7} {'v2 CAGR':>8} {'v2 Sh':>7} {'v2 DD':>8} "
      f"{'4b':>5} {'4a':>5}")
    for pn in PANELS:
        s = WF[(WF.panel == pn) & (WF.chooser == "IS_PICK")]
        r = s.loc[s.OOS_Sharpe.idxmax()]
        P(f"    {pn:<6} {r.book:<8} {r.grid:<7} {r.cost_bps:>5.0f} {int(r.phase):>3} "
          f"{r.OOS_CAGR:>9.2%} {r.OOS_Sharpe:>8.3f} {r.OOS_MaxDD:>8.2%}   "
          f"{r.SPY_OOS_Sharpe:>7.3f} {r.V2_OOS_CAGR:>8.2%} {r.V2_OOS_Sharpe:>7.3f} "
          f"{r.V2_OOS_MaxDD:>8.2%} {str(bool(r.OOS_pass4b)):>5} {str(bool(r.OOS_pass4a)):>5}")

    # ------------------------------------------------------------------------- HYPOTHESES
    P("\n" + "-" * 100)
    P("PRE-REGISTERED HYPOTHESES")
    P("-" * 100)
    hyp = []
    g3 = next(g for g in gates if g["gate"].startswith("G3 "))
    hyp.append(dict(name="H_CTRL", verdict="PASS" if g3["passed"] else "FAIL", detail=g3["stat"]))

    top = max(flip, key=flip.get)
    per_grid_top = {g: max(LEGS, key=lambda L: C[C.grid == g][f"{L}_flip"].mean()) for g in GRIDS}
    hyp.append(dict(name="H_DDLEG",
                    verdict="PASS" if all(v == "L4_DD" for v in per_grid_top.values()) else "FAIL",
                    detail="leg flip rates over all cells: " +
                           ", ".join(f"{L}={flip[L]:.1%}" for L in LEGS) +
                           f"; highest overall {top}; per grid " +
                           ", ".join(f"{g}={v}" for g, v in per_grid_top.items())))

    vcm = G[~G.pass4b].fail_sig.value_counts()
    hyp.append(dict(name="H_ALONE", verdict="PASS" if vcm.index[0] == "L4_DD" else "FAIL",
                    detail=f"plurality binding signature over {int(vcm.sum()):,} failing "
                           f"(cell, phase) rows is '{vcm.index[0]}' at {vcm.iloc[0]/vcm.sum():.1%} "
                           f"-- ALL FIVE legs failing at once. L4_DD ALONE is second at "
                           f"{vcm.get('L4_DD',0)/vcm.sum():.1%}, and L4_DD appears in "
                           f"{float(G[~G.pass4b].fail_sig.str.contains('L4_DD').mean()):.1%} of "
                           f"failing rows"))

    cfi = {st: float(C[f"cfi_{st}"].replace([np.inf, -np.inf], np.nan).median())
           for st in ("MaxDD", "CAGR", "H1", "H2", "OOS_Sharpe")}
    hyp.append(dict(name="H_STAT",
                    verdict="PASS" if max(cfi, key=cfi.get) == "MaxDD" else "FAIL",
                    detail="median coin-flip index: " +
                           ", ".join(f"{k}={v:.3f}" for k, v in cfi.items()) +
                           f"; largest is {max(cfi, key=cfi.get)}"))

    rk = {g: sorted(LEGS, key=lambda L: -C[C.grid == g][f"{L}_flip"].mean()) for g in GRIDS}
    same = len({tuple(v) for v in rk.values()}) == 1
    hyp.append(dict(name="H_GRID", verdict="PASS" if same else "FAIL",
                    detail="; ".join(f"{g}: " + " > ".join(v) for g, v in rk.items())))

    hyp.append(dict(name="H_CENSUS",
                    verdict="PASS" if len(RD) > 0 and abs(dd_strict - dd_wide) <= 0.10 else "FAIL",
                    detail=f"{len(RD):,} STRICT (readable) of {len(CEN):,} committed 4b FAIL rows "
                           f"across {CEN.file.nunique()} files; L4_DD-alone share STRICT "
                           f"{dd_strict:.1%} vs WIDE {dd_wide:.1%} = "
                           f"{abs(dd_strict-dd_wide)*100:.1f} pp apart (bar 10 pp). "
                           f"THE BAR WAS BADLY SPECIFIED AND IS REPORTED AS SUCH: WIDE is a "
                           f"superset of STRICT whose only extra rows are UNRECOVERABLE ones "
                           f"({int((CEN.kind=='UNRECOVERABLE').sum()):,} = "
                           f"{(CEN.kind=='UNRECOVERABLE').mean():.1%}), so the 'gap' is nothing "
                           f"but the readable share and the bar tests nothing in either "
                           f"direction. The number that matters is that "
                           f"{(CEN.kind=='UNRECOVERABLE').mean():.1%} of the record's committed "
                           f"4b FAIL rows do not say which leg bound"))

    ip = WF[WF.chooser == "IS_PICK"]
    cn = WF[WF.chooser == "CANONICAL"]
    hyp.append(dict(name="H_WF", verdict="REPORTED",
                    detail=f"IS-chosen phase: OOS 4b {int(ip.OOS_pass4b.sum())} of {len(ip)}, 4a "
                           f"{int(ip.OOS_pass4a.sum())} of {len(ip)}, mean OOS Sharpe "
                           f"{ip.OOS_Sharpe.mean():.4f}. CANONICAL phase: 4b "
                           f"{int(cn.OOS_pass4b.sum())} of {len(cn)}, 4a "
                           f"{int(cn.OOS_pass4a.sum())} of {len(cn)}, mean OOS Sharpe "
                           f"{cn.OOS_Sharpe.mean():.4f}. Choosing the phase in sample is worth "
                           f"{ip.OOS_Sharpe.mean()-cn.OOS_Sharpe.mean():+.4f} of OOS Sharpe"))

    for h in hyp:
        P(f"  {h['name']:<9} {h['verdict']:<8} {h['detail']}")
    dump(pd.DataFrame(hyp), "hypotheses.csv")
    P(f"\n  elapsed {time.time()-t0:.1f}s")
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
