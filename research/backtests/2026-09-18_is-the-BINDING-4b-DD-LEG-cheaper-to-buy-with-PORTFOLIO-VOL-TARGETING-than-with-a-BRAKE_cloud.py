#!/usr/bin/env python3
"""Idea 1263 (lane cloud, 2026-09-18): is the BINDING 4b DD LEG cheaper to buy with
PORTFOLIO VOL TARGETING than with a BRAKE?

THE PREMISE.  Five dials on the standing 2026-09-04 KEEP 4b book — rebalance phase (1253),
calendar years (1254), ex-post winner names (1255), the signal (1257), sector caps (1258) —
all landed on one sentence: every other 4b leg passes at essentially every grid point and the
DRAWDOWN CAP is the only leg that ever fails.  1257 priced what that costs: the M12_1-ALONE
book earns +1.00pp of CAGR and +0.0413 of full Sharpe at LESS turnover and is disqualified by
1.45pp of MaxDD and nothing else.  1264 then showed the leg IS buyable — inverse-vol slot
sizing converts three committed 4b FAILs into PASSes — but that full Sharpe falls monotonically
in the sizing exponent on 6 of 6 arms and rule 8 picks EQUAL WEIGHT (the incumbent's own
sizing) at 4 of 4 large-cap cells with delta exactly +0.0000.  So the DD leg is buyable and
slot sizing is not the way to buy it.

THIS RUN PRICES THE OTHER MECHANISM: PORTFOLIO VOLATILITY TARGETING.  Instead of moving weight
BETWEEN names (1264) or reacting to a realised equity drawdown (1262, not yet run), it moves
weight between the BOOK and CASH as a function of the book's own trailing realised volatility:

    gross(t) = clip( GROSS * TARGET / vol_hat(t-1), 0, GROSS_CAP )

where vol_hat(t-1) is the annualised realised volatility of the FROZEN book's own daily return
path over the trailing VOL_LOOK days, read at the DECISION date t-1 and applied at t (rule 2).
Under a riskless cash sleeve the book's volatility is very nearly proportional to its gross, so
this is the textbook one-line way to hold a constant risk budget, it has NO path dependence (no
state to carry, no trigger to arm and disarm, unlike a drawdown brake) and it needs no extra
data.  If the DD leg is cheap to buy anywhere, it should be cheap here.

THE TWO DIALS AND NO MORE (PROTOCOL rule 4):
    TARGET   {OFF, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20} annualised portfolio volatility.
             OFF is EXACTLY the committed anchor book (constant gross 0.75) and is in the grid
             so the do-nothing control is measured, not assumed.
    VOL_LOOK {21, 63, 126} trading days — the lookback of vol_hat.
  7 x 3 = 21 cells per (panel, signal).  EVERY ONE PUBLISHED in the .grid.csv.

NOT DIALS, reported at every value (1264's convention, so the two mechanisms are read on the
same objects): PANEL {U56, B135, SMALL} (rule 9); SIGNAL {COMPOSITE3 = the committed three-leg
average of percentile ranks, M12_1 = 1257's single 21/252 leg — the higher-return book that
failed 4b on drawdown alone}; both KEEP paths leg by leg; full / halves / IS / OOS; annual
turnover; realised annualised volatility; mean and range of the realised gross; the share of
rebalances at which the cap binds.  126 cells in all.

THE CONTROL ARM THAT MAKES THE HEADLINE READABLE, AND WITHOUT WHICH IT IS NOT.  A vol scaler
that is allowed up to GROSS_CAP does not only re-time exposure — it CHANGES THE AVERAGE
EXPOSURE, and this record has already established (the 2026-09-17 gross-dial run) that gross
alone is a pure CAGR-for-drawdown slide.  So every targeted cell is also run against a
CONSTANT-GROSS control held at that cell's OWN realised mean gross, and the reported effect of
the mechanism is the targeted cell MINUS that control, not minus the 0.75 anchor.  The raw
comparison against the anchor is published too, so both readings are visible.  The control is
not a dial: it is determined cell by cell by the cell itself.

FROZEN AT THE RECORD'S CONSTRUCTION, not touched by this run: eligibility = above own 200d MA
AND vol20 < 0.60; N = 20; H = 126 minimum hold; base GROSS = 0.75 of NAV; WEEKLY decide-Friday
/ trade-Monday; 10 bps per unit turnover; t+1 execution; 260-row warm-up; RAW-composite
ranking; equal 1/len(held) slots (1264's answer: the incumbent's own sizing is the one rule 8
picks).  SELECTION IS IDENTICAL AT EVERY CELL BY CONSTRUCTION — the dials touch only how much
of NAV the same names are held at.

FROZEN CONSTANTS, DECLARED SO THEY ARE NOT MISTAKEN FOR DIALS.  GROSS_CAP = 1.00, i.e. the
scaler may take the book from 0.75 up to FULLY INVESTED but NEVER to leverage (PROTOCOL rule 2
forbids leverage unless the idea says so, and this idea does not).  There is no floor: the
scaler may go to zero if realised vol explodes, and the realised minimum is published.
vol_hat is measured on the FROZEN (constant-gross) book's own returns, never on the scaled
book's — that avoids a fixed point, is exactly what an implementer can observe in real time,
and is stated here rather than buried.

PRE-DECLARED OUTCOMES, written before any number was read:
  (A) INERT — the scaler barely moves (realised gross stays within a few points of 0.75) and
      MaxDD moves less than 0.20pp.  Then this tape's book has too stable a volatility for the
      mechanism to bite.
  (B) THE DD LEG IS BOUGHT AND CHEAPLY — some cell materially improves MaxDD while holding the
      4b CAGR floor and both half-Sharpe legs, converts a committed 4b FAIL to a PASS, is
      CHEAPER in CAGR and Sharpe than 1264's inverse-vol conversion, AND rule 8 reaches it.
      That is a KEEP-candidate memo with exact RULES wording.
  (C) BOUGHT AND OVERPAID FOR — MaxDD improves but CAGR falls through 4b's floor, or a half
      Sharpe falls below SPY, or the extra rebalancing turnover eats it at 10 bps.
  (D) WORSE — vol targeting de-grosses AFTER volatility arrives, i.e. it sells the bottom, and
      drawdown deepens.
  (A)-(D) are not mutually exclusive across panels; whichever fire are reported as they fall,
  and the capital verdict follows rule 8, not the best cell.

RULE 8 (walk-forward, required).  (TARGET, VOL_LOOK) is CHOSEN on warm-up..2016-12-31 by IS
Sharpe ALONE and 2017-2026 is read ONCE, per (panel, signal).  Reported against (i) the
DO-NOTHING control = TARGET OFF (the committed constant-gross book), (ii) the mean over all 21
cells, (iii) the WORST cell, with the IS/OOS rank correlation over the 21.  The capital verdict
is the sign of chooser-minus-do-nothing, never the best cell's number.

GATES.  G1 vintage-pinned replay: truncated at 2026-09-16 (the cache end the committed numbers
were produced on — see 1264's bycatch), the U56 COMPOSITE3 OFF cell must replay the committed
15.71% / 1.1480 / -19.13% to 1e-4.  G4 the same for M12_1 against 1257's 16.71% / 1.1893 /
-20.58%.  G2 OFF is bit-identical at all three VOL_LOOK values.  G3 realised gross is inside
[0, 1.00] at every rebalance of every cell — no leverage anywhere.  G5 determinism: the whole
U56 COMPOSITE3 grid recomputed bit for bit.  G6 the mechanism does what it says — realised
annualised volatility is monotone increasing in TARGET at the frozen VOL_LOOK.  G7 the one-day
cache drift is published, not toleranced.

PROTOCOL: rule 2 costs and execution; rule 4 both KEEP paths at every grid point; rule 5 one
idea, one script, deterministic, standalone; rule 8 as above; rule 9 survivorship stated.
RULES.md, PROTOCOL.md, scan.py, bot.py and baseline.py are NOT modified by this script.

SURVIVORSHIP (rule 9).  U56 and B135 are CURRENT-constituent lists and SMALL is a current
sub-$2B screen (tickers with max_1d_move >= 1.0 in data/small_meta.csv are dropped before
anything is computed).  Every absolute level printed here is optimistic and every 4b pass is an
UPPER bound.  The headline is a DIFFERENCE between gross schedules applied to the SAME holdings
on the SAME panel — the selected names are identical at every cell by construction — which is
first-order immune to a level bias that moves all cells together.  One direction is NOT neutral
and is stated: a current-constituent panel UNDERSTATES the deep drawdowns a real momentum book
took in names that were later delisted, so the anchor's drawdown is flattered and any DD
improvement this mechanism posts here is a LOWER bound on what it would post on a live panel —
and, symmetrically, the CAGR it gives up is measured against a flattered comparand.

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
SLUG = "is-the-BINDING-4b-DD-LEG-cheaper-to-buy-with-PORTFOLIO-VOL-TARGETING-than-with-a-BRAKE"
STEM = ROOT / "research" / "backtests" / f"{DATE}_{SLUG}_cloud"

COST, WARMUP, MAXVOL = 10.0, 260, 0.60
OOS_START = pd.Timestamp("2017-01-01")
DD_CAP, CAGR_FLOOR = 0.60, 0.70
A_N, A_H, A_G = 20, 126, 0.75                       # the frozen 2026-09-04 book
SIGNALS = {"COMPOSITE3": [(21, 252), (0, 126), (0, 63)], "M12_1": [(21, 252)]}
TARGETS = ["OFF", 0.06, 0.08, 0.10, 0.12, 0.15, 0.20]   # DIAL 1 (OFF == committed anchor)
LOOKS = [21, 63, 126]                                    # DIAL 2
GROSS_CAP = 1.00                                         # frozen constant: NO LEVERAGE
COMMITTED_U56 = (0.157147, 1.14804, -0.191276)           # gate G1
COMMITTED_M12 = (0.167116, 1.18933, -0.205813)           # gate G4
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


# ------------------------------------------------------------------ panel (1264's, unchanged)
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
    """The frozen selection frame at GROSS = 1.0.  Identical to 1264's build at ALPHA = 0."""
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
    drift between, 10 bps on traded notional (1264's run, generalised to a gross schedule)."""
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


def gross_schedule(pan, anchor_r, target, look, lag=1):
    """gross(t) = clip(A_G * target / vol_hat(t-lag), 0, GROSS_CAP), vol_hat = trailing
    annualised realised vol of the FROZEN book's own returns.  No look-ahead: the value used at
    rebalance row t is computed from returns up to and including row t-lag."""
    s = pd.Series(anchor_r)
    vh = (s.rolling(look).std(ddof=0) * np.sqrt(252)).values
    out = np.empty(len(pan.reb))
    capped = 0
    for i, t in enumerate(pan.reb):
        ts = max(t - lag, 0)
        v = vh[ts]
        if not np.isfinite(v) or v <= 0:
            out[i] = A_G                      # pre-warm-up: the anchor's own gross
            continue
        m = A_G * target / v
        if m > GROSS_CAP:
            m = GROSS_CAP
            capped += 1
        out[i] = max(m, 0.0)
    w0 = int(np.searchsorted(pan.reb, WARMUP))
    diag = dict(g_mean=float(out[w0:].mean()), g_min=float(out[w0:].min()),
                g_max=float(out[w0:].max()),
                cap_share=float(np.mean(out[w0:] >= GROSS_CAP - 1e-12)))
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
    say(f"# {DATE} idea 1263 lane cloud — {SLUG}")
    say(f"# frozen book: RAW composite, gate = above 200d MA AND vol20 < {MAXVOL}, N={A_N}, H={A_H}, "
        f"base GROSS={A_G}, weekly, {COST:.0f} bps, t+1, warm-up {WARMUP}, equal 1/len(held) slots")
    say(f"# DIAL 1 TARGET = {TARGETS}   (OFF = COMMITTED CONSTANT-GROSS ANCHOR)")
    say(f"# DIAL 2 VOL_LOOK = {LOOKS} days")
    say(f"# reported-not-dials: panel {{U56,B135,SMALL}} x signal {list(SIGNALS)}")
    say(f"# frozen constant (NOT a dial): GROSS_CAP = {GROSS_CAP:.2f} — the scaler may reach FULLY "
        f"INVESTED but NEVER leverage (rule 2); no floor; vol_hat read on the FROZEN book's own path")
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
    for pi, (pname, p_px, inv) in enumerate(panels):
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
            say(f"\n   --- signal {sig} ---   anchor vol {vol(anchor_r[WARMUP:]):.2%}, "
                f"turnover {anchor_turn:.2f}/yr")
            say("   TARGET look |    CAGR   Sharpe    MaxDD    vol |  H1/H2 Sharpe |  OOS Sh | "
                "turn  gmean gmin gmax cap | 4a 4b | fail4b")
            cells = {}
            for target in TARGETS:
                for look in LOOKS:
                    if target == "OFF":
                        g, diag = A_G, dict(g_mean=A_G, g_min=A_G, g_max=A_G, cap_share=0.0)
                    else:
                        g, diag = gross_schedule(pan, anchor_r, float(target), look)
                    r, turn, expo = run(pan, Wt, g)
                    r = r[WARMUP:]
                    w = windows(idx, r)
                    # GROSS-MATCHED CONTROL: constant gross at this cell's own mean gross
                    cr, cturn, _ = run(pan, Wt, diag["g_mean"])
                    cw = windows(idx, cr[WARMUP:])
                    cb4 = legs_4b(cw, spy)
                    a4, b4 = legs_4a(w, live), legs_4b(w, spy)
                    rec = dict(panel=pname, signal=sig, target=str(target), look=look,
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
                    cells[(str(target), look)] = rec
                    say(f"   {str(target):6s} {look:4d} | {w['full']['CAGR']:7.2%} "
                        f"{w['full']['Sharpe']:8.4f} {w['full']['MaxDD']:8.2%} {w['full']['Vol']:6.2%} | "
                        f"{w['h1']['Sharpe']:.4f}/{w['h2']['Sharpe']:.4f} | {w['oos']['Sharpe']:7.4f} | "
                        f"{turn:5.2f} {diag['g_mean']:5.3f} {diag['g_min']:4.2f} {diag['g_max']:4.2f} "
                        f"{diag['cap_share']:4.2f} | {'Y' if all(a4.values()) else 'n'}  "
                        f"{'Y' if all(b4.values()) else 'n'} | {failed(b4):12s} | vs GROSS-MATCHED "
                        f"CAGR {rec['d_CAGR']*100:+5.2f}pp Sh {rec['d_Sharpe']:+.4f} "
                        f"DD {rec['d_MaxDD']*100:+5.2f}pp OOS {rec['d_oos_Sharpe']:+.4f}")

            # ---- gates
            if pname == "U56":
                q = p_px.loc[:VINTAGE]
                vpan = Panel("U56v", q, [c for c in q.columns if c != "SPY"])
                rv, _, _ = run(vpan, build(vpan, sig), A_G)
                tv = stats(rv[WARMUP:])
                tgt = COMMITTED_U56 if sig == "COMPOSITE3" else COMMITTED_M12
                err = max(abs(tv["CAGR"] - tgt[0]), abs(tv["Sharpe"] - tgt[1]), abs(tv["MaxDD"] - tgt[2]))
                gate(f"{'G1' if sig == 'COMPOSITE3' else 'G4'} vintage-pinned replay (U56 {sig} OFF "
                     f"@ {VINTAGE.date()})",
                     f"{tv['CAGR']:.4%}/{tv['Sharpe']:.4f}/{tv['MaxDD']:.4%} err {err:.2e}",
                     f"committed {tgt[0]:.4%}/{tgt[1]:.4f}/{tgt[2]:.4%}, err < 1e-4", err < 1e-4)
                a = cells[("OFF", LOOKS[0])]
                gate(f"G7 one-extra-day cache drift ({sig})",
                     f"CAGR {a['full_CAGR']-tv['CAGR']:+.4%}  Sharpe {a['full_Sharpe']-tv['Sharpe']:+.4f}",
                     "published, not toleranced", True)
            if pname == "U56" and sig == "COMPOSITE3":
                d = max(abs(cells[("OFF", L)]["full_Sharpe"] - cells[("OFF", LOOKS[0])]["full_Sharpe"])
                        for L in LOOKS)
                gate("G2 OFF is VOL_LOOK-invariant", f"{d:.3e}", "== 0.0", d == 0.0)
                gm = max(cells[(str(t), L)]["g_max"] for t in TARGETS for L in LOOKS)
                gn = min(cells[(str(t), L)]["g_min"] for t in TARGETS for L in LOOKS)
                gate("G3 realised gross inside [0, 1.00] — NO LEVERAGE anywhere",
                     f"[{gn:.4f}, {gm:.4f}]", f"[0, {GROSS_CAP}]", gn >= 0.0 and gm <= GROSS_CAP + 1e-12)
                vs = [cells[(str(t), 63)]["full_Vol"] for t in TARGETS if t != "OFF"]
                mono = all(vs[i] < vs[i + 1] for i in range(len(vs) - 1))
                gate("G6 realised vol monotone increasing in TARGET (VOL_LOOK 63)",
                     " < ".join(f"{v:.2%}" for v in vs), "strictly increasing", mono)

            if pname == "U56" and sig == "COMPOSITE3":
                o = cells[("OFF", LOOKS[0])]
                e = max(abs(o["d_CAGR"]), abs(o["d_Sharpe"]), abs(o["d_MaxDD"]))
                gate("G8 the OFF cell's gross-matched control IS the OFF cell", f"{e:.3e}",
                     "== 0.0", e == 0.0)

            # ---- rule 8
            ks = list(cells)
            is_s = np.array([cells[k]["is__Sharpe"] for k in ks])
            oos_s = np.array([cells[k]["oos_Sharpe"] for k in ks])
            pick = ks[int(np.nanargmax(is_s))]
            nothing = cells[("OFF", LOOKS[0])]
            r8 = dict(panel=pname, signal=sig, pick_target=pick[0], pick_look=pick[1],
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
            say(f"   RULE 8  IS-argmax = TARGET {pick[0]} / VOL_LOOK {pick[1]} (IS Sh {r8['pick_IS']:.4f}) "
                f"-> OOS {r8['pick_OOS']:.4f}  vs do-nothing {r8['donothing_OOS']:.4f}  "
                f"delta {r8['delta']:+.4f}   cellmean {r8['cellmean_OOS']:.4f}  worst {r8['worst_OOS']:.4f} "
                f" rank corr IS/OOS {r8['rank_IS_OOS']:+.2f}")

    grid = pd.DataFrame(rows)
    wf = pd.DataFrame(r8rows)
    grid.to_csv(f"{STEM}.grid.csv", index=False)
    wf.to_csv(f"{STEM}.walkforward.csv", index=False)

    # ---- G5 determinism
    pan = Panel("U56", panels[0][1], panels[0][2])
    Wt = build(pan, "COMPOSITE3")
    ar, _, _ = run(pan, Wt, A_G)
    chk = []
    for target in TARGETS:
        for look in LOOKS:
            g = A_G if target == "OFF" else gross_schedule(pan, ar, float(target), look)[0]
            r, _, _ = run(pan, Wt, g)
            chk.append(sharpe(r[WARMUP:]))
    ref = grid[(grid.panel == "U56") & (grid.signal == "COMPOSITE3")].full_Sharpe.values
    dd = float(np.max(np.abs(np.array(chk) - ref)))
    gate("G5 determinism (U56 COMPOSITE3 grid re-run)", f"{dd:.3e}", "== 0.0", dd == 0.0)
    pd.DataFrame(GATES).to_csv(f"{STEM}.gates.csv", index=False)

    say("\n## SUMMARY")
    say(f"   cells {len(grid)}   4a passes {int(grid.keep4a.sum())}   4b passes {int(grid.keep4b.sum())}")
    for pname in grid.panel.unique():
        for sig in SIGNALS:
            g = grid[(grid.panel == pname) & (grid.signal == sig)]
            off = g[g.target == "OFF"].iloc[0]
            say(f"   {pname:9s} {sig:11s} 4b {int(g.keep4b.sum()):2d}/{len(g)}   "
                f"OFF {off.full_CAGR:6.2%}/{off.full_Sharpe:.4f}/{off.full_MaxDD:7.2%}   "
                f"MaxDD {g.full_MaxDD.min():7.2%}..{g.full_MaxDD.max():7.2%}   "
                f"CAGR {g.full_CAGR.min():6.2%}..{g.full_CAGR.max():6.2%}   "
                f"Sharpe {g.full_Sharpe.min():.4f}..{g.full_Sharpe.max():.4f}   "
                f"turn {g.turnover.min():.2f}..{g.turnover.max():.2f}")
    # the direct question: what does a converted DD cost?
    say("\n   COST OF THE DD LEG, PER PANEL/SIGNAL (best MaxDD improvement over OFF and its price):")
    for pname in grid.panel.unique():
        for sig in SIGNALS:
            g = grid[(grid.panel == pname) & (grid.signal == sig)]
            off = g[g.target == "OFF"].iloc[0]
            on = g[g.target != "OFF"]
            j = on.full_MaxDD.idxmax()
            b = grid.loc[j]
            say(f"   {pname:9s} {sig:11s} best DD cell TARGET {b.target}/{b.look}: MaxDD "
                f"{off.full_MaxDD:7.2%} -> {b.full_MaxDD:7.2%} ({(b.full_MaxDD-off.full_MaxDD)*100:+.2f}pp) "
                f"costs CAGR {(b.full_CAGR-off.full_CAGR)*100:+.2f}pp, Sharpe "
                f"{b.full_Sharpe-off.full_Sharpe:+.4f}, turnover {b.turnover-off.turnover:+.2f}/yr; "
                f"4b {'PASS' if b.keep4b else 'FAIL(' + b.fail4b + ')'} vs OFF "
                f"{'PASS' if off.keep4b else 'FAIL(' + off.fail4b + ')'}")
    say("\n   THE MECHANISM ALONE (targeted cell MINUS constant gross at the SAME mean exposure):")
    on = grid[grid.target != "OFF"]
    for pname in grid.panel.unique():
        for sig in SIGNALS:
            g = on[(on.panel == pname) & (on.signal == sig)]
            say(f"   {pname:9s} {sig:11s} n={len(g)}  d_CAGR {g.d_CAGR.mean()*100:+5.2f}pp  "
                f"d_Sharpe {g.d_Sharpe.mean():+.4f} (>0 at {int((g.d_Sharpe>0).sum())}/{len(g)})  "
                f"d_MaxDD {g.d_MaxDD.mean()*100:+5.2f}pp (>0 at {int((g.d_MaxDD>0).sum())}/{len(g)})  "
                f"d_OOS_Sharpe {g.d_oos_Sharpe.mean():+.4f}  "
                f"turnover {g.turnover.mean()-g.ctrl_turnover.mean():+.2f}/yr")
    say(f"   POOLED over {len(on)} targeted cells: d_CAGR {on.d_CAGR.mean()*100:+.2f}pp, "
        f"d_Sharpe {on.d_Sharpe.mean():+.4f} (>0 at {int((on.d_Sharpe>0).sum())}/{len(on)}), "
        f"d_MaxDD {on.d_MaxDD.mean()*100:+.2f}pp (>0 at {int((on.d_MaxDD>0).sum())}/{len(on)}), "
        f"d_OOS {on.d_oos_Sharpe.mean():+.4f} (>0 at {int((on.d_oos_Sharpe>0).sum())}/{len(on)})")
    say(f"   4b passes: targeted {int(grid.keep4b.sum())} of {len(grid)}  vs  their own "
        f"GROSS-MATCHED controls {int(grid.ctrl_keep4b.sum())} of {len(grid)}")
    say(f"\n   RULE 8 chooser-minus-do-nothing: {wf.delta.round(4).tolist()}  mean {wf.delta.mean():+.4f}  "
        f"beats do-nothing at {int((wf.delta > 0).sum())} of {len(wf)}")
    off_fail = {(r.panel, r.signal): (not r.keep4b) for _, r in grid[grid.target == "OFF"].iterrows()}
    conv = grid[[off_fail[(r.panel, r.signal)] and r.keep4b for _, r in grid.iterrows()]]
    say(f"   4b CONVERSIONS (OFF fails 4b, the cell passes): {len(conv)} of {len(grid)} cells")
    for _, r in conv.iterrows():
        say(f"      {r.panel:9s} {r.signal:11s} TARGET {r.target}/{r.look}: {r.full_CAGR:6.2%} / "
            f"{r.full_Sharpe:.4f} / {r.full_MaxDD:7.2%} (OFF fails on "
            f"{grid[(grid.panel==r.panel)&(grid.signal==r.signal)&(grid.target=='OFF')].fail4b.iloc[0]})")
    say(f"   GATES {sum(g['pass_'] for g in GATES)} of {len(GATES)} pass   {time.time()-t0:.0f}s")
    Path(f"{STEM}.console.txt").write_text("\n".join(_LOG) + "\n")


if __name__ == "__main__":
    main()
