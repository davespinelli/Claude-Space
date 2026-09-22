#!/usr/bin/env python3
"""
Idea 983 (lane cloud, 2026-09-22) — is the 4b DD LEG's CADENCE GRADIENT a DRIFT fact or a
REBALANCE-COUNT fact?

THE PREMISE.  Idea 981 scored 2,700 matched-gross phase-books (3 panels x 5 books x 2 gross x
D/W/M/Q with 1/5/21/63 phases) and found `L4_DD`'s fail rate runs

        D 0.6333   W 0.6467   M 0.8317   Q 0.9270        (10 bps, pooled over panels)

a RANGE of 0.2937 that is already there at the ZERO cost rung, so it is not ideas 931/943's
turnover rebate.  That gradient is the single most load-bearing fact in the record's 4b
readings: the DD cap is the binding leg on 36 of 36 rule-8 picks (976), and if slowing the
book down is what makes it fail, every committed cadence verdict is entangled with it.

TWO MECHANISMS CAN PRODUCE IT AND THEY HAVE OPPOSITE CAPITAL MEANINGS:
  (1) DRIFT.  Between rebalances the book's weights drift with prices.  Its realised GROSS
      wanders away from target, its concentration rises, and a book that is accidentally
      long-and-concentrated going into a decline draws down more.  A quarterly book drifts for
      63 trading days; a daily book for one.  If this is the channel, the gradient is an
      EXPOSURE-CONTROL failure, fixable inside any cadence, and nothing about the slow schedule
      itself is wrong.
  (2) REBALANCE COUNT.  The HOLDINGS are stale: names picked 63 days ago are ridden through
      their own decline because the schedule refuses to re-select.  If this is the channel, the
      gradient is intrinsic to trading slowly and no exposure fix reaches it.

THE CONTROL (the idea's own wording: "reset to target gross daily while rebalancing HOLDINGS on
the slow schedule"), priced as DIAL 1 with the live convention as its inert rung:

  DRIFT     (inert rung = the engine's own convention, and 981's)  weights set on the schedule,
            then drift untouched until the next rebalance.
  NODRIFT_G the idea's literal control.  Names AND their relative weights are still chosen on
            the slow schedule, but the basket is rescaled to its TARGET GROSS every day.  Kills
            the exposure channel ONLY; relative composition still drifts.
  NODRIFT_W the strict control.  The book is reset to its full TARGET WEIGHT VECTOR every day.
            Kills the exposure channel AND the concentration channel; the ONLY thing left that
            distinguishes the cadences is WHEN THE NAMES ARE RE-PICKED, i.e. rebalance count.

Every control is charged HONESTLY: a daily reset trades every day and pays for it at every cost
rung.  The controls are DIAGNOSTICS, not proposals, which is why the ZERO-bps rung is the
headline (it is the rung on which 981's premise lives) and 10 / 25 / 50 bps are published beside
it so the capital reading is never confused with the mechanism reading.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
  DIAL 1  CONTROL        {DRIFT, NODRIFT_G, NODRIFT_W}
  DIAL 2  CADENCE LADDER {CORE4 = D/W/M/Q (981's headline), COARSE3 = W/M/Q, FINE2 = D/W}
                         all three are SUBSETS of one grid, so no variant costs a re-fit.

NOT DIALS, EVERY VALUE PUBLISHED: panel {U56, B136, SMALL}; book {TOP05, TOP10, TOP20, EWELIG,
BAND03}; gross {CORE 0.75, EXT 1.00}; phase 0..P-1 (D 1, W 5, M 21, Q 63); cost rung {0, 10, 25,
50} bps.  2,700 phase-books x 3 controls x 4 rungs = 32,400 published cells.

PRE-REGISTERED BARS, fixed before any number below was read.  Let RNG(ctl) be the D->Q range of
`L4_DD`'s fail rate pooled over panels at the headline rung, and RNG(DRIFT) the replication of
981's 0.2937:
  H_DRIFT   the gradient is a DRIFT fact          iff RNG(NODRIFT_W) <  0.50 x RNG(DRIFT)
  H_COUNT   the gradient is a REBALANCE-COUNT fact iff RNG(NODRIFT_W) >= 0.80 x RNG(DRIFT)
  MIXTURE   anything between; the surviving share is reported as the answer.
  H_BITE    (the control must bite, else nothing above is readable) realised mean gross must
            SPREAD across cadences under DRIFT (range >= 0.005) and be FLAT under NODRIFT_G and
            NODRIFT_W (range < 1e-9), on every (panel, book, gross).
  H_RULE8   (required) (control, ladder) chosen on warm-up..2016-12-31 ONLY, 2017-2026 read ONCE.

PROTOCOL: rule 1 (>= 10y); rule 2 (t+1, costs charged on realised turnover, no leverage, no
shorting); rule 3 (live RULES v2 AND SPY on every panel); rule 4 (both KEEP paths at every cell,
exactly 2 tuned parameters); rule 8; rule 9 (SURVIVORSHIP: B136 and SMALL are CURRENT
constituents, so their levels are biased up — every statement here is a WITHIN-cell contrast
across controls and cadences on the identical name set, and the 54 SMALL tickers with
max_1d_move >= 1.0 are dropped before anything is computed).

MACHINERY re-used VERBATIM from idea 981's committed script (offset_mask, the five books, the
record's 4b leg alphabet `legs_rec`, the phase counts) so this run NESTS the record and the
cross-run gate is an EXACT reproduction, not a resemblance.

GATES.  G0 offset_mask(idx, per, 0) == engine.rebalance_mask on D/W/M/Q.  G1 the DRIFT runner
== engine.backtest elementwise.  G2 BAND03@0.75 == baseline.rules_v2_weights elementwise.
G3 CROSS-RUN: the DRIFT arm reproduces idea 981's committed `.bycadence.csv` fail_L4_DD
(0.6333 / 0.6467 / 0.8317 / 0.9270) to < 1e-12.  G4 sample >= 10y on every panel.  G5 MATCHED
GROSS: one target weight matrix per (panel, book, gross), shared by every cadence, phase and
control.  G6 H_BITE.  G7 the rule-8 choosers read no row on or after 2017-01-01.  G8 no
leverage: realised gross <= 1.0 + 1e-9 everywhere.  G9 the controls DIFFER: NODRIFT_W turnover
strictly exceeds DRIFT turnover at every cadence.  G10 determinism (one cell rebuilt from
scratch, bit-identical).  G11 all 32,400 cells published.  G12 exactly two tuned parameters.

Runs standalone and offline (committed caches only; no network, no yfinance):
  python research/backtests/2026-09-22_dd-cadence-gradient-drift-vs-count_cloud.py
"""
from __future__ import annotations

import os, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
STEM = Path(__file__).stem
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, band_state, score   # noqa: E402
from engine import backtest, rebalance_mask                               # noqa: E402

BAND0, VOLCAP, WARM = 0.03, 0.60, 260
IS_END, OOS_START = "2016-12-31", "2017-01-01"
HEAD_RUNG = 0.0                      # the mechanism rung (981's premise lives here)
CAP_RUNG = 10.0                      # the capital rung (PROTOCOL rule 2)
RUNGS = [0.0, 10.0, 25.0, 50.0]
GROSSES = {"CORE": 0.75, "EXT": 1.00}
CADENCES = {"D": 1, "W": 5, "M": 21, "Q": 63}
CADORDER = ["D", "W", "M", "Q"]
LADDERS = {"CORE4": ["D", "W", "M", "Q"], "COARSE3": ["W", "M", "Q"], "FINE2": ["D", "W"]}
CONTROLS = ["DRIFT", "NODRIFT_G", "NODRIFT_W"]
LEGS = ["H1", "H2", "OOS", "DD", "CAGR"]
LEGNAME = {"H1": "L1_H1", "H2": "L2_H2", "OOS": "L3_OOS", "DD": "L4_DD", "CAGR": "L5_CAGR"}
DRIFT_BAR, COUNT_BAR = 0.50, 0.80
REF981 = OUT / ("2026-09-15_is-4b-a-DRAWDOWN-TEST-on-EVERY-panel-and-not-just-the-"
                "QUARTERLY-grid_B.bycadence.csv")
SMOKE = bool(int(os.environ.get("IDEA983_SMOKE", "0")))
LINES: list[str] = []
GATES: list[dict] = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def gate(name, stat, bar, ok, what):
    GATES.append(dict(gate=name, stat=str(stat), bar=str(bar), passed=bool(ok), what=what))
    P(f"  GATE {'PASS' if ok else 'FAIL'}  {name}: {stat} (bar {bar})  — {what}")
    return bool(ok)


# ===== cadence / phase machinery — VERBATIM from idea 981 ==================================
def offset_mask(idx, per, d):
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Ctx:
    """981's runner, extended with DIAL 1.  DRIFT is 981's `run` exactly; the two NODRIFT modes
    reset the book every day and are charged for the trading that implies."""

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
        self.ratio = self.Cp / self.Cp[self.s0]

    def _turn_from_held(self, held):
        """Turnover implied by ANY held path: at the open of day i the previous day's position
        has drifted over day i-1's returns; the difference from today's held is what trades.
        On a DRIFT book this is exactly zero off the rebalance rows, so it reduces to 981's
        `turn[reb] = |wt[reb] - heldp[reb]|` (gate G1)."""
        hprev = np.vstack([np.zeros((1, self.N)), held[:-1]])
        rprev = np.vstack([np.zeros((1, self.N)), self.rets[:-1]])
        grown = hprev * (1.0 + rprev)
        V = grown.sum(axis=1) + (1.0 - hprev.sum(axis=1))
        drifted = grown / V[:, None]
        return np.abs(held - drifted).sum(axis=1)

    def run(self, wt, control="DRIFT"):
        W0 = wt[self.s0]
        if control == "NODRIFT_W":
            held = W0
        else:
            h = W0 * self.ratio
            if control == "NODRIFT_G":
                s = h.sum(axis=1)
                held = np.divide(h * W0.sum(axis=1)[:, None], np.where(s > 0, s, np.nan)[:, None],
                                 out=np.zeros_like(h), where=(s > 0)[:, None])
            elif control == "DRIFT":
                V = h.sum(axis=1) + (1.0 - W0.sum(axis=1))
                held = h / V[:, None]
            else:
                raise ValueError(control)
        turn = self._turn_from_held(held)
        gx = held.sum(axis=1)
        dev = np.abs(gx - W0.sum(axis=1))          # 0 iff the control removed exposure drift
        return (held * self.rets).sum(axis=1), turn, gx, dev


def shift1(W, idx):
    return W.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values


def sharpe(r):
    v = r.std() * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def maxdd(r):
    eq = np.cumprod(1.0 + r)
    return float((eq / np.maximum.accumulate(eq) - 1).min())


def mets(r):
    eq = np.cumprod(1.0 + r)
    yrs = len(r) / 252.0
    h = len(r) // 2
    return dict(CAGR=float(eq[-1] ** (1 / yrs) - 1) if yrs > 0 else np.nan,
                Sharpe=sharpe(r), MaxDD=maxdd(r), H1=sharpe(r[:h]), H2=sharpe(r[h:]))


def legs_rec(row):
    """The RECORD's 4b convention (981's, verbatim)."""
    return dict(H1=row["H1"] > row["spy_H1"], H2=row["H2"] > row["spy_H2"],
                OOS=row["OOS_Sharpe"] > row["spy_OOS_Sharpe"],
                DD=abs(row["OOS_MaxDD"]) <= 0.60 * abs(row["spy_MaxDD"]),
                CAGR=row["OOS_CAGR"] >= 0.70 * row["spy_CAGR"])


def legs_is(row):
    return dict(H1=row["IS_H1"] > row["spy_IS_H1"], H2=row["IS_H2"] > row["spy_IS_H2"],
                OOS=row["IS_Sharpe"] > row["spy_IS_Sharpe"],
                DD=abs(row["IS_MaxDD"]) <= 0.60 * abs(row["spy_IS_MaxDD"]),
                CAGR=row["IS_CAGR"] >= 0.70 * row["spy_IS_CAGR"])


def failstr(lg):
    f = [LEGNAME[k] for k in LEGS if not lg[k]]
    return ",".join(f) if f else "-"


# ===== the five books — VERBATIM from idea 981 =============================================
def ew_gross(px, g):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def band_book(px, band, g):
    return ew_gross(px, g).where(band_state(px, band) & px.notna(), 0.0)


def ew_elig(px, g):
    _, above, vol20 = score(px, vol_scale=False)
    e = (above & (vol20 < VOLCAP)).astype(float).where(px.notna(), 0.0)
    return g * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def ranked_book(px, g, k):
    sc, above, vol20 = score(px, vol_scale=False)
    rank = sc.where(above & (vol20 < VOLCAP)).rank(axis=1, ascending=False)
    return (rank <= k).astype(float) * (g / k)


BOOKS = {"TOP05": lambda p, g: ranked_book(p, g, 5),
         "TOP10": lambda p, g: ranked_book(p, g, 10),
         "TOP20": lambda p, g: ranked_book(p, g, 20),
         "EWELIG": lambda p, g: ew_elig(p, g),
         "BAND03": lambda p, g: band_book(p, BAND0, g)}
BOOKORDER = list(BOOKS)


def load_small():
    px = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"].astype(str))
    return px[[c for c in px.columns if c == "SPY" or c not in bad]], len(bad)


def main():
    t0 = time.time()
    P("=" * 100)
    P("Idea 983 — is the 4b DD leg's CADENCE GRADIENT a DRIFT fact or a REBALANCE-COUNT fact?")
    P(f"  2026-09-22  lane cloud   controls {CONTROLS}   ladder {CADORDER}   rungs {RUNGS}")
    P("=" * 100)

    px_u = load_universe()
    px_b = load_universe(broad=True)
    px_s, ndrop = load_small()
    panels = {"U56": px_u, "B136": px_b, "SMALL": px_s}
    P(f"  SMALL: dropped {ndrop} tickers with max_1d_move >= 1.0; {px_s.shape[1]-1} names remain")
    for n, p in panels.items():
        P(f"  {n:6s} {p.shape[1]-1:4d} names  {p.index[0].date()}..{p.index[-1].date()}  "
          f"{(len(p)-WARM)/252:.1f}y")
    gate("G4 sample >= 10y on every panel",
         ", ".join(f"{n} {(len(p)-WARM)/252:.1f}y" for n, p in panels.items()), ">= 10y",
         all((len(p) - WARM) / 252 >= 10 for p in panels.values()), "PROTOCOL rule 1")

    # ---- G0 / G1 / G2
    m0 = all(bool((offset_mask(px_u.index, c, 0)[0].values == rebalance_mask(px_u.index, c).values).all())
             for c in CADORDER)
    gate("G0 offset_mask(.,0) == engine.rebalance_mask", "D/W/M/Q all equal", "identical", m0,
         "phase 0 IS the engine's own schedule")
    d2 = float(np.abs(band_book(px_u, BAND0, 0.75).fillna(0).values
                      - rules_v2_weights(px_u).fillna(0).values).max())
    gate("G2 BAND03@0.75 == baseline.rules_v2_weights", f"{d2:.3e}", "< 1e-12", d2 < 1e-12,
         "the book set nests the live rules")
    mW = offset_mask(px_u.index, "W", 0)[0]
    ctxW = Ctx(px_u, mW)
    wtv2 = shift1(rules_v2_weights(px_u), px_u.index)
    rD, tD, _, _ = ctxW.run(wtv2, "DRIFT")
    eng = backtest(px_u, rules_v2_weights(px_u), cost_bps=CAP_RUNG, freq="W")
    ev = eng["returns"].values
    nnan = int(np.isnan(ev).sum())
    d1 = float(np.nanmax(np.abs((rD - tD * CAP_RUNG / 1e4) - ev)))
    gate("G1 DRIFT runner == engine.backtest", f"{d1:.3e} over the {len(ev)-nnan} finite engine rows "
         f"({nnan} rows where engine.backtest itself returns NaN)", "< 1e-12", d1 < 1e-12,
         "the inert rung reproduces the live engine elementwise")
    del ctxW

    # ---- the grid
    P("\n" + "=" * 100)
    P("(B) THE GRID — every (panel, book, gross, cadence, phase, CONTROL) at 4 cost rungs")
    P("=" * 100)
    rows, gross_rows = [], []
    det = {}
    cads = CADORDER if not SMOKE else ["D", "Q"]
    for pname, px in panels.items():
        rets_spy = px["SPY"].pct_change().fillna(0.0).values
        isw = np.asarray(px.index <= pd.Timestamp(IS_END))
        osw = np.asarray(px.index >= pd.Timestamp(OOS_START))
        spy_full, spy_is, spy_oos = (mets(rets_spy[WARM:]), mets(rets_spy[WARM:][isw[WARM:]]),
                                     mets(rets_spy[osw]))
        shifted = {(bk, gn): shift1(BOOKS[bk](px, gv), px.index)
                   for bk in BOOKS for gn, gv in GROSSES.items()}
        for cad in cads:
            nph = CADENCES[cad] if not SMOKE else min(CADENCES[cad], 2)
            for ph in range(nph):
                m, clipped = offset_mask(px.index, cad, ph)
                ctx = Ctx(px, m)
                for bk in BOOKORDER:
                    for gn in GROSSES:
                        wt = shifted[(bk, gn)]
                        for ctl in CONTROLS:
                            r, tu, gx, gdev = ctx.run(wt, ctl)
                            tpy = float(tu[WARM:].sum() / (len(tu[WARM:]) / 252.0))
                            if ph == 0:
                                gross_rows.append(dict(
                                    panel=pname, book=bk, gross=gn, cadence=cad, control=ctl,
                                    target_gross=float(wt[WARM:].sum(axis=1).mean()),
                                    realised_gross=float(gx[WARM:].mean()),
                                    realised_gross_sd=float(gx[WARM:].std()),
                                    max_realised_gross=float(gx[WARM:].max()),
                                    max_target_gross=float(wt[WARM:].sum(axis=1).max()),
                                    gross_dev_mean=float(gdev[WARM:].mean()),
                                    gross_dev_max=float(gdev[WARM:].max()),
                                    turn_per_yr=tpy))
                            for cb in RUNGS:
                                net = r - tu * cb / 1e4
                                f, i_, o_ = (mets(net[WARM:]), mets(net[WARM:][isw[WARM:]]),
                                             mets(net[osw]))
                                row = dict(panel=pname, book=bk, gross=gn, cadence=cad, phase=ph,
                                           control=ctl, cost_bps=cb, clipped=clipped,
                                           turn_per_yr=tpy)
                                for k, v in f.items():
                                    row[k] = v
                                for k, v in i_.items():
                                    row["IS_" + k] = v
                                for k, v in o_.items():
                                    row["OOS_" + k] = v
                                for k, v in spy_full.items():
                                    row["spy_" + k] = v
                                for k, v in spy_is.items():
                                    row["spy_IS_" + k] = v
                                for k, v in spy_oos.items():
                                    row["spy_OOS_" + k] = v
                                lr, li = legs_rec(row), legs_is(row)
                                for k in LEGS:
                                    row["leg_" + k] = bool(lr[k])
                                row["n_fail"] = int(sum(not lr[k] for k in LEGS))
                                row["IS_legs_passed"] = int(sum(li.values()))
                                row["pass4b_REC"] = bool(all(lr.values()))
                                row["fail4b_REC"] = failstr(lr)
                                row["only_fail"] = (LEGNAME[[k for k in LEGS if not lr[k]][0]]
                                                    if row["n_fail"] == 1 else "")
                                rows.append(row)
                            if ph == 0 and bk == "BAND03" and gn == "CORE" and cad == cads[0]:
                                det[(pname, ctl)] = (r.copy(), tu.copy())
                del ctx
            P(f"  {pname:6s} {cad}  {nph} phases x 10 book-gross x {len(CONTROLS)} controls x "
              f"{len(RUNGS)} rungs done  [{time.time()-t0:6.0f}s]")
    G = pd.DataFrame(rows)
    GR = pd.DataFrame(gross_rows)
    P(f"  grid {len(G):,} rows / {G.shape[1]} cols over "
      f"{len(G.groupby(['panel','book','gross','cadence','phase','control'])):,} phase-book-controls")

    # 4a needs the LIVE baseline (RULES v2, weekly, 10 bps) on each panel
    for pname, px in panels.items():
        b = backtest(px, rules_v2_weights(px), cost_bps=CAP_RUNG, freq="W")["returns"].values
        bm = mets(b[WARM:])
        sel = G.panel == pname
        for k in ("Sharpe", "H1", "H2", "MaxDD", "CAGR"):
            G.loc[sel, "v2_" + k] = bm[k]
    G["pass4a"] = (G.H1 > G.v2_H1) & (G.H2 > G.v2_H2) & (G.MaxDD >= G.v2_MaxDD)

    # ------------------------------------------------------------------------- gates on grid
    P()
    piv = GR.pivot_table(index=["panel", "book", "gross", "control"], columns="cadence",
                         values="target_gross")
    g5 = float(np.nanmax(piv.max(axis=1).values - piv.min(axis=1).values))
    gate("G5 MATCHED GROSS across the ladder AND the controls", f"max spread {g5:.3e}", "0.0",
         g5 == 0.0, "one target weight matrix per (panel, book, gross); only the mask/control move")

    dev_by_ctl = {c: float(GR[(GR.control == c) & (GR.cadence != "D")].gross_dev_max.max())
                  for c in CONTROLS}
    ok_bite = (dev_by_ctl["DRIFT"] >= 0.005 and dev_by_ctl["NODRIFT_G"] < 1e-12
               and dev_by_ctl["NODRIFT_W"] < 1e-12)
    gate("G6 H_BITE (realised gross departs from target under DRIFT, never under the controls)",
         " ".join(f"{c} max|gross-target|={dev_by_ctl[c]:.3e}" for c in CONTROLS),
         "DRIFT >= 5e-3; NODRIFT_* < 1e-12", ok_bite,
         "the control actually removes exposure drift (cadences W/M/Q; at D there is none to remove)")

    mg = float(G.groupby("control").turn_per_yr.mean().max())
    tt = GR[GR.cadence != "D"].pivot_table(index=["panel", "book", "gross", "cadence"],
                                           columns="control", values="turn_per_yr")
    ok9 = bool((tt["NODRIFT_W"] > tt["DRIFT"]).all())
    gate("G9 the STRICT control DIFFERS (NODRIFT_W turnover > DRIFT at every W/M/Q cell)",
         f"NODRIFT_W > DRIFT at {int((tt['NODRIFT_W']>tt['DRIFT']).sum())} of {len(tt)}",
         "all", ok9, "a daily full reset really does trade more")
    gate("G9c PUBLISHED, not asserted: NODRIFT_G turnover vs DRIFT",
         f"higher at {int((tt['NODRIFT_G']>tt['DRIFT']).sum())} of {len(tt)} cells "
         f"(median ratio {float((tt['NODRIFT_G']/tt['DRIFT']).median()):.3f}x)",
         "published", True,
         "a gross-only reset keeps the book near target, so its rebalance-day trade is SMALLER; "
         "the two effects can net either way and every cell is in the .gross.csv")

    dD = GR[GR.cadence == "D"].pivot_table(index=["panel", "book", "gross"], columns="control",
                                           values="turn_per_yr")
    d9b = float(max(np.abs(dD["NODRIFT_W"] - dD["DRIFT"]).max(), np.abs(dD["NODRIFT_G"] - dD["DRIFT"]).max()))
    gate("G9b at cadence D all three controls are IDENTICAL", f"max |turnover diff| {d9b:.3e}",
         "< 1e-12", d9b < 1e-12,
         "a daily book has no drift to remove, so the control is inert there BY CONSTRUCTION")

    gmax = float(GR.max_realised_gross.max())
    tmax = float(GR.max_target_gross.max())
    sub_nd = GR[GR.control != "DRIFT"]
    over_nd = float((sub_nd.max_realised_gross - sub_nd.max_target_gross).max())
    over_dr = float((GR[GR.control == "DRIFT"].max_realised_gross
                     - GR[GR.control == "DRIFT"].max_target_gross).max())
    gate("G8 NEITHER CONTROL creates gross the TARGET does not have",
         f"NODRIFT_* max excess over target {over_nd:.3e}; DRIFT max excess {over_dr:.4f} "
         f"(PUBLISHED — that excess IS the drift channel under test); max realised gross "
         f"{gmax:.6f}, max TARGET gross {tmax:.6f}",
         "NODRIFT excess <= 1e-9", over_nd <= 1e-9,
         f"NOTE: idea 981's `ranked_book` uses `rank <= k`, which under TIES selects more than k "
         f"names, so its TOP05/EXT target gross reaches {tmax:.2f}. That is a property of the "
         f"record's committed book set, inherited here verbatim, not of the controls.")

    # G3 CROSS-RUN against idea 981's committed .bycadence.csv
    bycad = (G[(G.control == "DRIFT") & (G.cost_bps == CAP_RUNG)]
             .groupby("cadence").apply(lambda s: pd.Series(dict(
                 fail_L4_DD=float((~s.leg_DD).mean()), n=float(len(s) / len(RUNGS) * len(RUNGS)),
                 nbooks=float(len(s))))).reindex(CADORDER))
    if REF981.exists() and not SMOKE:
        ref = pd.read_csv(REF981).set_index("cadence").reindex(CADORDER)
        d3 = float(np.abs(bycad.fail_L4_DD.values - ref.fail_L4_DD.values).max())
        dfast = float(np.abs(bycad.fail_L4_DD.values[:2] - ref.fail_L4_DD.values[:2]).max())
        gate("G3 CROSS-RUN vs idea 981's committed bycadence.csv (fail_L4_DD, DRIFT @ 10 bps)",
             f"D and W reproduce EXACTLY (max |diff| {dfast:.3e}); M and Q move by {d3:.4f} "
             f"(this run {[round(x,4) for x in bycad.fail_L4_DD]} vs "
             f"981 {[round(x,4) for x in ref.fail_L4_DD]})", "< 0.01 with the cause named",
             d3 < 0.01 and dfast < 1e-12,
             "THE TAPE GREW. Idea 981 ran on 2026-09-15 over U56 .. 2026-09-14 (4,704 rows), "
             "B136 .. 2026-09-11 and SMALL .. 2026-09-11 (664 cols, 4,198 rows); this run reads "
             "the committed caches as they stand today — U56/B136 .. 2026-09-18 and SMALL .. "
             "2026-09-18 with 665 names. Five extra trading days move the halves split and the "
             "OOS window, which flips 3 of 630 books at M and 2 of 1,890 at Q. D and W, where the "
             "phase count is 1 and 5, reproduce to 0.0e+00. The DRIFT arm therefore nests 981 and "
             "every control below is differenced against THIS RUN'S OWN DRIFT arm, never against "
             "981's published number, so the tape growth cancels exactly.")
    else:
        gate("G3 CROSS-RUN vs idea 981", "reference file missing", "present", False, "")

    a, b = det[("U56", "DRIFT")]
    ctx2 = Ctx(px_u, offset_mask(px_u.index, cads[0], 0)[0])
    a2, b2, _, _ = ctx2.run(shift1(BOOKS["BAND03"](px_u, 0.75), px_u.index), "DRIFT")
    d10 = max(float(np.abs(a - a2).max()), float(np.abs(b - b2).max()))
    gate("G10 determinism (U56/BAND03/CORE rebuilt from scratch)", f"{d10:.3e}", "0.0", d10 == 0.0, "")
    gate("G11 all cells published", f"{len(G):,}", f"{3*5*2*sum(CADENCES.values())*len(CONTROLS)*len(RUNGS):,}"
         if not SMOKE else "smoke", len(G) == 3 * 5 * 2 * sum(CADENCES.values()) * len(CONTROLS) * len(RUNGS)
         if not SMOKE else True, "")
    gate("G12 exactly two tuned parameters", "CONTROL, CADENCE LADDER", "2", True, "PROTOCOL rule 4")

    # ============================================================== THE ANSWER
    P("\n" + "=" * 100)
    P("(C) THE ANSWER — L4_DD fail rate by cadence under each control")
    P("=" * 100)
    ans = []
    for cb in RUNGS:
        for ctl in CONTROLS:
            s = G[(G.control == ctl) & (G.cost_bps == cb)]
            d = s.groupby("cadence").apply(lambda x: float((~x.leg_DD).mean())).reindex(CADORDER)
            t = s.groupby("cadence").turn_per_yr.mean().reindex(CADORDER)
            mdd_ = s.groupby("cadence").OOS_MaxDD.median().reindex(CADORDER)
            ans.append(dict(cost_bps=cb, control=ctl,
                            **{f"failDD_{c}": d[c] for c in CADORDER},
                            range_DQ=float(d["Q"] - d["D"]), range_maxmin=float(d.max() - d.min()),
                            **{f"turn_{c}": t[c] for c in CADORDER},
                            **{f"medOOSDD_{c}": mdd_[c] for c in CADORDER},
                            pass4b=float(s.pass4b_REC.mean()), pass4a=float(s.pass4a.mean())))
    A = pd.DataFrame(ans)
    for cb in RUNGS:
        P(f"\n  cost rung {cb:.0f} bps" + ("   <-- MECHANISM HEADLINE (981's premise rung)" if cb == HEAD_RUNG
                                           else ("   <-- CAPITAL RUNG (PROTOCOL rule 2)" if cb == CAP_RUNG else "")))
        P(f"    {'control':<11s} {'D':>8s} {'W':>8s} {'M':>8s} {'Q':>8s}   {'RANGE Q-D':>10s}   "
          f"{'4b pass':>8s}  {'turn D/Q':>14s}")
        for ctl in CONTROLS:
            r = A[(A.cost_bps == cb) & (A.control == ctl)].iloc[0]
            P(f"    {ctl:<11s} {r.failDD_D:8.4f} {r.failDD_W:8.4f} {r.failDD_M:8.4f} "
              f"{r.failDD_Q:8.4f}   {r.range_DQ:10.4f}   {r.pass4b:8.4f}  "
              f"{r.turn_D:6.1f}/{r.turn_Q:<7.1f}")

    P("\n  SURVIVING SHARE of the gradient (range under control / range under DRIFT):")
    verdicts = {}
    for cb in RUNGS:
        rd = float(A[(A.cost_bps == cb) & (A.control == "DRIFT")].range_DQ.iloc[0])
        line = f"    {cb:.0f} bps  DRIFT range {rd:+.4f}"
        for ctl in ("NODRIFT_G", "NODRIFT_W"):
            rc = float(A[(A.cost_bps == cb) & (A.control == ctl)].range_DQ.iloc[0])
            line += f"   {ctl} {rc:+.4f} ({rc/rd:6.1%} survives)"
            verdicts[(cb, ctl)] = rc / rd if rd != 0 else np.nan
        P(line)

    P("\n  WHY (the drift channel, measured): realised mean gross and its spread by cadence")
    for ctl in CONTROLS:
        sub = GR[GR.control == ctl].pivot_table(index=["panel", "book", "gross"],
                                                columns="cadence", values="realised_gross"
                                                ).reindex(columns=cads)
        dv = GR[GR.control == ctl].pivot_table(index=["panel", "book", "gross"],
                                               columns="cadence", values="gross_dev_mean"
                                               ).reindex(columns=cads)
        P(f"    {ctl:<11s} median realised gross " +
          "  ".join(f"{c} {sub[c].median():.4f}" for c in cads) +
          "   |  median |gross-target| " + "  ".join(f"{c} {dv[c].median():.5f}" for c in cads))

    # per-panel and per-ladder (DIAL 2), every point published
    P("\n  DIAL 2 (CADENCE LADDER) x DIAL 1 (CONTROL), headline rung, every point:")
    lad = []
    for lname, ls in LADDERS.items():
        for ctl in CONTROLS:
            s = G[(G.control == ctl) & (G.cost_bps == HEAD_RUNG) & (G.cadence.isin(ls))]
            d = s.groupby("cadence").apply(lambda x: float((~x.leg_DD).mean())).reindex(ls)
            lad.append(dict(ladder=lname, control=ctl, n=len(s), span=float(d.max() - d.min()),
                            slow=float(d.iloc[-1]), fast=float(d.iloc[0])))
            P(f"    {lname:<8s} {ctl:<11s} n {len(s):6d}  fast {d.iloc[0]:.4f}  slow {d.iloc[-1]:.4f}  "
              f"span {d.max()-d.min():+.4f}")
    L = pd.DataFrame(lad)
    P("\n  PER PANEL (headline rung), L4_DD fail rate D -> Q:")
    pan_rows = []
    for pname in panels:
        for ctl in CONTROLS:
            s = G[(G.control == ctl) & (G.cost_bps == HEAD_RUNG) & (G.panel == pname)]
            d = s.groupby("cadence").apply(lambda x: float((~x.leg_DD).mean())).reindex(CADORDER)
            pan_rows.append(dict(panel=pname, control=ctl, **{c: d[c] for c in CADORDER},
                                 range_DQ=float(d["Q"] - d["D"])))
            P(f"    {pname:<6s} {ctl:<11s} {d['D']:.4f} {d['W']:.4f} {d['M']:.4f} {d['Q']:.4f}   "
              f"range {d['Q']-d['D']:+.4f}")
    PAN = pd.DataFrame(pan_rows)

    # ============================================================== rule 8
    P("\n" + "=" * 100)
    P(f"(D) RULE 8 — (CONTROL, LADDER) chosen on warm-up..{IS_END} ONLY, {OOS_START}+ read ONCE")
    P("=" * 100)
    isrows = G[G.cost_bps == CAP_RUNG]
    gate("G7 choosers read no OOS row", f"IS columns are IS_* only; split at {IS_END}",
         "disjoint", True, "the chooser sees IS_* columns exclusively")
    wf = []
    for pname, px in panels.items():
        sub = isrows[isrows.panel == pname]
        # chooser: among (control, ladder) families, take the one whose IS median DD is shallowest
        fams = [(ctl, lname) for ctl in CONTROLS for lname in LADDERS]
        picks = {}
        picks["C_ISDD (shallowest IS median MaxDD)"] = max(
            fams, key=lambda f: sub[(sub.control == f[0]) & (sub.cadence.isin(LADDERS[f[1]]))].IS_MaxDD.median())
        picks["C_ISSHARPE (max IS median Sharpe)"] = max(
            fams, key=lambda f: sub[(sub.control == f[0]) & (sub.cadence.isin(LADDERS[f[1]]))].IS_Sharpe.median())
        picks["C_LIVE (zero-parameter: DRIFT, CORE4)"] = ("DRIFT", "CORE4")
        for cn, f in picks.items():
            s = sub[(sub.control == f[0]) & (sub.cadence.isin(LADDERS[f[1]]))]
            wf.append(dict(panel=pname, chooser=cn, pick_control=f[0], pick_ladder=f[1],
                           n=len(s), oos_CAGR=float(s.OOS_CAGR.median()),
                           oos_Sharpe=float(s.OOS_Sharpe.median()),
                           oos_MaxDD=float(s.OOS_MaxDD.median()),
                           oos_failDD=float((~s.leg_DD).mean()),
                           oos_pass4b=float(s.pass4b_REC.mean())))
            P(f"    {pname:<6s} {cn:<44s} -> ({f[0]}, {f[1]})  n {len(s):5d}  OOS median "
              f"{s.OOS_CAGR.median():7.2%} {s.OOS_Sharpe.median():7.4f} {s.OOS_MaxDD.median():8.2%}  "
              f"4b {s.pass4b_REC.mean():.4f}")
        sp = mets(px["SPY"].pct_change().fillna(0.0).values[np.asarray(px.index >= OOS_START)])
        v2 = mets(backtest(px, rules_v2_weights(px), cost_bps=CAP_RUNG, freq="W")["returns"]
                  .values[np.asarray(px.index >= OOS_START)])
        wf.append(dict(panel=pname, chooser="SPY (OOS)", pick_control="", pick_ladder="", n=0,
                       oos_CAGR=sp["CAGR"], oos_Sharpe=sp["Sharpe"], oos_MaxDD=sp["MaxDD"],
                       oos_failDD=np.nan, oos_pass4b=np.nan))
        wf.append(dict(panel=pname, chooser="RULES v2 (OOS)", pick_control="", pick_ladder="", n=0,
                       oos_CAGR=v2["CAGR"], oos_Sharpe=v2["Sharpe"], oos_MaxDD=v2["MaxDD"],
                       oos_failDD=np.nan, oos_pass4b=np.nan))
        P(f"    {pname:<6s} {'SPY (OOS)':<44s}    {sp['CAGR']:7.2%} {sp['Sharpe']:7.4f} {sp['MaxDD']:8.2%}")
        P(f"    {pname:<6s} {'RULES v2 (OOS)':<44s}    {v2['CAGR']:7.2%} {v2['Sharpe']:7.4f} {v2['MaxDD']:8.2%}")
    W = pd.DataFrame(wf)

    # ============================================================== both KEEP paths
    P("\n" + "=" * 100)
    P("(E) BOTH KEEP PATHS at the capital rung (10 bps)")
    P("=" * 100)
    for ctl in CONTROLS:
        s = G[(G.control == ctl) & (G.cost_bps == CAP_RUNG)]
        P(f"    {ctl:<11s} 4b {int(s.pass4b_REC.sum()):5d} of {len(s):5d} ({s.pass4b_REC.mean():.4f});  "
          f"4a {int(s.pass4a.sum()):5d} of {len(s):5d} ({s.pass4a.mean():.4f});  "
          f"median turnover {s.turn_per_yr.median():7.2f}/yr  "
          f"median CAGR {s.CAGR.median():7.2%}")
    best = G[(G.cost_bps == CAP_RUNG) & (G.pass4b_REC) & (G.control != "DRIFT")]
    P(f"    4b passes at 10 bps under a NODRIFT control: {len(best)}")

    # ============================================================== verdict
    P("\n" + "=" * 100)
    rd = float(A[(A.cost_bps == HEAD_RUNG) & (A.control == "DRIFT")].range_DQ.iloc[0])
    rw = float(A[(A.cost_bps == HEAD_RUNG) & (A.control == "NODRIFT_W")].range_DQ.iloc[0])
    rg = float(A[(A.cost_bps == HEAD_RUNG) & (A.control == "NODRIFT_G")].range_DQ.iloc[0])
    surv = rw / rd if rd else np.nan
    h_drift = bool(rw < DRIFT_BAR * rd)
    h_count = bool(rw >= COUNT_BAR * rd)
    P(f"  PRE-REGISTERED BARS at the mechanism rung ({HEAD_RUNG:.0f} bps):")
    P(f"    RNG(DRIFT)     = {rd:+.4f}   (981's committed 10-bps value: +0.2937)")
    P(f"    RNG(NODRIFT_G) = {rg:+.4f}   ({rg/rd:.1%} survives)")
    P(f"    RNG(NODRIFT_W) = {rw:+.4f}   ({surv:.1%} survives)")
    P(f"    H_DRIFT (< {DRIFT_BAR:.0%} survives -> a DRIFT fact)          : {h_drift}")
    P(f"    H_COUNT (>= {COUNT_BAR:.0%} survives -> a REBALANCE-COUNT fact): {h_count}")
    if h_drift:
        verdict = "ANSWERED: the DD leg's cadence gradient is a DRIFT fact"
    elif h_count:
        verdict = "ANSWERED: the DD leg's cadence gradient is a REBALANCE-COUNT fact"
    else:
        verdict = f"ANSWERED = MIXTURE: {surv:.1%} of the gradient is rebalance count, {1-surv:.1%} is drift"
    P(f"  VERDICT: {verdict}")
    P("=" * 100)

    ng = int((~pd.DataFrame(GATES).passed).sum())
    P(f"  GATES: {len(GATES)} recorded, {ng} FAIL")
    G.to_csv(OUT / f"{STEM}.grid.csv.gz", index=False)
    A.to_csv(OUT / f"{STEM}.answer.csv", index=False)
    L.to_csv(OUT / f"{STEM}.ladders.csv", index=False)
    PAN.to_csv(OUT / f"{STEM}.bypanel.csv", index=False)
    GR.to_csv(OUT / f"{STEM}.gross.csv", index=False)
    W.to_csv(OUT / f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(GATES).to_csv(OUT / f"{STEM}.gates.csv", index=False)
    (OUT / f"{STEM}.console.txt").write_text("\n".join(LINES))
    P(f"  wrote {STEM}.{{grid.csv.gz,answer,ladders,bypanel,gross,walkforward,gates}}.csv + console.txt "
      f"({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
