#!/usr/bin/env python3
"""Idea 1266 (lane B, 2026-09-18): does a CORRELATION BRAKE see the DRAWDOWN that a VOLATILITY
BRAKE was BLIND to?

THE PREMISE.  Seven dials on the standing 2026-09-04 KEEP 4b book — rebalance phase (1253),
calendar years (1254), ex-post winner names (1255), the signal (1257), sector caps (1258), slot
sizing (1264), the N x H frame (1265) and the idle sleeve (1268) — all land on one sentence:
every other 4b leg passes at essentially every grid point and the DRAWDOWN CAP is the only leg
that ever fails.  Three purchase mechanisms have been priced and all three failed.  1264's
inverse-vol SLOT SIZING converts, but full Sharpe falls monotonically in the exponent and rule 8
picks EQUAL WEIGHT.  1263's portfolio VOL TARGETING converts 14 of 126 cells, 7 of them
reproduced by a flat gross cut with no timing at all.  1262's explicit DRAWDOWN BRAKE could not
arm at the only trough that matters, because 4b's DD leg reads a POINT on the equity path while a
brake can only act on a STATE the book occupies on a DECISION date.

THIS RUN PRICES THE ONE REMAINING MECHANISM THAT LOOKS AT THE BOOK'S CROSS-SECTION RATHER THAN
AT ITS OWN PAST RETURNS.  A portfolio drawdown is a CORRELATION event before it is a volatility
event: names that diversified each other stop doing so, and the book's realised vol only records
that AFTERWARDS.  So the trigger here is the MEAN PAIRWISE CORRELATION OF THE BOOK'S OWN
HOLDINGS, read at the decision close and applied at t+1 (rule 2):

    S_corr(i) = mean of the off-diagonal of corr(daily returns of the names the book is about to
                hold), over the trailing LOOK days ending at the decision close t-1
    p(i)      = share of that statistic's OWN STRICTLY PRIOR history at or below S_corr(i)
    u(i)      = max(0, 2*(p(i) - 0.5))                     in [0, 1]
    gross(i)  = A_G * (1 - SLOPE * u(i))                    in [0, A_G], never leveraged

WHY THE EXPANDING-PERCENTILE FORM AND NOT A RAW THRESHOLD.  A raw correlation threshold would
need a level (a third parameter) and the level is not comparable between a correlation and a
volatility, so the head-to-head this idea asks for would be unreadable.  Mapping each statistic
through ITS OWN expanding percentile makes the two brakes IDENTICALLY AGGRESSIVE BY
CONSTRUCTION — same marginal distribution of intensity, same mean gross up to arming order — so
the comparison is a pure TIMING comparison and nothing else.  That is the whole point of the run.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    LOOK  {20, 60, 126, 252} days  — the correlation lookback.
    SLOPE {0, 0.25, 0.50, 0.75, 1.00} — the de-gross slope: the fraction of gross removed when
          the statistic sits at the top of its own history.  SLOPE = 0 IS EXACTLY THE COMMITTED
          ANCHOR (constant gross 0.75) and is in the grid so the do-nothing control is MEASURED,
          not assumed.  SLOPE = 1.00 reaches exactly zero gross at a new historical high.
  4 x 5 = 20 cells per (panel, signal) per brake arm.  EVERY ONE PUBLISHED in the .grid.csv.

THE THREE COMPARANDS, none of them a dial, all of them reported at every cell:
  (1) GROSS-MATCHED FLAT CONTROL — constant gross at that cell's OWN realised mean gross.  The
      queue names this control explicitly, and the record has twice established (the 2026-09-17
      gross-dial run and 1263) that gross alone is a pure CAGR-for-drawdown slide, so a braked
      cell that only beats the 0.75 anchor has shown nothing.
  (2) THE VOLATILITY TWIN — the identical machinery driven by the ANCHOR BOOK'S OWN REALISED
      VOLATILITY over the same LOOK.  This is the literal question: same form, same intensity
      distribution, same slope, different statistic.
  (3) A TIMING PLACEBO — the SAME intensity series RANDOMLY PERMUTED (3 fixed seeds).  It has
      the identical marginal distribution and therefore the identical mean gross, so it is an
      EXACT gross match with the timing destroyed.  If the brake's value is timing, it must beat
      this; if it is exposure, it cannot.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: eligibility = above own 200d MA AND
vol20 < 0.60; N = 20; H = 126 minimum hold; base GROSS = 0.75 of NAV; WEEKLY decide-Friday /
trade-Monday; 10 bps per unit turnover; t+1 execution; 260-row warm-up; RAW-composite ranking;
equal 1/len(held) slots.  SELECTION IS IDENTICAL AT EVERY CELL BY CONSTRUCTION — the dials touch
only how much of NAV the same names are held at.

FROZEN CONSTANTS, DECLARED SO THEY ARE NOT MISTAKEN FOR DIALS.  (i) MINHIST = 52 decision dates
of prior finite history before the brake may arm at all; below that u = 0.  (ii) No hysteresis
band and no minimum brake duration — a release band would be a third parameter and rule 4
forbids it; the consequence (chatter) is measured as turnover rather than tuned away.  (iii) The
brake never raises gross above the anchor's 0.75; there is no leverage anywhere (rule 2).
(iv) A name enters the correlation window only if it is PRICED at both ends of that window, so a
listing gap cannot masquerade as a zero-return diversifier; the number of columns dropped this
way is published.  (v) The correlation is EQUAL-WEIGHTED over pairs, not weighted by slot size,
because the committed book is equal-weighted anyway.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) INERT — the brake barely moves MaxDD (< 0.20pp) at any cell.
  (B) THE DD LEG IS BOUGHT AND CHEAPLY, AND CORRELATION IS WHY — some cell materially improves
      MaxDD, holds 4b's CAGR floor and both half-Sharpe legs, converts a committed 4b FAIL,
      BEATS its gross-matched control AND its timing placebo AND its volatility twin, and rule 8
      reaches it.  That is a KEEP-candidate memo with exact RULES wording.
  (C) BOUGHT AND OVERPAID FOR, or BOUGHT BY EXPOSURE RATHER THAN BY TIMING — MaxDD improves but
      CAGR falls through the floor, or a half Sharpe falls below SPY, or the gain is reproduced
      by the flat control or by the placebo.
  (D) CORRELATION IS THE SAME BRAKE AS VOLATILITY — the two intensity series are near-identical
      and the answer to the title is simply NO, there was nothing extra to see.
  (E) WORSE — the brake de-grosses into the recovery and degrades Sharpe or drawdown against a
      flat schedule at the same mean exposure.
  Outcomes are not mutually exclusive across panels; whichever fire are reported as they fall,
  and the capital verdict follows rule 8, not the best cell.

RULE 8 (walk-forward, required).  (LOOK, SLOPE) is CHOSEN on warm-up..2016-12-31 by IS Sharpe
ALONE and 2017-2026 is read ONCE, per (panel, signal, brake).  Reported against (i) the
DO-NOTHING control = SLOPE 0 (the committed constant-gross book), (ii) the mean over all 20
cells, (iii) the WORST cell, with the IS/OOS rank correlation over the 20.  The capital verdict
is the sign of chooser-minus-do-nothing, never the best cell's number.

GATES.  G1 vintage-pinned replay truncated at 2026-09-16 (the cache vintage the committed
numbers were produced on): U56 COMPOSITE3 SLOPE 0 must replay the committed 15.7147% / 1.1480 /
-19.1276% to 1e-4.  G2 the same for M12_1 against 1257's 16.7116% / 1.1893 / -20.5813%.  G3
SLOPE 0 is bit-identical at all four LOOK values and in both brake arms.  G4 realised gross
inside [0, 0.75] at every rebalance of every cell.  G5 CAUSALITY: the intensity at decision i
recomputed from the statistic TRUNCATED AT i is bit-identical to the full-sample intensity, and
the brake is not inert.  G6 u == 0 wherever p <= 0.5 and u is monotone non-decreasing in p.  G7
SLOPE 1.00 reaches exactly zero gross.  G8 the SLOPE 0 cell's gross-matched control IS that
cell.  G9 determinism: the whole U56 COMPOSITE3 CORR grid recomputed bit for bit.  G10 the
one-extra-day cache drift against the pinned vintage is published, not toleranced.  G11 the
correlation statistic is inside [-1, 1] everywhere and the counts of undefined windows and of
columns dropped for a listing gap are published.  G12 the PLACEBO's mean gross equals the real
brake's mean gross exactly (it is a permutation), so it is an exact gross match.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B135 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is an
UPPER bound.  The headline is a DIFFERENCE between gross schedules applied to the SAME holdings
on the SAME panel — the selected names are identical at every cell by construction — which is
first-order immune to a level bias that moves all cells together.  One direction is NOT neutral
and is stated: a current-constituent panel UNDERSTATES both the deep drawdowns and the
correlation spikes a real momentum book took in names later delisted, so the anchor's drawdown is
FLATTERED and the correlation signal is MUTED; any DD improvement reported here is a LOWER bound
on a live panel, while the CAGR it gives up is measured against a flattered comparand.

Runs standalone and offline (committed price caches only).
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
SLUG = "does-a-CORRELATION-BRAKE-see-the-DRAWDOWN-that-a-VOLATILITY-BRAKE-was-BLIND-to"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_B"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
IS_END = pd.Timestamp("2016-12-31")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                       # the frozen 2026-09-04 book
SIGNALS = {"COMPOSITE3": [(21, 252), (0, 126), (0, 63)], "M12_1": [(21, 252)]}
LOOKS = [20, 60, 126, 252]                          # DIAL 1
SLOPES = [0.00, 0.25, 0.50, 0.75, 1.00]             # DIAL 2 (0.00 == committed anchor)
BRAKES = ["CORR", "VOL"]                            # reported, not a dial
MINHIST = 52                                        # frozen constant, not a dial
SEEDS = [11, 23, 37]                                # placebo permutations, fixed
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)      # gate G1
COMMITTED_M12 = (0.167116, 1.18933, -0.205813)      # gate G2
VINTAGE = pd.Timestamp("2026-09-16")
_LOG: list[str] = []
GATES: list[dict] = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    _LOG.append(s)


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
    return float(np.prod(1.0 + r) ** (252.0 / len(r)) - 1.0)


def mdd(r):
    e = np.cumprod(1.0 + np.asarray(r, float))
    return float((e / np.maximum.accumulate(e) - 1.0).min())


def vol(r):
    return float(np.asarray(r, float).std(ddof=0) * np.sqrt(252))


def stats(r):
    return dict(CAGR=cagr(r), Sharpe=sharpe(r), MaxDD=mdd(r), Vol=vol(r))


def rankcorr(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return float("nan")
    ra, rb = pd.Series(a[ok]).rank().values, pd.Series(b[ok]).rank().values
    sa, sb = ra.std(ddof=0), rb.std(ddof=0)
    if sa == 0 or sb == 0:
        return float("nan")
    return float(((ra - ra.mean()) * (rb - rb.mean())).mean() / (sa * sb))


def windows(idx, r):
    n = len(r)
    h = n // 2
    o = int(np.searchsorted(idx.values, OOS_START.to_datetime64()))
    return dict(full=stats(r), h1=stats(r[:h]), h2=stats(r[h:]), oos=stats(r[o:]), is_=stats(r[:o]))


def flat(w):
    return {f"{k}_{m}": x for k, v in w.items() for m, x in v.items()}


# ------------------------------------------------------------------ panel (1262/1263/1264's, unchanged)
class Panel:
    def __init__(self, name, px, invest):
        self.name, self.px, self.invest = name, px, invest
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
            comp = (sum(parts) / len(parts)).values
            self.keys[sig] = np.where(np.isfinite(comp), -comp, np.inf)
        self.above = (q > q.rolling(200).mean()).values
        qr = q.pct_change()
        vol20 = (qr.rolling(20).std() * np.sqrt(252)).values
        self.volok = np.nan_to_num(vol20, nan=1e9) < MAXVOL
        self.elig = self.above & self.volok
        self.spy = px["SPY"].pct_change().fillna(0.0).values
        m = rebalance_mask(px.index, "W").shift(1, fill_value=False).values.copy()
        m[0] = True
        self.reb = np.flatnonzero(m)


def build(pan, sig, N=A_N, H=A_H, lag=1):
    """The frozen selection frame at GROSS = 1.0.  Identical to 1262/1263/1264's build."""
    T, M = pan.rets.shape
    K = len(pan.iinv)
    W = np.zeros((T, M))
    cur = np.full(K, -1, dtype=np.int64)
    pr = pan.priced[:, pan.iinv]
    key = pan.keys[sig]
    nreb = len(pan.reb)
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
        w = np.full(len(sel), 1.0 / len(sel))
        stop = pan.reb[i + 1] if i + 1 < nreb else T
        W[t:stop, pan.iinv[sel]] = w
    return W


def run(pan, Wt, gross):
    """gross: scalar or one value per rebalance date.  Hold gross*Wt from each rebalance, drift
    between, 10 bps on traded notional (1262/1263/1264's run, unchanged)."""
    rets = pan.rets
    T, M = rets.shape
    C = np.cumprod(1.0 + rets, axis=0)
    Cp = np.vstack([np.ones((1, M)), C[:-1]])
    held = np.zeros((T, M))
    turn = np.zeros(T)
    curw = np.zeros(M)
    ends = np.append(pan.reb[1:], T)
    g = np.full(len(pan.reb), float(gross)) if np.isscalar(gross) else np.asarray(gross, float)
    for i, (i0, i1) in enumerate(zip(pan.reb, ends)):
        w0 = g[i] * Wt[i0]
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


# ------------------------------------------------------------------ the two statistics
def corr_series(pan, Wt, look):
    """Mean pairwise correlation of the names the book is ABOUT TO HOLD, over the trailing `look`
    days ending at the DECISION close t-1.  A column enters only if PRICED at both ends of the
    window (frozen convention iv), so a listing gap cannot pose as a zero-return diversifier."""
    S = np.full(len(pan.reb), np.nan)
    undefined, dropped = 0, 0
    for i, t in enumerate(pan.reb):
        ts = max(t - 1, 0)
        a = ts - look + 1
        if a < 0:
            undefined += 1
            continue
        cols = np.flatnonzero(Wt[t] > 0)
        if len(cols) < 2:
            undefined += 1
            continue
        ok = pan.priced[a, cols] & pan.priced[ts, cols]
        dropped += int(len(cols) - ok.sum())
        cols = cols[ok]
        if len(cols) < 2:
            undefined += 1
            continue
        R = pan.rets[a:ts + 1][:, cols]
        sd = R.std(axis=0, ddof=0)
        R = R[:, sd > 0]
        if R.shape[1] < 2:
            undefined += 1
            continue
        C = np.corrcoef(R, rowvar=False)
        iu = np.triu_indices(C.shape[0], 1)
        v = C[iu]
        v = v[np.isfinite(v)]
        if not len(v):
            undefined += 1
            continue
        S[i] = float(v.mean())
    return S, undefined, dropped


def vol_series(pan, anchor_r, look):
    """Realised volatility of the ANCHOR BOOK'S OWN returns over the trailing `look` days ending
    at the decision close t-1 — the volatility brake this idea is asked to beat."""
    S = np.full(len(pan.reb), np.nan)
    undefined = 0
    for i, t in enumerate(pan.reb):
        ts = max(t - 1, 0)
        a = ts - look + 1
        if a < 0:
            undefined += 1
            continue
        S[i] = float(np.std(anchor_r[a:ts + 1], ddof=0) * np.sqrt(252.0))
    return S, undefined, 0


def intensity(S, minhist=MINHIST):
    """u(i) = max(0, 2*(p(i)-0.5)) where p(i) is the share of the statistic's OWN STRICTLY PRIOR
    finite history at or below S(i).  Strictly causal by construction (gate G5)."""
    n = len(S)
    u = np.zeros(n)
    p = np.full(n, np.nan)
    hist: list[float] = []
    for i in range(n):
        s = S[i]
        if np.isfinite(s):
            if len(hist) >= minhist:
                h = np.asarray(hist, float)
                pi = float((h <= s).mean())
                p[i] = pi
                u[i] = max(0.0, 2.0 * (pi - 0.5))
            hist.append(float(s))
    return u, p


def schedule(u, slope):
    g = A_G * (1.0 - float(slope) * np.asarray(u, float))
    return np.clip(g, 0.0, A_G)


def gdiag(pan, g, u):
    w0 = int(np.searchsorted(pan.reb, WARMUP))
    on = (g < A_G - 1e-12)
    ep = int(np.sum(on[w0:] & ~np.concatenate([[False], on[w0:-1]]))) if len(on) > w0 else 0
    return dict(g_mean=float(g[w0:].mean()), g_min=float(g[w0:].min()), g_max=float(g[w0:].max()),
                brake_share=float(on[w0:].mean()), episodes=ep, u_mean=float(u[w0:].mean()),
                u_max=float(u[w0:].max()))


# ------------------------------------------------------------------ KEEP paths
def legs_4a(bk, live):
    return dict(H1=bk["h1"]["Sharpe"] > live["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > live["h2"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= live["full"]["MaxDD"])


def legs_4b(bk, spy):
    return dict(H1=bk["h1"]["Sharpe"] > spy["h1"]["Sharpe"],
                H2=bk["h2"]["Sharpe"] > spy["h2"]["Sharpe"],
                OOS=bk["oos"]["Sharpe"] > spy["oos"]["Sharpe"],
                DD=bk["full"]["MaxDD"] >= DD_CAP * spy["full"]["MaxDD"],
                CAGR=bk["full"]["CAGR"] >= CAGR_FLOOR * spy["full"]["CAGR"])


def failed(d):
    return ",".join(k for k, v in d.items() if not v) or "-"


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    say(f"# {DATE} idea 1266 lane B — {SLUG}")
    say(f"# frozen book: RAW composite, gate = above 200d MA AND vol20 < {MAXVOL}, N={A_N}, "
        f"H={A_H}, base GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}, equal slots")
    say(f"# DIAL 1 LOOK  = {LOOKS}   (correlation / volatility lookback, days)")
    say(f"# DIAL 2 SLOPE = {SLOPES}  (0.00 = COMMITTED CONSTANT-GROSS ANCHOR; 1.00 = flat at a "
        f"new historical high of the statistic)")
    say(f"# reported-not-dials: panel {{U56,B135,SMALL}} x signal {list(SIGNALS)} x brake {BRAKES}")
    say(f"# comparands at every cell: (1) gross-matched FLAT control, (2) the VOLATILITY TWIN, "
        f"(3) a TIMING PLACEBO = the same intensity series permuted, seeds {SEEDS}")
    say(f"# frozen constants (NOT dials): MINHIST={MINHIST} decision dates before the brake may "
        f"arm; no hysteresis band; no minimum duration; gross never above {A_G}; priced-at-both-"
        f"ends column filter; equal-weighted pairs")
    say("# SELECTION IS IDENTICAL AT EVERY CELL BY CONSTRUCTION — only the gross schedule moves")
    say("# BOTH BRAKES SHARE THE EXPANDING-PERCENTILE FORM, SO THEIR INTENSITY DISTRIBUTIONS ARE "
        "IDENTICAL AND THE HEAD-TO-HEAD IS A PURE TIMING COMPARISON")

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

    rows, r8rows, sigrows, eprows = [], [], [], []
    for pname, p_px, inv in panels:
        pan = Panel(pname, p_px, inv)
        idx = pan.idx[WARMUP:]
        spy = windows(idx, pan.spy[WARMUP:])
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST,
                          freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)

        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  "
            f"{idx[0].date()}..{idx[-1].date()}  n_rebalances={len(pan.reb)}")
        say(f"   SPY     full {spy['full']['CAGR']:7.2%} / {spy['full']['Sharpe']:.4f} / "
            f"{spy['full']['MaxDD']:7.2%} / vol {spy['full']['Vol']:.2%}   "
            f"halves {spy['h1']['Sharpe']:.4f}/{spy['h2']['Sharpe']:.4f}   OOS {spy['oos']['Sharpe']:.4f}")
        say(f"   LIVE v2 full {live['full']['CAGR']:7.2%} / {live['full']['Sharpe']:.4f} / "
            f"{live['full']['MaxDD']:7.2%}   OOS {live['oos']['Sharpe']:.4f}")
        say(f"   4b bars: DD cap {DD_CAP*spy['full']['MaxDD']:7.2%}   CAGR floor "
            f"{CAGR_FLOOR*spy['full']['CAGR']:7.2%}   Sharpe bars H1 {spy['h1']['Sharpe']:.4f} "
            f"H2 {spy['h2']['Sharpe']:.4f} OOS {spy['oos']['Sharpe']:.4f}")

        for sig in SIGNALS:
            Wt = build(pan, sig)
            anchor_r, anchor_turn, _ = run(pan, Wt, A_G)
            aw = windows(idx, anchor_r[WARMUP:])
            say(f"\n   --- signal {sig} ---   anchor {aw['full']['CAGR']:.2%} / "
                f"{aw['full']['Sharpe']:.4f} / {aw['full']['MaxDD']:.2%}, turnover {anchor_turn:.2f}/yr")

            # ---- the anchor's worst drawdown episode: what did each statistic see, and when?
            e = np.cumprod(1.0 + anchor_r)
            ddp = e / np.maximum.accumulate(e) - 1.0
            tr = WARMUP + int(np.argmin(ddp[WARMUP:]))
            pk = int(np.argmax(e[:tr + 1]))
            say(f"   worst drawdown episode: peak {pan.idx[pk].date()} -> trough "
                f"{pan.idx[tr].date()} ({ddp[tr]:.2%})")

            # ---- statistics and intensities, once per (brake, LOOK)
            U, P, S = {}, {}, {}
            for look in LOOKS:
                sc, und_c, drop_c = corr_series(pan, Wt, look)
                sv, und_v, _ = vol_series(pan, anchor_r, look)
                for br, s, und, drp in (("CORR", sc, und_c, drop_c), ("VOL", sv, und_v, 0)):
                    u, p = intensity(s)
                    U[(br, look)], P[(br, look)], S[(br, look)] = u, p, s
                    w0 = int(np.searchsorted(pan.reb, WARMUP))
                    sigrows.append(dict(panel=pname, signal=sig, brake=br, look=look,
                                        undefined=und, gap_dropped=drp,
                                        S_min=float(np.nanmin(s)), S_max=float(np.nanmax(s)),
                                        S_mean=float(np.nanmean(s)),
                                        u_mean=float(u[w0:].mean()),
                                        armed_share=float((u[w0:] > 0).mean())))
                rc = rankcorr(U[("CORR", look)], U[("VOL", look)])
                # what each brake saw going INTO the trough (decision dates in the episode)
                ep_i = np.flatnonzero((pan.reb >= pk) & (pan.reb <= tr))
                pre_i = np.flatnonzero((pan.reb >= max(pk - 42, 0)) & (pan.reb < pk))
                def _first(br):
                    a = np.flatnonzero(U[(br, look)][ep_i] >= 0.5)
                    return pan.idx[pan.reb[ep_i[a[0]]]].date() if len(a) else None
                row = dict(panel=pname, signal=sig, look=look, peak=str(pan.idx[pk].date()),
                           trough=str(pan.idx[tr].date()), dd=float(ddp[tr]),
                           n_decisions=len(ep_i),
                           corr_u_mean=float(np.mean(U[("CORR", look)][ep_i])) if len(ep_i) else np.nan,
                           vol_u_mean=float(np.mean(U[("VOL", look)][ep_i])) if len(ep_i) else np.nan,
                           corr_u_pre=float(np.mean(U[("CORR", look)][pre_i])) if len(pre_i) else np.nan,
                           vol_u_pre=float(np.mean(U[("VOL", look)][pre_i])) if len(pre_i) else np.nan,
                           corr_first_half=str(_first("CORR")), vol_first_half=str(_first("VOL")),
                           rank_corr_u=rc)
                eprows.append(row)
                say(f"      LOOK {look:3d}: rank corr u(CORR) vs u(VOL) {rc:+.3f} | over the "
                    f"{len(ep_i)} decision dates INSIDE the episode mean u CORR "
                    f"{row['corr_u_mean']:.3f} vs VOL {row['vol_u_mean']:.3f} | in the 42 rows "
                    f"BEFORE the peak CORR {row['corr_u_pre']:.3f} vs VOL {row['vol_u_pre']:.3f} | "
                    f"first u>=0.5 CORR {row['corr_first_half']} VOL {row['vol_first_half']}")

            say("   brake LOOK slope |    CAGR   Sharpe    MaxDD    vol |  H1/H2 Sharpe |  OOS Sh | "
                "turn  gmean gmin  on% ep | 4a 4b | fail4b | vs FLAT / vs PLACEBO")
            cells, ctrl_cache = {}, {}
            for br in BRAKES:
                for look in LOOKS:
                    u = U[(br, look)]
                    for sl in SLOPES:
                        g = schedule(u, sl)
                        diag = gdiag(pan, g, u)
                        r, turn, expo = run(pan, Wt, g)
                        w = windows(idx, r[WARMUP:])
                        key = round(diag["g_mean"], 12)
                        if key not in ctrl_cache:
                            cr, cturn, _ = run(pan, Wt, diag["g_mean"])
                            ctrl_cache[key] = (windows(idx, cr[WARMUP:]), cturn)
                        cw, cturn = ctrl_cache[key]
                        cb4 = legs_4b(cw, spy)
                        # timing placebo: same intensity series, permuted -> identical mean gross
                        pl = []
                        for sd in SEEDS:
                            if sl == 0.0:
                                pl.append((w, turn))
                                continue
                            rng = np.random.default_rng(sd)
                            up = u.copy()
                            rng.shuffle(up)
                            pr_, pt_, _ = run(pan, Wt, schedule(up, sl))
                            pl.append((windows(idx, pr_[WARMUP:]), pt_))
                        pm = {k: float(np.mean([x[0]["full"][k] for x in pl]))
                              for k in ("CAGR", "Sharpe", "MaxDD")}
                        pm_oos = float(np.mean([x[0]["oos"]["Sharpe"] for x in pl]))
                        a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                        rec = dict(panel=pname, signal=sig, brake=br, look=look, slope=sl,
                                   **flat(w), turnover=turn, exposure=expo, **diag,
                                   ctrl_CAGR=cw["full"]["CAGR"], ctrl_Sharpe=cw["full"]["Sharpe"],
                                   ctrl_MaxDD=cw["full"]["MaxDD"],
                                   ctrl_oos_Sharpe=cw["oos"]["Sharpe"], ctrl_turnover=cturn,
                                   ctrl_keep4b=all(cb4.values()), ctrl_fail4b=failed(cb4),
                                   d_CAGR=w["full"]["CAGR"] - cw["full"]["CAGR"],
                                   d_Sharpe=w["full"]["Sharpe"] - cw["full"]["Sharpe"],
                                   d_MaxDD=w["full"]["MaxDD"] - cw["full"]["MaxDD"],
                                   d_oos_Sharpe=w["oos"]["Sharpe"] - cw["oos"]["Sharpe"],
                                   plac_CAGR=pm["CAGR"], plac_Sharpe=pm["Sharpe"],
                                   plac_MaxDD=pm["MaxDD"], plac_oos_Sharpe=pm_oos,
                                   t_CAGR=w["full"]["CAGR"] - pm["CAGR"],
                                   t_Sharpe=w["full"]["Sharpe"] - pm["Sharpe"],
                                   t_MaxDD=w["full"]["MaxDD"] - pm["MaxDD"],
                                   t_oos_Sharpe=w["oos"]["Sharpe"] - pm_oos,
                                   keep4a=all(a4.values()), keep4b=all(b4.values()),
                                   fail4a=failed(a4), fail4b=failed(b4))
                        rows.append(rec)
                        cells[(br, look, sl)] = rec
                        say(f"   {br:5s} {look:4d} {sl:5.2f} | {w['full']['CAGR']:7.2%} "
                            f"{w['full']['Sharpe']:8.4f} {w['full']['MaxDD']:8.2%} "
                            f"{w['full']['Vol']:6.2%} | {w['h1']['Sharpe']:.4f}/"
                            f"{w['h2']['Sharpe']:.4f} | {w['oos']['Sharpe']:7.4f} | {turn:5.2f} "
                            f"{diag['g_mean']:5.3f} {diag['g_min']:4.2f} "
                            f"{diag['brake_share']*100:4.1f} {diag['episodes']:3d} | "
                            f"{'Y' if all(a4.values()) else 'n'}  "
                            f"{'Y' if all(b4.values()) else 'n'} | {failed(b4):12s} | "
                            f"FLAT dCAGR {rec['d_CAGR']*100:+5.2f}pp dSh {rec['d_Sharpe']:+.4f} "
                            f"dDD {rec['d_MaxDD']*100:+5.2f}pp | PLAC dCAGR "
                            f"{rec['t_CAGR']*100:+5.2f}pp dSh {rec['t_Sharpe']:+.4f} dDD "
                            f"{rec['t_MaxDD']*100:+5.2f}pp")

            # ---- gates
            if pname == "U56":
                q = p_px.loc[:VINTAGE]
                vpan = Panel("U56v", q, [c for c in q.columns if c != "SPY"])
                rv, _, _ = run(vpan, build(vpan, sig), A_G)
                tv = stats(rv[WARMUP:])
                tgt = COMMITTED_U56 if sig == "COMPOSITE3" else COMMITTED_M12
                err = max(abs(tv["CAGR"] - tgt[0]), abs(tv["Sharpe"] - tgt[1]),
                          abs(tv["MaxDD"] - tgt[2]))
                gate(f"{'G1' if sig == 'COMPOSITE3' else 'G2'} vintage-pinned replay (U56 {sig} "
                     f"SLOPE 0 @ {VINTAGE.date()})",
                     f"{tv['CAGR']:.4%}/{tv['Sharpe']:.4f}/{tv['MaxDD']:.4%} err {err:.2e}",
                     f"committed {tgt[0]:.4%}/{tgt[1]:.4f}/{tgt[2]:.4%}, err < 1e-4", err < 1e-4)
                a = cells[("CORR", LOOKS[0], 0.0)]
                gate(f"G10 one-extra-day cache drift ({sig})",
                     f"CAGR {a['full_CAGR']-tv['CAGR']:+.4%}  Sharpe {a['full_Sharpe']-tv['Sharpe']:+.4f}",
                     "published, not toleranced", True)
            if pname == "U56" and sig == "COMPOSITE3":
                base = cells[("CORR", LOOKS[0], 0.0)]["full_Sharpe"]
                d = max(abs(cells[(br, lk, 0.0)]["full_Sharpe"] - base)
                        for br in BRAKES for lk in LOOKS)
                gate("G3 SLOPE 0 is LOOK- and BRAKE-invariant (it IS the committed anchor)",
                     f"{d:.3e}", "== 0.0", d == 0.0)
                gm = max(c["g_max"] for c in cells.values())
                gn = min(c["g_min"] for c in cells.values())
                gate("G4 realised gross inside [0, 0.75] — NO LEVERAGE, never above the anchor",
                     f"[{gn:.4f}, {gm:.4f}]", f"[0, {A_G}]", gn >= -1e-15 and gm <= A_G + 1e-12)
                worst, nonzero = 0.0, 0
                for br in BRAKES:
                    s = S[(br, LOOKS[2])]
                    uf, _ = intensity(s)
                    nonzero += int((uf > 0).sum())
                    for i in range(0, len(s), 7):
                        ut, _ = intensity(s[:i + 1])
                        worst = max(worst, abs(ut[i] - uf[i]))
                gate("G5 CAUSALITY (intensity at i recomputed from the statistic TRUNCATED at i)",
                     f"max |du| {worst:.3e} over every 7th decision date of both brakes; "
                     f"{nonzero} armed rows", "== 0.0 and not inert",
                     worst == 0.0 and nonzero > 0)
                bad6 = 0
                mono6 = True
                for br in BRAKES:
                    for lk in LOOKS:
                        u, p = U[(br, lk)], P[(br, lk)]
                        f = np.isfinite(p)
                        bad6 += int(((p[f] <= 0.5) & (u[f] > 0)).sum())
                        o = np.argsort(p[f], kind="stable")
                        uu = u[f][o]
                        mono6 &= bool(np.all(np.diff(uu) >= -1e-15))
                gate("G6 u == 0 wherever p <= 0.5, and u monotone non-decreasing in p",
                     f"{bad6} violations, monotone={mono6}", "0 violations and monotone",
                     bad6 == 0 and mono6)
                z = min(cells[(br, lk, 1.00)]["g_min"] for br in BRAKES for lk in LOOKS)
                gate("G7 SLOPE 1.00 reaches exactly zero gross at a new historical high",
                     f"{z:.3e}", "== 0.0", z == 0.0)
                o = cells[("CORR", LOOKS[0], 0.0)]
                er = max(abs(o["d_CAGR"]), abs(o["d_Sharpe"]), abs(o["d_MaxDD"]))
                gate("G8 the SLOPE 0 cell's gross-matched control IS the SLOPE 0 cell",
                     f"{er:.3e}", "== 0.0", er == 0.0)
                sr = pd.DataFrame(sigrows)
                sr = sr[(sr.panel == pname) & (sr.signal == sig) & (sr.brake == "CORR")]
                gate("G11 correlation statistic inside [-1, 1]; undefined windows and gap-dropped "
                     "columns published",
                     f"S in [{sr.S_min.min():.4f}, {sr.S_max.max():.4f}]; undefined "
                     f"{sr.undefined.tolist()}; gap-dropped {sr.gap_dropped.tolist()}",
                     "inside [-1, 1]",
                     sr.S_min.min() >= -1.0 - 1e-12 and sr.S_max.max() <= 1.0 + 1e-12)
                gmax = 0.0
                for br in BRAKES:
                    for lk in LOOKS:
                        for sl in SLOPES[1:]:
                            u = U[(br, lk)]
                            w0 = int(np.searchsorted(pan.reb, WARMUP))
                            for sd in SEEDS:
                                rng = np.random.default_rng(sd)
                                up = u.copy()
                                rng.shuffle(up)
                                gmax = max(gmax, abs(schedule(up, sl)[w0:].mean()
                                                     - schedule(u, sl)[w0:].mean()))
                gate("G12 the PLACEBO is an EXACT gross match (a permutation of the same "
                     "intensity series)", f"max |d mean gross| {gmax:.3e}", "== 0.0 (to fp)",
                     gmax < 1e-15)

            # ---- rule 8, per brake
            for br in BRAKES:
                ks = [(br, lk, sl) for lk in LOOKS for sl in SLOPES]
                is_s = np.array([cells[k]["is__Sharpe"] for k in ks])
                oos_s = np.array([cells[k]["oos_Sharpe"] for k in ks])
                pick = ks[int(np.nanargmax(is_s))]
                nothing = cells[(br, LOOKS[0], 0.0)]
                r8 = dict(panel=pname, signal=sig, brake=br, pick_look=pick[1], pick_slope=pick[2],
                          pick_IS=cells[pick]["is__Sharpe"], pick_OOS=cells[pick]["oos_Sharpe"],
                          donothing_OOS=nothing["oos_Sharpe"],
                          delta=cells[pick]["oos_Sharpe"] - nothing["oos_Sharpe"],
                          pick_OOS_CAGR=cells[pick]["oos_CAGR"],
                          pick_OOS_MaxDD=cells[pick]["oos_MaxDD"],
                          nothing_OOS_CAGR=nothing["oos_CAGR"],
                          nothing_OOS_MaxDD=nothing["oos_MaxDD"],
                          cellmean_OOS=float(np.nanmean(oos_s)), worst_OOS=float(np.nanmin(oos_s)),
                          best_OOS=float(np.nanmax(oos_s)), rank_IS_OOS=rankcorr(is_s, oos_s),
                          spy_OOS=spy["oos"]["Sharpe"], live_OOS=live["oos"]["Sharpe"],
                          pick_keep4a=cells[pick]["keep4a"], pick_keep4b=cells[pick]["keep4b"],
                          nothing_keep4b=nothing["keep4b"])
                r8rows.append(r8)
                say(f"   RULE 8 [{br}] IS-argmax = LOOK {pick[1]} / SLOPE {pick[2]:.2f} "
                    f"(IS Sh {r8['pick_IS']:.4f}) -> OOS {r8['pick_OOS']:.4f}  vs do-nothing "
                    f"{r8['donothing_OOS']:.4f}  delta {r8['delta']:+.4f}   cellmean "
                    f"{r8['cellmean_OOS']:.4f}  worst {r8['worst_OOS']:.4f}  rank corr IS/OOS "
                    f"{r8['rank_IS_OOS']:+.2f}")

    grid = pd.DataFrame(rows)
    wf = pd.DataFrame(r8rows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)
    pd.DataFrame(sigrows).to_csv(f"{STEM}.statistic.csv", index=False)
    pd.DataFrame(eprows).to_csv(f"{STEM}.episode.csv", index=False)

    # ---- G9 determinism
    pan = Panel("U56", panels[0][1], panels[0][2])
    Wt = build(pan, "COMPOSITE3")
    ar, _, _ = run(pan, Wt, A_G)
    chk = []
    for look in LOOKS:
        s, _, _ = corr_series(pan, Wt, look)
        u, _ = intensity(s)
        for sl in SLOPES:
            r, _, _ = run(pan, Wt, schedule(u, sl))
            chk.append(sharpe(r[WARMUP:]))
    ref = grid[(grid.panel == "U56") & (grid.signal == "COMPOSITE3")
               & (grid.brake == "CORR")].full_Sharpe.values
    dmax = float(np.max(np.abs(np.array(chk) - ref)))
    gate("G9 determinism (U56 COMPOSITE3 CORR grid re-run)", f"{dmax:.3e}", "== 0.0", dmax == 0.0)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    # ------------------------------------------------------------------ summary
    say("\n## SUMMARY")
    say(f"   cells {len(grid)}   4a passes {int(grid.keep4a.sum())}   4b passes {int(grid.keep4b.sum())}")
    for pname in grid.panel.unique():
        for sig in SIGNALS:
            for br in BRAKES:
                g = grid[(grid.panel == pname) & (grid.signal == sig) & (grid.brake == br)]
                off = g[g.slope == 0.0].iloc[0]
                say(f"   {pname:9s} {sig:11s} {br:5s} 4b {int(g.keep4b.sum()):2d}/{len(g)}   "
                    f"SLOPE0 {off.full_CAGR:6.2%}/{off.full_Sharpe:.4f}/{off.full_MaxDD:7.2%}   "
                    f"MaxDD {g.full_MaxDD.min():7.2%}..{g.full_MaxDD.max():7.2%}   "
                    f"CAGR {g.full_CAGR.min():6.2%}..{g.full_CAGR.max():6.2%}   "
                    f"Sharpe {g.full_Sharpe.min():.4f}..{g.full_Sharpe.max():.4f}   "
                    f"turn {g.turnover.min():.2f}..{g.turnover.max():.2f}")

    on = grid[grid.slope > 0.0]
    say("\n   (1) THE MECHANISM AGAINST A FLAT SCHEDULE AT THE SAME MEAN EXPOSURE:")
    for br in BRAKES:
        g = on[on.brake == br]
        say(f"      {br:5s} n={len(g)}  d_CAGR {g.d_CAGR.mean()*100:+5.2f}pp  d_Sharpe "
            f"{g.d_Sharpe.mean():+.4f} (>0 at {int((g.d_Sharpe>0).sum())}/{len(g)})  d_MaxDD "
            f"{g.d_MaxDD.mean()*100:+5.2f}pp (>0 at {int((g.d_MaxDD>0).sum())}/{len(g)})  "
            f"d_OOS {g.d_oos_Sharpe.mean():+.4f} (>0 at {int((g.d_oos_Sharpe>0).sum())}/{len(g)})")
    say("   (2) THE MECHANISM AGAINST ITS OWN TIMING PLACEBO (exact gross match, timing destroyed):")
    for br in BRAKES:
        g = on[on.brake == br]
        say(f"      {br:5s} n={len(g)}  t_CAGR {g.t_CAGR.mean()*100:+5.2f}pp  t_Sharpe "
            f"{g.t_Sharpe.mean():+.4f} (>0 at {int((g.t_Sharpe>0).sum())}/{len(g)})  t_MaxDD "
            f"{g.t_MaxDD.mean()*100:+5.2f}pp (>0 at {int((g.t_MaxDD>0).sum())}/{len(g)})  "
            f"t_OOS {g.t_oos_Sharpe.mean():+.4f} (>0 at {int((g.t_oos_Sharpe>0).sum())}/{len(g)})")
    say("   (3) THE LITERAL QUESTION — CORR MINUS VOL AT MATCHED (panel, signal, LOOK, SLOPE):")
    piv = on.pivot_table(index=["panel", "signal", "look", "slope"], columns="brake",
                         values=["full_CAGR", "full_Sharpe", "full_MaxDD", "oos_Sharpe"])
    dd = piv["full_MaxDD"]["CORR"] - piv["full_MaxDD"]["VOL"]
    dc = piv["full_CAGR"]["CORR"] - piv["full_CAGR"]["VOL"]
    ds = piv["full_Sharpe"]["CORR"] - piv["full_Sharpe"]["VOL"]
    do = piv["oos_Sharpe"]["CORR"] - piv["oos_Sharpe"]["VOL"]
    say(f"      pooled over {len(dd)} matched pairs: d_MaxDD {dd.mean()*100:+5.2f}pp (CORR better "
        f"at {int((dd>0).sum())}/{len(dd)})  d_CAGR {dc.mean()*100:+5.2f}pp  d_Sharpe "
        f"{ds.mean():+.4f} (CORR better at {int((ds>0).sum())}/{len(ds)})  d_OOS {do.mean():+.4f} "
        f"(CORR better at {int((do>0).sum())}/{len(do)})")
    for pn in grid.panel.unique():
        for sig in SIGNALS:
            m = [k for k in dd.index if k[0] == pn and k[1] == sig]
            if not m:
                continue
            say(f"      {pn:9s} {sig:11s} d_MaxDD {dd.loc[m].mean()*100:+5.2f}pp (CORR better at "
                f"{int((dd.loc[m]>0).sum())}/{len(m)})  d_Sharpe {ds.loc[m].mean():+.4f}  d_OOS "
                f"{do.loc[m].mean():+.4f}")
    ep = pd.DataFrame(eprows)
    say(f"      rank corr of the two intensity series: mean {ep.rank_corr_u.mean():+.3f}, range "
        f"{ep.rank_corr_u.min():+.3f}..{ep.rank_corr_u.max():+.3f} over {len(ep)} "
        f"(panel, signal, LOOK) cells")
    say(f"      INSIDE the worst drawdown episode mean intensity: CORR "
        f"{ep.corr_u_mean.mean():.3f} vs VOL {ep.vol_u_mean.mean():.3f}; in the 42 rows BEFORE "
        f"the peak CORR {ep.corr_u_pre.mean():.3f} vs VOL {ep.vol_u_pre.mean():.3f}  "
        f"(CORR higher pre-peak at {int((ep.corr_u_pre>ep.vol_u_pre).sum())}/{len(ep)})")

    say("\n   (4) STRUCTURE IN THE DIALS (pooled over panels and signals, braked cells only):")
    for br in BRAKES:
        for lk in LOOKS:
            g = on[(on.brake == br) & (on.look == lk)]
            say(f"      {br:5s} LOOK {lk:4d}: d_CAGR {g.d_CAGR.mean()*100:+5.2f}pp  d_Sharpe "
                f"{g.d_Sharpe.mean():+.4f}  d_MaxDD {g.d_MaxDD.mean()*100:+5.2f}pp  d_OOS "
                f"{g.d_oos_Sharpe.mean():+.4f}  t_Sharpe {g.t_Sharpe.mean():+.4f}  "
                f"on% {g.brake_share.mean()*100:4.1f}")
    for br in BRAKES:
        for sl in SLOPES[1:]:
            g = on[(on.brake == br) & (on.slope == sl)]
            say(f"      {br:5s} SLOPE {sl:.2f}: d_CAGR {g.d_CAGR.mean()*100:+5.2f}pp  d_Sharpe "
                f"{g.d_Sharpe.mean():+.4f}  d_MaxDD {g.d_MaxDD.mean()*100:+5.2f}pp  d_OOS "
                f"{g.d_oos_Sharpe.mean():+.4f}  t_Sharpe {g.t_Sharpe.mean():+.4f}")

    say("\n   (5) COST OF THE DD LEG, PER PANEL/SIGNAL/BRAKE (best MaxDD cell and its price):")
    for pn in grid.panel.unique():
        for sig in SIGNALS:
            for br in BRAKES:
                g = grid[(grid.panel == pn) & (grid.signal == sig) & (grid.brake == br)]
                off = g[g.slope == 0.0].iloc[0]
                b = g.loc[g[g.slope > 0].full_MaxDD.idxmax()]
                say(f"      {pn:9s} {sig:11s} {br:5s} best DD cell LOOK {b.look}/SLOPE "
                    f"{b.slope:.2f}: MaxDD {off.full_MaxDD:7.2%} -> {b.full_MaxDD:7.2%} "
                    f"({(b.full_MaxDD-off.full_MaxDD)*100:+.2f}pp) costs CAGR "
                    f"{(b.full_CAGR-off.full_CAGR)*100:+.2f}pp, Sharpe "
                    f"{b.full_Sharpe-off.full_Sharpe:+.4f}, turnover {b.turnover-off.turnover:+.2f}"
                    f"/yr; 4b {'PASS' if b.keep4b else 'FAIL(' + b.fail4b + ')'} vs SLOPE0 "
                    f"{'PASS' if off.keep4b else 'FAIL(' + off.fail4b + ')'}")

    off_fail = {(r.panel, r.signal, r.brake): (not r.keep4b)
                for _, r in grid[grid.slope == 0.0].iterrows()}
    conv = grid[[off_fail[(r.panel, r.signal, r.brake)] and r.keep4b for _, r in grid.iterrows()]]
    say(f"\n   (6) 4b CONVERSIONS (the cell's own SLOPE 0 fails 4b, the cell passes): {len(conv)} "
        f"of {len(grid)} cells")
    for _, r in conv.iterrows():
        say(f"      {r.panel:9s} {r.signal:11s} {r.brake:5s} LOOK {r.look}/SLOPE {r.slope:.2f}: "
            f"{r.full_CAGR:6.2%} / {r.full_Sharpe:.4f} / {r.full_MaxDD:7.2%}  OOS "
            f"{r.oos_Sharpe:.4f}  turn {r.turnover:.2f} | flat gross-matched control "
            f"{'ALSO PASSES (not the timing)' if r.ctrl_keep4b else 'FAILS (genuinely the timing)'}"
            f" | vs placebo dSh {r.t_Sharpe:+.4f} dDD {r.t_MaxDD*100:+.2f}pp")
    both = on[(on.d_MaxDD > 0) & (on.d_Sharpe > 0) & (on.t_MaxDD > 0) & (on.t_Sharpe > 0)]
    say(f"   cells beating BOTH the flat control AND the placebo on BOTH DD and Sharpe: "
        f"{len(both)} of {len(on)}"
        + ("" if not len(both) else "  -> " + ", ".join(
            f"{r.panel}/{r.signal}/{r.brake}/{r.look}/{r.slope:.2f}" for _, r in both.iterrows())))

    say(f"\n   (7) RULE 8 chooser-minus-do-nothing: mean {wf.delta.mean():+.4f}, beats do-nothing "
        f"at {int((wf.delta > 0).sum())} of {len(wf)}")
    for br in BRAKES:
        g = wf[wf.brake == br]
        say(f"      {br:5s} mean {g.delta.mean():+.4f}  positive at {int((g.delta>0).sum())}/"
            f"{len(g)}  mean rank corr IS/OOS {g.rank_IS_OOS.mean():+.3f}")
    for _, r in wf.iterrows():
        say(f"      {r.panel:9s} {r.signal:11s} {r.brake:5s} pick LOOK {r.pick_look}/SLOPE "
            f"{r.pick_slope:.2f}  OOS {r.pick_OOS:.4f} vs do-nothing {r.donothing_OOS:.4f} "
            f"({r.delta:+.4f})  SPY OOS {r.spy_OOS:.4f}  live v2 OOS {r.live_OOS:.4f}  4b pick "
            f"{'PASS' if r.pick_keep4b else 'FAIL'} / SLOPE0 "
            f"{'PASS' if r.nothing_keep4b else 'FAIL'}")

    fails = grid[~grid.keep4b]
    if len(fails):
        legs = {k: int(sum(k in f.split(",") for f in fails.fail4b)) for k in
                ("DD", "CAGR", "H1", "H2", "OOS")}
        say(f"\n   (8) WHICH 4b LEG FAILS, over the {len(fails)} failures: " +
            "  ".join(f"{k} {v}" for k, v in legs.items()))
    say(f"   GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass   {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
