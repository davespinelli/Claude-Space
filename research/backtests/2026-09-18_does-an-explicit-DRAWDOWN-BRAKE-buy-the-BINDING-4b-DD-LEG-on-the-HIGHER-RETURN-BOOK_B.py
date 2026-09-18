#!/usr/bin/env python3
"""Idea 1262 (lane B, 2026-09-18): does an explicit DRAWDOWN BRAKE buy the BINDING 4b DD LEG
on the HIGHER-RETURN BOOK?

THE PREMISE.  Six dials on the standing 2026-09-04 KEEP 4b book — rebalance phase (1253),
calendar years (1254), ex-post winner names (1255), the signal (1257), sector caps (1258),
slot sizing (1264) — all land on one sentence: every other 4b leg passes at essentially every
grid point and the DRAWDOWN CAP is the only leg that ever fails.  1257 priced what that costs:
the M12_1-ALONE book earns +1.00pp of CAGR and +0.0413 of full Sharpe at LESS turnover and is
disqualified by 1.45pp of MaxDD and nothing else.  Two purchase mechanisms have now been
priced and both failed: 1264's inverse-vol slot sizing (converts, but full Sharpe falls
monotonically in the exponent and rule 8 picks EQUAL WEIGHT) and 1263's portfolio VOL
TARGETING (converts 14 of 126 cells, but 7 of the 14 conversions are reproduced by a flat
gross cut with no timing at all, the pooled mechanism is a 1.41pp/yr drag for a coin-flip
drawdown, and rule 8's chooser loses to do-nothing at 4 of 6 arms).

THIS RUN PRICES THE THIRD AND LAST OBVIOUS MECHANISM, AND THE ONLY PATH-DEPENDENT ONE: AN
EXPLICIT DRAWDOWN BRAKE.  Vol targeting reacts to the SECOND moment of the book's returns; a
brake reacts to the thing 4b actually measures — the book's own realised equity drawdown:

    dd(t-1) = equity(t-1) / running_max(equity)(t-1) - 1          on the FROZEN book's path
    gross(t) = A_G * (1 - DEGROSS)   if dd(t-1) <= -TRIGGER
             = A_G                   otherwise

read at the DECISION close t-1 and applied at t (rule 2).  This is the cheapest risk clause
anyone would actually write into RULES.md ("if the book is down X from its high, hold Y less
of it"), it needs no extra data, and it aims at the binding leg directly rather than at a
proxy for it.  If the DD leg is buyable at an acceptable price anywhere, it should be buyable
here.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    TRIGGER {OFF, 0.05, 0.10, 0.15, 0.20, 0.25} — depth of the brake's arming drawdown.
            OFF is EXACTLY the committed anchor book (constant gross 0.75) and is in the grid
            so the do-nothing control is measured, not assumed.
    DEGROSS {0.25, 0.50, 0.75, 1.00} — fraction of gross removed while the brake is on.
            1.00 is FULLY FLAT (the whole book to cash).
  6 x 4 = 24 cells per (panel, signal).  EVERY ONE PUBLISHED in the .grid.csv.

NOT DIALS, reported at every value (1263/1264's convention, so the three mechanisms are read
on the same objects): PANEL {U56, B135, SMALL} (rule 9); SIGNAL {COMPOSITE3 = the committed
three-leg average of percentile ranks, M12_1 = 1257's single 21/252 leg — the higher-return
book that failed 4b on drawdown alone}; both KEEP paths leg by leg; full / halves / IS / OOS;
annual turnover; realised vol; mean/min realised gross; the share of rebalances braked and the
number of distinct brake episodes.  144 cells in all.

THE CONTROL ARM THAT MAKES THE HEADLINE READABLE, AND WITHOUT WHICH IT IS NOT.  A brake does
not only re-time exposure — it LOWERS THE AVERAGE EXPOSURE, and this record has established
twice over (the 2026-09-17 gross-dial run, and 1263's finding that 7 of 14 vol-target
conversions survive no gross-matched control) that gross alone is a pure CAGR-for-drawdown
slide.  So every braked cell is also run against a CONSTANT-GROSS control held at that cell's
OWN realised mean gross, and the reported effect of the mechanism is the braked cell MINUS
that control.  The raw comparison against the 0.75 anchor is published too, so both readings
are visible.  The control is not a dial: it is fixed cell by cell by the cell itself.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: eligibility = above own 200d MA
AND vol20 < 0.60; N = 20; H = 126 minimum hold; base GROSS = 0.75 of NAV; WEEKLY decide-Friday
/ trade-Monday; 10 bps per unit turnover; t+1 execution; 260-row warm-up; RAW-composite
ranking; equal 1/len(held) slots.  SELECTION IS IDENTICAL AT EVERY CELL BY CONSTRUCTION — the
dials touch only how much of NAV the same names are held at.

FROZEN CONSTANTS, DECLARED SO THEY ARE NOT MISTAKEN FOR DIALS.  (i) There is NO HYSTERESIS
BAND and no minimum brake duration: the brake is a pure function of dd(t-1), so it releases at
the first rebalance at which the drawdown has recovered through the same trigger.  A release
band would be a THIRD parameter and rule 4 forbids it; the consequence (the brake can chatter,
which shows up as turnover) is measured rather than tuned away.  (ii) The brake never
increases gross above the anchor's 0.75 — there is no leverage anywhere (rule 2).  (iii)
dd is measured on the FROZEN constant-gross book's own equity path, never on the braked book's
— that avoids a fixed point and is exactly what an implementer observes in real time.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) INERT — the brake almost never arms at useful depths, MaxDD moves < 0.20pp.
  (B) THE DD LEG IS BOUGHT AND CHEAPLY — some cell materially improves MaxDD, holds 4b's CAGR
      floor and both half-Sharpe legs, converts a committed 4b FAIL to a PASS, SURVIVES its
      gross-matched control, is cheaper than 1263's and 1264's conversions, AND rule 8 reaches
      it.  That is a KEEP-candidate memo with exact RULES wording.
  (C) BOUGHT AND OVERPAID FOR — MaxDD improves but CAGR falls through 4b's floor, or a half
      Sharpe falls below SPY, or the extra brake turnover eats it at 10 bps, or the whole gain
      is reproduced by the flat gross-matched control.
  (D) WORSE — the brake sells the bottom and buys the recovery back higher, so drawdown or
      Sharpe DEGRADES relative to flat gross at the same mean exposure.
  (A)-(D) are not mutually exclusive across panels; whichever fire are reported as they fall,
  and the capital verdict follows rule 8, not the best cell.

RULE 8 (walk-forward, required).  (TRIGGER, DEGROSS) is CHOSEN on warm-up..2016-12-31 by IS
Sharpe ALONE and 2017-2026 is read ONCE, per (panel, signal).  Reported against (i) the
DO-NOTHING control = TRIGGER OFF (the committed constant-gross book), (ii) the mean over all
24 cells, (iii) the WORST cell, with the IS/OOS rank correlation over the 24.  The capital
verdict is the sign of chooser-minus-do-nothing, never the best cell's number.

GATES.  G1 vintage-pinned replay truncated at 2026-09-16 (the cache vintage the committed
numbers were produced on): U56 COMPOSITE3 OFF must replay the committed 15.71% / 1.1480 /
-19.13% to 1e-4.  G2 the same for M12_1 against 1257's 16.71% / 1.1893 / -20.58%.  G3 OFF is
bit-identical at all four DEGROSS values.  G4 realised gross inside [0, 0.75] at every
rebalance of every cell — no leverage, never above the anchor.  G5 NO LOOK-AHEAD: perturbing
the anchor's return ON a rebalance row cannot change that row's own brake state.  G6 the brake
share is monotone non-increasing in TRIGGER depth.  G7 the DEGROSS 1.00 cells reach exactly
zero gross while braked.  G8 the OFF cell's gross-matched control IS the OFF cell.  G9
determinism: the whole U56 COMPOSITE3 grid recomputed bit for bit.  G10 the one-day cache
drift is published, not toleranced.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B135 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is
an UPPER bound.  The headline is a DIFFERENCE between gross schedules applied to the SAME
holdings on the SAME panel — the selected names are identical at every cell by construction —
which is first-order immune to a level bias that moves all cells together.  One direction is
NOT neutral and is stated: a current-constituent panel UNDERSTATES the deep drawdowns a real
momentum book took in names later delisted, so the anchor's drawdown is FLATTERED and any DD
improvement a brake posts here is a LOWER bound on a live panel — while the CAGR it gives up
is measured against a flattered comparand.

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
SLUG = "does-an-explicit-DRAWDOWN-BRAKE-buy-the-BINDING-4b-DD-LEG-on-the-HIGHER-RETURN-BOOK"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_B"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                       # the frozen 2026-09-04 book
SIGNALS = {"COMPOSITE3": [(21, 252), (0, 126), (0, 63)], "M12_1": [(21, 252)]}
TRIGGERS = ["OFF", 0.05, 0.10, 0.15, 0.20, 0.25]    # DIAL 1 (OFF == committed anchor)
DEGROSS = [0.25, 0.50, 0.75, 1.00]                  # DIAL 2
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


# ------------------------------------------------------------------ panel (1263/1264's, unchanged)
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
    """The frozen selection frame at GROSS = 1.0.  Identical to 1263/1264's build."""
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
    """gross: scalar or one value per rebalance date.  Hold gross*Wt from each rebalance,
    drift between, 10 bps on traded notional (1263/1264's run, unchanged)."""
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


def dd_path(anchor_r):
    """Realised equity drawdown of the FROZEN book, daily, from its own running high."""
    e = np.cumprod(1.0 + np.asarray(anchor_r, float))
    return e / np.maximum.accumulate(e) - 1.0


def brake_schedule(pan, dd, trigger, degross, lag=1):
    """gross(t) = A_G*(1-degross) if dd(t-lag) <= -trigger else A_G.  No look-ahead: the value
    used at rebalance row t is read from the equity path at row t-lag.  No hysteresis band and
    no minimum duration (a third parameter rule 4 forbids) — release is the same threshold."""
    out = np.full(len(pan.reb), A_G)
    on = np.zeros(len(pan.reb), dtype=bool)
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        if dd[ts] <= -trigger:
            out[i] = A_G * (1.0 - degross)
            on[i] = True
    w0 = int(np.searchsorted(pan.reb, WARMUP))
    ep = int(np.sum(on[w0:] & ~np.concatenate([[False], on[w0:-1]]))) if len(on) > w0 else 0
    diag = dict(g_mean=float(out[w0:].mean()), g_min=float(out[w0:].min()),
                g_max=float(out[w0:].max()),
                brake_share=float(on[w0:].mean()), episodes=ep)
    return out, diag


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
    say(f"# {DATE} idea 1262 lane B — {SLUG}")
    say(f"# frozen book: RAW composite, gate = above 200d MA AND vol20 < {MAXVOL}, N={A_N}, H={A_H}, "
        f"base GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}, equal 1/len(held) slots")
    say(f"# DIAL 1 TRIGGER = {TRIGGERS}   (OFF = COMMITTED CONSTANT-GROSS ANCHOR)")
    say(f"# DIAL 2 DEGROSS = {DEGROSS}   (1.00 = fully flat while braked)")
    say(f"# reported-not-dials: panel {{U56,B135,SMALL}} x signal {list(SIGNALS)}")
    say("# frozen constants (NOT dials): no hysteresis band, no minimum brake duration; gross "
        "never exceeds the anchor's 0.75; dd read on the FROZEN book's own equity path at t-1")
    say("# SELECTION IS IDENTICAL AT EVERY CELL BY CONSTRUCTION — only the gross schedule moves")

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
        live_r = backtest(p_px, rules_v2_weights(p_px), cost_bps=COST, freq="W")["returns"].fillna(0.0).values[WARMUP:]
        live = windows(idx, live_r)

        say(f"\n## {pname}  n_days={len(pan.idx)}  n_names={len(inv)}  {idx[0].date()}..{idx[-1].date()}")
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
            dd = dd_path(anchor_r)
            aw = windows(idx, anchor_r[WARMUP:])
            say(f"\n   --- signal {sig} ---   anchor {aw['full']['CAGR']:.2%} / "
                f"{aw['full']['Sharpe']:.4f} / {aw['full']['MaxDD']:.2%}, turnover {anchor_turn:.2f}/yr")
            # WHY THE DEEP TRIGGERS CANNOT SEE THE DISQUALIFYING DRAWDOWN: 4b's DD leg reads a
            # POINT on the equity path, a brake can only act on a STATE the book OCCUPIES on a
            # DECISION DATE.  Both counts are published so the gap is visible, not asserted.
            reb_post = pan.reb[pan.reb > WARMUP]
            dec = dd[np.maximum(reb_post - 1, 0)]
            say(f"   anchor dd path: worst {dd[WARMUP:].min():.2%} on "
                f"{pan.idx[WARMUP + int(np.argmin(dd[WARMUP:]))].date()}")
            for t in [x for x in TRIGGERS if x != "OFF"]:
                nd = int((dd[WARMUP:] <= -t).sum())
                nr = int((dec <= -t).sum())
                say(f"      at or below -{t:.0%}: {nd:5d} of {len(dd)-WARMUP} DAYS "
                    f"({nd/(len(dd)-WARMUP):5.1%})   {nr:4d} of {len(reb_post)} REBALANCE "
                    f"DECISION DATES ({nr/len(reb_post):5.1%})")
            say("   TRIG   degr |    CAGR   Sharpe    MaxDD    vol |  H1/H2 Sharpe |  OOS Sh | "
                "turn  gmean gmin  on% ep | 4a 4b | fail4b")
            cells = {}
            for trig in TRIGGERS:
                for f in DEGROSS:
                    if trig == "OFF":
                        g = A_G
                        diag = dict(g_mean=A_G, g_min=A_G, g_max=A_G, brake_share=0.0, episodes=0)
                    else:
                        g, diag = brake_schedule(pan, dd, float(trig), f)
                    r, turn, expo = run(pan, Wt, g)
                    r = r[WARMUP:]
                    w = windows(idx, r)
                    # GROSS-MATCHED CONTROL: constant gross at this cell's own mean gross
                    cr, cturn, _ = run(pan, Wt, diag["g_mean"])
                    cw = windows(idx, cr[WARMUP:])
                    cb4 = legs_4b(cw, spy)
                    a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                    rec = dict(panel=pname, signal=sig, trigger=str(trig), degross=f,
                               **flat(w), turnover=turn, exposure=expo, **diag,
                               ctrl_CAGR=cw["full"]["CAGR"], ctrl_Sharpe=cw["full"]["Sharpe"],
                               ctrl_MaxDD=cw["full"]["MaxDD"], ctrl_oos_Sharpe=cw["oos"]["Sharpe"],
                               ctrl_turnover=cturn, ctrl_keep4b=all(cb4.values()),
                               ctrl_fail4b=failed(cb4),
                               d_CAGR=w["full"]["CAGR"] - cw["full"]["CAGR"],
                               d_Sharpe=w["full"]["Sharpe"] - cw["full"]["Sharpe"],
                               d_MaxDD=w["full"]["MaxDD"] - cw["full"]["MaxDD"],
                               d_oos_Sharpe=w["oos"]["Sharpe"] - cw["oos"]["Sharpe"],
                               keep4a=all(a4.values()), keep4b=all(b4.values()),
                               fail4a=failed(a4), fail4b=failed(b4))
                    rows.append(rec)
                    cells[(str(trig), f)] = rec
                    say(f"   {str(trig):6s} {f:4.2f} | {w['full']['CAGR']:7.2%} "
                        f"{w['full']['Sharpe']:8.4f} {w['full']['MaxDD']:8.2%} {w['full']['Vol']:6.2%} | "
                        f"{w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f} | {w['oos']['Sharpe']:7.4f} | "
                        f"{turn:5.2f} {diag['g_mean']:5.3f} {diag['g_min']:4.2f} "
                        f"{diag['brake_share']*100:4.1f} {diag['episodes']:3d} | "
                        f"{'Y' if all(a4.values()) else 'n'}  {'Y' if all(b4.values()) else 'n'} | "
                        f"{failed(b4):12s} | vs GROSS-MATCHED CAGR {rec['d_CAGR']*100:+5.2f}pp "
                        f"Sh {rec['d_Sharpe']:+.4f} DD {rec['d_MaxDD']*100:+5.2f}pp "
                        f"OOS {rec['d_oos_Sharpe']:+.4f}")

            # ---- gates
            if pname == "U56":
                q = p_px.loc[:VINTAGE]
                vpan = Panel("U56v", q, [c for c in q.columns if c != "SPY"])
                rv, _, _ = run(vpan, build(vpan, sig), A_G)
                tv = stats(rv[WARMUP:])
                tgt = COMMITTED_U56 if sig == "COMPOSITE3" else COMMITTED_M12
                err = max(abs(tv["CAGR"] - tgt[0]), abs(tv["Sharpe"] - tgt[1]), abs(tv["MaxDD"] - tgt[2]))
                gate(f"{'G1' if sig == 'COMPOSITE3' else 'G2'} vintage-pinned replay (U56 {sig} OFF "
                     f"@ {VINTAGE.date()})",
                     f"{tv['CAGR']:.4%}/{tv['Sharpe']:.4f}/{tv['MaxDD']:.4%} err {err:.2e}",
                     f"committed {tgt[0]:.4%}/{tgt[1]:.4f}/{tgt[2]:.4%}, err < 1e-4", err < 1e-4)
                a = cells[("OFF", DEGROSS[0])]
                gate(f"G10 one-extra-day cache drift ({sig})",
                     f"CAGR {a['full_CAGR']-tv['CAGR']:+.4%}  Sharpe {a['full_Sharpe']-tv['Sharpe']:+.4f}",
                     "published, not toleranced", True)
            if pname == "U56" and sig == "COMPOSITE3":
                d = max(abs(cells[("OFF", f)]["full_Sharpe"] - cells[("OFF", DEGROSS[0])]["full_Sharpe"])
                        for f in DEGROSS)
                gate("G3 OFF is DEGROSS-invariant", f"{d:.3e}", "== 0.0", d == 0.0)
                gm = max(cells[(str(t), f)]["g_max"] for t in TRIGGERS for f in DEGROSS)
                gn = min(cells[(str(t), f)]["g_min"] for t in TRIGGERS for f in DEGROSS)
                gate("G4 realised gross inside [0, 0.75] — NO LEVERAGE, never above the anchor",
                     f"[{gn:.4f}, {gm:.4f}]", f"[0, {A_G}]", gn >= 0.0 and gm <= A_G + 1e-12)
                # G5 no look-ahead: a return shock ON a rebalance row cannot move that row's own
                # brake state.  ONE row is shocked at a time — shocking many at once would let an
                # earlier shock contaminate a later row's legitimate t-1 decision date, which is
                # a defect of the test and not of the mechanism.  The gate also checks the shock
                # is NOT INERT (it must move gross at some LATER rebalance) so it cannot pass
                # vacuously.
                g_ref, _ = brake_schedule(pan, dd, 0.10, 0.50)
                worst, moved_later = 0.0, 0
                for i, t in enumerate(pan.reb):
                    if t <= WARMUP or i % 5:
                        continue
                    pert = anchor_r.copy()
                    pert[t] = -0.50
                    g_per, _ = brake_schedule(pan, dd_path(pert), 0.10, 0.50)
                    worst = max(worst, abs(g_ref[i] - g_per[i]))
                    if np.abs(g_ref[i + 1:] - g_per[i + 1:]).max(initial=0.0) > 0:
                        moved_later += 1
                gate("G5 NO LOOK-AHEAD (a -50% shock ON a rebalance row, one row at a time)",
                     f"max |dgross| on the shocked row itself {worst:.3e}; the same shock moves a "
                     f"LATER rebalance's gross in {moved_later} of the shocked rows",
                     "== 0.0 on the row itself, and not inert", worst == 0.0 and moved_later > 0)
                shares = [cells[(str(t), DEGROSS[0])]["brake_share"] for t in TRIGGERS if t != "OFF"]
                mono = all(shares[i] >= shares[i + 1] for i in range(len(shares) - 1))
                gate("G6 brake share monotone non-increasing in TRIGGER depth",
                     " >= ".join(f"{v:.3f}" for v in shares), "non-increasing", mono)
                zero = min(cells[(str(t), 1.00)]["g_min"] for t in TRIGGERS if t != "OFF")
                gate("G7 DEGROSS 1.00 reaches exactly flat while braked", f"{zero:.3e}", "== 0.0",
                     zero == 0.0)
                o = cells[("OFF", DEGROSS[0])]
                e = max(abs(o["d_CAGR"]), abs(o["d_Sharpe"]), abs(o["d_MaxDD"]))
                gate("G8 the OFF cell's gross-matched control IS the OFF cell", f"{e:.3e}",
                     "== 0.0", e == 0.0)

            # ---- rule 8
            ks = list(cells)
            is_s = np.array([cells[k]["is__Sharpe"] for k in ks])
            oos_s = np.array([cells[k]["oos_Sharpe"] for k in ks])
            pick = ks[int(np.nanargmax(is_s))]
            nothing = cells[("OFF", DEGROSS[0])]
            r8 = dict(panel=pname, signal=sig, pick_trigger=pick[0], pick_degross=pick[1],
                      pick_IS=cells[pick]["is__Sharpe"], pick_OOS=cells[pick]["oos_Sharpe"],
                      donothing_OOS=nothing["oos_Sharpe"],
                      delta=cells[pick]["oos_Sharpe"] - nothing["oos_Sharpe"],
                      pick_OOS_CAGR=cells[pick]["oos_CAGR"], pick_OOS_MaxDD=cells[pick]["oos_MaxDD"],
                      nothing_OOS_CAGR=nothing["oos_CAGR"], nothing_OOS_MaxDD=nothing["oos_MaxDD"],
                      cellmean_OOS=float(np.nanmean(oos_s)), worst_OOS=float(np.nanmin(oos_s)),
                      best_OOS=float(np.nanmax(oos_s)), rank_IS_OOS=rankcorr(is_s, oos_s),
                      spy_OOS=spy["oos"]["Sharpe"], live_OOS=live["oos"]["Sharpe"],
                      pick_keep4a=cells[pick]["keep4a"], pick_keep4b=cells[pick]["keep4b"],
                      nothing_keep4b=nothing["keep4b"])
            r8rows.append(r8)
            say(f"   RULE 8  IS-argmax = TRIGGER {pick[0]} / DEGROSS {pick[1]} (IS Sh {r8['pick_IS']:.4f}) "
                f"-> OOS {r8['pick_OOS']:.4f}  vs do-nothing {r8['donothing_OOS']:.4f}  "
                f"delta {r8['delta']:+.4f}   cellmean {r8['cellmean_OOS']:.4f}  worst {r8['worst_OOS']:.4f} "
                f" rank corr IS/OOS {r8['rank_IS_OOS']:+.2f}")

    grid = pd.DataFrame(rows)
    wf = pd.DataFrame(r8rows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)

    # ---- G9 determinism
    pan = Panel("U56", panels[0][1], panels[0][2])
    Wt = build(pan, "COMPOSITE3")
    ar, _, _ = run(pan, Wt, A_G)
    dd = dd_path(ar)
    chk = []
    for trig in TRIGGERS:
        for f in DEGROSS:
            g = A_G if trig == "OFF" else brake_schedule(pan, dd, float(trig), f)[0]
            r, _, _ = run(pan, Wt, g)
            chk.append(sharpe(r[WARMUP:]))
    ref = grid[(grid.panel == "U56") & (grid.signal == "COMPOSITE3")].full_Sharpe.values
    dmax = float(np.max(np.abs(np.array(chk) - ref)))
    gate("G9 determinism (U56 COMPOSITE3 grid re-run)", f"{dmax:.3e}", "== 0.0", dmax == 0.0)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    say("\n## SUMMARY")
    say(f"   cells {len(grid)}   4a passes {int(grid.keep4a.sum())}   4b passes {int(grid.keep4b.sum())}")
    for pname in grid.panel.unique():
        for sig in SIGNALS:
            g = grid[(grid.panel == pname) & (grid.signal == sig)]
            off = g[g.trigger == "OFF"].iloc[0]
            say(f"   {pname:9s} {sig:11s} 4b {int(g.keep4b.sum()):2d}/{len(g)}   "
                f"OFF {off.full_CAGR:6.2%}/{off.full_Sharpe:.4f}/{off.full_MaxDD:7.2%}   "
                f"MaxDD {g.full_MaxDD.min():7.2%}..{g.full_MaxDD.max():7.2%}   "
                f"CAGR {g.full_CAGR.min():6.2%}..{g.full_CAGR.max():6.2%}   "
                f"Sharpe {g.full_Sharpe.min():.4f}..{g.full_Sharpe.max():.4f}   "
                f"turn {g.turnover.min():.2f}..{g.turnover.max():.2f}")
    say("\n   COST OF THE DD LEG, PER PANEL/SIGNAL (best MaxDD improvement over OFF and its price):")
    for pname in grid.panel.unique():
        for sig in SIGNALS:
            g = grid[(grid.panel == pname) & (grid.signal == sig)]
            off = g[g.trigger == "OFF"].iloc[0]
            on = g[g.trigger != "OFF"]
            b = grid.loc[on.full_MaxDD.idxmax()]
            say(f"   {pname:9s} {sig:11s} best DD cell TRIG {b.trigger}/{b.degross:.2f}: MaxDD "
                f"{off.full_MaxDD:7.2%} -> {b.full_MaxDD:7.2%} ({(b.full_MaxDD-off.full_MaxDD)*100:+.2f}pp) "
                f"costs CAGR {(b.full_CAGR-off.full_CAGR)*100:+.2f}pp, Sharpe "
                f"{b.full_Sharpe-off.full_Sharpe:+.4f}, turnover {b.turnover-off.turnover:+.2f}/yr; "
                f"4b {'PASS' if b.keep4b else 'FAIL(' + b.fail4b + ')'} vs OFF "
                f"{'PASS' if off.keep4b else 'FAIL(' + off.fail4b + ')'}")
    say("\n   THE MECHANISM ALONE (braked cell MINUS constant gross at the SAME mean exposure):")
    on = grid[grid.trigger != "OFF"]
    for pname in grid.panel.unique():
        for sig in SIGNALS:
            g = on[(on.panel == pname) & (on.signal == sig)]
            say(f"   {pname:9s} {sig:11s} n={len(g)}  d_CAGR {g.d_CAGR.mean()*100:+5.2f}pp  "
                f"d_Sharpe {g.d_Sharpe.mean():+.4f} (>0 at {int((g.d_Sharpe>0).sum())}/{len(g)})  "
                f"d_MaxDD {g.d_MaxDD.mean()*100:+5.2f}pp (>0 at {int((g.d_MaxDD>0).sum())}/{len(g)})  "
                f"d_OOS_Sharpe {g.d_oos_Sharpe.mean():+.4f}  "
                f"turnover {g.turnover.mean()-g.ctrl_turnover.mean():+.2f}/yr")
    say(f"   POOLED over {len(on)} braked cells: d_CAGR {on.d_CAGR.mean()*100:+.2f}pp, "
        f"d_Sharpe {on.d_Sharpe.mean():+.4f} (>0 at {int((on.d_Sharpe>0).sum())}/{len(on)}), "
        f"d_MaxDD {on.d_MaxDD.mean()*100:+.2f}pp (>0 at {int((on.d_MaxDD>0).sum())}/{len(on)}), "
        f"d_OOS {on.d_oos_Sharpe.mean():+.4f} (>0 at {int((on.d_oos_Sharpe>0).sum())}/{len(on)})")
    both = on[(on.d_MaxDD > 0) & (on.d_Sharpe > 0)]
    say(f"   cells where the BRAKE beats flat gross on BOTH DD and Sharpe: {len(both)} of {len(on)}"
        + ("" if not len(both) else "  -> " + ", ".join(
            f"{r.panel}/{r.signal}/{r.trigger}/{r.degross:.2f}" for _, r in both.iterrows())))
    say(f"   4b passes: braked {int(grid.keep4b.sum())} of {len(grid)}  vs  their own "
        f"GROSS-MATCHED controls {int(grid.ctrl_keep4b.sum())} of {len(grid)}")
    say("\n   STRUCTURE IN THE DIALS (pooled over panels and signals, braked cells only):")
    for t in [x for x in TRIGGERS if x != "OFF"]:
        g = on[on.trigger == str(t)]
        say(f"      TRIGGER {t:.2f}: d_CAGR {g.d_CAGR.mean()*100:+5.2f}pp  d_Sharpe {g.d_Sharpe.mean():+.4f}  "
            f"d_MaxDD {g.d_MaxDD.mean()*100:+5.2f}pp  d_OOS {g.d_oos_Sharpe.mean():+.4f}  "
            f"on% {g.brake_share.mean()*100:4.1f}")
    for f in DEGROSS:
        g = on[on.degross == f]
        say(f"      DEGROSS {f:.2f}: d_CAGR {g.d_CAGR.mean()*100:+5.2f}pp  d_Sharpe {g.d_Sharpe.mean():+.4f}  "
            f"d_MaxDD {g.d_MaxDD.mean()*100:+5.2f}pp  d_OOS {g.d_oos_Sharpe.mean():+.4f}")
    say(f"\n   RULE 8 chooser-minus-do-nothing: {wf.delta.round(4).tolist()}  mean {wf.delta.mean():+.4f}  "
        f"beats do-nothing at {int((wf.delta > 0).sum())} of {len(wf)}")
    for _, r in wf.iterrows():
        say(f"      {r.panel:9s} {r.signal:11s} pick TRIG {r.pick_trigger}/{r.pick_degross:.2f}  "
            f"OOS {r.pick_OOS:.4f} vs do-nothing {r.donothing_OOS:.4f} ({r.delta:+.4f})  "
            f"SPY OOS {r.spy_OOS:.4f}  live v2 OOS {r.live_OOS:.4f}  4b pick "
            f"{'PASS' if r.pick_keep4b else 'FAIL'} / OFF {'PASS' if r.nothing_keep4b else 'FAIL'}")
    off_fail = {(r.panel, r.signal): (not r.keep4b) for _, r in grid[grid.trigger == "OFF"].iterrows()}
    conv = grid[[off_fail[(r.panel, r.signal)] and r.keep4b for _, r in grid.iterrows()]]
    say(f"   4b CONVERSIONS (OFF fails 4b, the cell passes): {len(conv)} of {len(grid)} cells")
    for _, r in conv.iterrows():
        say(f"      {r.panel:9s} {r.signal:11s} TRIG {r.trigger}/{r.degross:.2f}: {r.full_CAGR:6.2%} / "
            f"{r.full_Sharpe:.4f} / {r.full_MaxDD:7.2%}  OOS {r.oos_Sharpe:.4f}  turn {r.turnover:.2f}  "
            f"| gross-matched control {'ALSO PASSES (not the timing)' if r.ctrl_keep4b else 'FAILS (genuinely the timing)'}")
    say(f"   GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass   {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
