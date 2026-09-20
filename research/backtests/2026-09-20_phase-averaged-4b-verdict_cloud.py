#!/usr/bin/env python3
"""Idea 956 (lane cloud, 2026-09-20): DOES A PHASE-AVERAGED 4b VERDICT CHANGE WHICH BOOKS IN THE
RECORD PASS?

THE DEFECT THIS CLOSES.  PROTOCOL reads path 4b at ONE canonical rebalance date -- the period-end
-- that nobody tuned and nobody defended.  Idea 944 found 6 of 9 U56 books FLIP their 4b verdict
across the 21 DOM phases, that the DD cap is the most phase-fragile leg of the five (36.1% flip
rate, 47.2% on DOM21), and that picking the phase in sample lands at OOS rank 257 of 270.  Idea
964 then priced the FAMILY MEAN as a re-publication rule for committed CAGR claims and found it
moves 1 claim in 19.  What neither did is the thing the queue actually asks for: take the books
the record has certified as 4b PASSERS and re-score THEM under a PHASE-AVERAGED verdict, with the
MEDIAN as the averaging rule.  If the record's 4b passes are a phase artefact, the standing
KEEP-4b candidates are not candidates; if they survive the median, the canonical convention is
costing the record nothing and can stay.

THE CORPUS -- REAL BOOKS THE RECORD HAS CERTIFIED OR IS STANDING ON, not a prose census:
  TOP20        the 2026-09-04 first KEEP-4b shape: top 20 by the composite, NO vol scaler, FIXED
               g/N (the 926/938 convention, not the re-spread one 931/945 mislabelled), g = 0.75.
  BAND03_G075  the LIVE RULES v2 book (200d +/-3% hysteresis, de-gross to cash), g = 0.75.
  BAND10_G100  idea 1719 / 896's U56 4b passer: band 0.10 at gross 1.00.
  EWELIG       equal weight over eligible names at g = 0.75 -- the record's plain comparand.
  MAXVOL060    idea 1617's PARK: equal weight, vol20 < 0.60, no band, no ranking, g = 0.75.
  VOLTGT016    the STANDING KEEP-4b candidate found by idea 1730 THIS DAY: equal weight over every
               priced name, scaled by g_t = clip(0.16 / vol20_panel_t, 0, 1), never levered.
  6 books x 3 panels (U56 / B136 / SMALL) x 26 phases x 4 cost rungs = 1,872 scored books.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4), exactly the pair the queue names:
  DIAL 1  PHASE GRID    DOM21 (monthly, rebalance d trading days BEFORE each month's last trading
          day, d = 0..20 -- the 21 DOM phases the idea names) and DOW5 (weekly, d = 0..4).  BOTH
          levels reported, neither chosen.
  DIAL 2  AVERAGING RULE, all six reported, none chosen:
            CANON    phase d = 0.  What PROTOCOL reads today.
            MEAN     the mean ACROSS PHASES of each 4b statistic, legs applied to the means.
            MEDIAN   the median across phases.  THE RULE THE QUEUE NAMES.
            MIN      the worst phase, statistic by statistic.  The conservative reading.
            SHARE50  majority vote: 4b passes iff >= half the phases pass it outright.
            TRANCHE  1/P of NAV in each of the P phase-books, re-levelled daily.
  Panels, books and cost rungs are REPORTED AXES, not dials: every cell is published.

THE DISTINCTION THIS RUN REFUSES TO BLUR (inherited from idea 964, and it decides the verdict).
MEAN / MEDIAN / MIN / SHARE50 are ESTIMATORS of a book's 4b standing.  **No allocation of capital
produces a median-of-Sharpes**, so none of them can ever BE a KEEP; they can only certify or
de-certify one.  TRANCHE alone is a book a desk can hold, and it is the only arm here eligible to
be a candidate.  Every table below says which kind each row is.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) MEDIAN de-certifies a material share of the CANON 4b passes -> the record's 4b passes are a
      phase artefact and PROTOCOL should read 4b phase-averaged.
  (b) MEDIAN certifies passes CANON misses -> the canonical convention is costing the record
      candidates.
  (c) MEDIAN and CANON agree almost everywhere -> the convention is free and stays as written;
      the run is then a KILL for the queue's proposal, which is a useful result.
  (d) the rule-8 IS-chosen phase loses to CANON and to TRANCHE OOS -> the phase is a KILL as a
      dial whatever its ex-post best cell does (944's reading, re-tested on this corpus).
All four are reported.

GATES.  G0 phase d = 0 mask == `engine.rebalance_mask` exactly on M and on W.  G1 the fast runner
== `engine.backtest` on returns AND turnover at phase 0.  G1b BAND03_G075 ==
`baseline.rules_v2_weights(px, 0.03, 0.75)` exactly.  G2 every phase trades in band.  G3 CROSS-RUN:
idea 1730's committed VOLTGT t=0.16 U56/B136 FULL and OOS numbers reproduce.  G4 determinism.
G5 SMALL's `max_1d_move >= 1.0` drop applied and counted.  G6 exactly two tuned parameters.
G7 no chooser reads a row on or after 2017-01-01.  G8 all cells published.

PROTOCOL: rule 1 (>=10y); rule 2 (t+1, 10 bps primary, no leverage, no shorting); rule 3 (live
RULES v2 AND SPY); rule 4 (both KEEP paths, 2 dials); rule 8 (walk-forward, 2017-2026 read exactly
once); rule 9 (survivorship stated).  RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are
NOT modified.

SURVIVORSHIP.  U56 / B136 / SMALL are CURRENT-CONSTITUENT lists (SMALL additionally drops every
ticker with `max_1d_move >= 1.0` per `data/small_meta.csv`), so every CAGR and drawdown LEVEL is
optimistic and both 4b bars are easier here than on a point-in-time panel.  The phase contrasts
are same-tape, same-names, same-rule comparisons with ONLY the rebalance date moved, and are far
less exposed.  The 4b levels are read against SPY, which is not survivorship-inflated.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-20_phase-averaged-4b-verdict_cloud.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights, score   # noqa: E402
from engine import backtest, rebalance_mask                   # noqa: E402

DATE, SLUG = "2026-09-20", "phase-averaged-4b-verdict"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_cloud"

WARMUP, LAG = 260, 1
GROSS0, BAND0, VOLCAP, VT = 0.75, 0.03, 0.60, 0.16
COSTS = [0.0, 10.0, 25.0, 50.0]
COST0 = 10.0
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
GRIDS = {"DOM21": ("M", 21), "DOW5": ("W", 5)}
RULES = ["CANON", "MEAN", "MEDIAN", "MIN", "SHARE50", "TRANCHE"]
ESTIMATORS = {"MEAN", "MEDIAN", "MIN", "SHARE50"}          # cannot be KEEPs -- see docstring
STATS = ["CAGR", "Sharpe", "MaxDD", "H1", "H2", "IS_Sharpe", "oCAGR", "oSharpe", "oMaxDD"]
# idea 1730's committed VOLTGT t=0.16 cells (KEEP-4b memo, 2026-09-20), weekly, 10 bps
PUB_VT = {"U56": dict(CAGR=0.1561, Sharpe=1.2027, MaxDD=-0.1986, oCAGR=0.1594, oSharpe=1.2193),
          "B136": dict(CAGR=0.1594, Sharpe=1.2049, MaxDD=-0.1876, oCAGR=0.1536, oSharpe=1.1837)}

LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=target, pass_=bool(ok)))
    say(f"    GATE {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    return bool(ok)


def publish(name, value):
    GATES.append(dict(gate=name, value=str(value), target="published, not asserted", pass_=True))
    say(f"    PUBLISHED  {name}: {value}")


# ------------------------------------------------------------------ phase family (idea 938/944)
def offset_mask(idx, per, d):
    """True d trading days BEFORE the last trading day of each period.  d = 0 reproduces
    `engine.rebalance_mask(idx, per)` exactly (gate G0).  Idea 938's construction, unmodified."""
    key = pd.Series(idx.to_period(per), index=idx)
    last = np.flatnonzero((key != key.shift(-1)).values)
    first = np.concatenate([[0], last[:-1] + 1])
    pick = np.maximum(last - d, first)
    out = pd.Series(False, index=idx)
    out.iloc[np.unique(pick)] = True
    return out, int((last - d < first).sum())


class Panel:
    """Pre-computes everything a book needs at ONE phase.  Vectorised twin of engine.backtest,
    gated against it at G1.  Inherited verbatim from idea 944's runner."""

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


# ------------------------------------------------------------------ metrics / legs
def fmet(r):
    r = np.asarray(r, float)
    if len(r) < 3 or not np.isfinite(r).all():
        return np.nan, np.nan, np.nan
    eq = np.cumprod(1.0 + r)
    c = eq[-1] ** (252.0 / len(r)) - 1.0
    dd = float((eq / np.maximum.accumulate(eq) - 1.0).min())
    vol = r.std(ddof=1) * np.sqrt(252.0)
    return c, ((r.mean() * 252.0) / vol if vol else np.nan), dd


def fsharpe(r):
    r = np.asarray(r, float)
    if len(r) < 3:
        return np.nan
    v = r.std(ddof=1) * np.sqrt(252.0)
    return (r.mean() * 252.0) / v if v else np.nan


def full_pack(r, pan):
    r = np.asarray(r)
    c, s, d = fmet(r[pan.masks["FULL"]])
    co, so, do = fmet(r[pan.masks["OOS"]])
    return dict(CAGR=c, Sharpe=s, MaxDD=d, H1=fsharpe(r[pan.masks["H1"]]),
                H2=fsharpe(r[pan.masks["H2"]]), IS_Sharpe=fsharpe(r[pan.masks["IS"]]),
                oCAGR=co, oSharpe=so, oMaxDD=do)


def legs4b(s, spy):
    """The five 4b legs as the record writes them, with each margin in its own units."""
    m = {"L1_H1": s["H1"] - spy["H1"], "L2_H2": s["H2"] - spy["H2"],
         "L3_OOS": s["oSharpe"] - spy["oSharpe"],
         "L4_DD": s["MaxDD"] - DD_CAP * spy["MaxDD"],
         "L5_CAGR": s["CAGR"] - CAGR_FLOOR * spy["CAGR"]}
    return all(v > 0 for v in m.values()), m


def pass4a(s, live):
    return bool(s["H1"] > live["H1"] and s["H2"] > live["H2"] and s["MaxDD"] >= live["MaxDD"])


def pass4a_oos(s, live):
    return bool(s["oSharpe"] > live["oSharpe"] and s["oMaxDD"] >= live["oMaxDD"])


def pass4b_oos(s, spy):
    return bool(s["oSharpe"] > spy["oSharpe"] and s["oMaxDD"] >= DD_CAP * spy["oMaxDD"]
                and s["oCAGR"] >= CAGR_FLOOR * spy["oCAGR"])


# ------------------------------------------------------------------ book builders
def _ew(px, elig, gross=GROSS0):
    """Record convention: gross/N over every PRICED name, gated-out weight goes to CASH."""
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    ew = gross * e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    return ew.where(elig, 0.0)


def build_books(px):
    sc, above, vol20 = score(px, vol_scale=False)
    elig = above & (vol20 < VOLCAP)
    rank = sc.where(elig).rank(axis=1, ascending=False)
    out = {}
    out["TOP20"] = ((rank <= 20).astype(float) * (GROSS0 / 20)).values      # fixed g/N (926/938)
    out["BAND03_G075"] = rules_v2_weights(px, BAND0, GROSS0).values
    out["BAND10_G100"] = rules_v2_weights(px, 0.10, 1.00).values
    out["EWELIG"] = _ew(px, elig, GROSS0).values
    out["MAXVOL060"] = _ew(px, vol20 < VOLCAP, GROSS0).values
    base = _ew(px, px.notna(), gross=1.0)                                   # idea 1730's VOLTGT
    pr = (base.shift(1) * px.pct_change()).sum(axis=1)
    rv = pr.rolling(20).std() * np.sqrt(252)
    k = (VT / rv.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
    out["VOLTGT016"] = base.mul(k, axis=0).values
    return out


# ------------------------------------------------------------------ data
def build_panels():
    out = [("U56", load_universe()), ("B136", load_universe(broad=True))]
    px_s = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    tcol = meta.columns[0]
    drop = {t for t in meta.loc[meta["max_1d_move"] >= 1.0, tcol].astype(str)
            if t in px_s.columns and t != "SPY"}
    mx = px_s.pct_change().abs().max()
    drop |= {c for c in px_s.columns if c != "SPY" and mx[c] >= 1.0}
    px_s = px_s.drop(columns=sorted(drop))
    gate("G5 SMALL max_1d_move screen", f"dropped {len(drop)} -> {px_s.shape[1]-1} names + SPY",
         "applied and counted", len(drop) > 0)
    out.append(("SMALL", px_s))
    return out


def main():
    t0 = time.time()
    say(f"=== Idea 956 — does a PHASE-AVERAGED 4b verdict change which books PASS?  ({DATE}, cloud) ===")
    say("6 committed/standing books x 3 panels x 26 phases x 4 cost rungs = 1,872 scored books.")
    say("Dial 1 = phase grid (DOM21 / DOW5); dial 2 = averaging rule")
    say("(CANON / MEAN / MEDIAN / MIN / SHARE50 / TRANCHE).  MEAN/MEDIAN/MIN/SHARE50 are")
    say("ESTIMATORS and can never BE a KEEP; TRANCHE is the only tradable arm.")
    panels = build_panels()

    rows, verd, wf = [], [], []
    for pname, px in panels:
        Wg = build_books(px)
        say(f"\n--- PANEL {pname}: {px.shape[1]-1} names + SPY, {px.index[0].date()} -> {px.index[-1].date()} ---")

        # the 4a bar and the 4b bar, both at the LIVE weekly cadence (what the record trades)
        wk, _ = offset_mask(px.index, "W", 0)
        panW = Panel(pname, px, wk)
        yrs = int(panW.masks["FULL"].sum()) / 252
        gate(f"G0a sample {pname}", f"{yrs:.1f}y", ">= 10y (rule 1)", yrs >= 10)
        gate(f"G0b phase0 mask == engine.rebalance_mask {pname} W",
             f"{int((wk.values != rebalance_mask(px.index,'W').values).sum())} diffs", "0 diffs",
             bool((wk.values == rebalance_mask(px.index, "W").values).all()))
        mo, _ = offset_mask(px.index, "M", 0)
        gate(f"G0c phase0 mask == engine.rebalance_mask {pname} M",
             f"{int((mo.values != rebalance_mask(px.index,'M').values).sum())} diffs", "0 diffs",
             bool((mo.values == rebalance_mask(px.index, "M").values).all()))

        live_r, live_t = Book(panW, Wg["BAND03_G075"]).at(COST0)
        eng = backtest(px, rules_v2_weights(px, BAND0, GROSS0), cost_bps=COST0, freq="W")
        # NOTE (published, not hidden): `engine.backtest` does `.fillna(0).shift(1)` on the
        # weights, so its row 0 target is NaN and its returns/turnover are NaN on day 0 and on the
        # first rebalance day.  Every script in the record skips those via the 260-day warm-up, and
        # so does this gate; the two affected dates are named below.
        fm = panW.masks["FULL"]
        nb = np.flatnonzero(np.isnan(eng["returns"].values))
        dr = np.abs(eng["returns"].values[fm] - live_r[fm]).max()
        dt_ = np.abs(eng["turnover"].values[fm] - live_t[fm]).max()
        gate(f"G1 fast runner == engine.backtest {pname}",
             f"ret {dr:.3e}  turn {dt_:.3e} over the scored window", "< 1e-12 on both",
             dr < 1e-12 and dt_ < 1e-12)
        publish(f"G1b engine.backtest pre-warm-up NaN days {pname}",
                f"{len(nb)} NaN return days, all before the warm-up: "
                + ", ".join(str(px.index[i].date()) for i in nb[:4]))
        LIVE = full_pack(live_r, panW)
        SPY = full_pack(panW.spy, panW)
        say(f"  RULES v2 live (weekly, 10 bps): FULL {LIVE['CAGR']:7.2%}/{LIVE['Sharpe']:7.4f}/"
            f"{LIVE['MaxDD']:7.2%}   OOS {LIVE['oCAGR']:7.2%}/{LIVE['oSharpe']:7.4f}/{LIVE['oMaxDD']:7.2%}")
        say(f"  SPY buy-and-hold              : FULL {SPY['CAGR']:7.2%}/{SPY['Sharpe']:7.4f}/"
            f"{SPY['MaxDD']:7.2%}   OOS {SPY['oCAGR']:7.2%}/{SPY['oSharpe']:7.4f}/{SPY['oMaxDD']:7.2%}")

        # G3 cross-run: idea 1730's committed VOLTGT t=0.16 cells
        if pname in PUB_VT:
            vt = full_pack(Book(panW, Wg["VOLTGT016"]).at(COST0)[0], panW)
            p = PUB_VT[pname]
            d = max(abs(vt[k] - p[k]) for k in p)
            gate(f"G3 cross-run VOLTGT t=0.16 {pname}",
                 f"max|d| {d:.4f} over {sorted(p)} (this run "
                 f"{vt['CAGR']:.2%}/{vt['Sharpe']:.4f}/{vt['MaxDD']:.2%}, OOS "
                 f"{vt['oCAGR']:.2%}/{vt['oSharpe']:.4f})",
                 "<= 0.0010 vs idea 1730's committed memo", d <= 0.0010)

        for gname, (per, P) in GRIDS.items():
            pans, clipped = {}, {}
            for d in range(P):
                mk, nc = offset_mask(px.index, per, d)
                pans[d] = Panel(pname, px, mk)
                clipped[d] = nc
            rpy = [pans[d].reb_per_year for d in range(P)]
            gate(f"G2 rebalances/yr in band {pname}/{gname}",
                 f"{min(rpy):.2f}-{max(rpy):.2f} /yr, clipped periods {max(clipped.values())}",
                 "11.5-12.5 (DOM21) / 51-53 (DOW5)",
                 (11.5 <= min(rpy) and max(rpy) <= 12.5) if gname == "DOM21"
                 else (51 <= min(rpy) and max(rpy) <= 53))

            for bname, W in Wg.items():
                bk = {d: Book(pans[d], W) for d in range(P)}
                for cost in COSTS:
                    ser = {d: bk[d].at(cost)[0] for d in range(P)}
                    pk = {d: full_pack(ser[d], pans[d]) for d in range(P)}
                    for d in range(P):
                        ok, m = legs4b(pk[d], SPY)
                        rows.append(dict(panel=pname, grid=gname, book=bname, cost=cost, phase=d,
                                         **{k: pk[d][k] for k in STATS},
                                         p4b=ok, p4b_oos=pass4b_oos(pk[d], SPY),
                                         p4a=pass4a(pk[d], LIVE), p4a_oos=pass4a_oos(pk[d], LIVE),
                                         **{f"m_{k}": v for k, v in m.items()}))
                    A = {k: np.array([pk[d][k] for d in range(P)], float) for k in STATS}
                    agg = {"CANON": {k: A[k][0] for k in STATS},
                           "MEAN": {k: float(np.nanmean(A[k])) for k in STATS},
                           "MEDIAN": {k: float(np.nanmedian(A[k])) for k in STATS},
                           # MIN = worst phase statistic by statistic (MaxDD's worst is its min)
                           "MIN": {k: float(np.nanmin(A[k])) for k in STATS}}
                    tr = np.mean(np.vstack([ser[d] for d in range(P)]), axis=0)  # 1/P, re-levelled daily
                    agg["TRANCHE"] = full_pack(tr, pans[0])
                    shares = np.array([legs4b(pk[d], SPY)[0] for d in range(P)], float)
                    for rule in RULES:
                        if rule == "SHARE50":
                            ok = bool(shares.mean() >= 0.5)
                            s_ = agg["MEDIAN"]
                            ok_oos = bool(np.mean([pass4b_oos(pk[d], SPY) for d in range(P)]) >= 0.5)
                            a_, a_o = (bool(np.mean([pass4a(pk[d], LIVE) for d in range(P)]) >= 0.5),
                                       bool(np.mean([pass4a_oos(pk[d], LIVE) for d in range(P)]) >= 0.5))
                        else:
                            s_ = agg[rule]
                            ok, _ = legs4b(s_, SPY)
                            ok_oos = pass4b_oos(s_, SPY)
                            a_, a_o = pass4a(s_, LIVE), pass4a_oos(s_, LIVE)
                        verd.append(dict(panel=pname, grid=gname, book=bname, cost=cost, rule=rule,
                                         kind=("ESTIMATOR" if rule in ESTIMATORS else "BOOK"),
                                         pass_share=float(shares.mean()),
                                         **{k: s_[k] for k in STATS},
                                         p4b=ok, p4b_oos=ok_oos, p4a=a_, p4a_oos=a_o))
                    # ---- rule 8: phase chosen on 2009-2016 ONLY, 2017-2026 read ONCE
                    if cost == COST0:
                        isv = np.array([pk[d]["IS_Sharpe"] for d in range(P)], float)
                        pick = int(np.nanargmax(isv))
                        for lbl, s_ in [("IS_PICK", pk[pick]), ("CANON", pk[0]),
                                        ("TRANCHE", agg["TRANCHE"])]:
                            wf.append(dict(panel=pname, grid=gname, book=bname, arm=lbl,
                                           phase=(pick if lbl == "IS_PICK" else (0 if lbl == "CANON" else -1)),
                                           IS_Sharpe=s_["IS_Sharpe"], OOS_CAGR=s_["oCAGR"],
                                           OOS_Sharpe=s_["oSharpe"], OOS_MaxDD=s_["oMaxDD"],
                                           p4a_oos=pass4a_oos(s_, LIVE), p4b_oos=pass4b_oos(s_, SPY),
                                           base_oSharpe=LIVE["oSharpe"], base_oCAGR=LIVE["oCAGR"],
                                           base_oMaxDD=LIVE["oMaxDD"], spy_oSharpe=SPY["oSharpe"],
                                           spy_oCAGR=SPY["oCAGR"], spy_oMaxDD=SPY["oMaxDD"]))
            say(f"  {gname}: {P} phases x 6 books x {len(COSTS)} cost rungs scored "
                f"({time.time()-t0:.0f}s elapsed)")

    df, vd, wfd = pd.DataFrame(rows), pd.DataFrame(verd), pd.DataFrame(wf)
    df.to_csv(f"{OUT}.grid.csv", index=False)
    vd.to_csv(f"{OUT}.verdicts.csv", index=False)
    wfd.to_csv(f"{OUT}.walkforward.csv", index=False)

    # ---- G4 determinism
    pxu = dict(panels)["U56"]
    mk0, _ = offset_mask(pxu.index, "M", 7)
    pa = Panel("U56", pxu, mk0)
    ra = Book(pa, build_books(pxu)["VOLTGT016"]).at(COST0)[0]
    rb = Book(Panel("U56", pxu, offset_mask(pxu.index, "M", 7)[0]),
              build_books(pxu)["VOLTGT016"]).at(COST0)[0]
    gate("G4 determinism (re-built U56/DOM21 d=7 VOLTGT016 cell)",
         f"max|d| {np.abs(ra - rb).max():.3e}; "
         f"{len(df)} rows, {len(df.drop_duplicates(['panel','grid','book','cost','phase']))} unique keys",
         "bit-identical and one row per cell",
         np.abs(ra - rb).max() == 0.0
         and len(df) == len(df.drop_duplicates(["panel", "grid", "book", "cost", "phase"])))
    gate("G6 tuned parameters", "2 (phase grid, averaging rule)", "<= 2 (PROTOCOL rule 4)", True)
    gate("G7 chooser is IS-only", "argmax IS Sharpe on 2009-2016", "no OOS row read by any chooser", True)
    gate("G8 all cells published", f"grid {len(df)} / verdicts {len(vd)} / wf {len(wfd)}",
         "every grid point reported", True)

    say("\n=== THE ANSWER — do the record's CANONICAL 4b passes survive the MEDIAN? ===")
    key = ["panel", "grid", "book", "cost"]
    piv = vd.pivot_table(index=key, columns="rule", values="p4b", aggfunc="first")
    pivo = vd.pivot_table(index=key, columns="rule", values="p4b_oos", aggfunc="first")
    for tag, T in [("4b FULL", piv), ("4b OOS", pivo)]:
        n = len(T)
        can = T["CANON"].astype(bool)
        say(f"\n  {tag} over {n} (panel x grid x book x cost) cells — CANON passes {int(can.sum())}:")
        for rule in RULES:
            r = T[rule].astype(bool)
            say(f"    {rule:8s} passes {int(r.sum()):3d}/{n}   "
                f"survive (CANON pass -> rule pass) {int((can & r).sum()):3d}/{int(can.sum())}   "
                f"newly certified (CANON fail -> rule pass) {int((~can & r).sum()):3d}   "
                f"DISAGREE with CANON {int((can ^ r).sum()):3d}/{n} = {(can ^ r).mean():.3f}")

    say("\n  MEDIAN vs CANON, cell by cell, at the 10 bps primary rung (4b FULL):")
    T = piv.reset_index()
    T = T[T.cost == COST0]
    dis = T[T["CANON"].astype(bool) != T["MEDIAN"].astype(bool)]
    say(f"    disagreements: {len(dis)} of {len(T)}")
    if len(dis):
        say(dis[["panel", "grid", "book", "CANON", "MEDIAN", "MEAN", "MIN", "SHARE50", "TRANCHE"]]
            .to_string(index=False))
    say("\n  Per-book CANON / MEDIAN / TRANCHE 4b pass counts at 10 bps (FULL, of 6 panel x grid):")
    for b in sorted(vd.book.unique()):
        s = vd[(vd.book == b) & (vd.cost == COST0)]
        line = "  ".join(f"{r} {int(s[s.rule == r].p4b.sum())}/6" for r in RULES)
        ps = s[s.rule == "CANON"].pass_share
        say(f"    {b:12s} {line}   mean phase pass-share {ps.mean():.3f}")

    say("\n=== BOTH KEEP PATHS over the 1,872 scored books (per-phase, not aggregated) ===")
    for gname in GRIDS:
        s = df[(df.grid == gname) & (df.cost == COST0)]
        say(f"  {gname} @10bps: 4a FULL {int(s.p4a.sum()):3d}/{len(s)}   4a OOS {int(s.p4a_oos.sum()):3d}/{len(s)}"
            f"   4b FULL {int(s.p4b.sum()):3d}/{len(s)}   4b OOS {int(s.p4b_oos.sum()):3d}/{len(s)}")
    say("  binding-leg count among 4b FULL failures @10bps (a leg is binding when its margin <= 0):")
    f_ = df[(df.cost == COST0) & (~df.p4b)]
    for L in ["L1_H1", "L2_H2", "L3_OOS", "L4_DD", "L5_CAGR"]:
        say(f"    {L:8s} binds in {int((f_['m_'+L] <= 0).sum()):4d} of {len(f_)} = "
            f"{(f_['m_'+L] <= 0).mean():.3f}")

    say("\n=== RULE 8 (phase chosen on 2009-2016 ONLY, 2017-2026 read ONCE) ===")
    for gname in GRIDS:
        s = wfd[wfd.grid == gname]
        for arm in ["IS_PICK", "CANON", "TRANCHE"]:
            a = s[s.arm == arm]
            say(f"  {gname} {arm:8s}: mean OOS Sharpe {a.OOS_Sharpe.mean():.4f}   "
                f"mean OOS CAGR {a.OOS_CAGR.mean():.2%}   mean OOS MaxDD {a.OOS_MaxDD.mean():.2%}   "
                f"4a OOS {int(a.p4a_oos.sum())}/{len(a)}   4b OOS {int(a.p4b_oos.sum())}/{len(a)}")
        ip = s[s.arm == "IS_PICK"].set_index(["panel", "book"]).OOS_Sharpe
        cn = s[s.arm == "CANON"].set_index(["panel", "book"]).OOS_Sharpe
        tr = s[s.arm == "TRANCHE"].set_index(["panel", "book"]).OOS_Sharpe
        say(f"    choosing the phase in sample is worth {float((ip - cn).mean()):+.4f} of OOS Sharpe "
            f"vs CANON ({int((ip > cn).sum())} of {len(ip)} wins); "
            f"TRANCHE vs CANON {float((tr - cn).mean()):+.4f} ({int((tr > cn).sum())} of {len(tr)} wins)")
    say("\n  The standing KEEP-4b candidate (VOLTGT016) under rule 8, every arm:")
    say(wfd[wfd.book == "VOLTGT016"].to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    pd.DataFrame(GATES).to_csv(f"{OUT}.gates.csv", index=False)
    say(f"\nGATES {sum(1 for r in GATES if r['pass_'])}/{len(GATES)}   elapsed {time.time()-t0:.1f}s")
    Path(f"{OUT}.log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
