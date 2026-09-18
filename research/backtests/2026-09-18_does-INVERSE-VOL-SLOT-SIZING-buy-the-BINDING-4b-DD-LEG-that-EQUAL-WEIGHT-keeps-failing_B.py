#!/usr/bin/env python3
"""
Idea 1264 (lane B, 2026-09-18) — does INVERSE-VOL SLOT SIZING buy the BINDING 4b DD LEG that
EQUAL WEIGHT keeps failing?

THE PREMISE, AND WHY IT IS THE ONLY PRICE QUESTION LEFT ON THIS BOOK.  Four consecutive dials on
the standing 2026-09-04 KEEP 4b candidate — rebalance phase (1253), calendar years (1254),
ex-post winner names (1255), the signal itself (1257) — all landed on the same sentence: every
other 4b leg (H1 Sharpe, H2 Sharpe, OOS Sharpe, the CAGR floor) passes at essentially every grid
point, and the DRAWDOWN CAP is the only leg that ever fails.  1257 put a price on it: the
M12_1-ALONE book earns +1.00pp of CAGR and +0.0413 of full Sharpe at 0.24/yr LESS turnover than
the committed composite and is disqualified by 1.45pp of MaxDD and nothing else.  So the
capital question is no longer "which signal" — it is whether the drawdown leg can be BOUGHT.

This run prices the cheapest way to buy it that does not touch the signal, the screen, the
cadence or the gross: SLOT SIZING.  The committed book puts 1/len(held) into every name it
holds.  Equal weight is a choice — the one sizing choice in the whole construction that no run
in this record has ever walked — and inverse-volatility (risk-parity) sizing is the textbook
cheapest drawdown reduction, costing nothing in expected return under the textbook's own
assumptions.  If the DD leg is buyable at all, this is where it is cheapest.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    ALPHA {0.00, 0.25, 0.50, 0.75, 1.00, 1.50, 2.00} — slot weight proportional to vol^-ALPHA,
          normalised across the held names.  ALPHA = 0 is EXACTLY equal weight, i.e. THE
          COMMITTED ANCHOR BOOK; ALPHA = 1 is inverse volatility; ALPHA = 2 is inverse variance.
    LOOK  {20, 60, 126} trading days — the lookback of the trailing realised volatility that
          sizes the slots, measured at the DECISION date (t-1), never at application.
  7 x 3 = 21 cells per (panel, signal).  EVERY ONE PUBLISHED in the .grid.csv.

NOT DIALS, reported at every value: PANEL {U56, B136, SMALL} (rule 9); SIGNAL {COMPOSITE3 = the
committed three-leg average of percentile ranks, M12_1 = 1257's single 21/252 leg, the
higher-return book that failed 4b on drawdown alone} — a fully reported control arm, never a
chooser, so that the run answers both "does sizing fix the committed book" and "does sizing fix
the book the committed one was beaten by"; the 4a and 4b legs individually; full / halves / IS /
OOS; annual turnover; realised max and effective slot weight.  126 cells in all.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: eligibility = above own 200d MA
AND vol20 < 0.60; N = 20; H = 126 minimum hold; GROSS = 0.75 of NAV; WEEKLY decide-Friday /
trade-Monday; 10 bps per unit turnover (rule 2); t+1 execution; 260-row warm-up; ranking on the
RAW composite (scan.py's 0.5 + 0.5*above multiplier is identically 1.0 on every eligible name
under the committed gate, so it is a no-op, exactly as in the committed 2026-09-17 runs); and
the 1/len(held) SPREAD convention (the gated-out-weight-to-cash defect idea 1096 published and
which is deliberately NOT changed here, so ALPHA = 0 replays the committed number bit for bit).

FROZEN CONSTANTS, DECLARED SO THEY ARE NOT MISTAKEN FOR DIALS.  VOL_FLOOR = 0.08 annualised (the
same floor baseline.py's own vol scaler uses; below it vol^-ALPHA explodes on a stale price).
A held name with no volatility history is sized at the cross-sectional MEDIAN of the names
selected that day.  There is NO max-slot-weight cap: a cap would be a third tuned parameter, so
instead the realised max and effective slot weights are PUBLISHED at every cell and the reader
can see exactly how much concentration each ALPHA buys or removes.

PRE-DECLARED OUTCOMES, written before any number is read:
  (A) INERT — the sizing changes MaxDD by less than 0.20pp at every ALPHA, i.e. the book's names
      are close enough in volatility that risk parity and equal weight are the same book.  Then
      equal weight is not a defect and the RULES line should say the sizing was priced and is
      free either way.
  (B) THE DD LEG IS BOUGHT — some cell materially improves MaxDD while holding the 4b CAGR floor
      and both half-Sharpe legs, converting a 4b FAIL into a PASS (on the M12_1 arm, or widening
      the committed book's own 1.10pp margin), AND rule 8 reaches it.  That is a KEEP-candidate
      memo with exact RULES wording.
  (C) THE DD LEG IS BOUGHT AND OVERPAID FOR — MaxDD improves but CAGR falls through 4b's floor
      (70% of SPY), or a half-Sharpe falls below SPY, or the extra rebalancing turnover eats the
      gain at 10 bps.  Then sizing is a risk story this tape does not pay for.
  (D) THE DD LEG GETS WORSE — inverse-vol tilts the book toward names whose LOW realised vol is
      itself the stale-price / low-liquidity artefact, and drawdown deepens.
  (A)-(D) are not mutually exclusive across panels; whichever fire are reported as they fall,
  and the capital verdict follows rule 8 (below), not the best cell.

RULE 8 (walk-forward, required).  (ALPHA, LOOK) is CHOSEN on warm-up..2016-12-31 by IS Sharpe
ALONE and 2017-2026 is read ONCE, per (panel, signal).  Reported against (i) the DO-NOTHING
control = always ALPHA 0 (the committed equal-weight book), (ii) the mean over all 21 cells,
(iii) the WORST cell, with the IS/OOS rank correlation over the 21.  The capital verdict is the
sign of chooser-minus-do-nothing, not the best cell's number.

GATES, AND A TAPE-VINTAGE FACT FOUND BY THEM AND PUBLISHED RATHER THAN TOLERANCED AWAY.  The
committed anchor triples were produced on 2026-09-17, when the cache ended 2026-09-16; today's
cache carries one more trading day (2026-09-17).  That single day moves the committed U56
composite triple from 15.71% / 1.1480 to 15.78% / 1.1522 and SPY's from 15.06% / 0.8815 to
15.13% / 0.8849 — a 4.2e-03 drift that is NOT a construction difference.  The gates are
therefore PINNED TO THE VINTAGE rather than loosened: G1 truncates U56 at 2026-09-16 and
requires the (COMPOSITE3, ALPHA 0) cell to replay 15.71% / 1.1480 / -19.13% to 1e-4, and G4 does
the same for (M12_1, ALPHA 0) against 1257's 16.71% / 1.1893 / -20.58%.  G6 publishes the
one-day drift itself.  Every number in the grid is reported on the FULL current tape (ending
2026-09-17), and every bar (SPY, LIVE v2) is recomputed on that same tape, so the comparisons
are internally consistent.  G2 ALPHA 0 is bit-identical across all three LOOK values (the vol
lookback cannot matter when the exponent is zero) — a construction check on the sizing code.
G3 every cell's slot weights sum to 1.0 on every rebalance.  G5 determinism: the whole U56
COMPOSITE3 grid recomputed a second time, bit for bit.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (PROTOCOL rule 9).  U56 and B136 are CURRENT-constituent lists and SMALL is a
current sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped
before anything is computed).  Every absolute level printed here is optimistic and every 4b pass
is an UPPER bound.  The headline is a DIFFERENCE between sizing rules applied to the SAME
holdings on the SAME panel — the selected names are identical at every ALPHA by construction,
only their weights move — which makes it first-order immune to a level bias that moves all cells
together.  One direction of bias is NOT neutral and is stated: a current-constituent list is
KIND TO THE HIGH-VOL WINNERS a momentum screen piles into, because the high-vol names that did
not survive are absent, so the EQUAL-WEIGHT (and more so the low-ALPHA) arm is the more
flattered of the two and any win inverse-vol posts here is a LOWER bound on its win.

Runs standalone and offline (committed price caches only):
  python research/backtests/2026-09-18_does-INVERSE-VOL-SLOT-SIZING-buy-the-BINDING-4b-DD-LEG-that-EQUAL-WEIGHT-keeps-failing_B.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research"))
sys.path.insert(0, str(ROOT / "products" / "backtester"))
from baseline import load_universe, rules_v2_weights  # noqa: E402
from engine import backtest, rebalance_mask  # noqa: E402

DATE = "2026-09-18"
SLUG = "does-INVERSE-VOL-SLOT-SIZING-buy-the-BINDING-4b-DD-LEG-that-EQUAL-WEIGHT-keeps-failing"
OUT = ROOT / "research" / "backtests"
STEM = OUT / f"{DATE}_{SLUG}_B"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                      # the frozen 2026-09-04 book
SIGNALS = {"COMPOSITE3": [(21, 252), (0, 126), (0, 63)], "M12_1": [(21, 252)]}
ALPHAS = [0.00, 0.25, 0.50, 0.75, 1.00, 1.50, 2.00]   # DIAL 1  (0.00 == committed anchor)
LOOKS = [20, 60, 126]                                  # DIAL 2
VOL_FLOOR = 0.08                                       # frozen constant, NOT a dial
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)         # gate G1 (composite3, alpha 0)
COMMITTED_M12 = (0.167116, 1.18933, -0.205813)         # gate G4 (1257's single-leg book)
VINTAGE = pd.Timestamp("2026-09-16")                   # the cache end date 1257/1258 ran on
GATES: list[dict] = []


def say(*a):
    print(" ".join(str(x) for x in a), flush=True)


def gate(name, value, target, ok):
    GATES.append(dict(gate=name, value=str(value), target=str(target), pass_=bool(ok)))
    say(f"   GATE {name}: {value} vs {target} -> {'PASS' if ok else 'FAIL'}")
    return bool(ok)


# ------------------------------------------------------------------ metrics
def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    v = r.std(ddof=0) * np.sqrt(252)
    return float(r.mean() * 252 / v) if v > 0 else np.nan


def cagr(r):
    r = np.asarray(r, float)
    if len(r) < 20:
        return np.nan
    return float(np.prod(1.0 + r)) ** (252.0 / len(r)) - 1.0


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3:
        return float("nan")
    ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r))


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]), is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


# ------------------------------------------------------------------ panel
class Panel:
    """Everything that does not depend on the two dials, built once per panel."""

    def __init__(self, name, px, invest):
        self.name = name
        self.px = px
        self.invest = invest
        cols = list(px.columns)
        self.iinv = np.array([cols.index(c) for c in invest])
        self.rets = px.pct_change().fillna(0.0).values
        self.priced = px.notna().values
        self.idx = px.index
        q = px[invest]
        self.keys = {}
        for sig, legs in SIGNALS.items():
            parts = []
            for skip, look in legs:
                x = (q.shift(skip) / q.shift(look) - 1.0) if skip else (q / q.shift(look) - 1.0)
                parts.append(x.rank(axis=1, pct=True))
            comp = (sum(parts) / len(parts)).values            # RAW composite (see docstring)
            self.keys[sig] = np.where(np.isfinite(comp), -comp, np.inf)
        self.above = (q > q.rolling(200).mean()).values
        qr = q.pct_change()
        vol20 = (qr.rolling(20).std() * np.sqrt(252)).values
        self.volok = np.nan_to_num(vol20, nan=1e9) < MAXVOL
        self.elig = self.above & self.volok                    # the committed screen, frozen
        # the sizing volatilities: one panel-wide matrix per LOOK, decision-date values
        self.sizevol = {L: np.clip((qr.rolling(L).std() * np.sqrt(252)).values, VOL_FLOOR, None)
                        for L in LOOKS}
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


# ------------------------------------------------------------------ the book
def build(pan, sig, alpha, look, N=A_N, H=A_H, lag=1):
    """The frozen book's selection frame at GROSS = 1.0, with slot weights proportional to
    vol^-alpha across the held names (alpha = 0 -> the committed 1/len(held) equal weight).

    SELECTION IS IDENTICAL AT EVERY ALPHA BY CONSTRUCTION: the dials touch only the weights.
    Row t is the APPLICATION-time weight (rule 2: decided at t-lag, applied at t).
    """
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    key = pan.keys[sig]
    sv = pan.sizevol[look]
    nreb = len(pan.reb)
    wmax = np.zeros(nreb)          # realised max slot weight
    weff = np.zeros(nreb)          # effective N = 1 / sum(w^2)
    nheld = np.zeros(nreb)
    sumdev = 0.0
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        held = np.flatnonzero(cur >= 0)
        young = held[(t - cur[held]) < H] if len(held) else held
        if len(young):
            young = young[pr[t, young]]
        keep = [int(c) for c in young]
        need = N - len(keep)
        take = []
        if need > 0:
            k = key[ts].copy()
            k[~(pan.elig[ts] & pr[ts])] = np.inf
            for c in keep:
                k[c] = np.inf
            order = np.argsort(k, kind="stable")
            for c in order:
                if need == 0 or not np.isfinite(k[c]):
                    break
                take.append(int(c))
                need -= 1
        new = np.full(K, -1, dtype=np.int64)
        for c in keep:
            new[c] = cur[c]
        for c in take:
            new[c] = t
        cur = new
        sel = np.flatnonzero(cur >= 0)
        if not len(sel):
            continue
        if alpha == 0.0:
            w = np.full(len(sel), 1.0 / len(sel))
        else:
            v = sv[ts, sel].astype(float)
            if not np.all(np.isfinite(v)):
                med = np.nanmedian(v[np.isfinite(v)]) if np.any(np.isfinite(v)) else VOL_FLOOR
                v = np.where(np.isfinite(v), v, med)
            raw = np.power(v, -alpha)
            w = raw / raw.sum()
        sumdev = max(sumdev, abs(float(w.sum()) - 1.0))        # gate G3
        wmax[i], weff[i], nheld[i] = float(w.max()), 1.0 / float((w ** 2).sum()), len(sel)
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = w
    w0 = int(np.searchsorted(pan.reb, WARMUP))
    diag = dict(w_max=float(wmax[w0:].max()), w_max_mean=float(wmax[w0:].mean()),
                n_eff=float(weff[w0:].mean()), n_held=float(nheld[w0:].mean()),
                sum_dev=float(sumdev))
    return W, diag


def run(pan, Wt, gross=A_G):
    """Hold gross*Wt from each rebalance date, drift between, 10 bps on traded notional."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    for i0, i1 in zip(pan.reb, ends):
        w0 = gross * Wt[i0]
        turn[i0] = np.abs(w0 - curw).sum()
        base = Cp[i0]
        A = w0[None, :] * (Cp[i0:i1] / base[None, :])
        c0 = 1.0 - w0.sum()
        V = A.sum(axis=1) + c0
        held[i0:i1] = A / V[:, None]
        Ae = w0 * (C[i1 - 1] / base)
        curw = Ae / (Ae.sum() + c0)
    r = (held * rets).sum(axis=1) - turn * COST / 1e4
    return r, float(turn.sum() / (T / 252.0)), float(held[WARMUP:].sum(axis=1).mean())


# ------------------------------------------------------------------ KEEP paths
def legs_4a(book, live):
    return dict(H1=book["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(book, spy):
    return dict(H1=book["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=book["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=book["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=book["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=book["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1264 lane B — {SLUG}")
    say("# frozen book: RAW composite, gate = above 200d MA AND vol20 < 0.60, "
        f"N={A_N}, H={A_H}, GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}")
    say(f"# DIAL 1 alpha = {ALPHAS}   (0.00 = COMMITTED EQUAL-WEIGHT ANCHOR)")
    say(f"# DIAL 2 look  = {LOOKS} days")
    say(f"# reported-not-dials: panel {{U56,B136,SMALL}} x signal {list(SIGNALS)}")
    say(f"# frozen constant (NOT a dial): VOL_FLOOR = {VOL_FLOOR}; no max-slot cap (published instead)")
    say("# SELECTION IS IDENTICAL AT EVERY ALPHA BY CONSTRUCTION — only the slot weights move")

    panels = []
    px = load_universe()
    panels.append(("U56", px, [c for c in px.columns if c != "SPY"]))
    pb = load_universe(broad=True)
    panels.append((f"B{pb.shape[1]-1}", pb, [c for c in pb.columns if c != "SPY"]))
    psm = load_universe(small=True)
    meta = pd.read_csv(ROOT / "data" / "small_meta.csv")
    bad = set(meta.loc[meta.max_1d_move >= 1.0, "ticker"])
    inv_s = [c for c in psm.columns if c != "SPY" and c not in bad]
    say(f"# SMALL panel: {psm.shape[1]-1} names, {len(bad & set(psm.columns))} dropped for "
        f"max_1d_move >= 1.0 -> {len(inv_s)} investable")
    panels.append((f"SMALL{len(inv_s)}", psm, inv_s))

    rows, r8rows = [], []
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].values[WARMUP:]
        live = windows(idx, live_r)

        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  window {idx[0].date()}..{idx[-1].date()}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / {spy['full']['MaxDD']:7.2%}"
            f"   halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}"
            f"   OOS {spy['oos']['CAGR']:7.2%} / {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / {live['full']['MaxDD']:7.2%}"
            f"   halves {live['h1']['Sharpe']:.4f}/{live['h2']['Sharpe']:.4f}"
            f"   OOS {live['oos']['CAGR']:7.2%} / {live['oos']['Sharpe']:.4f}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}   "
            f"CAGR floor {CAGR_FLOOR*spy['full']['CAGR']:7.2%}   "
            f"Sharpe bars H1 {spy['h1']['Sharpe']:.4f} H2 {spy['h2']['Sharpe']:.4f} OOS {spy['oos']['Sharpe']:.4f}")

        for sig in SIGNALS:
            say(f"\n   --- signal {sig} ---")
            say("   alpha look |    CAGR   Sharpe    MaxDD |  H1/H2 Sharpe |  OOS Sh |  turn  wmax  Neff | 4a 4b | fail4b")
            cells = {}
            for alpha in ALPHAS:
                for look in LOOKS:
                    W, diag = build(pan, sig, alpha, look)
                    r, turn, expo = run(pan, W)
                    r = r[WARMUP:]
                    w = windows(idx, r)
                    a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                    rec = dict(panel=pname, signal=sig, alpha=alpha, look=look,
                               **flat(w), turnover=turn, exposure=expo, **diag,
                               keep4a=all(a4.values()), keep4b=all(b4.values()),
                               fail4a=failed(a4), fail4b=failed(b4))
                    rows.append(rec)
                    cells[(alpha, look)] = rec
                    say(f"   {alpha:5.2f} {look:4d} | {w['full']['CAGR']:7.2%} {w['full']['Sharpe']:8.4f} "
                        f"{w['full']['MaxDD']:8.2%} | {w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f} | "
                        f"{w['oos']['Sharpe']:7.4f} | {turn:5.2f} {diag['w_max']:5.3f} {diag['n_eff']:5.2f} | "
                        f"{'Y' if all(a4.values()) else 'n'}  {'Y' if all(b4.values()) else 'n'} | {failed(b4)}")

            # ---- gates on the anchor cells
            if pname == "U56":
                # VINTAGE-PINNED replay: truncate to the cache end date the committed numbers
                # were produced on, so the gate tests CONSTRUCTION and not the extra tape day.
                q = p_px.loc[:VINTAGE]
                vpan = Panel("U56v", q, [c for c in q.columns if c != "SPY"])
                Wv, _ = build(vpan, sig, 0.00, 20)
                rv, _, _ = run(vpan, Wv)
                tv = stats(rv[WARMUP:])
                tgt = COMMITTED_U56 if sig == "COMPOSITE3" else COMMITTED_M12
                err = max(abs(tv["CAGR"] - tgt[0]), abs(tv["Sharpe"] - tgt[1]), abs(tv["MaxDD"] - tgt[2]))
                gate(f"{'G1' if sig == 'COMPOSITE3' else 'G4'} vintage-pinned replay "
                     f"(U56 {sig} alpha0 @ {VINTAGE.date()})",
                     f"{tv['CAGR']:.4%}/{tv['Sharpe']:.4f}/{tv['MaxDD']:.4%} err {err:.2e}",
                     f"committed {tgt[0]:.4%}/{tgt[1]:.4f}/{tgt[2]:.4%}, err < 1e-4", err < 1e-4)
                a = cells[(0.00, 20)]
                gate(f"G6 one-extra-day drift ({sig})",
                     f"CAGR {a['full_CAGR']-tv['CAGR']:+.4%}  Sharpe {a['full_Sharpe']-tv['Sharpe']:+.4f}  "
                     f"MaxDD {a['full_MaxDD']-tv['MaxDD']:+.4%}",
                     "published, not toleranced (see docstring)", True)
            if pname == "U56" and sig == "COMPOSITE3":
                d = max(abs(cells[(0.00, L)]["full_Sharpe"] - cells[(0.00, 20)]["full_Sharpe"]) for L in LOOKS)
                gate("G2 alpha0 is LOOK-invariant", f"{d:.3e}", "== 0.0", d == 0.0)
                sd = max(cells[(al, L)]["sum_dev"] for al in ALPHAS for L in LOOKS)
                gate("G3 slot weights sum to 1", f"{sd:.3e}", "< 1e-12", sd < 1e-12)

            # ---- rule 8: choose (alpha, look) on IS only, read OOS once
            ks = list(cells)
            is_s = np.array([cells[k]["is__Sharpe"] for k in ks])
            oos_s = np.array([cells[k]["oos_Sharpe"] for k in ks])
            pick = ks[int(np.nanargmax(is_s))]
            nothing = cells[(0.00, 20)]
            r8 = dict(panel=pname, signal=sig, pick_alpha=pick[0], pick_look=pick[1],
                      pick_IS=cells[pick]["is__Sharpe"], pick_OOS=cells[pick]["oos_Sharpe"],
                      donothing_OOS=nothing["oos_Sharpe"],
                      delta=cells[pick]["oos_Sharpe"] - nothing["oos_Sharpe"],
                      cellmean_OOS=float(np.nanmean(oos_s)), worst_OOS=float(np.nanmin(oos_s)),
                      best_OOS=float(np.nanmax(oos_s)), rank_IS_OOS=rankcorr(is_s, oos_s),
                      pick_OOS_MaxDD=cells[pick]["oos_MaxDD"], nothing_OOS_MaxDD=nothing["oos_MaxDD"],
                      spy_OOS=spy["oos"]["Sharpe"], live_OOS=live["oos"]["Sharpe"],
                      pick_keep4b=cells[pick]["keep4b"], nothing_keep4b=nothing["keep4b"])
            r8rows.append(r8)
            say(f"   RULE 8  IS-argmax = alpha {pick[0]:.2f} / look {pick[1]} (IS Sh {r8['pick_IS']:.4f}) "
                f"-> OOS {r8['pick_OOS']:.4f}  vs do-nothing {r8['donothing_OOS']:.4f}  "
                f"delta {r8['delta']:+.4f}   cellmean {r8['cellmean_OOS']:.4f}  worst {r8['worst_OOS']:.4f}  "
                f"rank corr IS/OOS {r8['rank_IS_OOS']:+.2f}")

    grid = pd.DataFrame(rows)
    wf = pd.DataFrame(r8rows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)

    # ---- G5 determinism
    pan = Panel("U56", panels[0][1], panels[0][2])
    chk = []
    for alpha in ALPHAS:
        for look in LOOKS:
            W, _ = build(pan, "COMPOSITE3", alpha, look)
            r, _, _ = run(pan, W)
            chk.append(sharpe(r[WARMUP:]))
    ref = grid[(grid.panel == "U56") & (grid.signal == "COMPOSITE3")].full_Sharpe.values
    dd = float(np.max(np.abs(np.array(chk) - ref)))
    gate("G5 determinism (U56 composite3 grid re-run)", f"{dd:.3e}", "== 0.0", dd == 0.0)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    say("\n## SUMMARY")
    say(f"   cells {len(grid)}   4a passes {int(grid.keep4a.sum())}   4b passes {int(grid.keep4b.sum())}")
    for pname in grid.panel.unique():
        for sig in SIGNALS:
            g = grid[(grid.panel == pname) & (grid.signal == sig)]
            say(f"   {pname:9s} {sig:11s} 4b {int(g.keep4b.sum()):2d}/{len(g)}   "
                f"MaxDD range {g.full_MaxDD.min():7.2%}..{g.full_MaxDD.max():7.2%}   "
                f"CAGR range {g.full_CAGR.min():6.2%}..{g.full_CAGR.max():6.2%}   "
                f"turnover {g.turnover.min():.2f}..{g.turnover.max():.2f}")
    say(f"   rule 8 chooser-minus-do-nothing: {wf.delta.round(4).tolist()}  mean {wf.delta.mean():+.4f}  "
        f"reaches do-nothing at {int((wf.delta > 0).sum())} of {len(wf)}")
    say(f"   GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass   {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
