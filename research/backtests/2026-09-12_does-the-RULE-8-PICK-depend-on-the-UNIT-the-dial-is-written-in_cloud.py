#!/usr/bin/env python3
"""Idea 590 (cloud, 2026-09-12) - does-the-RULE-8-PICK-depend-on-the-UNIT-the-dial-is-written-in.

QUESTION
--------
Idea 320 found that the ABS and REL parameterisations of the SAME width dial pick different points
in 2 of 3 panels, and that on B136 the disagreement flips the 4b verdict outright (ABS n0=30 fails
on H2,DD; REL c=1.00 passes).  PROTOCOL rule 8 says "parameters chosen on 2009-2016 only, evaluate
2017-2026 untouched" - it does not say in WHICH UNIT the parameter is written.  If the unit changes
the pick, rule 8 is under-specified and every committed rule-8 pick is quoting an unnamed dial.

The queue's own wording asks for a CENSUS of committed picks.  A census of markdown carries no price
leg and therefore cannot carry this run's mandatory walk-forward, so this run does the RE-PRICING
the census would only count: it takes THREE dials that each have a natural second unit, runs rule 8
under BOTH units on THREE panels, and measures how far the pick moves, whether the two picked books
are the same book at all, and whether the KEEP verdict moves with them.

THE THREE DIALS AND THEIR TWO UNITS (stated before any number)
--------------------------------------------------------------
    WIDTH   how many names to hold, from the eligible (above-200d) set, ranked by 6-month return
            ABS  n      hold the top n names                        n in {5,10,15,20,25,30,40,50,60}
            REL  c      hold the top c-fraction of the ELIGIBLE set  c in {0.05..0.90}, n_t = round(c*E_t)
    VOLCAP  which names are admissible at all
            ABS  v      admit vol20 < v                             v in {0.20..0.80}
            REL  q      admit vol20 below the q-th cross-sectional percentile that day
    TREND   the 200d MA band that decides IN / OUT (hysteresis as in baseline.band_state)
            ABS  b      band = b, the same +/- b% for every name     b in {0.00..0.10}
            REL  k      band = k * the name's own daily sigma        k in {0.0..4.0}
Every dial is a WIDTH-of-book dial in some unit; gross (0.75), cadence (weekly), cost (10 bps) and
the ranking signal are held FIXED and reported, never selected on.

TUNED PARAMETERS (PROTOCOL rule 4, exactly two)
    1. DIAL VALUE  9 rungs per unit.  ALL 9 reported for all 18 (panel, dial, unit) ladders.
    2. UNIT        ABS or REL.  Both reported side by side - that IS the question.
REPORTED-NEVER-SELECTED: panel (U56 / B136 / SMALL), dial family, gross, cadence, cost rung,
window (FULL / IS / OOS), and both KEEP paths.

GATES (printed before any pick is read)
    G1 engine    : fast_backtest vs engine.backtest on one book.                        bar 1e-9
    G2 comparands: live RULES v2 and SPY per panel over this run's window.              no bar
    G3 matched span: the ABS and REL ladders must cover COMPARABLE book space or the comparison is
                  confounded with the grid rather than the unit.  Measured as the overlap of the two
                  ladders' realised COMMON-CURRENCY ranges (mean held names / mean admitted share /
                  mean days IN).  Published per cell, NOT barred - a cell whose ladders do not
                  overlap is named as such and its disagreement read with that caveat attached.
    G4 floor     : each picked book's own CONVENTION FLOOR - the max-min OOS Sharpe over the five
                  weekday offsets of the same 5-trading-day cadence (idea 582's floor).  A Sharpe
                  gap between units smaller than this floor is not a unit effect, it is the calendar.

PRE-REGISTERED HYPOTHESES (written before any grid point was read)
    H_MOVE   : the two units' IS picks differ, in common currency, by more than one grid step in
               >= 2/3 of the 9 (panel, dial) cells.
    H_BOOK   : the two picked books are materially different books - mean L1/2 weight distance
               >= 0.05 of NAV - in >= 2/3 of cells.  (If they are the same book, the unit is cosmetic.)
    H_VERDICT: the full-sample 4b verdict differs between the two units in >= 1/3 of cells
               (idea 320's single B136 flip generalises).
    H_OOS    : |OOS Sharpe(ABS pick) - OOS Sharpe(REL pick)| exceeds that book's G4 convention floor
               in >= 1/2 of cells.
    H_PROTO  : the queue's conclusion - if H_MOVE and H_VERDICT both hold, PROTOCOL 8 needs to name
               the unit.  Decided by those two, not separately measured.

RULE 8 WALK-FORWARD (required, and it is the object of study here)
    IS = ..2016-12-31, OOS = 2017-01-01.. , OOS read ONCE per ladder.
    The dial value is chosen inside each unit by IS Sharpe ALONE; OOS CAGR / Sharpe / MaxDD are then
    read once against live RULES v2 on the same panel and against SPY, and both KEEP paths are
    evaluated at the pick and at every rung.

KEEP PATHS: 4a and 4b evaluated at all 3 panels x 3 dials x 2 units x 9 rungs = 162 books and counted.

SURVIVORSHIP: U56 and B136 are current constituents of universe.json / universe_broad.json; SMALL is
    the current constituent list of its sub-$2B screen with every ticker whose max_1d_move >= 1.0 in
    data/small_meta.csv dropped first, per PROTOCOL.  Dead names are absent from all three, so every
    CAGR here is biased upward and every 4b CAGR-floor pass is easier than on a point-in-time panel.

PROTOCOL: 10 bps per unit turnover, next-day fills (engine), no shorting, no leverage.
Deterministic, standalone, no network.  Reads research/baseline.py; modifies nothing but its own
outputs: .ladders.csv .picks.csv .floors.csv .keeppaths.csv .console.txt
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
from baseline import load_universe, rules_v2_weights, metrics, backtest  # noqa: E402
from engine import rebalance_mask  # noqa: E402

STAMP = "2026-09-12_does-the-RULE-8-PICK-depend-on-the-UNIT-the-dial-is-written-in_cloud"
OUT = ROOT / "research" / "backtests"

COST = 10.0
GROSS = 0.75
FREQ = "W"
MA_WIN = 200
IS_END, OOS_START = "2016-12-31", "2017-01-01"
TOL = 1e-9

# TUNED 1 - dial value, 9 rungs per unit.  TUNED 2 - unit (ABS / REL).
GRIDS = {
    ("WIDTH", "ABS"):  [5, 10, 15, 20, 25, 30, 40, 50, 60],
    ("WIDTH", "REL"):  [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.55, 0.70, 0.90],
    ("VOLCAP", "ABS"): [0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.70, 0.80],
    ("VOLCAP", "REL"): [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.85, 1.00],
    ("TREND", "ABS"):  [0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10],
    ("TREND", "REL"):  [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0],
}
DIALS = ["WIDTH", "VOLCAP", "TREND"]
UNITS = ["ABS", "REL"]
PANELS = ["U56", "B136", "SMALL"]

_LOG: list[str] = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


# ------------------------------------------------------------------ runner (idea 574's, mask-able)
def fast_backtest(prices, weights, cost_bps, freq=FREQ, mask=None):
    idx = prices.index
    rets = prices.pct_change().fillna(0.0).values
    wt = weights.reindex(idx).fillna(0.0).shift(1).fillna(0.0).values
    if mask is None:
        m = rebalance_mask(idx, freq).shift(1, fill_value=False).values.copy()
    else:
        m = np.concatenate([[False], mask[:-1]])
    m[0] = True
    T, N = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, N)), C[:-1]])
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
    port = (held * rets).sum(axis=1) - turn * cost_bps / 1e4
    return pd.Series(port, index=idx)


def halves(r):
    h = len(r) // 2
    return metrics(r.iloc[:h])["Sharpe"], metrics(r.iloc[h:])["Sharpe"]


def keep_4a(r, b):
    a1, a2 = halves(r)
    b1, b2 = halves(b)
    return bool(a1 > b1 and a2 > b2 and metrics(r)["MaxDD"] >= metrics(b)["MaxDD"])


def fail_4b(r, spy, lo=None, hi=None, oos=True):
    rr, ss = r.loc[lo:hi], spy.loc[lo:hi]
    a1, a2 = halves(rr)
    s1, s2 = halves(ss)
    m, ms = metrics(rr), metrics(ss)
    f = []
    if not a1 > s1:
        f.append("H1")
    if not a2 > s2:
        f.append("H2")
    if oos and not metrics(r.loc[OOS_START:])["Sharpe"] > metrics(spy.loc[OOS_START:])["Sharpe"]:
        f.append("OOS")
    if not m["MaxDD"] >= 0.60 * ms["MaxDD"]:
        f.append("DD")
    if not m["CAGR"] >= 0.70 * ms["CAGR"]:
        f.append("CAGR")
    return ",".join(f) if f else "-"


# ------------------------------------------------------------------ panels
def panels():
    px56 = load_universe()
    px136 = load_universe(broad=True)
    pxs = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    s_stk = [c for c in pxs.columns if c != "SPY" and c not in bad]

    def sub(px, cols):
        cols = [c for c in cols if c in px.columns]
        keep = list(dict.fromkeys(cols + ["SPY"]))
        return px[keep].dropna(how="all").ffill(), set(cols)

    return ({"U56": sub(px56, [c for c in px56.columns]),
             "B136": sub(px136, [c for c in px136.columns]),
             "SMALL": sub(pxs, s_stk)}, len(bad), len(s_stk))


# ------------------------------------------------------------------ the dials
class Panel:
    """Everything a dial needs, computed once per panel."""

    def __init__(self, px, tradable):
        self.px = px
        self.cols = [c for c in px.columns if c in tradable]
        sub = px[self.cols]
        self.sub = sub
        self.priced = sub.notna()
        self.ma = sub.rolling(MA_WIN).mean()
        self.above = (sub > self.ma) & self.priced
        self.vol20 = sub.pct_change().rolling(20).std() * np.sqrt(252)
        self.volq = self.vol20.rank(axis=1, pct=True)
        self.r6 = (sub / sub.shift(126) - 1.0).where(self.priced)
        self.dsig = self.vol20 / np.sqrt(252)

    def _expand(self, w):
        out = pd.DataFrame(0.0, index=self.px.index, columns=self.px.columns)
        out[self.cols] = w[self.cols].values
        return out

    def band_state(self, band):
        """baseline.band_state generalised to a per-name, per-day band matrix."""
        raw = pd.DataFrame(np.nan, index=self.sub.index, columns=self.sub.columns)
        raw = raw.mask(self.sub > self.ma * (1 + band), 1.0).mask(self.sub < self.ma * (1 - band), 0.0)
        return (raw.ffill().fillna(0.0) > 0.5) & self.priced

    def weights(self, dial, unit, val):
        if dial == "WIDTH":
            elig = self.r6.where(self.above)
            rk = elig.rank(axis=1, ascending=False)
            if unit == "ABS":
                sel = rk <= val
            else:
                E = self.above.sum(axis=1)
                n_t = np.maximum(1, np.round(val * E)).astype(float)
                sel = rk.le(pd.Series(n_t, index=rk.index), axis=0)
            sel = sel & self.above
        elif dial == "VOLCAP":
            adm = (self.vol20 < val) if unit == "ABS" else (self.volq <= val)
            sel = self.above & adm & self.priced
        elif dial == "TREND":
            band = val if unit == "ABS" else self.dsig * val
            sel = self.band_state(band)
        else:
            raise ValueError(dial)
        cnt = sel.sum(axis=1).replace(0, np.nan)
        w = GROSS * sel.astype(float).div(cnt, axis=0).fillna(0.0)
        return self._expand(w), sel

    @staticmethod
    def currency(dial, sel, above, priced):
        """Common currency: the realised book width the dial actually produced."""
        if dial == "WIDTH":
            return float(sel.sum(axis=1).mean())                       # mean names held
        if dial == "VOLCAP":
            n = above.sum(axis=1).replace(0, np.nan)
            return float((sel.sum(axis=1) / n).mean())                 # mean share of above-MA names admitted
        return float((sel.sum(axis=1) / priced.sum(axis=1).replace(0, np.nan)).mean())  # mean share IN


def offset_mask(idx, off):
    """Every 5th trading day, starting at offset `off` - the five weekday conventions of a 5-day
    cadence (idea 582's convention floor)."""
    a = np.zeros(len(idx), dtype=bool)
    a[off::5] = True
    return a


def main():
    t0 = time.time()
    P(f"# Idea 590 - {STAMP}")
    P(f"# run {pd.Timestamp.utcnow():%Y-%m-%d %H:%M} UTC | PROTOCOL 10 bps, next-day fills, gross {GROSS}, weekly")

    PXD, n_bad, n_small = panels()
    P("\nPanels: " + ", ".join(f"{k}={len(v[1])} tradable ({len(v[0])} rows "
                               f"{v[0].index[0]:%Y-%m-%d}..{v[0].index[-1]:%Y-%m-%d})" for k, v in PXD.items()))
    P(f"SMALL panel: dropped {n_bad} tickers with max_1d_move >= 1.0 per PROTOCOL -> {n_small} tradable.")

    PN = {k: Panel(v[0], v[1]) for k, v in PXD.items()}
    START = {k: v[0].index[260] for k, v in PXD.items()}
    SPY = {k: v[0]["SPY"].pct_change().fillna(0.0).loc[START[k]:] for k, v in PXD.items()}
    BASE = {k: fast_backtest(v[0], rules_v2_weights(v[0]), COST).loc[START[k]:] for k, v in PXD.items()}

    # ---------------- G1
    p = PN["U56"]
    w, _ = p.weights("WIDTH", "ABS", 20)
    a = fast_backtest(p.px, w, COST)
    b = backtest(p.px, w, cost_bps=COST, freq=FREQ)["returns"]
    d = float(np.abs(a.reindex(b.index).fillna(0) - b).max())
    P(f"\nG1 engine agreement  max|fast - engine| = {d:.3e}  bar 1e-9  -> {'PASS' if d < TOL else 'FAIL'}")
    assert d < TOL, "G1 failed"

    # ---------------- G2
    P("\nG2 comparands (this run's windows):")
    for k in PANELS:
        mb, ms = metrics(BASE[k]), metrics(SPY[k])
        P(f"    {k:6s} RULES v2 {mb['CAGR']:.2%} / {mb['Sharpe']:.2f} / {mb['MaxDD']:.1%} "
          f"(halves {halves(BASE[k])[0]:.2f}/{halves(BASE[k])[1]:.2f}) | SPY {ms['CAGR']:.2%} / "
          f"{ms['Sharpe']:.2f} / {ms['MaxDD']:.1%} (halves {halves(SPY[k])[0]:.2f}/{halves(SPY[k])[1]:.2f}) "
          f"| 4b bars CAGR>={0.70*ms['CAGR']:.2%} DD>={0.60*ms['MaxDD']:.1%}")

    # ---------------- the 18 ladders
    P(f"\nLadders: {len(PANELS)} panels x {len(DIALS)} dials x {len(UNITS)} units x 9 rungs = "
      f"{len(PANELS)*len(DIALS)*len(UNITS)*9} books.  ALL reported.")
    rows = []
    for pk in PANELS:
        pn = PN[pk]
        spy, base, st = SPY[pk], BASE[pk], START[pk]
        for dial in DIALS:
            for unit in UNITS:
                for val in GRIDS[(dial, unit)]:
                    w, sel = pn.weights(dial, unit, val)
                    r = fast_backtest(pn.px, w, COST).loc[st:]
                    m = metrics(r)
                    mi, mo = metrics(r.loc[:IS_END]), metrics(r.loc[OOS_START:])
                    rows.append(dict(panel=pk, dial=dial, unit=unit, val=val,
                                     cur=Panel.currency(dial, sel.loc[st:], pn.above.loc[st:],
                                                        pn.priced.loc[st:]),
                                     CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"],
                                     H1=halves(r)[0], H2=halves(r)[1],
                                     IS_Sharpe=mi["Sharpe"], IS_CAGR=mi["CAGR"], IS_MaxDD=mi["MaxDD"],
                                     OOS_Sharpe=mo["Sharpe"], OOS_CAGR=mo["CAGR"], OOS_MaxDD=mo["MaxDD"],
                                     fail4b=fail_4b(r, spy), pass4b=fail_4b(r, spy) == "-",
                                     OOS_fail4b=fail_4b(r, spy, lo=OOS_START, oos=False),
                                     pass4a=keep_4a(r, base)))
            P(f"    {pk:6s} {dial:7s} done ({time.time()-t0:.0f}s)")
    L = pd.DataFrame(rows)
    L.to_csv(OUT / f"{STAMP}.ladders.csv", index=False)

    # ---------------- the ladders, printed
    P("\n## The 18 ladders (all 9 rungs each; * = the rule-8 pick by IS Sharpe alone)")
    for pk in PANELS:
        for dial in DIALS:
            for unit in UNITS:
                sub = L[(L.panel == pk) & (L.dial == dial) & (L.unit == unit)].reset_index(drop=True)
                k = int(sub.IS_Sharpe.idxmax())
                P(f"    {pk:6s} {dial:7s} {unit:3s}  " + "  ".join(
                    f"{'*' if i == k else ' '}{v:g}:IS{r.IS_Sharpe:.2f}/OOS{r.OOS_Sharpe:.2f}"
                    for i, (v, r) in enumerate(zip(sub.val, sub.itertuples()))))

    # ---------------- G3 matched span + the picks
    P("\n## G3 matched span, and the picks side by side")
    picks, floors = [], []
    for pk in PANELS:
        pn = PN[pk]
        spy, base, st = SPY[pk], BASE[pk], START[pk]
        for dial in DIALS:
            d = {}
            for unit in UNITS:
                sub = L[(L.panel == pk) & (L.dial == dial) & (L.unit == unit)].reset_index(drop=True)
                k = int(sub.IS_Sharpe.idxmax())
                d[unit] = (sub.iloc[k], sub)
            a_row, a_lad = d["ABS"]
            r_row, r_lad = d["REL"]
            lo = max(a_lad.cur.min(), r_lad.cur.min())
            hi = min(a_lad.cur.max(), r_lad.cur.max())
            span = max(0.0, hi - lo) / max(a_lad.cur.max() - a_lad.cur.min(),
                                           r_lad.cur.max() - r_lad.cur.min(), 1e-12)
            # common-currency step of the ABS ladder, the yardstick for "more than one grid step"
            step = float(np.median(np.abs(np.diff(np.sort(a_lad.cur.values)))))
            moved = abs(a_row.cur - r_row.cur) > step
            wa, _ = pn.weights(dial, "ABS", a_row.val)
            wr, _ = pn.weights(dial, "REL", r_row.val)
            l1 = float((np.abs(wa.loc[st:].values - wr.loc[st:].values).sum(axis=1) / 2).mean())
            # G4 convention floor on the two picked books
            fl = {}
            for unit, wx in (("ABS", wa), ("REL", wr)):
                sh = [metrics(fast_backtest(pn.px, wx, COST, mask=offset_mask(pn.px.index, o))
                              .loc[st:].loc[OOS_START:])["Sharpe"] for o in range(5)]
                fl[unit] = max(sh) - min(sh)
                floors.append(dict(panel=pk, dial=dial, unit=unit, val=wx is wa and a_row.val or r_row.val,
                                   floor=fl[unit], sharpes=";".join(f"{s:.3f}" for s in sh)))
            floor = max(fl["ABS"], fl["REL"])
            gap = abs(a_row.OOS_Sharpe - r_row.OOS_Sharpe)
            picks.append(dict(panel=pk, dial=dial,
                              abs_val=a_row.val, rel_val=r_row.val,
                              abs_cur=a_row.cur, rel_cur=r_row.cur, step=step, moved=bool(moved),
                              span_overlap=span, l1=l1,
                              abs_IS=a_row.IS_Sharpe, rel_IS=r_row.IS_Sharpe,
                              abs_OOS_Sharpe=a_row.OOS_Sharpe, rel_OOS_Sharpe=r_row.OOS_Sharpe,
                              abs_OOS_CAGR=a_row.OOS_CAGR, rel_OOS_CAGR=r_row.OOS_CAGR,
                              abs_OOS_MaxDD=a_row.OOS_MaxDD, rel_OOS_MaxDD=r_row.OOS_MaxDD,
                              gap=gap, floor=floor, gap_over_floor=bool(gap > floor),
                              abs_fail4b=a_row.fail4b, rel_fail4b=r_row.fail4b,
                              verdict_moved=bool((a_row.fail4b == "-") != (r_row.fail4b == "-")),
                              abs_pass4a=bool(a_row.pass4a), rel_pass4a=bool(r_row.pass4a),
                              spy_OOS_Sharpe=metrics(spy.loc[OOS_START:])["Sharpe"],
                              spy_OOS_CAGR=metrics(spy.loc[OOS_START:])["CAGR"],
                              spy_OOS_MaxDD=metrics(spy.loc[OOS_START:])["MaxDD"],
                              base_OOS_Sharpe=metrics(base.loc[OOS_START:])["Sharpe"],
                              base_OOS_CAGR=metrics(base.loc[OOS_START:])["CAGR"]))
    K = pd.DataFrame(picks)
    F = pd.DataFrame(floors)
    K.to_csv(OUT / f"{STAMP}.picks.csv", index=False)
    F.to_csv(OUT / f"{STAMP}.floors.csv", index=False)

    P(f"    {'panel':6s} {'dial':7s} {'ABS pick':10s} {'REL pick':10s} {'common currency ABS/REL':26s} "
      f"{'step':6s} {'moved':6s} {'span':6s} {'L1/2':6s}")
    for _, r in K.iterrows():
        P(f"    {r.panel:6s} {r.dial:7s} {str(r.abs_val):10s} {str(r.rel_val):10s} "
          f"{r.abs_cur:>11.3f} / {r.rel_cur:<11.3f} {r.step:<6.3f} {str(r.moved):6s} "
          f"{r.span_overlap:<6.2f} {r.l1:<6.3f}")

    P("\n## G4 convention floor (max-min OOS Sharpe over the 5 weekday offsets of a 5-day cadence)")
    for _, r in F.iterrows():
        P(f"    {r.panel:6s} {r.dial:7s} {r.unit:3s} val={r.val!s:<6s} floor {r.floor:.4f}   [{r.sharpes}]")

    # ---------------- rule 8 read-once table
    P("\n## RULE 8 - dial chosen on IS Sharpe alone inside each unit, OOS read ONCE")
    P(f"    {'panel':6s} {'dial':7s} {'unit':4s} {'pick':7s} {'OOS CAGR':9s} {'OOS Sh':7s} {'OOS DD':8s} "
      f"{'full 4b':16s} 4a")
    for _, r in K.iterrows():
        for u, v, c, s, dd, f4, f4a in (("ABS", r.abs_val, r.abs_OOS_CAGR, r.abs_OOS_Sharpe,
                                         r.abs_OOS_MaxDD, r.abs_fail4b, r.abs_pass4a),
                                        ("REL", r.rel_val, r.rel_OOS_CAGR, r.rel_OOS_Sharpe,
                                         r.rel_OOS_MaxDD, r.rel_fail4b, r.rel_pass4a)):
            P(f"    {r.panel:6s} {r.dial:7s} {u:4s} {v!s:7s} {c:<9.2%} {s:<7.2f} {dd:<8.1%} "
              f"{('PASSES 4b' if f4 == '-' else 'fails ' + f4):16s} {f4a}")
        P(f"    {'':6s} {'':7s} SPY  {'':7s} {r.spy_OOS_CAGR:<9.2%} {r.spy_OOS_Sharpe:<7.2f} "
          f"{r.spy_OOS_MaxDD:<8.1%} | RULES v2 OOS {r.base_OOS_CAGR:.2%} / {r.base_OOS_Sharpe:.2f}"
          f"   gap {r.gap:.4f} vs floor {r.floor:.4f} -> {'REAL' if r.gap_over_floor else 'INSIDE THE FLOOR'}"
          f" | verdict moved: {r.verdict_moved}")

    # ---------------- hypotheses
    n = len(K)
    P("\n## Pre-registered hypotheses")
    res = {
        "H_MOVE": (K.moved.sum() >= 2 / 3 * n, f"the pick moves more than one grid step in {int(K.moved.sum())}/{n} cells"),
        "H_BOOK": ((K.l1 >= 0.05).sum() >= 2 / 3 * n,
                   f"picked books differ by >= 0.05 of NAV (mean L1/2) in {int((K.l1 >= 0.05).sum())}/{n} cells; "
                   f"median distance {K.l1.median():.3f}"),
        "H_VERDICT": (K.verdict_moved.sum() >= 1 / 3 * n,
                      f"the full-sample 4b verdict differs between units in {int(K.verdict_moved.sum())}/{n} cells"),
        "H_OOS": (K.gap_over_floor.sum() >= 0.5 * n,
                  f"|OOS Sharpe gap| clears the book's own convention floor in "
                  f"{int(K.gap_over_floor.sum())}/{n} cells; median gap {K.gap.median():.4f} vs median floor "
                  f"{K.floor.median():.4f}"),
    }
    for k, (v, txt) in res.items():
        P(f"    {k:10s} {'PASS' if v else 'FAIL'}  - {txt}")
    proto = res["H_MOVE"][0] and res["H_VERDICT"][0]
    P(f"    {'H_PROTO':10s} {'PASS' if proto else 'FAIL'}  - decided by H_MOVE and H_VERDICT together: "
      f"PROTOCOL 8 {'NEEDS' if proto else 'does not need'} to name the unit on this evidence")

    # ---------------- keep paths
    n4a, n4b = int(L.pass4a.sum()), int(L.pass4b.sum())
    both = int((L.pass4a & L.pass4b).sum())
    P(f"\n## KEEP PATHS over all {len(L)} books: 4a {n4a} | 4b {n4b} | BOTH {both}")
    L[["panel", "dial", "unit", "val", "CAGR", "Sharpe", "MaxDD", "H1", "H2", "OOS_Sharpe",
       "pass4a", "pass4b", "fail4b"]].to_csv(OUT / f"{STAMP}.keeppaths.csv", index=False)
    if n4b:
        P("    4b-passing books:")
        for _, c in L[L.pass4b].iterrows():
            P(f"      {c.panel:6s} {c.dial:7s} {c.unit:3s} val={c.val!s:<6s} CAGR {c.CAGR:.2%} "
              f"Sharpe {c.Sharpe:.2f} MaxDD {c.MaxDD:.1%} halves {c.H1:.2f}/{c.H2:.2f} "
              f"OOS Sh {c.OOS_Sharpe:.2f} 4a={c.pass4a}")
    P("\nSURVIVORSHIP: U56 / B136 / SMALL are all CURRENT constituents; every CAGR above is biased "
      "upward and every 4b CAGR-floor pass is easier than it would be on a point-in-time panel.")
    P(f"\ndone in {time.time()-t0:.0f}s")
    (OUT / f"{STAMP}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
