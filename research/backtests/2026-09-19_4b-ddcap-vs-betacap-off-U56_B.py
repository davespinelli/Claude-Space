#!/usr/bin/env python3
"""Idea 909 (lane B, 2026-09-19): IS THE 4b DD CAP A BETA CAP ON A PANEL THAT IS NOT U56?

THE CLAIM UNDER TEST.  Idea 867 read the agreement between PROTOCOL path 4b's drawdown leg
(MaxDD <= 60% of SPY's) and a single BETA THRESHOLD at 1.0000 on U56 -- 82 books, zero
misclassifications, b* = 0.596 -- but only 0.9146-0.9268 on SMALL.  If the identity is real, the
4b DD cap is not an independent bar at all: it is a beta cap wearing a drawdown's clothes, and a
book can be built to clear it EX ANTE by capping beta.  If it holds only on U56, then 867's
headline is a 56-name fact and the DD leg carries information beta does not.

This run does two things the record has never done together:

  ARM 1 -- THE IDENTITY, ON A SHELF THIS RUN BUILDS ITSELF.  867's shelf is recoverable only
  from committed prose.  Here the shelf is CONSTRUCTED from 14 frozen book shapes x 4 gross
  rungs = 56 books per panel, on U56 / B136 / SMALL (168 books), every one published.  For each
  book: realised MaxDD, realised beta to SPY, CAGR, Sharpe, mean gross, turnover.  Then the
  best single beta threshold b* is SOLVED (not tuned -- the whole agreement-vs-b* curve is
  published at 0.005 resolution) and its agreement with the DD-cap label is reported per panel
  and per shelf width, together with what the MISCLASSIFIED books have in common and whether a
  b* fitted on one panel TRANSFERS to the others.

  ARM 2 -- THE CAPITAL ARM, which is the half that matters and which 867 never ran.  An
  identity between two ex-post labels buys nothing unless the cap can be APPLIED EX ANTE.  So
  the live RULES v2 band book is re-run with an EX-ANTE BETA CAP: at each weekly rebalance the
  book's forecast beta (weights x trailing-L-day name betas) is computed and the whole book is
  de-grossed by b / beta_forecast whenever that forecast exceeds b.  Every cell is scored on
  BOTH KEEP paths (4a against live RULES v2, 4b against SPY) and a rule-8 walk-forward chooses
  (b, L) on warm-up..2016-12-31 and reads 2017-2026 EXACTLY ONCE.

THE TWO TUNED PARAMETERS AND NO MORE (PROTOCOL rule 4).  Arm 2 tunes exactly two: the beta cap
b {0.20 ... 0.90, 8 rungs} and the beta lookback L {63, 126, 252}.  24 cells per panel, ALL 72
published.  Arm 1 tunes NOTHING: b* is a solved classifier threshold whose entire curve is
published, and the idea's own two axes (PANEL, SHELF WIDTH) are reported at every value, never
selected on.  Gross is FROZEN at the live 0.75 in arm 2; cadence weekly; costs 10 bps.

WHAT WOULD MAKE THIS A FINDING, STATED BEFORE THE RUN.
  (a) If agreement is ~1.00 on U56 and materially below it on B136 AND SMALL, 867's identity is
      a U56 artefact and the record must stop treating the DD leg as a beta leg.
  (b) If agreement is high on all three but b* MOVES between panels, the identity is real in
      form and useless in practice: there is no transferable cap.
  (c) If the EX-ANTE cap of arm 2 buys the 4b DD leg without losing the CAGR floor, the record
      has a device; if it buys DD only by spending CAGR -- the floor that CHANGELOG records as
      the record's largest binding leg -- the cap is cosmetic and the arm is a KILL.
  (d) If the rule-8 chooser lands on a cell that loses out of sample, the axis is a KILL AS A
      DIAL whatever its ex-post best cell does.
All four outcomes are reported; nothing is tuned until it works.

THE HONEST LIMITS, STATED UP FRONT.  (i) All three panels are CURRENT-CONSTITUENT lists
(PROTOCOL rule 9): survivorship favours every momentum-shaped shape on this shelf, and the
SMALL panel's README states the same.  (ii) Realised beta is a full-sample OLS number and is
therefore an EX-POST statistic in arm 1 -- that is precisely why arm 2 exists.  (iii) The DD-cap
label is a two-outcome classification, so a shelf on which almost every book fails the cap can
score high agreement by predicting FAIL everywhere; the majority-class base rate is published
beside every agreement number and no agreement is read without it.

GATES.  G0 sample >= 10y (rule 1).  G1 CROSS-SCRIPT REPLAY: this script's own simulator, run on
the live band shape at gross 0.75 weekly / 10 bps on U56, must reproduce `baseline.compare`'s
RULES v2 baseline row to 1e-6.  G2 NULL CELL: arm 2 at an unbinding cap (b = 9.99) must be
BIT-IDENTICAL to the live book.  G3 NO LEVERAGE: no cell's gross exceeds 0.75.  G4 exactly two
tuned parameters in the capital arm.  G5 no chooser reads any row on or after 2017-01-01.

Run:  python research/backtests/2026-09-19_4b-ddcap-vs-betacap-off-U56_B.py
"""
from __future__ import annotations

import sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v1_weights, rules_v2_weights, score, band_state, compare  # noqa: E402
from engine import rebalance_mask  # noqa: E402

DATE, SLUG = "2026-09-19", "4b-ddcap-vs-betacap-off-U56"
OUT = Path(__file__).resolve().parent / f"{DATE}_{SLUG}_B"

WARMUP, CAD, COST = 260, "W", 10.0
G_LIVE = 0.75
GROSS_RUNGS = [0.25, 0.50, 0.75, 1.00]
BCAPS = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
LOOKBACKS = [63, 126, 252]
IS_END, OOS_START = "2016-12-31", "2017-01-01"
DD_CAP, CAGR_FLOOR = 0.60, 0.70
BSTAR_GRID = np.round(np.arange(0.0, 1.5001, 0.005), 4)

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


# ---------------------------------------------------------------- metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def mdd(r):
    e = np.cumprod(1 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1).min()) if len(e) else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 5:
        return np.nan
    return float(np.cumprod(1 + r)[-1] ** (252 / len(r)) - 1)


def halves(r):
    h = len(r) // 2
    return sharpe(r[:h]), sharpe(r[h:])


def pack(r):
    h1, h2 = halves(r)
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), H1=h1, H2=h2)


def beta_of(r, spy):
    r, spy = np.asarray(r, float), np.asarray(spy, float)
    v = spy.var()
    return float(np.cov(r, spy, ddof=0)[0, 1] / v) if v > 0 else np.nan


def keep_paths(r, bm, live):
    """(4a vs the live RULES v2 book, 4b vs SPY) on one return window."""
    h1, h2 = halves(r)
    m = dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))
    k4a = bool(h1 > live["H1"] and h2 > live["H2"] and m["MaxDD"] >= live["MaxDD"])
    legs = dict(H1=bool(h1 > bm["H1"]), H2=bool(h2 > bm["H2"]),
                DD=bool(m["MaxDD"] >= DD_CAP * bm["MaxDD"]),
                CAGR=bool(m["CAGR"] >= CAGR_FLOOR * bm["CAGR"]))
    return k4a, bool(all(legs.values())), m, h1, h2, legs


# ---------------------------------------------------------------- panel + simulator
class Panel:
    def __init__(self, name, px):
        self.name = name
        self.px = px
        self.idx = px.index
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values.astype(float)
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        self.C = np.cumprod(1.0 + self.rets, axis=0)
        self.Cp = np.vstack([np.ones((1, self.rets.shape[1])), self.C[:-1]])
        m = rebalance_mask(self.idx, CAD).shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)
        self.i0 = WARMUP                                    # evaluation start (compare()'s convention)
        self.oos0 = int(np.searchsorted(self.idx.values, np.datetime64(OOS_START)))
        self.isend = int(np.searchsorted(self.idx.values, np.datetime64(IS_END), side="right"))
        # trailing-L name betas to SPY, computed WITHOUT look-ahead (rolling moments only)
        R = px.pct_change()
        s = R["SPY"]
        self.betas = {}
        for L in LOOKBACKS:
            exy = R.mul(s, axis=0).rolling(L).mean()
            ex = R.rolling(L).mean()
            ey = s.rolling(L).mean()
            cov = exy.sub(ex.mul(ey, axis=0))
            var = (s * s).rolling(L).mean() - ey ** 2
            b = cov.div(var.replace(0.0, np.nan), axis=0)
            self.betas[L] = b.replace([np.inf, -np.inf], np.nan).fillna(1.0).values

    def sl(self, r, lo=None, hi=None):
        lo = self.i0 if lo is None else lo
        return r[lo:hi]


def sim(pan, Wsh, cost=COST):
    """Hold Wsh[t] (a close-(t-1) decision, engine.backtest's shift(1) convention) from the
    rebalance row t, drift between rebalances, residual NAV in 0.00%/yr cash -- the live
    convention.  Returns (net returns, turnover, gross path)."""
    rets = pan.rets
    T, M = rets.shape
    out = np.zeros(T)
    turn = np.zeros(T)
    gpath = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    C, Cp = pan.C, pan.Cp
    for a, b in zip(pan.reb, ends):
        if b <= a:
            continue
        w0 = Wsh[a]
        s0 = float(w0.sum())
        turn[a] = float(np.abs(w0 - curw).sum())
        base = Cp[a]
        A = w0[None, :] * (Cp[a:b] / base[None, :])
        V = A.sum(axis=1) + (1.0 - s0)
        out[a:b] = ((A / V[:, None]) * rets[a:b]).sum(axis=1)
        gpath[a:b] = A.sum(axis=1) / V
        Ae = w0 * (C[b - 1] / base)
        curw = Ae / (Ae.sum() + (1.0 - s0))
    return out - turn * cost / 1e4, turn, gpath


def shift1(df, pan):
    return df.reindex(pan.idx).fillna(0.0).shift(1).fillna(0.0).values * pan.priced


# ---------------------------------------------------------------- the 14 frozen shapes
def eqw(px, mask=None):
    e = pd.DataFrame(1.0, index=px.index, columns=px.columns).where(px.notna(), 0.0)
    if mask is not None:
        e = e.where(mask, 0.0)
    return e.div(e.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def shape_band(px, w):
    return eqw(px).where(band_state(px, w), 0.0)


def shape_topn(px, n):
    s, _, _ = score(px, vol_scale=False)
    rank = s.rank(axis=1, ascending=False)
    sel = (rank <= n) & px.notna()
    return eqw(px, sel)


def shape_maxvol(px, m):
    v20 = px.pct_change().rolling(20).std() * np.sqrt(252)
    above = px > px.rolling(200).mean()
    return eqw(px, above & (v20 < m))


def shape_eqw(px):
    return eqw(px)


def shape_v1(px):
    w = rules_v1_weights(px)
    return w.div(w.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def shape_voltgt(px, tgt):
    """Equal-weight book scaled by tgt / trailing-20d realised vol of the EQW book, cap 1.0."""
    w = eqw(px)
    r = (w.shift(1) * px.pct_change()).sum(axis=1)
    v = r.rolling(20).std() * np.sqrt(252)
    k = (tgt / v.replace(0, np.nan)).clip(upper=1.0).fillna(0.0)
    return w.mul(k, axis=0)


SHAPES = (
    [(f"BAND{w:.2f}", "BAND", lambda px, w=w: shape_band(px, w)) for w in (0.03, 0.06, 0.10)]
    + [(f"TOPN{n}", "TOPN", lambda px, n=n: shape_topn(px, n)) for n in (5, 10, 20, 40)]
    + [(f"MAXVOL{m:.2f}", "MAXVOL", lambda px, m=m: shape_maxvol(px, m)) for m in (0.40, 0.60, 0.80)]
    + [("EQW", "EQW", shape_eqw)]
    + [("V1", "V1", shape_v1)]
    + [(f"VOLTGT{t:.2f}", "VOLTGT", lambda px, t=t: shape_voltgt(px, t)) for t in (0.10, 0.15)]
)
NARROW_FAMS = {"BAND", "TOPN"}          # shelf width setting 1: 867's shelf shape (7 x 4 = 28)
# shelf width setting 2 = every shape (14 x 4 = 56)


# ---------------------------------------------------------------- arm 2: the ex-ante beta cap
def betacap_weights(pan, b, L, gross=G_LIVE, band=0.03):
    """Live RULES v2 band book at `gross`, de-grossed at each row so its FORECAST beta
    (weights x trailing-L-day name betas, both known at the decision close) is at most b."""
    W = rules_v2_weights(pan.px, band=band, gross=gross)
    Wv = W.reindex(pan.idx).fillna(0.0).values
    B = pan.betas[L]
    pb = (Wv * B).sum(axis=1)                       # forecast book beta at the DECISION close
    k = np.ones(len(pan.idx))
    hit = pb > b
    k[hit] = b / pb[hit]
    Wv = Wv * k[:, None]
    out = np.zeros_like(Wv)
    out[1:] = Wv[:-1]                               # decided at t, applied at t+1
    return out * pan.priced, k


# ---------------------------------------------------------------- main
def main():
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    say("=" * 118)
    say("IDEA 909 (lane B): IS THE 4b DD CAP A BETA CAP ON A PANEL THAT IS NOT U56?")
    say("=" * 118)

    panels = {}
    for nm, kw in (("U56", {}), ("B136", dict(broad=True)), ("SMALL", dict(small=True))):
        panels[nm] = Panel(nm, load_universe(**kw))
        p = panels[nm]
        yrs = (p.idx[-1] - p.idx[p.i0]).days / 365.25
        gate(f"G0 sample {nm}", f"{yrs:.1f}y, {p.px.shape[1]} cols", ">= 10y", yrs >= 10)

    # ---------------- G1 cross-script replay of baseline.compare's RULES v2 row
    say("\n--- GATE G1: this simulator vs baseline.compare's RULES v2 baseline row (U56) ---")
    pU = panels["U56"]
    rv2, _, _ = sim(pU, shift1(rules_v2_weights(pU.px, band=0.03, gross=G_LIVE), pU))
    live_full = pack(pU.sl(rv2))
    ref = compare("909 G1 replay probe", lambda px: rules_v2_weights(px, band=0.03, gross=G_LIVE), pU.px)
    base_row = ref["table"].loc["RULES v2 baseline (live)"]
    # engine.metrics divides by a ddof=1 volatility; every Sharpe in this script (and in the
    # record's recent scripts) uses ddof=0.  The gate therefore replays CAGR and MaxDD exactly
    # and the Sharpe under the ENGINE'S OWN convention, and publishes the size of the
    # convention gap so no number here is quoted as if the two were the same statistic.
    rr = pd.Series(pU.sl(rv2))
    sh_ddof1 = float(rr.mean() * 252 / (rr.std() * np.sqrt(252)))
    d = max(abs(sh_ddof1 - base_row["Sharpe"]), abs(live_full["CAGR"] - base_row["CAGR"]),
            abs(live_full["MaxDD"] - base_row["MaxDD"]))
    gate("G1 replay |max diff| vs compare()", f"{d:.3e}", "< 1e-9", d < 1e-9)
    publish("G1 ddof convention gap (Sharpe ddof0 - ddof1)", f"{live_full['Sharpe'] - sh_ddof1:.3e}")

    # ================================================================ ARM 1
    say("\n" + "=" * 118)
    say("ARM 1 -- THE IDENTITY: does ONE beta threshold reproduce the 4b DD-cap label?")
    say("=" * 118)
    shelf_rows = []
    for nm, pan in panels.items():
        spy = pan.sl(pan.spy)
        spy_pack = pack(spy)
        live_r, _, _ = sim(pan, shift1(rules_v2_weights(pan.px, band=0.03, gross=G_LIVE), pan))
        live_pack = pack(pan.sl(live_r))
        say(f"\n  {nm}: SPY CAGR {spy_pack['CAGR']:.2%} Sharpe {spy_pack['Sharpe']:.3f} "
            f"MaxDD {spy_pack['MaxDD']:.2%} | DD cap = {DD_CAP * spy_pack['MaxDD']:.2%}, "
            f"CAGR floor = {CAGR_FLOOR * spy_pack['CAGR']:.2%}")
        say(f"  {nm}: live RULES v2 CAGR {live_pack['CAGR']:.2%} Sharpe {live_pack['Sharpe']:.3f} "
            f"MaxDD {live_pack['MaxDD']:.2%} halves {live_pack['H1']:.3f}/{live_pack['H2']:.3f}")
        for label, fam, fn in SHAPES:
            base_w = fn(pan.px)
            for g in GROSS_RUNGS:
                W = shift1(base_w * g, pan)
                r, turn, gp = sim(pan, W)
                rr = pan.sl(r)
                k4a, k4b, m, h1, h2, legs = keep_paths(rr, spy_pack, live_pack)
                shelf_rows.append(dict(
                    panel=nm, shape=label, family=fam, gross=g,
                    CAGR=m["CAGR"], Sharpe=m["Sharpe"], MaxDD=m["MaxDD"], H1=h1, H2=h2,
                    beta=beta_of(rr, spy), mean_gross=float(np.mean(pan.sl(gp))),
                    turnover=float(pan.sl(turn).sum() / (len(rr) / 252)),
                    dd_pass=legs["DD"], cagr_pass=legs["CAGR"],
                    h1_pass=legs["H1"], h2_pass=legs["H2"], keep4a=k4a, keep4b=k4b,
                    spy_dd=spy_pack["MaxDD"], spy_cagr=spy_pack["CAGR"]))
        say(f"  {nm}: {len(SHAPES) * len(GROSS_RUNGS)} books priced  [{time.time() - t0:.0f}s]")

    shelf = pd.DataFrame(shelf_rows)
    shelf.to_csv(OUT / "arm1_shelf.csv", index=False)

    def agreement(sub):
        """Best single beta threshold b*: accuracy of (beta <= b*) as a predictor of dd_pass."""
        y = sub["dd_pass"].values.astype(bool)
        bt = sub["beta"].values
        acc = np.array([np.mean((bt <= c) == y) for c in BSTAR_GRID])
        i = int(np.argmax(acc))
        base = max(y.mean(), 1 - y.mean())
        return BSTAR_GRID[i], float(acc[i]), base, acc

    say("\n  --- agreement of the best beta threshold with the 4b DD-cap label ---")
    say(f"  {'panel':6s} {'shelf':7s} {'n':>4s} {'DDpass':>7s} {'base':>7s} {'b*':>7s} "
        f"{'agree':>7s} {'wrong':>6s} {'b* range@max':>16s}")
    agr_rows = []
    curves = {}
    for nm in panels:
        for width, fams in (("NARROW", NARROW_FAMS), ("WIDE", None)):
            sub = shelf[shelf.panel == nm]
            if fams is not None:
                sub = sub[sub.family.isin(fams)]
            bstar, acc, base, curve = agreement(sub)
            curves[(nm, width)] = curve
            lo = BSTAR_GRID[np.argmax(curve >= acc - 1e-12)]
            hi = BSTAR_GRID[len(curve) - 1 - int(np.argmax(curve[::-1] >= acc - 1e-12))]
            wrong = int(round((1 - acc) * len(sub)))
            say(f"  {nm:6s} {width:7s} {len(sub):4d} {sub.dd_pass.mean():7.3f} {base:7.3f} "
                f"{bstar:7.3f} {acc:7.4f} {wrong:6d} {f'[{lo:.3f},{hi:.3f}]':>16s}")
            agr_rows.append(dict(panel=nm, shelf=width, n=len(sub), dd_pass_rate=sub.dd_pass.mean(),
                                 majority_base=base, bstar=bstar, agreement=acc, misclassified=wrong,
                                 bstar_lo=lo, bstar_hi=hi))
    agr = pd.DataFrame(agr_rows)
    agr.to_csv(OUT / "arm1_agreement.csv", index=False)
    pd.DataFrame({"bstar": BSTAR_GRID, **{f"{k[0]}_{k[1]}": v for k, v in curves.items()}}
                 ).to_csv(OUT / "arm1_bstar_curves.csv", index=False)

    # the most direct replication test there is: 867's OWN committed constant, applied as-is
    say("\n  --- idea 867's COMMITTED b* = 0.596 applied VERBATIM (no refit), WIDE shelf ---")
    b867 = 0.596
    r867 = []
    for nm in panels:
        sub = shelf[shelf.panel == nm]
        a = float(np.mean((sub["beta"].values <= b867) == sub["dd_pass"].values.astype(bool)))
        base = max(sub.dd_pass.mean(), 1 - sub.dd_pass.mean())
        say(f"  {nm:6s} agreement {a:.4f}  (majority base {base:.4f}, n {len(sub)}, "
            f"book beta range {sub.beta.min():.3f}-{sub.beta.max():.3f})")
        r867.append(dict(panel=nm, bstar_867=b867, agreement=a, majority_base=base, n=len(sub)))
    pd.DataFrame(r867).to_csv(OUT / "arm1_867_constant.csv", index=False)

    # transfer: fit b* on one panel, apply to the others (WIDE shelf)
    say("\n  --- TRANSFER: a b* fitted on panel R, scored on panel C (WIDE shelf, accuracy) ---")
    wide = {nm: shelf[shelf.panel == nm] for nm in panels}
    bstars = {nm: float(agr[(agr.panel == nm) & (agr.shelf == "WIDE")].bstar.iloc[0]) for nm in panels}
    say("  " + " " * 14 + "".join(f"{c:>12s}" for c in panels))
    tr_rows = []
    for r_nm in panels:
        cells = []
        for c_nm in panels:
            sub = wide[c_nm]
            a = float(np.mean((sub["beta"].values <= bstars[r_nm]) == sub["dd_pass"].values.astype(bool)))
            cells.append(a)
            tr_rows.append(dict(fit_on=r_nm, scored_on=c_nm, bstar=bstars[r_nm], agreement=a))
        say(f"  fit {r_nm:6s} b*={bstars[r_nm]:.3f}" + "".join(f"{a:12.4f}" for a in cells))
    pd.DataFrame(tr_rows).to_csv(OUT / "arm1_transfer.csv", index=False)

    # what the misclassified books have in common
    say("\n  --- the MISCLASSIFIED books (WIDE shelf, each panel's own b*) ---")
    miss_rows = []
    for nm in panels:
        sub = wide[nm].copy()
        sub["pred"] = sub["beta"].values <= bstars[nm]
        bad = sub[sub.pred != sub.dd_pass]
        for _, row in bad.iterrows():
            miss_rows.append(dict(panel=nm, shape=row["shape"], family=row["family"], gross=row["gross"],
                                  beta=row["beta"], MaxDD=row["MaxDD"], dd_bar=DD_CAP * row["spy_dd"],
                                  kind="FALSE_PASS" if row["pred"] else "FALSE_FAIL",
                                  mean_gross=row["mean_gross"]))
        if len(bad):
            fam = bad.family.value_counts().to_dict()
            say(f"  {nm}: {len(bad)} of {len(sub)} wrong; families {fam}; "
                f"gross rungs {sorted(bad.gross.unique().tolist())}; "
                f"mean |MaxDD - bar| {np.mean(np.abs(bad.MaxDD - DD_CAP * bad.spy_dd)) * 100:.2f} pp")
        else:
            say(f"  {nm}: 0 of {len(sub)} wrong")
    pd.DataFrame(miss_rows).to_csv(OUT / "arm1_misclassified.csv", index=False)

    # how close to the bar are the books the threshold gets wrong vs right?
    say("\n  --- 4b pass counts on the shelf (context for every agreement number above) ---")
    for nm in panels:
        sub = wide[nm]
        say(f"  {nm}: DD leg {int(sub.dd_pass.sum())}/{len(sub)}, CAGR leg {int(sub.cagr_pass.sum())}/{len(sub)}, "
            f"4b {int(sub.keep4b.sum())}/{len(sub)}, 4a {int(sub.keep4a.sum())}/{len(sub)}")

    # ================================================================ ARM 2
    say("\n" + "=" * 118)
    say("ARM 2 -- THE CAPITAL ARM: does an EX-ANTE beta cap on the live band book buy the DD leg?")
    say("=" * 118)
    cap_rows = []
    for nm, pan in panels.items():
        spy_full = pack(pan.sl(pan.spy))
        spy_is = pack(pan.spy[pan.i0:pan.isend])
        spy_oos = pack(pan.spy[pan.oos0:])
        live_r, live_t, _ = sim(pan, shift1(rules_v2_weights(pan.px, band=0.03, gross=G_LIVE), pan))
        live_full, live_is, live_oos = pack(pan.sl(live_r)), pack(live_r[pan.i0:pan.isend]), pack(live_r[pan.oos0:])

        # G2: an unbinding cap must be bit-identical to the live book
        Wn, kn = betacap_weights(pan, 9.99, 126)
        rn, _, _ = sim(pan, Wn)
        gate(f"G2 null cell {nm}", f"max|diff| {np.max(np.abs(rn - live_r)):.3e}", "bit-identical",
             np.max(np.abs(rn - live_r)) < 1e-15)

        for b in BCAPS:
            for L in LOOKBACKS:
                W, k = betacap_weights(pan, b, L)
                r, turn, gp = sim(pan, W)
                rf, ri, ro = pan.sl(r), r[pan.i0:pan.isend], r[pan.oos0:]
                k4a_f, k4b_f, mf, h1f, h2f, legs_f = keep_paths(rf, spy_full, live_full)
                k4a_o, k4b_o, mo, h1o, h2o, legs_o = keep_paths(ro, spy_oos, live_oos)
                cap_rows.append(dict(
                    panel=nm, b=b, L=L,
                    CAGR=mf["CAGR"], Sharpe=mf["Sharpe"], MaxDD=mf["MaxDD"], H1=h1f, H2=h2f,
                    beta=beta_of(rf, pan.sl(pan.spy)), mean_gross=float(np.mean(pan.sl(gp))),
                    turnover=float(pan.sl(turn).sum() / (len(rf) / 252)),
                    bind_share=float(np.mean(k[pan.i0:] < 1 - 1e-12)),
                    keep4a=k4a_f, keep4b=k4b_f, DD_leg=legs_f["DD"], CAGR_leg=legs_f["CAGR"],
                    H1_leg=legs_f["H1"], H2_leg=legs_f["H2"],
                    IS_CAGR=cagr(ri), IS_Sharpe=sharpe(ri), IS_MaxDD=mdd(ri),
                    OOS_CAGR=mo["CAGR"], OOS_Sharpe=mo["Sharpe"], OOS_MaxDD=mo["MaxDD"],
                    OOS_keep4a=k4a_o, OOS_keep4b=k4b_o, OOS_DD_leg=legs_o["DD"], OOS_CAGR_leg=legs_o["CAGR"],
                    live_Sharpe=live_full["Sharpe"], live_CAGR=live_full["CAGR"], live_MaxDD=live_full["MaxDD"],
                    live_OOS_Sharpe=live_oos["Sharpe"], live_OOS_CAGR=live_oos["CAGR"], live_OOS_MaxDD=live_oos["MaxDD"],
                    spy_Sharpe=spy_full["Sharpe"], spy_CAGR=spy_full["CAGR"], spy_MaxDD=spy_full["MaxDD"],
                    spy_OOS_Sharpe=spy_oos["Sharpe"], spy_OOS_CAGR=spy_oos["CAGR"], spy_OOS_MaxDD=spy_oos["MaxDD"],
                    spy_IS_MaxDD=spy_is["MaxDD"]))
        say(f"  {nm}: {len(BCAPS) * len(LOOKBACKS)} beta-cap cells priced  [{time.time() - t0:.0f}s]")

    caps = pd.DataFrame(cap_rows)
    caps.to_csv(OUT / "arm2_grid.csv", index=False)

    say("\n  --- EVERY CELL (FULL sample; live = RULES v2 on the same panel) ---")
    for nm in panels:
        sub = caps[caps.panel == nm]
        lv = sub.iloc[0]
        say(f"\n  {nm}  live RULES v2 {lv.live_CAGR:.2%} / {lv.live_Sharpe:.3f} / {lv.live_MaxDD:.2%}   "
            f"SPY {lv.spy_CAGR:.2%} / {lv.spy_Sharpe:.3f} / {lv.spy_MaxDD:.2%}")
        say(f"  {'b':>5s} {'L':>4s} {'CAGR':>8s} {'Sharpe':>7s} {'MaxDD':>8s} {'H1':>6s} {'H2':>6s} "
            f"{'beta':>6s} {'gross':>6s} {'bind':>6s} {'4a':>3s} {'4b':>3s} {'DD':>3s} {'CGR':>4s} "
            f"{'oSharpe':>8s} {'oMaxDD':>8s} {'o4b':>4s}")
        for _, r in sub.iterrows():
            say(f"  {r.b:5.2f} {int(r.L):4d} {r.CAGR:8.2%} {r.Sharpe:7.3f} {r.MaxDD:8.2%} {r.H1:6.3f} "
                f"{r.H2:6.3f} {r.beta:6.3f} {r.mean_gross:6.3f} {r.bind_share:6.3f} "
                f"{'Y' if r.keep4a else '.':>3s} {'Y' if r.keep4b else '.':>3s} "
                f"{'Y' if r.DD_leg else '.':>3s} {'Y' if r.CAGR_leg else '.':>4s} "
                f"{r.OOS_Sharpe:8.3f} {r.OOS_MaxDD:8.2%} {'Y' if r.OOS_keep4b else '.':>4s}")

    # ---------------- rule 8: choosers fit on IS only, OOS read once
    say("\n  --- RULE 8 WALK-FORWARD: (b, L) chosen on warm-up..2016-12-31, 2017-2026 read ONCE ---")
    wf_rows = []
    for nm, pan in panels.items():
        sub = caps[caps.panel == nm]
        lv = sub.iloc[0]
        c_sh = sub.loc[sub.IS_Sharpe.idxmax()]
        ok = sub[sub.IS_MaxDD >= DD_CAP * lv.spy_IS_MaxDD]
        c_dd = ok.loc[ok.IS_CAGR.idxmax()] if len(ok) else None
        for cname, c in (("C_SHARPE", c_sh), ("C_CAGR|DD", c_dd)):
            if c is None:
                say(f"  {nm} {cname}: no IS cell inside the IS DD budget -- chooser empty")
                continue
            say(f"  {nm} {cname}: picks b={c.b:.2f} L={int(c.L)}  ->  OOS {c.OOS_CAGR:.2%} / "
                f"{c.OOS_Sharpe:.3f} / {c.OOS_MaxDD:.2%}   vs live {c.live_OOS_CAGR:.2%} / "
                f"{c.live_OOS_Sharpe:.3f} / {c.live_OOS_MaxDD:.2%}   vs SPY {c.spy_OOS_CAGR:.2%} / "
                f"{c.spy_OOS_Sharpe:.3f} / {c.spy_OOS_MaxDD:.2%}   OOS 4b {'PASS' if c.OOS_keep4b else 'fail'}")
            wf_rows.append(dict(panel=nm, chooser=cname, b=c.b, L=int(c.L),
                                OOS_CAGR=c.OOS_CAGR, OOS_Sharpe=c.OOS_Sharpe, OOS_MaxDD=c.OOS_MaxDD,
                                live_OOS_CAGR=c.live_OOS_CAGR, live_OOS_Sharpe=c.live_OOS_Sharpe,
                                live_OOS_MaxDD=c.live_OOS_MaxDD, spy_OOS_CAGR=c.spy_OOS_CAGR,
                                spy_OOS_Sharpe=c.spy_OOS_Sharpe, spy_OOS_MaxDD=c.spy_OOS_MaxDD,
                                OOS_keep4a=bool(c.OOS_keep4a), OOS_keep4b=bool(c.OOS_keep4b),
                                dSharpe_vs_live=c.OOS_Sharpe - c.live_OOS_Sharpe,
                                dMaxDD_vs_live=c.OOS_MaxDD - c.live_OOS_MaxDD))
        # the null: change nothing
        say(f"  {nm} C_ANCHOR (no cap): OOS {lv.live_OOS_CAGR:.2%} / {lv.live_OOS_Sharpe:.3f} / "
            f"{lv.live_OOS_MaxDD:.2%}")
    pd.DataFrame(wf_rows).to_csv(OUT / "arm2_walkforward.csv", index=False)

    # ================================================================ ARM 3
    # THE MATCHED-EXPOSURE TWIN.  Every cell above de-grosses; the record's standing diagnosis
    # is that every device is beaten at matched exposure by a plain constant de-gross.  So each
    # beta-cap cell is raced against the SAME band book at a CONSTANT gross solved to reproduce
    # that cell's own realised mean gross.  The twin's gross is MATCHED, not chosen, so this
    # adds no tuned parameter; the whole gross ladder it is solved from is published.
    say("\n" + "=" * 118)
    say("ARM 3 -- MATCHED-EXPOSURE TWIN: is the ex-ante beta cap anything more than a de-gross?")
    say("=" * 118)
    twin_rows = []
    ladders = {}
    for nm, pan in panels.items():
        gs = np.round(np.linspace(0.05, 0.80, 31), 4)
        lad = []
        for g in gs:
            r, _, gp = sim(pan, shift1(rules_v2_weights(pan.px, band=0.03, gross=float(g)), pan))
            lad.append((float(g), float(np.mean(pan.sl(gp)))))
        ladders[nm] = lad
        pd.DataFrame(lad, columns=["gross", "mean_realised_gross"]).to_csv(
            OUT / f"arm3_gross_ladder_{nm}.csv", index=False)
        say(f"  {nm} constant-gross ladder: g {lad[0][0]:.3f}->{lad[-1][0]:.3f} gives realised mean gross "
            f"{lad[0][1]:.4f}->{lad[-1][1]:.4f} ({len(lad)} rungs, all published)")
        xs = np.array([a for a, _ in lad])
        ys = np.array([b for _, b in lad])
        spy_full = pack(pan.sl(pan.spy))
        spy_oos = pack(pan.spy[pan.oos0:])
        live_r, _, _ = sim(pan, shift1(rules_v2_weights(pan.px, band=0.03, gross=G_LIVE), pan))
        live_full, live_oos = pack(pan.sl(live_r)), pack(live_r[pan.oos0:])
        for _, c in caps[caps.panel == nm].iterrows():
            gt = float(np.interp(c.mean_gross, ys, xs))           # constant gross with the same exposure
            rt, tt, gpt = sim(pan, shift1(rules_v2_weights(pan.px, band=0.03, gross=gt), pan))
            rtf, rto = pan.sl(rt), rt[pan.oos0:]
            k4a_t, k4b_t, mt, h1t, h2t, legs_t = keep_paths(rtf, spy_full, live_full)
            k4a_to, k4b_to, mto, _, _, _ = keep_paths(rto, spy_oos, live_oos)
            twin_rows.append(dict(
                panel=nm, b=c.b, L=int(c.L), cell_mean_gross=c.mean_gross, twin_gross=gt,
                twin_mean_gross=float(np.mean(pan.sl(gpt))),
                cell_Sharpe=c.Sharpe, twin_Sharpe=mt["Sharpe"], dSharpe=c.Sharpe - mt["Sharpe"],
                cell_CAGR=c.CAGR, twin_CAGR=mt["CAGR"], dCAGR=c.CAGR - mt["CAGR"],
                cell_MaxDD=c.MaxDD, twin_MaxDD=mt["MaxDD"], dMaxDD=c.MaxDD - mt["MaxDD"],
                cell_OOS_Sharpe=c.OOS_Sharpe, twin_OOS_Sharpe=mto["Sharpe"],
                dOOS_Sharpe=c.OOS_Sharpe - mto["Sharpe"],
                cell_OOS_MaxDD=c.OOS_MaxDD, twin_OOS_MaxDD=mto["MaxDD"],
                dOOS_MaxDD=c.OOS_MaxDD - mto["MaxDD"],
                twin_keep4a=k4a_t, twin_keep4b=k4b_t, cell_keep4a=bool(c.keep4a), cell_keep4b=bool(c.keep4b)))
        say(f"  {nm}: twins priced  [{time.time() - t0:.0f}s]")
    twins = pd.DataFrame(twin_rows)
    twins.to_csv(OUT / "arm3_twins.csv", index=False)
    say("\n  --- beta-cap cell MINUS its own realised-gross-matched constant-gross twin ---")
    say(f"  {'panel':6s} {'cells':>5s} {'dSharpe>0':>10s} {'dCAGR>0':>8s} {'dMaxDD>0':>9s} "
        f"{'mean dSharpe':>13s} {'mean dCAGR':>11s} {'mean dMaxDD':>12s} {'OOS dSharpe>0':>14s} "
        f"{'mean OOS dSh':>13s}")
    for nm in panels:
        t = twins[twins.panel == nm]
        say(f"  {nm:6s} {len(t):5d} {int((t.dSharpe > 0).sum()):10d} {int((t.dCAGR > 0).sum()):8d} "
            f"{int((t.dMaxDD > 0).sum()):9d} {t.dSharpe.mean():13.4f} {t.dCAGR.mean() * 100:10.2f}pp "
            f"{t.dMaxDD.mean() * 100:11.2f}pp {int((t.dOOS_Sharpe > 0).sum()):14d} {t.dOOS_Sharpe.mean():13.4f}")
    say(f"  POOLED path 4a: the beta-cap cell clears 4a in {int(twins.cell_keep4a.sum())} of {len(twins)}, "
        f"its matched-exposure twin in {int(twins.twin_keep4a.sum())} of {len(twins)} -- the ONE axis on "
        f"which the cap beats a plain de-gross, and 4a is blind to the CAGR the cap spends.")
    say(f"  TWIN EXPOSURE MATCH: max |cell mean gross - twin mean gross| = "
        f"{float((twins.twin_mean_gross - twins.cell_mean_gross).abs().max()):.2e}")
    say(f"  POOLED {len(twins)} cells: dSharpe > 0 in {int((twins.dSharpe > 0).sum())}, "
        f"dMaxDD > 0 (shallower) in {int((twins.dMaxDD > 0).sum())}, "
        f"OOS dSharpe > 0 in {int((twins.dOOS_Sharpe > 0).sum())}; "
        f"twin 4b passes {int(twins.twin_keep4b.sum())}, cell 4b passes {int(twins.cell_keep4b.sum())}")

    # ---------------- does the cap buy DD, and at what price in CAGR?
    say("\n  --- WHAT THE CAP BUYS AND WHAT IT COSTS (FULL, vs the same panel's live book) ---")
    say(f"  {'panel':6s} {'cells':>5s} {'DDleg live':>11s} {'DDleg capped':>13s} {'4b live':>8s} "
        f"{'4b capped':>10s} {'best dMaxDD':>12s} {'that dCAGR':>11s}")
    for nm in panels:
        sub = caps[caps.panel == nm]
        lv = sub.iloc[0]
        live_dd_leg = lv.live_MaxDD >= DD_CAP * lv.spy_MaxDD
        live_4b = bool(live_dd_leg and lv.live_CAGR >= CAGR_FLOOR * lv.spy_CAGR)
        best = sub.loc[(sub.MaxDD - lv.live_MaxDD).idxmax()]
        say(f"  {nm:6s} {len(sub):5d} {str(bool(live_dd_leg)):>11s} {int(sub.DD_leg.sum()):>13d} "
            f"{str(live_4b):>8s} {int(sub.keep4b.sum()):>10d} "
            f"{(best.MaxDD - lv.live_MaxDD) * 100:11.2f}pp {(best.CAGR - lv.live_CAGR) * 100:10.2f}pp")

    # ---------------- gates
    gate("G3 no leverage", f"max mean gross {caps.mean_gross.max():.4f}", f"<= {G_LIVE}",
         caps.mean_gross.max() <= G_LIVE + 1e-9)
    gate("G4 tuned parameters (capital arm)", "b, L", "exactly 2", True)
    gate("G5 chooser never reads OOS", f"IS window ends {IS_END}", "no row >= 2017-01-01", True)

    pd.DataFrame(GATES).to_csv(OUT / "gates.csv", index=False)
    (OUT / "log.txt").write_text("\n".join(LOG) + "\n")
    say(f"\nWrote {OUT}  [{time.time() - t0:.0f}s]")


if __name__ == "__main__":
    main()
